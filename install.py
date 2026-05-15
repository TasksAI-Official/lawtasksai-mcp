#!/usr/bin/env python3
"""
LawTasksAI MCP Installer

Detects and configures LawTasksAI for all supported MCP clients:
  - Claude Desktop
  - Cursor
  - Windsurf

Backs up existing configs before making any changes.

Usage:
    python3 install.py
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def get_python_path():
    """Return full path to python3 so MCP clients can find it regardless of PATH."""
    for candidate in [sys.executable, shutil.which("python3"),
                      "/opt/homebrew/bin/python3", "/usr/bin/python3",
                      "/usr/local/bin/python3"]:
        if candidate and Path(candidate).exists():
            return candidate
    return sys.executable


def get_server_path():
    return str(Path(__file__).parent.resolve() / "server.py")


def get_license_key():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("LAWTASKSAI_LICENSE_KEY="):
                    key = line.split("=", 1)[1].strip()
                    if key and key != "YOUR_KEY_HERE":
                        return key
    print("\n  Enter your LawTasksAI license key (starts with lt_):")
    key = input("   > ").strip()
    if not key:
        print("  No license key provided. Check your purchase confirmation email.")
        sys.exit(1)
    return key


def check_python_version():
    """Warn if Python version is too old."""
    if sys.version_info < (3, 10):
        print(f"  ⚠️  Python {sys.version_info.major}.{sys.version_info.minor} detected.")
        print("  LawTasksAI requires Python 3.10 or later.")
        print("  Download Python at: https://python.org/downloads")
        sys.exit(1)


def _resolve_client_path(candidates):
    """
    Given a list of candidate config paths (in priority order), return the
    first one whose parent directory already exists, or the first candidate
    as the default write target (installer will create the dir).
    """
    for path in candidates:
        if path.parent.exists():
            return path
    # No existing parent found — return the first (highest-priority) path.
    # update_config() will mkdir -p the parent before writing.
    return candidates[0]


def get_mcp_clients():
    """
    Return dict of {client_name: config_path} for all installed MCP clients.

    For Cursor and Windsurf we check their native MCP config paths first.
    If those don't exist, we fall back to the Cline extension path so users
    who run Cursor/Windsurf via the Cline plugin are also covered.
    """
    system = platform.system()
    clients = {}

    if system == "Darwin":
        # Claude Desktop
        claude_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        if (Path.home() / "Applications" / "Claude.app").exists() or \
           Path("/Applications/Claude.app").exists() or \
           claude_path.parent.exists():
            clients["Claude Desktop"] = claude_path

        # Cursor — native path first, Cline extension fallback
        cursor_native  = Path.home() / ".cursor" / "mcp.json"
        cursor_cline   = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if (Path.home() / "Applications" / "Cursor.app").exists() or \
           Path("/Applications/Cursor.app").exists() or \
           cursor_native.parent.exists() or cursor_cline.parent.exists():
            clients["Cursor"] = _resolve_client_path([cursor_native, cursor_cline])

        # Windsurf — native path first, Cline extension fallback
        windsurf_native = Path.home() / ".codeium" / "windsurf" / "mcp_config.json"
        windsurf_cline  = Path.home() / "Library" / "Application Support" / "Windsurf" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if (Path.home() / "Applications" / "Windsurf.app").exists() or \
           Path("/Applications/Windsurf.app").exists() or \
           windsurf_native.parent.exists() or windsurf_cline.parent.exists():
            clients["Windsurf"] = _resolve_client_path([windsurf_native, windsurf_cline])

        # Cline (standalone VS Code extension)
        cline_vscode = Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if cline_vscode.parent.exists() and "Cursor" not in clients and "Windsurf" not in clients:
            clients["Cline (VS Code)"] = cline_vscode

    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        local   = os.environ.get("LOCALAPPDATA", "")

        # Claude Desktop
        claude_path = Path(appdata) / "Claude" / "claude_desktop_config.json"
        if claude_path.parent.exists():
            clients["Claude Desktop"] = claude_path

        # Cursor — native path first, Cline extension fallback
        cursor_native = Path(appdata) / "Cursor" / "User" / "globalStorage" / "cursor-mcp" / "mcp.json"
        cursor_cline  = Path(appdata) / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if cursor_native.parent.exists() or cursor_cline.parent.exists():
            clients["Cursor"] = _resolve_client_path([cursor_native, cursor_cline])

        # Windsurf — native path first, Cline extension fallback
        windsurf_native = Path(local) / "Windsurf" / "User" / "globalStorage" / "windsurf-mcp" / "mcp_config.json"
        windsurf_cline  = Path(local) / "Windsurf" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if windsurf_native.parent.exists() or windsurf_cline.parent.exists():
            clients["Windsurf"] = _resolve_client_path([windsurf_native, windsurf_cline])

        # Cline (standalone VS Code extension)
        cline_vscode = Path(appdata) / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if cline_vscode.parent.exists() and "Cursor" not in clients and "Windsurf" not in clients:
            clients["Cline (VS Code)"] = cline_vscode

    else:
        # Linux
        claude_path = Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
        if claude_path.parent.exists():
            clients["Claude Desktop"] = claude_path

        # Cursor — native path first, Cline extension fallback
        cursor_native = Path.home() / ".cursor" / "mcp.json"
        cursor_cline  = Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if cursor_native.parent.exists() or cursor_cline.parent.exists():
            clients["Cursor"] = _resolve_client_path([cursor_native, cursor_cline])

        # Windsurf — native path first, Cline extension fallback
        windsurf_native = Path.home() / ".codeium" / "windsurf" / "mcp_config.json"
        windsurf_cline  = Path.home() / ".config" / "Windsurf" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if windsurf_native.parent.exists() or windsurf_cline.parent.exists():
            clients["Windsurf"] = _resolve_client_path([windsurf_native, windsurf_cline])

        # Cline (standalone VS Code extension)
        cline_vscode = Path.home() / ".config" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        if cline_vscode.parent.exists() and "Cursor" not in clients and "Windsurf" not in clients:
            clients["Cline (VS Code)"] = cline_vscode

    return clients


def install_dependencies():
    req_path = Path(__file__).parent / "requirements.txt"
    if req_path.exists():
        print("\n  Installing required packages...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(req_path)],
            capture_output=True, text=True
        )
        # Handle externally-managed Python environments (e.g. Homebrew Python on macOS)
        if result.returncode != 0 and "externally-managed-environment" in result.stderr:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "-r", str(req_path)],
                capture_output=True, text=True
            )
        if result.returncode != 0:
            print("  ⚠️  Could not install packages automatically.")
            print("  Run manually: pip3 install mcp httpx python-dotenv")
        else:
            print("  ✅ Packages installed.")


def update_config(client_name, config_path, server_path, python_path, license_key):
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config = {}
    if config_path.exists():
        backup_path = config_path.with_suffix(
            f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        )
        shutil.copy2(config_path, backup_path)
        print(f"    💾 Backed up existing config to: {backup_path.name}")
        with open(config_path) as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print("    ⚠️  Existing config was invalid — starting fresh (backup saved).")
                config = {}

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    config["mcpServers"]["lawtasksai"] = {
        "command": python_path,
        "args": [server_path],
        "env": {"LAWTASKSAI_LICENSE_KEY": license_key}
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"    ✅ Config updated: {config_path}")


def verify_installation(license_key):
    """
    After config is written, make a live API call to confirm:
    - License key is valid
    - Credits are accessible
    - Skills are available

    Returns True on success, False on failure.
    """
    import urllib.request
    import urllib.error

    API_BASE = "https://api.taskvaultai.com"
    print()
    print("  Verifying installation...")

    # Step 1: Check license / credits
    try:
        req = urllib.request.Request(
            f"{API_BASE}/v1/credits/balance",
            headers={"Authorization": f"Bearer {license_key}"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            import json as _json
            data = _json.loads(resp.read())
            credits = data.get("credits_balance", "?")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("  ❌ License key is invalid or expired.")
            print("     Check your purchase confirmation email or visit lawtasksai.com/account")
        elif e.code == 402:
            print("  ⚠️  License key valid but no credits remaining.")
            print("     Purchase more at: https://lawtasksai.com/#pricing")
        else:
            print(f"  ⚠️  Could not verify license (HTTP {e.code}).")
            print("     Installation may still work — restart your MCP client and try.")
        return False
    except Exception as e:
        print(f"  ⚠️  Could not reach LawTasksAI servers ({type(e).__name__}).")
        print("     Check your internet connection. Installation files are in place.")
        return False

    # Step 2: Count available skills
    try:
        req = urllib.request.Request(
            f"{API_BASE}/v1/skills",
            headers={"Authorization": f"Bearer {license_key}"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            import json as _json
            skills = _json.loads(resp.read())
            skill_count = len(skills) if isinstance(skills, list) else "?"
    except Exception:
        skill_count = "?"

    print(f"  ✅ License verified — {credits} credits available, {skill_count} skills ready")
    return True


def no_python_fallback():
    """Shown when no MCP clients are detected."""
    print()
    print("  No supported MCP clients detected on this machine.")
    print("  Supported clients: Claude Desktop, Cursor, Windsurf")
    print()
    print("  ─────────────────────────────────────────────────")
    print("  Don't have Python or a supported MCP client?")
    print()
    print("  You can use LawTasksAI without any installation:")
    print("  → Web app:   https://lawtasksai.com")
    print("  → OpenClaw:  Works out of the box, no Python needed.")
    print("               See: https://lawtasksai.com/getting-started.html")
    print()
    print("  For manual MCP setup instructions:")
    print("  → https://lawtasksai.com/getting-started.html")
    print("  ─────────────────────────────────────────────────")
    print()
    print("  Support: hello@lawtasksai.com")


def main():
    print()
    print("  " + "=" * 50)
    print("  LawTasksAI MCP Installer  v1.4.0")
    print("  " + "=" * 50)
    print()

    check_python_version()

    clients = get_mcp_clients()
    if not clients:
        no_python_fallback()
        sys.exit(0)

    print(f"  Detected MCP client(s): {', '.join(clients.keys())}")
    print()
    print("  This installer will:")
    print("    1. Install required Python packages")
    print("    2. Configure LawTasksAI in each detected client")
    print("       (existing configs are backed up first)")
    print()
    input("  Press Enter to continue (or Ctrl+C to cancel)... ")

    license_key = get_license_key()
    server_path = get_server_path()
    python_path = get_python_path()

    install_dependencies()

    print()
    configured = []
    for client_name, config_path in clients.items():
        print(f"  Configuring {client_name}...")
        try:
            update_config(client_name, config_path, server_path, python_path, license_key)
            configured.append(client_name)
        except Exception as e:
            print(f"    ⚠️  Warning: could not configure {client_name}: {e}")

    # Post-install verification
    verified = False
    if configured:
        verified = verify_installation(license_key)

    print()
    print("  " + "=" * 50)
    print("  ✅ Installation complete!")
    print("  " + "=" * 50)
    print()
    if configured:
        print(f"  Configured: {', '.join(configured)}")
        print()
        if verified:
            print("  Next steps:")
            print("    1. Restart your MCP client(s)")
            print("    2. Start asking legal questions!")
            print()
            print("  Try asking:")
            print('    "Search for a motion to compel skill"')
            print('    "What statute of limitations skills do you have?"')
        else:
            print("  ⚠️  Verification did not complete — see message above.")
            print("     Your config files are in place. Once the issue is resolved,")
            print("     restart your MCP client and try again.")
    print()
    print("  Support: hello@lawtasksai.com")
    print("  Website: https://lawtasksai.com")
    print()


if __name__ == "__main__":
    main()
