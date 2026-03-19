# LawTasksAI MCP Server

**200+ AI-powered legal research and drafting skills for attorneys — accessible directly inside Claude, Cursor, and any MCP-compatible AI client.**

[![License Key Required](https://img.shields.io/badge/license-key-required-blue)](https://lawtasksai.com)
[![Website](https://img.shields.io/badge/website-lawtasksai.com-green)](https://lawtasksai.com)

---

## What It Does

LawTasksAI connects your AI assistant to a comprehensive library of legal skills built specifically for attorneys and paralegals:

- **Legal Research** — case law analysis, statute interpretation, regulatory review
- **Drafting** — motions, demand letters, contracts, briefs, memos
- **Litigation Support** — deposition prep, witness outlines, discovery checklists
- **Compliance** — ABA ethics guidance, jurisdiction-specific rules
- **Document Review** — contract analysis, risk identification, redline summaries

All 200+ skills are maintained and updated by legal professionals.

---

## Privacy

**LawTasksAI never receives your client data.**

Skills execute through your chosen AI provider (Claude, GPT, etc.). Your AI provider processes the content — LawTasksAI only delivers the skill instructions. Client confidences stay between you and your AI provider.

---

## Getting Started

### 1. Get a License Key

Sign up at **[lawtasksai.com](https://lawtasksai.com)** and purchase a credit pack. You'll receive a license key by email.

### 2. Add to Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lawtasksai": {
      "command": "npx",
      "args": ["-y", "@lawtasksai/mcp-server"],
      "env": {
        "LAWTASKSAI_LICENSE_KEY": "your-license-key-here"
      }
    }
  }
}
```

### 3. Start Using Skills

Once connected, ask Claude anything legal:

> *"Draft a motion to compel discovery for a breach of contract case in Colorado."*

> *"Analyze this contract clause for indemnification risk."*

> *"Prepare deposition outline for a plaintiff in a personal injury case."*

---

## Pricing

| Plan | Credits | Price |
|------|---------|-------|
| Trial | 10 tasks | $20 |
| Essentials | 50 tasks | $75 |
| Accelerator | 100 tasks | $125 |
| Efficient | 250 tasks | $250 |
| Unstoppable | 625 tasks | $500 |
| Apex | 1,500 tasks | $1,000 |

---

## Disclaimer

LawTasksAI is software that assists attorneys and paralegals with legal research and drafting. It is not a law firm and does not provide legal advice. Always apply your own professional review and judgment to any output.

---

## Support

- **Website:** [lawtasksai.com](https://lawtasksai.com)
- **Email:** hello@lawtasksai.com
