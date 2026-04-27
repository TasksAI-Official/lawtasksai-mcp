"""
LawTasksAI MCP Server — Smart Router

Instead of exposing 200+ tools (token bloat), we expose 4 clean tools:
  1. lawtasksai_search     — Find the right skill for a legal task
  2. lawtasksai_execute    — Get a skill's expert framework (runs locally)
  3. lawtasksai_balance    — Check credit balance
  4. lawtasksai_categories — Browse skill categories

lawtasksai.com never sees your prompts, your client files, or your client data.
Skills run entirely on your machine — your documents stay local if using OpenClaw,
or go to your LLM provider if using a cloud AI.
"""

import os
import re
import time
import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Prompt, PromptMessage, PromptArgument
from mcp.types import GetPromptResult

load_dotenv()

API_BASE = os.getenv("LAWTASKSAI_API_BASE", "https://api.taskvaultai.com")
LICENSE_KEY = os.getenv("LAWTASKSAI_LICENSE_KEY", "")

if not LICENSE_KEY:
    raise ValueError("LAWTASKSAI_LICENSE_KEY is required. Set it in .env file.")

AUTH_HEADERS = {
    "Authorization": f"Bearer {LICENSE_KEY}",
    "Content-Type": "application/json",
    "X-Client-Type": "mcp-server",
    "X-Client-Version": "1.4.0",
    "X-Product-ID": "law",
}

async def api_get(path):
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{API_BASE}{path}", headers=AUTH_HEADERS)
        resp.raise_for_status()
        return resp.json()

TOOLS = [
    Tool(
        name="lawtasksai_search",
        description=(
            "Search for LawTasksAI skills by keyword. "
            "After getting results, ALWAYS present the top matches to the user as a numbered list "
            "with the skill name and a brief description of each. "
            "Then ask the user: 'Which of these best fits your situation? (reply with a number, "
            "or describe your task differently for a new search)' "
            "NEVER call lawtasksai_execute without explicit user confirmation of which skill to use."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Legal topic to search for (e.g. 'motion to compel', 'statute of limitations', 'NDA review', 'deposition prep', 'ABA ethics')"
                }
            },
            "required": ["query"]
        },
    ),
    Tool(
        name="lawtasksai_execute",
        description=(
            "Get a skill's expert legal analysis framework by skill ID. "
            "Returns the full prompt/schema for your AI to apply locally. Costs 1 credit. "
            "Only call this after the user has confirmed which skill they want from lawtasksai_search results. "
            "All analysis runs locally — client data never leaves your machine."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "skill_id": {
                    "type": "string",
                    "description": "Skill ID from lawtasksai_search results, confirmed by the user"
                }
            },
            "required": ["skill_id"]
        },
    ),
    Tool(
        name="lawtasksai_balance",
        description="Check your remaining LawTasksAI credit balance.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="lawtasksai_categories",
        description=(
            "List all available skill categories to browse by legal practice area. "
            "Categories include: Litigation, Contracts, Criminal Defense, Real Estate, "
            "Family Law, Estate Planning, Employment, ABA Ethics, and more."
        ),
        inputSchema={"type": "object", "properties": {}},
    ),
]

# ─────────────────────────────────────────────
# System prompt — injected at session start
# Instructs Claude to always confirm skill
# selection with the user before executing.
# ─────────────────────────────────────────────

SYSTEM_PROMPT_TEXT = """\
You have access to LawTasksAI, a library of 200+ expert legal analysis skills for attorneys.

## How to use LawTasksAI

**Always follow this 3-step flow:**

1. **Search** — Call lawtasksai_search with the user's legal topic to find matching skills.

2. **Confirm** — Present the top results to the user as a numbered list, like this:
   > I found these skills that match your request:
   > 1. **[Skill Name]** — [brief description]
   > 2. **[Skill Name]** — [brief description]
   > 3. **[Skill Name]** — [brief description]
   >
   > Which of these best fits your situation? (Reply with a number, or describe your task differently and I'll search again.)

3. **Execute** — Only after the user confirms their choice, call lawtasksai_execute with that skill's ID.

## Important rules
- NEVER auto-execute a skill without explicit user confirmation.
- If the user's reply is ambiguous, ask a clarifying question rather than guessing.
- If no skills match, suggest the user try lawtasksai_categories to browse by practice area.
- After executing a skill, apply its framework to the user's specific case facts and produce the full output.
- Always remind the user that outputs require their professional review and legal judgment.
- Client confidentiality: all analysis runs locally — no client data leaves the user's machine.
"""

PROMPTS = [
    Prompt(
        name="lawtasksai-workflow",
        description="LawTasksAI skill selection workflow — always confirm skill choice with user before executing.",
        arguments=[],
    )
]

# ── Cache configuration ─────────────────────────────────────────────────────
CACHE_TTL      = 600   # 10 minutes — refresh skills + triggers after this
ERROR_COOLDOWN = 30    # retry a failed API call after 30 seconds

# ── Skills cache ─────────────────────────────────────────────────────────────
_skills_cache         = None
_skills_cache_ts      = 0.0
_skills_cache_err_until = 0.0

