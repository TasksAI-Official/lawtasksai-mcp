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
    if sys.version_info < (3, 8):
        print(f"  ⚠️  Python {sys.version_info.major}.{sys.version_info.minor} detected.")
        print("  LawTasksAI requires Python 3.8 or later.")
        print("  Download Python at: https://python.org/downloads")
        sys.exit(1)


def get_mcp_clients():
    """Return dict of {client_name: config_path} for all installed MCP clients."""
    system = platform.system()
    clients = {}

    if system == "Darwin":
        claude_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        cursor_path = Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        windsurf_path = Path.home() / "Library" / "Application Support" / "Windsurf" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"

        if (Path.home() / "Applications" / "Claude.app").exists() or \
           Path("/Applications/Claude.app").exists() or \
           claude_path.parent.exists():
            clients["Claude Desktop"] = claude_path
        if (Path.home() / "Applications" / "Cursor.app").exists() or \
           Path("/Applications/Cursor.app").exists():
            clients["Cursor"] = cursor_path
        if (Path.home() / "Applications" / "Windsurf.app").exists() or \
           Path("/Applications/Windsurf.app").exists():
            clients["Windsurf"] = windsurf_path

    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        local = os.environ.get("LOCALAPPDATA", "")
        claude_path = Path(appdata) / "Claude" / "claude_desktop_config.json"
        cursor_path = Path(appdata) / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        windsurf_path = Path(local) / "Windsurf" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"

        for name, path in [("Claude Desktop", claude_path), ("Cursor", cursor_path), ("Windsurf", windsurf_path)]:
            if path and path.parent.exists():
                clients[name] = path

    else:
        claude_path = Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
        cursor_path = Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
        for name, path in [("Claude Desktop", claude_path), ("Cursor", cursor_path)]:
            if path and path.parent.exists():
                clients[name] = path

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

    print()
    print("  " + "=" * 50)
    print("  ✅ Installation complete!")
    print("  " + "=" * 50)
    print()
    if configured:
        print(f"  Configured: {', '.join(configured)}")
        print()
        print("  Next steps:")
        print("    1. Restart your MCP client(s)")
        print("    2. Start asking legal questions!")
        print()
        print("  Try asking:")
        print('    "Search for a motion to compel skill"')
        print('    "What statute of limitations skills do you have?"')
    print()
    print("  Support: hello@lawtasksai.com")
    print("  Website: https://lawtasksai.com")
    print()


if __name__ == "__main__":
    main()
