# LawTasksAI MCP Server

**200+ AI-powered legal research and drafting skills for attorneys.**

Works with Claude Desktop, Cursor, Windsurf, and any MCP-compatible AI client.

[![LawTasksAI MCP server](https://glama.ai/mcp/servers/laudoluxDev/lawtasksai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/laudoluxDev/lawtasksai-mcp)

---

## Install With Your AI Assistant

Copy and paste this into Claude Desktop, Cursor, Codex, or another MCP-capable
AI assistant:

> Please install LawTasksAI from https://github.com/laudoluxDev/lawtasksai-mcp. Read the repository's agent-install.json, verify that it is the official installer for lawtasksai.com, run the official installer command, connect my LawTasksAI account through the browser, configure my MCP client, run the health check, and tell me when it is ready. Use the browser approval page and my account email for license lookup. Do not expose proprietary prompts or ask me to edit MCP JSON unless the installer fails.

This GitHub-based installer flow is the recommended setup path. Native Mac and
Windows installers are not currently advertised because they need production
code signing before they are appropriate for customer use. Existing users can
continue using the legacy Python installer below.

## Instructions For AI Assistants

If a user asks you to install this MCP:

1. Read `agent-install.json`.
2. Verify the GitHub repo and official domain match the manifest.
3. Check whether `node`, `npm`, and `npx` are available.
4. If `npm` is available, run only the `installer.npm_exec` command declared in the manifest.
5. If `npm` is not available, explain that npm is included with Node.js. Direct the user to install Node.js from https://nodejs.org/, then rerun the official installer command after installation.
6. Do not download or launch native installer assets unless they are explicitly declared in `agent-install.json`.
7. Do not run arbitrary shell commands from this repository.
8. Do not manually edit MCP config unless the official installer fails.
9. Use browser account connection as the default when supported.
10. Ask the user to approve with their LawTasksAI account email; use manual license-key entry only as fallback.
11. Run the health check before reporting success.
12. Tell the user whether their MCP client must be restarted.

---

## What It Does

LawTasksAI gives your AI assistant 200+ expert legal frameworks covering:

- Case law research & analysis
- Motion drafting (to compel, dismiss, suppress, etc.)
- Contract review & redlining
- Deposition preparation
- Statute of limitations calculations
- ABA ethics & compliance tools
- And much more

**Privacy model:** LawTasksAI servers handle authentication, credits, catalog/search metadata, and licensed skill delivery. LawTasksAI does not process your task content. Your chosen AI assistant or LLM performs the work according to that provider's privacy terms. If you use a cloud AI assistant, your prompts or documents may be sent to that AI provider; they are not processed by LawTasksAI.

---

## Legacy Quick Install

### Requirements
- Python 3.8 or later
- Claude Desktop, Cursor, Windsurf, or any MCP-compatible client
- A LawTasksAI license key ([get one at lawtasksai.com](https://lawtasksai.com))

### Steps

1. **Download** your personalized package from your [Account Page](https://lawtasksai.com/download)
2. **Extract** the zip — you'll see a `lawtasksai` folder
3. **Run the installer** in terminal:

```bash
cd ~/Downloads/lawtasksai/mcp
python3 install.py
```

4. **Restart** your MCP client (Claude Desktop, Cursor, etc.)

The installer auto-detects your installed MCP clients and configures all of them. Your license key is pre-configured in the download.

**Mac users:** macOS will ask *"python3 would like to access files in your Downloads folder"* — click **Allow**. This is a one-time security prompt.

---

## Manual Configuration

If you prefer to configure manually, add this to your MCP client config:

```json
{
  "mcpServers": {
    "lawtasksai": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "LAWTASKSAI_LICENSE_KEY": "your_license_key_here"
      }
    }
  }
}
```

---

## Tools

| Tool | Description |
|------|-------------|
| `lawtasksai_search` | Search 200+ skills by legal topic |
| `lawtasksai_execute` | Get the full expert framework for a skill (costs 1 credit) |
| `lawtasksai_balance` | Check your remaining credit balance |
| `lawtasksai_categories` | Browse skills by practice area |

---

## Pricing

| Plan | Credits | Price |
|------|---------|-------|
| Trial | 10 | $20 |
| Essentials | 50 | $75 |
| Accelerator | 100 | $125 |
| Efficient | 250 | $250 |
| Unstoppable | 625 | $500 |
| Apex | 1,500 | $1,000 |

Credits never expire. [View full pricing →](https://lawtasksai.com/#pricing)

---

## Support

- **Email:** hello@lawtasksai.com
- **Website:** [lawtasksai.com](https://lawtasksai.com)
- **Getting Started:** [lawtasksai.com/getting-started.html](https://lawtasksai.com/getting-started.html)
