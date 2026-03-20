"""
LawTasksAI MCP Server — Smart Router

Instead of exposing 200+ tools (token bloat), we expose 4 clean tools:
  1. lawtasks_search     — Find the right skill for a legal question
  2. lawtasks_execute    — Get a skill's expert framework (runs locally)
  3. lawtasks_balance    — Check credit balance
  4. lawtasks_categories — Browse skill categories

All skills run locally — your documents never leave your machine.
LawTasksAI delivers the expert analysis framework; your AI applies it.
"""

import os
import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

load_dotenv()

API_BASE = os.getenv("LAWTASKSAI_API_BASE", "https://lawtasksai-api-10437713249.us-central1.run.app")
LICENSE_KEY = os.getenv("LAWTASKSAI_LICENSE_KEY", "")

if not LICENSE_KEY:
    raise ValueError("LAWTASKSAI_LICENSE_KEY is required. Set it in .env file.")

AUTH_HEADERS = {
    "Authorization": f"Bearer {LICENSE_KEY}",
    "Content-Type": "application/json",
    "X-Client-Type": "mcp-server",
    "X-Client-Version": "1.3.0",
}

async def api_get(path):
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{API_BASE}{path}", headers=AUTH_HEADERS)
        resp.raise_for_status()
        return resp.json()

TOOLS = [
    Tool(
        name="lawtasks_search",
        description="Search for legal skills by keyword. Use this FIRST to find the right skill before executing it. Returns skill IDs, names, and descriptions.",
        inputSchema={"type": "object", "properties": {"query": {"type": "string", "description": "Legal topic to search for (e.g. 'statute of limitations', 'motion to compel', 'NDA review')"}}, "required": ["query"]},
    ),
    Tool(
        name="lawtasks_execute",
        description="Get a skill's expert analysis framework by skill ID. Returns the full prompt/schema for your AI to apply locally. Costs 1 credit. Use lawtasks_search first to find the skill ID.",
        inputSchema={"type": "object", "properties": {"skill_id": {"type": "string", "description": "Skill ID from lawtasks_search results"}}, "required": ["skill_id"]},
    ),
    Tool(
        name="lawtasks_balance",
        description="Check your remaining LawTasksAI credit balance.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="lawtasks_categories",
        description="List all available skill categories to browse by practice area.",
        inputSchema={"type": "object", "properties": {}},
    ),
]

_skills_cache = None

async def get_skills():
    global _skills_cache
    if _skills_cache is None:
        try:
            _skills_cache = await api_get("/v1/skills")
        except Exception:
            _skills_cache = []
    return _skills_cache

server = Server("lawtasksai")

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name, arguments):
    try:
        if name == "lawtasks_search":
            skills = await get_skills()
            query = arguments.get("query", "").lower()
            words = query.split()
            scored = []
            for s in skills:
                text = (s.get("name", "") + " " + s.get("description", "")).lower()
                score = sum(1 for w in words if w in text)
                if score > 0:
                    scored.append((score, s))
            scored.sort(key=lambda x: -x[0])
            matches = [s for _, s in scored[:10]]
            if not matches:
                matches = skills[:10]
            lines = ["**Matching skills:**\\n"]
            for s in matches:
                lines.append(f"- **{s['name']}** (`{s['id']}`) — {s.get('description', '')[:80]}")
            lines.append(f"\\n*{len(skills)} total skills available. Use lawtasks_execute with a skill ID to get the full framework.*")
            return [TextContent(type="text", text="\\n".join(lines))]

        if name == "lawtasks_execute":
            skill_id = arguments.get("skill_id", "")
            if not skill_id:
                return [TextContent(type="text", text="Error: skill_id is required. Use lawtasks_search first to find a skill ID.")]
            result = await api_get(f"/v1/skills/{skill_id}/schema")
            schema = result.get("schema", "")
            instructions = result.get("instructions", "")
            credits_used = result.get("credits_used", 1)
            credits_remaining = result.get("credits_remaining", "?")
            text = f"# {result.get('skill_name', skill_id)}\\n\\n"
            text += f"{instructions}\\n\\n"
            text += f"## Expert Analysis Framework\\n\\n{schema}\\n\\n"
            text += f"---\\n*Credits used: {credits_used} | Remaining: {credits_remaining}*"
            return [TextContent(type="text", text=text)]

        if name == "lawtasks_balance":
            b = await api_get("/v1/credits/balance")
            return [TextContent(type="text", text=f"**Credit Balance:** {b.get('credits_balance', '?')} credits")]

        if name == "lawtasks_categories":
            cats = await api_get("/v1/categories")
            if isinstance(cats, list):
                lines = ["**Skill Categories:**\\n"]
                for c in cats:
                    lines.append(f"- **{c.get('name', '?')}** (`{c.get('id', '?')}`)")
                return [TextContent(type="text", text="\\n".join(lines))]
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
