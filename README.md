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

### Option A: Claude Desktop* (Recommended for Claude users)

> **Requires Python 3.8+.** If you don't have Python installed, use Option B (OpenClaw) instead — no Python needed.

#### How it works

Claude Desktop can't call external services on its own — it uses a protocol called MCP (Model Context Protocol) to connect to tools. LawTasksAI includes a small server that runs on your computer and acts as the bridge between Claude and LawTasksAI's 200+ legal skills. The installer below sets this up automatically and backs up your existing settings first.

#### 1. Buy a Credit Pack

Start with the [Trial pack ($20 for 10 tasks)](https://lawtasksai.com/#pricing). Each task costs one credit. Credits never expire. After purchase, you'll receive a license key by email (starts with `lt_`).

#### 2. Download and Unzip

Go to your [LawTasksAI Account Page](https://lawtasksai.com/download.html), log in with your license key, and click "Download Skill Loader." Unzip the download — you'll find a `lawtasksai-mcp` folder inside.

#### 3. Run the Installer

Open a terminal (Mac: Terminal app, Windows: Command Prompt) and run:

```bash
cd lawtasksai-mcp
python install.py
```

The installer will:
- Install the required packages
- Safely add LawTasksAI to your Claude Desktop settings (your existing settings are backed up first)
- Prompt for your license key if needed

#### 4. Restart Claude Desktop and Ask a Question

> *"What's the statute of limitations for breach of contract in Texas?"*

> *"Draft a motion to compel discovery in a breach of contract case in Colorado."*

> *"Summarize Colorado's rules on expert witness disclosures."*

You don't need to know which task to use — LawTasksAI automatically picks the right one based on your question.

Works with any MCP-compatible client (Cursor, Windsurf, etc.) — just run the installer.

### Option B: OpenClaw (Easiest — no terminal required)

[OpenClaw](https://openclaw.ai) is a personal AI assistant that runs on your computer. No config files, no terminal commands — just conversation.

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

*\*Claude Desktop, Cursor, and other AI clients require their own subscription or API access. LawTasksAI credit packs cover LawTasksAI skills only — charges from your AI provider (Anthropic, OpenAI, etc.) are separate.*

---

## Disclaimer

LawTasksAI is software that assists attorneys and paralegals with legal research and drafting. It is not a law firm and does not provide legal advice. Always apply your own professional review and judgment to any output.

---

## Support

- **Website:** [lawtasksai.com](https://lawtasksai.com)
- **Email:** hello@lawtasksai.com