# ── Triggers cache ───────────────────────────────────────────────────────────
# Shape: { skill_id: ["phrase1", "phrase2", ...], ... }
# Fetched from /v1/skills/triggers — does NOT send attorney queries to server.
# Privacy note: only skill metadata (phrases) is fetched, never query text.
_triggers_cache       = None
_triggers_cache_ts    = 0.0
_triggers_cache_err_until = 0.0


async def get_skills():
    global _skills_cache, _skills_cache_ts, _skills_cache_err_until
    now = time.monotonic()
    if _skills_cache is not None and (now - _skills_cache_ts) < CACHE_TTL:
        return _skills_cache
    if now < _skills_cache_err_until:
        return _skills_cache if _skills_cache is not None else []
    try:
        _skills_cache = await api_get("/v1/skills")
        _skills_cache_ts = now
        _skills_cache_err_until = 0.0
    except Exception:
        _skills_cache_err_until = now + ERROR_COOLDOWN
        if _skills_cache is None:
            _skills_cache = []
    return _skills_cache


async def get_triggers():
    """Return trigger phrases dict {skill_id: [phrase, ...]}.
    Fetches once then caches for CACHE_TTL seconds.
    Fails silently — search still works without triggers, just less smart.
    """
    global _triggers_cache, _triggers_cache_ts, _triggers_cache_err_until
    now = time.monotonic()
    if _triggers_cache is not None and (now - _triggers_cache_ts) < CACHE_TTL:
        return _triggers_cache
    if now < _triggers_cache_err_until:
        return _triggers_cache if _triggers_cache is not None else {}
    try:
        raw = await api_get("/v1/skills/triggers")
        # Normalise: {skill_id: {"triggers": [...]}} → {skill_id: [phrase.lower(), ...]}
        _triggers_cache = {
            skill_id: [p.lower() for p in v.get("triggers", [])]
            for skill_id, v in raw.items()
        }
        _triggers_cache_ts = now
        _triggers_cache_err_until = 0.0
    except Exception:
        _triggers_cache_err_until = now + ERROR_COOLDOWN
        if _triggers_cache is None:
            _triggers_cache = {}
    return _triggers_cache


# Common legal abbreviations not yet in the trigger phrase database.
# Expands the query before matching so 'MTC' finds motion-to-compel skills.
# Add entries here as gaps are identified; the long-term fix is adding them
# to the trigger phrases in the DB via the admin UI.
LEGAL_ABBREVS = {
    "mtc":   "motion to compel",
    "rogs":  "interrogatories",
    "rog":   "interrogatory",
    "rfa":   "request for admission",
    "rfp":   "request for production",
    "tro":   "temporary restraining order",
    "pi":    "personal injury",
    "msj":   "motion for summary judgment",
    "msk":   "motion to strike",
    "sj":    "summary judgment",
    "jnov":  "judgment notwithstanding verdict",
    "mil":   "motion in limine",
    "roe":   "rules of evidence",
    "frcp":  "federal rules civil procedure",
    "fre":   "federal rules evidence",
    "aff":   "affidavit",
    "decl":  "declaration",
    "depo":  "deposition",
    "deps":  "depositions",
    "compl": "complaint",
    "ans":   "answer",
    "countercl": "counterclaim",
    "xc":    "cross complaint",
    "sol":   "statute of limitations",
    "atty":  "attorney",
    "p/i":   "personal injury",
    "d/c":   "dismissal",
}


def expand_query(query):
    """Expand legal abbreviations in a query string.
    Preserves the original query and appends expansions.
    e.g. 'MTC discovery' -> 'MTC discovery motion to compel'
    """
    words = query.lower().split()
    expansions = []
    for w in words:
        clean = w.strip('.,;:?!')
        if clean in LEGAL_ABBREVS:
            expansions.append(LEGAL_ABBREVS[clean])
    if expansions:
        return query + " " + " ".join(expansions)
    return query


def _word_in_text(word, text):
    """True if `word` appears as a whole word in `text` (word-boundary aware)."""
    return bool(re.search(r'(?<![\w])' + re.escape(word) + r'(?![\w])', text))


def score_skill(skill, query_lower, query_words, triggers):
    """Score a single skill against a query.

    Scoring tiers (highest wins):
      10 — query matches a trigger phrase (whole-word, bidirectional substring)
       3 — query word appears as whole word in skill name
       1 — query word appears as whole word in skill description

    Trigger matching is whole-word to prevent 'sol' matching 'resolve'.
    Short all-caps terms (e.g. MTC, SOL, ROGs) bypass the length filter.
    """
    skill_id   = skill.get("id", "")
    name_text  = skill.get("name", "").lower()
    desc_text  = skill.get("description", "").lower()
    full_text  = name_text + " " + desc_text

    # Tier 1 — trigger phrase match (whole-word, bidirectional)
    # 'phrase in query' catches: query='just got served', phrase='got served'
    # 'query in phrase' catches: query='MTC', phrase='run the MTC'
    # Whole-word check prevents 'sol' matching 'resolve', 'solicits' etc.
    skill_triggers = triggers.get(skill_id, [])
    for phrase in skill_triggers:
        if _word_in_text(phrase, query_lower) or _word_in_text(query_lower, phrase):
            return 10

    # Tier 2 — keyword match on name/description (whole-word)
    keyword_score = sum(
        3 if _word_in_text(w, name_text) else 1
        for w in query_words
        if _word_in_text(w, full_text)
    )
    return keyword_score

