# TasksAI MCP — Product Roadmap
*Last updated: 2026-04-27 | Author: Clio*

---

## Current State (as of 2026-04-27)

### What's Live
- 29 verticals, ~4,500 skills, all published to `api.taskvaultai.com`
- 29 landing pages on Cloudflare Pages (per-vertical branding via template)
- LawTasksAI MCP server (`lawtasksai-mcp`) — the only working MCP package
- Admin UI (`lawtasksAI-admin`) — manages all verticals
- Download endpoint: `/download/loader/{license_key}` — ships MCP zip to customers

### Critical Architecture Gap
The MCP server (`server.py`) is **LawTasksAI-specific**. Every other vertical's
download endpoint ships the same law-branded server with `lawtasksai_search`,
`lawtasksai_execute`, and a legal system prompt. A realtor or contractor who
purchases and installs gets a broken experience.

The landing page template is already vertical-aware (`{{PRODUCT_ID}}` etc.).
The MCP runtime layer is not.

---

## Completed Work (2026-04-27 Session)

All on branch `feature/skill-versioning`. Not yet merged to main.

| # | Fix | Repo | Status |
|---|-----|------|--------|
| 1 | `is_published` bug — pusher no longer unpublishes live skills | `lawtasksai-api` | ✅ Deployed |
| 2 | Version history in admin UI — live panel with restore | `lawtasksAI-admin` + `lawtasksai-api` | ✅ Deployed |
| 3 | Cache TTL (10 min) + failure isolation (no poisoned cache) | `lawtasksai-mcp` | ✅ GitHub |
| 4 | README tool name mismatch fixed (`lawtasks_` → `lawtasksai_`) | `lawtasksai-mcp` | ✅ GitHub |
| 5 | Cursor/Windsurf native config paths fixed | `lawtasksai-mcp` | ✅ GitHub |
| 6 | Post-install verification (license + credits + skill count) | `lawtasksai-mcp` | ✅ GitHub |
| 7 | Workflow guardrail in every search result | `lawtasksai-mcp` | ✅ GitHub |
| 8 | Trigger-phrase search + abbreviation expansion | `lawtasksai-mcp` | ✅ GitHub + Deployed |
| 9 | DB migration: `updated_at` column on `skill_versions` | `lawtasksai-api` | ✅ Run |

**Pending:**
- Merge `feature/skill-versioning` → `main` on all three repos (requires laudoluxDev push from Windows)
- Add missing trigger phrases for `MTC`, `TRO` etc. via admin UI (content task)

---

## Roadmap

Items are ordered by impact and logical dependency.
Sprints are rough estimates assuming half-day work sessions.

---

### Sprint 1 — Multi-Vertical MCP (Critical Path)

**Goal:** One MCP codebase that works for all 29 verticals.
Without this, only LawTasksAI customers have a functional MCP.

#### 1.1 — `GET /v1/me` endpoint on the API
- Returns vertical metadata from the license key: `product_id`, `product_name`,
  `tool_prefix`, `display_name`, `support_email`
- Example: `lt_xxx` → `{product_id: "law", product_name: "LawTasksAI", tool_prefix: "lawtasksai"}`
- All 29 license prefixes already in `verticals.json` — wire to the DB
- **Effort:** 2 hours | **Repo:** `lawtasksai-api`

#### 1.2 — Self-configuring MCP server
- On startup, `server.py` calls `GET /v1/me` to get vertical metadata
- Tool names become `{tool_prefix}_search`, `{tool_prefix}_execute` etc.
- System prompt uses `product_name` and vertical-specific language
- `LEGAL_ABBREVS` map becomes a per-vertical abbrev map (law has legal terms,
  realtor has MLS/CMA/etc., contractor has RFI/SOW/CO/etc.)
- `.env` uses `TASKSAI_LICENSE_KEY` (generic) instead of `LAWTASKSAI_LICENSE_KEY`
- **Effort:** 4 hours | **Repo:** `lawtasksai-mcp`

#### 1.3 — Multi-vertical download endpoint
- `/download/loader/{license_key}` already detects the vertical from the key prefix
- Ships the same `server.py` but with the `.env` pre-seeded with the correct
  `TASKSAI_LICENSE_KEY` value
- No per-vertical copies of `server.py` needed — one file handles all
- **Effort:** 2 hours | **Repo:** `lawtasksai-api`

#### 1.4 — Per-vertical abbreviation maps
- `LEGAL_ABBREVS` in `server.py` becomes a dict-of-dicts keyed by `product_id`
- Law: MTC, ROGs, RFA, TRO, SOL, MSJ, etc.
- Realtor: MLS, CMA, DOM, ARV, HOA, COE, etc.
- Contractor: RFI, SOW, CO, GC, Sub, NTP, PCO, etc.
- Farmer: ARC, FSA, NRCS, CRP, etc.
- Others added as needed
- **Effort:** 2 hours | **Repo:** `lawtasksai-mcp`

**Sprint 1 Total Effort:** ~1 day

---

### Sprint 2 — Trigger Phrase Content Gaps

**Goal:** Fill the most common abbreviation gaps in the trigger phrase database.

#### 2.1 — Law vertical trigger phrases
Missing from DB (confirmed 2026-04-27):
- `MTC` → motion-to-compel-drafter
- `TRO` → no skill exists yet (needs skill creation first)
- `RFA` → request-for-admissions skill
- `JNOV` → post-trial motions skill
- Fix via admin UI — batch update triggers endpoint: `POST /admin/triggers/batch`
- **Effort:** 1 hour | **Tool:** Admin UI

