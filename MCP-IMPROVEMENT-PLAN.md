# LawTasksAI MCP — Improvement Plan
*Prepared: 2026-04-27 | Scope: lawtasksai-mcp, lawtasksAI-admin*

This document explains what is currently wrong or suboptimal in the MCP server and installer, why each issue matters to the attorney using the product, and what the improved experience looks like after the fix.

Issues are ordered by impact, not difficulty.

---

## 1. Search Quality — The Core User Experience Problem

### What's happening now

When an attorney types something like `"motion to compel discovery responses"`, the server runs this logic in `server.py` lines 158–173:

```python
words = [w for w in query.split() if w not in STOP_WORDS and len(w) > 2]
scored = []
for s in skills:
    text = (s.get("name", "") + " " + s.get("description", "")).lower()
    name_text = s.get("name", "").lower()
    score = sum(3 if w in name_text else 1 for w in words if w in text)
```

This is raw word frequency matching. It gives 3 points if a query word appears in the skill name, 1 point if it appears in the description. That's it.

**The silent failure case (lines 181–182):**
```python
if not matches:
    matches = skills[:5]
```

If nothing matches, the server returns the first 5 skills in the database and presents them to the user *as if they were search results*. The attorney sees a numbered list, picks one, and gets an irrelevant skill. They spend a credit, get garbage output, and lose trust in the product.

### Why it fails attorneys specifically

Attorneys don't speak in exact keyword terms. They say:
- `"MTC"` → should match `Motion to Compel`
- `"ROGs"` → should match `Interrogatories`
- `"suppression hearing"` → should match `Motion to Suppress Evidence`
- `"Rule 1.6"` → should match ABA ethics skills on confidentiality
- `"4th amendment"` → should match suppression, warrant, and search skills

None of these will score above zero with the current word-match system.

Additionally, there is no feedback when a search fails. The attorney never knows their query returned nothing real — they just see five apparently relevant results that aren't.

### What the fix looks like

**Short term (in server.py):**
- Return an honest "no match" message with a suggestion to use `lawtasksai_categories` instead of silently serving the first 5 skills.
- Add an abbreviation/synonym map for common legal shorthand (MTC, ROGs, depo, etc.).
- Fold the existing trigger phrases from the database into the scoring logic — any query that matches a trigger phrase should rank that skill at the top.

**Medium term (API-level):**
- Move search to the server side: `GET /v1/skills/search?q=motion+to+compel`
- This enables real text ranking (BM25 or vector similarity), logs zero-result queries so you can see what attorneys are asking for that you don't have, and makes both the MCP server and the admin UI faster.

### User experience impact

| Before | After |
|--------|-------|
| Attorney types `"MTC"`, gets 5 random skills | Attorney gets `Motion to Compel` as the top result |
| Failed search silently shows unrelated skills | Failed search says "no match — try browsing categories" |
| Abbreviations and legal shorthand never work | Common legal shorthand works out of the box |
| No data on what attorneys are searching for | Every query logged; gaps become a product roadmap |

---

## 2. README Tool Name Mismatch — Breaks Manual Installs

### What's happening now

The README's Tools table (line ~52) lists these tool names:

```
lawtasks_search
lawtasks_execute
lawtasks_balance
lawtasks_categories
```

The actual tool names defined in `server.py` (lines 45–105) are:

```
lawtasksai_search
lawtasksai_execute
lawtasksai_balance
lawtasksai_categories
```

These are different. `lawtasks_` vs `lawtasksai_`.

### Why it matters

Any attorney or developer who reads the README and tries to reference a tool name directly — in a custom prompt, in a manual MCP config, in a support ticket asking why something doesn't work — will use the wrong name and get a `tool not found` error with no useful explanation.

More concretely: the README is indexed publicly on GitHub and on the Glama.ai MCP directory badge. It is the primary discovery surface for this product. If the first technical detail a prospective customer reads is wrong, it undermines confidence before they've spent a dollar.

### The fix

One line change in README.md — update the four tool names in the table to match the actual code. Then decide: `lawtasks_` or `lawtasksai_`? Pick one canonical prefix and apply it everywhere: `server.py`, `README.md`, all tool descriptions, and the system prompt. The current code uses `lawtasksai_` throughout except the README, so the fix is update the README.

### User experience impact

| Before | After |
|--------|-------|
| README shows `lawtasks_search` | README shows `lawtasksai_search` — matches reality |
| Manual config users get silent `tool not found` | Tool names work as documented |
| Trust undermined on first read | Consistent, professional first impression |

---

## 3. Skills Cache Never Refreshes — New Skills Stay Invisible

### What's happening now

`server.py` lines 140–147:

```python
_skills_cache = None

async def get_skills():
    global _skills_cache
    if _skills_cache is None:
        try:
            _skills_cache = await api_get("/v1/skills")
        except Exception:
            _skills_cache = []
    return _skills_cache
```