server = Server("LawTasksAI — Legal Research & Drafting")

@server.list_prompts()
async def list_prompts():
    return PROMPTS

@server.get_prompt()
async def get_prompt(name, arguments):
    if name == "lawtasksai-workflow":
        return GetPromptResult(
            description="LawTasksAI skill selection workflow",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=SYSTEM_PROMPT_TEXT)
                )
            ]
        )
    raise ValueError(f"Unknown prompt: {name}")

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name, arguments):
    try:
        if name == "lawtasksai_search":
            skills, triggers = await get_skills(), await get_triggers()
            query = expand_query(arguments.get("query", ""))
            query_lower = query.lower()
            STOP_WORDS = {"a","an","the","and","or","of","in","to","for","is","are",
                          "with","at","by","on","from","as","it","its","be","was","can"}
            # Keep words that are either >2 chars OR all-caps abbreviations (MTC, SOL, TRO, etc.)
            raw_words = query.split()  # preserve original case for caps check
            query_words = [
                w_lower for w_orig, w_lower in zip(raw_words, query_lower.split())
                if w_lower not in STOP_WORDS and (len(w_lower) > 2 or w_orig.isupper())
            ]
            scored = []
            for s in skills:
                sc = score_skill(s, query_lower, query_words, triggers)
                if sc > 0:
                    scored.append((sc, s))
            scored.sort(key=lambda x: -x[0])
            matches = [s for _, s in scored[:5]]

            # Honest zero-result response — never silently serve unrelated skills
            if not matches:
                no_match_text = (
                    f"No skills found matching **'{arguments.get('query', '')}'**.\n\n"
                    "**Suggestions:**\n"
                    "- Try different keywords (e.g. 'motion to compel' instead of 'MTC')\n"
                    "- Use `lawtasksai_categories` to browse all skill categories\n"
                    "- Ask the user to rephrase their request\n\n"
                    "**DO NOT call lawtasksai_execute** — no skill has been selected."
                )
                return [TextContent(type="text", text=no_match_text)]

            lines = [f"**{len(matches)} skills found for '{arguments.get('query', '')}':**\n"]
            for i, s in enumerate(matches, 1):
                desc = s.get("description", "")[:100]
                lines.append(f"{i}. **{s['name']}** (`{s['id']}`)\n   {desc}\n")

            # Explicit workflow enforcement — injected into every search result.
            # Primary guardrail; the Prompt resource is supplementary only.
            lines.append("---")
            lines.append(
                "**\U0001f6d1 REQUIRED — DO NOT SKIP:**\n"
                "Present the numbered list above to the user EXACTLY as shown. "
                "Then ask: *\"Which of these best fits your situation? "
                "(Reply with a number, or describe your task differently and I'll search again.)\"*\n\n"
                "**DO NOT call `lawtasksai_execute` until the user replies with their choice. "
                "Each execution costs 1 credit and cannot be undone.**"
            )
            return [TextContent(type="text", text="\n".join(lines))]

        if name == "lawtasksai_execute":
            skill_id = arguments.get("skill_id", "")
            if not skill_id:
                return [TextContent(type="text", text="Error: skill_id is required. Use lawtasksai_search first to find a skill ID.")]
            result = await api_get(f"/v1/skills/{skill_id}/schema")
            schema = result.get("schema", "")
            instructions = result.get("instructions", "")
            credits_used = result.get("credits_used", 1)
            credits_remaining = result.get("credits_remaining", "?")
            text = f"# {result.get('skill_name', skill_id)}\n\n"
            text += f"{instructions}\n\n"
            text += f"## Expert Analysis Framework\n\n{schema}\n\n"
            text += f"---\n*Credits used: {credits_used} | Remaining: {credits_remaining}*"
            return [TextContent(type="text", text=text)]

        if name == "lawtasksai_balance":
            b = await api_get("/v1/credits/balance")
            return [TextContent(type="text", text=f"**Credit Balance:** {b.get('credits_balance', '?')} credits")]

        if name == "lawtasksai_categories":
            cats = await api_get("/v1/categories")
            if isinstance(cats, list):
                lines = ["**Skill Categories:**\n"]
                for c in cats:
                    lines.append(f"- **{c.get('name', '?')}** (`{c.get('id', '?')}`)")
                return [TextContent(type="text", text="\n".join(lines))]
            return [TextContent(type="text", text=str(cats))]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 402:
            return [TextContent(type="text", text="Insufficient credits. Purchase more at https://lawtasksai.com/#pricing")]
        if e.response.status_code == 401:
            return [TextContent(type="text", text="Invalid or expired license key. Check your .env file.")]
        return [TextContent(type="text", text=f"API error ({e.response.status_code}): {e.response.text[:200]}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]

if __name__ == "__main__":
    import asyncio

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )

    asyncio.run(main())