#### 2.2 — Other verticals
- Run a gap analysis per vertical: query common abbreviations, find zero-result cases
- Can be done systematically once Sprint 1 is live (use real customer queries
  once users exist, or run manual spot-checks per vertical now)
- **Effort:** 2 hours per vertical for spot-check | Ongoing

---

### Sprint 3 — Installer Polish

**Goal:** Professional install experience before marketing push.

#### 3.1 — `--uninstall` flag
- `python3 install.py --uninstall` removes MCP config entries from all clients
- Prevents orphaned config entries when customers switch products
- **Effort:** 2 hours | **Repo:** `lawtasksai-mcp`

#### 3.2 — Windows installer testing
- Currently written but untested on Windows
- Cursor/Windsurf paths on Windows need real-machine validation
- `%APPDATA%` vs `%LOCALAPPDATA%` paths for Windsurf need confirmation
- **Effort:** 1 hour | **Repo:** `lawtasksai-mcp`

#### 3.3 — `--update` flag
- `python3 install.py --update` re-downloads latest server.py from the API
  and replaces the local copy without touching `.env` or MCP configs
- Enables seamless updates without full re-install
- **Effort:** 2 hours | **Repo:** `lawtasksai-mcp`

---

### Sprint 4 — Admin UI Improvements

**Goal:** Make the admin UI a complete skills management tool.

#### 4.1 — Bulk publish / unpublish
- Select multiple skills, publish or unpublish in one action
- Currently requires individual skill edits
- **Effort:** 3 hours | **Repo:** `lawtasksAI-admin`

#### 4.2 — Trigger phrase editor
- Inline tag editor for trigger phrases in the skill editor
- Currently requires using the batch API directly
- **Effort:** 4 hours | **Repo:** `lawtasksAI-admin`

#### 4.3 — Search gap dashboard
- Eventually: table of most-searched terms that returned zero results
- Requires anonymous aggregate query logging (opt-in, no PII, client-side count only)
- Privacy-safe approach: client increments a counter on the API for zero-result
  queries using only the normalized query (not the original text, not any client data)
- **Effort:** 1 day | **Repos:** `lawtasksai-mcp` + `lawtasksai-api` + `lawtasksAI-admin`

#### 4.4 — Admin UI code split
- `index.html` is currently ~278KB of inline HTML/CSS/JS
- Split into modules for maintainability
- No user-facing impact — purely developer ergonomics
- **Effort:** 4 hours | **Repo:** `lawtasksAI-admin`

---

### Sprint 5 — Platform Hardening (Pre-Scale)

**Goal:** Ready for real marketing spend and customer volume.

#### 5.1 — Conversion tracking
- RealtorTasksAI Google Ads campaign is live but has no conversion tracking
- Need to link GA4 → Google Ads for all active campaigns
- **Effort:** 2 hours per vertical | **Tool:** Google Ads + GA4

#### 5.2 — Email capture on landing pages
- Currently no email capture on most landing pages
- Zoho Campaigns integration already exists for LawTasksAI
- Roll out to all verticals
- **Effort:** 2 hours per vertical | **Repo:** `tasksai-landing-template`

#### 5.3 — Rate limiting on download endpoint
- `/download/loader/{license_key}` is currently unauthenticated rate-limit-free
- Add per-key rate limiting (max 10 downloads/day) to prevent abuse
- **Effort:** 1 hour | **Repo:** `lawtasksai-api`

#### 5.4 — MCP server telemetry (privacy-safe)
- Anonymous counters: installs, tool calls, zero-result searches
- No query content, no client data, no PII — just counts
- Gives visibility into which verticals are actually being used
- **Effort:** 4 hours | **Repos:** `lawtasksai-mcp` + `lawtasksai-api`

---

## Priority Summary

| Sprint | Goal | Effort | Dependency |
|--------|------|--------|------------|
| 1 | Multi-vertical MCP | ~1 day | None — do first |
| 2 | Trigger phrase content | ~2 hours + ongoing | Sprint 1 for non-law verticals |
| 3 | Installer polish | ~1 day | Sprint 1 |
| 4 | Admin UI improvements | ~2 days | None — parallel with Sprint 1 |
| 5 | Platform hardening | ~1 week | Sprint 1 complete |

---

## Open Questions

1. **Merge strategy:** When to merge `feature/skill-versioning` to main?
   Recommendation: merge before starting Sprint 1 so the branch starts clean.

2. **`tasksai-api` repo:** Currently a README stub on GitHub. Should the
   full API source be pushed there? Or stay Google Drive only?
   Recommendation: push to GitHub (private repo) for proper version control
   and to enable Cloud Run's source-based deploy from GitHub.

3. **Vertical abbreviation maps:** Should these live in `server.py` (client-side)
   or in the DB as part of the trigger phrase system?
   Recommendation: DB long-term (admin-editable without code deploy), client-side
   as a bootstrap until the trigger phrases are complete.

4. **TRO and other missing law skills:** Some abbreviations (TRO) have no
   matching skill at all. Skill creation backlog exists separately from trigger
   phrase gaps.

---

*Session work documented in: `clio_obsidian_vault/Memory/` (end-of-session log)*