The cache is loaded exactly once when the server process starts. It is never refreshed. If you push a new skill to the API while a user's MCP client is running, that skill does not exist for that user until they restart Claude Desktop, Cursor, or Windsurf. There is no indication that anything is stale.

There is also a poisoned-cache bug: if the API is temporarily unavailable when the server first starts, `_skills_cache` is set to `[]` (empty list) and stays empty for the entire session. Every search returns nothing. The user has a functioning license key and a working API, but sees no skills at all — with no error message to explain why.

### Why it matters

In the early product phase you are adding and improving skills frequently. Early adopters who leave Claude Desktop open across days (common behavior) are running against a stale catalog. The attorney who doesn't find what they need and churns may have been one new skill away from staying.

The poisoned-cache case is worse: the user's first experience with the product is "it returned nothing" with no explanation. That's an immediate refund request.

### The fix

- Add a TTL: re-fetch the skills list if the cache is older than 10 minutes.
- Distinguish between "cache is empty because API is down" and "cache is empty because there are no skills" — don't cache API failures; retry on next call with a brief cooldown.

### User experience impact

| Before | After |
|--------|-------|
| New skills invisible until client restart | New skills appear within 10 minutes automatically |
| API outage at startup → permanently empty results | API outage retries; skills load once API recovers |
| No way to know if cache is stale | User always sees current skill catalog |

---

## 4. Cursor and Windsurf Detection Uses Wrong Config Paths

### What's happening now

`install.py` lines 65–71:

```python
cursor_path = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
windsurf_path = Path.home() / "Library" / "Application Support" / "Windsurf" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
```

Both paths point into the `saoudrizwan.claude-dev` extension directory — this is the Cline extension's config file, not Cursor's or Windsurf's native MCP config.

The correct native paths are:
- **Cursor:** `~/.cursor/mcp.json`
- **Windsurf:** `~/.codeium/windsurf/mcp_config.json`

An attorney or developer who has Cursor or Windsurf installed but not the Cline extension will have neither of those `saoudrizwan.claude-dev` directories. The installer will not detect their clients and will show "No supported MCP clients detected" — even though Cursor or Windsurf is open on their screen.

The same wrong paths appear in the Windows and Linux branches of `get_mcp_clients()`.

### Why it matters

Cursor and Windsurf are the growth market for MCP tools among legal tech-forward attorneys and the developers who recommend tools to them. If a Cursor user tries the installer and it says "no clients detected," they don't file a bug report — they leave and tell colleagues it doesn't work.

This is a silent, invisible failure. The installer exits with code 0 and shows a polite message about alternative install options. The user has no idea the installer was looking in the wrong place.

### The fix

Update `get_mcp_clients()` to check both paths for Cursor and Windsurf — the native path first, the Cline extension path second. Write to whichever one exists. On all three platforms (Mac, Windows, Linux).

### User experience impact

| Before | After |
|--------|-------|
| Cursor user: "No clients detected" | Cursor user: installed correctly, first try |
| Windsurf user: same failure | Windsurf user: same fix |
| Silent failure with no explanation | Correct detection across all supported clients |

---

## 5. The `is_published=False` Bug in the Skills Pusher

### What's happening now

`lawtasksAI-admin/archive/push-skills.py` (around line 50) constructs skill payloads that include `is_published: False` unconditionally on every push. The push script loops through all skills and POSTs each one to the admin API.

The result: every time you run `push-skills.py`, every skill in the database gets its `is_published` flag set to `False`. Skills that were live and visible to users are silently unpublished. No error is raised. No confirmation is asked. The script finishes with a success message.

This means every skills deployment cycle breaks the live catalog until someone manually re-publishes through the admin UI.

### Why it matters

With 4,117 skills across 29 verticals, re-publishing manually isn't feasible. More importantly, this is the kind of bug that corrupts production without leaving a trace. An attorney tries to use the product, the search returns nothing, and they have no way of knowing their account is fine but all skills are unpublished. You may not know either unless you check the admin dashboard.

Even with no customers yet, this bug will bite you the moment you run the pusher after launch.

### The fix

Two changes:
1. Read the current `is_published` state before updating a skill, and preserve it — never overwrite it with `False` unless explicitly setting it to draft.
2. Alternatively: remove `is_published` from the push payload entirely. The pusher's job is content, not publication state. Publication state should be managed separately through the admin UI or a dedicated endpoint.

### User experience impact

| Before | After |
|--------|-------|
| Running the pusher unpublishes all live skills | Running the pusher preserves publication state |
| Silent production failure after every skills update | Skills stay live through the update cycle |
| Manual re-publish required after every push | No manual intervention needed |

---

## 6. Post-Install Verification — Attorneys Need Confidence

### What's happening now

After `install.py` completes, it prints:
```
✅ Installation complete!
Configured: Claude Desktop

Next steps:
  1. Restart your MCP client(s)
  2. Start asking legal questions!
```

