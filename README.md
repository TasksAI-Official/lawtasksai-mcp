# LawTasksAI MCP Server

**200+ AI-powered legal research and drafting skills for attorneys.**

Works with Claude Desktop, Cursor, Windsurf, and any MCP-compatible AI client.

[![LawTasksAI MCP server](https://glama.ai/mcp/servers/laudoluxDev/lawtasksai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/laudoluxDev/lawtasksai-mcp)

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

**Privacy model:** LawTasksAI.com never sees your client data. Skills run entirely on your machine — your documents stay local. For full details see our [Zero Data Retention & ABA Compliance guide](https://lawtasksai.com/zdr-aba-compliance-guide).

---

## Quick Install

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
| `lawtasks_search` | Search 200+ skills by legal topic |
| `lawtasks_execute` | Get the full expert framework for a skill (costs 1 credit) |
| `lawtasks_balance` | Check your remaining credit balance |
| `lawtasks_categories` | Browse skills by practice area |

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
