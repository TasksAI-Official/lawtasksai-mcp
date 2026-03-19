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

### Option A: Claude Desktop / MCP Clients

#### 1. Buy a Credit Pack

Start with the [Trial pack ($20 for 10 tasks)](https://lawtasksai.com/#pricing). Each task costs one credit. Credits never expire. After purchase, you'll receive a license key by email (starts with `lt_`).

#### 2. Download the MCP Server

Go to your [LawTasksAI Account Page](https://lawtasksai.com/download.html), log in with your license key, and click "Download Skill Loader." Unzip the download — you'll find a `lawtasksai-mcp` folder inside.

#### 3. Install Dependencies

```bash
cd lawtasksai-mcp
pip install -r requirements.txt
```

#### 4. Configure Claude Desktop

Edit your Claude Desktop config file:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add:

```json
{
  "mcpServers": {
    "lawtasksai": {
      "command": "python",
      "args": ["/FULL/PATH/TO/lawtasksai-mcp/server.py"],
      "env": {
        "LAWTASKSAI_LICENSE_KEY": "lt_your_key_here"
      }
    }
  }
}
```

Your license key is also pre-configured in the `.env` file included in the download.

#### 5. Restart Claude Desktop and Ask a Question

> *"What's the statute of limitations for breach of contract in Texas?"*

> *"Draft a motion to compel discovery in a breach of contract case in Colorado."*

> *"Summarize Colorado's rules on expert witness disclosures."*

You don't need to know which task to use — LawTasksAI automatically picks the right one based on your question.

Works with any MCP-compatible client (Cursor, Windsurf, etc.) — just point it to `server.py`.

### Option B: OpenClaw (Easiest)

[OpenClaw](https://openclaw.ai) is a personal AI assistant that runs on your computer. No config file editing required.

1. Install [OpenClaw](https://openclaw.ai) (one command)
2. Download the skill file from your [Account Page](https://lawtasksai.com/download.html)
3. Tell OpenClaw: *"I just downloaded the LawTasksAI skill file to my Downloads folder. Please find it, unzip it if needed, and install it so I can use it. My license key is lt_XXXXX"*
4. Start asking legal questions — 200+ tasks ready to use

See [full setup guide](https://lawtasksai.com/getting-started.html) for detailed step-by-step instructions.

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