The installer has no idea if the installation actually works. It wrote a JSON config file and called it done. It does not:
- Attempt to start `server.py` and verify it runs
- Make a test API call to confirm the license key is valid
- Check that the credit balance is accessible
- Confirm the skill count visible through the server

### Why it matters

The most common support scenario for any MCP tool is: "I installed it but it doesn't work." The causes are usually a bad Python path, a missing dependency that wasn't installed correctly, a firewall blocking the API, or a license key that was entered with a typo. The current installer provides no signal on any of these.

Attorneys are not developers. They will not open a terminal and debug a JSON config file. If it doesn't work on first launch, they email support or ask for a refund. A post-install check that says either ✅ "Your license key is valid, 87 credits available, 206 skills ready" or ❌ "Could not connect — check your license key" eliminates the most common support request before it happens.

### The fix

After writing the config, run a quick test:
1. Import `server.py` or call `python3 server.py --check` (a new `--check` flag)
2. Make one API call to `/v1/credits/balance` with the provided license key
3. Print the result inline: `✅ License verified — 87 credits available, 206 skills ready`

If it fails, print what went wrong with a specific fix suggestion rather than a generic error.

### User experience impact

| Before | After |
|--------|-------|
| Installation "succeeds" regardless of actual state | Installation confirms the product is working |
| First failure is silent (client just shows no tools) | First failure is caught at install with a fix suggestion |
| Support: "I installed it but it doesn't work" | Support load drops; attorneys trust the product from minute one |

---

## 7. Workflow Enforcement — The Prompt Resource Is Dormant

### What's happening now

`server.py` defines a Prompt resource called `lawtasksai-workflow` (lines 118–131) that contains the full 3-step workflow instructions. The intent is to prevent Claude from auto-executing skills without user confirmation — a real concern since an AI assistant that charges a credit without asking would erode trust quickly.

However, Claude Desktop and Cursor do not automatically load Prompt resources. The user would have to manually select `lawtasksai-workflow` from a slash menu on every new conversation. In practice, this means the prompt is effectively dead — no user will do this consistently, and most won't know it exists.

The tool descriptions in `TOOLS` do include confirmation instructions, which is good. But the system prompt (the most reliable place to enforce workflow rules) is only accessible through the dormant Prompt resource.

### Why it matters

If the AI auto-executes skills without asking, attorneys will be charged credits they didn't intend to spend. Even one instance of "it just ran something and deducted my credits without asking" is a trust-destroying event for an attorney audience that is already cautious about new technology.

### The fix

The confirmation instructions already in the tool descriptions are solid. Reinforce them by embedding a condensed version of the workflow rules in the `lawtasksai_search` result itself — every search response should end with a line reminding the AI to confirm before executing. This is already partially done (line 178 in server.py), but it can be made stronger and more explicit. The Prompt resource can stay as an optional enhancement, but the primary enforcement should live in the tool response, not a resource users never load.

### User experience impact

| Before | After |
|--------|-------|
| Workflow rules in a Prompt resource no one loads | Rules enforced through tool response on every search |
| Risk of AI auto-executing and spending credits silently | Credit deductions only happen after user confirmation |
| Attorney loses trust on first accidental charge | Consistent, predictable behavior builds trust |

---

## Summary Table

| # | Issue | Effort | Impact | Priority |
|---|-------|--------|--------|----------|
| 1 | Search quality — abbreviations, zero-result honesty, trigger phrases | Medium | 🔴 Critical — core UX | 1 |
| 2 | README tool name mismatch | Trivial | 🟠 High — first impression | 2 |
| 3 | Skills cache never refreshes / poisoned on API failure | Small | 🟠 High — reliability | 3 |
| 4 | Cursor/Windsurf wrong config paths | Small | 🟠 High — silent install failure | 4 |
| 5 | `is_published=False` bug in skills pusher | Small | 🔴 Critical — production safety | 5 |
| 6 | Post-install verification | Medium | 🟡 Medium — support reduction | 6 |
| 7 | Workflow enforcement via tool responses | Small | 🟡 Medium — trust/billing safety | 7 |

---

## Recommended Implementation Order

1. **Fix `is_published=False` bug** before touching anything else — it's a silent production risk.
2. **Fix README tool names** — 5 minutes, removes an embarrassing public inconsistency.
3. **Fix cache TTL and poisoned-cache case** — prevents the "returns nothing" silent failure.
4. **Fix Cursor/Windsurf config paths** — broadens install success rate before any marketing.
5. **Improve search: zero-result honesty + abbreviation map** — biggest UX lift, phased approach.
6. **Post-install verification** — reduces support burden as users start arriving.
7. **Server-side search** — the right long-term architecture; plan this as a proper sprint once items 1–6 are done.

---

*All issues above are grounded in the actual code at `/Users/clio/dev/lawtasksai-mcp/` and `/Users/clio/dev/lawtasksAI-admin/`. Line references are to the current state of each file as of this writing.*
