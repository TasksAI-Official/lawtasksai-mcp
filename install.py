#!/usr/bin/env python3
"""
LawTasksAI Installer for Claude Desktop

This script adds LawTasksAI to your Claude Desktop configuration.
It backs up your existing config before making any changes.

Usage:
    python install.py
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def get_config_path():
    """Find the Claude Desktop config file for this OS."""
    system = platform.system()
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
    print(f"❌ Unsupported operating system: {system}")
    print("   Please see https://lawtasksai.com/getting-started.html for manual setup.")
    sys.exit(1)


def get_server_path():
    """Get the absolute path to server.py in the same directory as this script."""
    return str(Path(__file__).parent.resolve() / "server.py")


def get_license_key():
    """Read license key from .env file or prompt the user."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("LAWTASKSAI_LICENSE_KEY="):
                    key = line.split("=", 1)[1].strip()
                    if key and key != "YOUR_KEY_HERE":
                        return key
    
    print("\n🔑 Enter your LawTasksAI license key (starts with lt_):")
    key = input("   > ").strip()
    if not key:
        print("❌ No license key provided. You can find it in your purchase confirmation email.")
        sys.exit(1)
    return key


def install_dependencies():
    """Install required Python packages."""
    req_path = Path(__file__).parent / "requirements.txt"
    if req_path.exists():
        print("\n📦 Installing required packages...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(req_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"⚠️  Package install warning: {result.stderr[:200]}")
        else:
            print("   ✅ Packages installed.")


def update_config(config_path, server_path, license_key):
    """Add LawTasksAI to Claude Desktop config, preserving existing servers."""
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read existing config or start fresh
    config = {}
    if config_path.exists():
        # Back up existing config
        backup_path = config_path.with_suffix(f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
        shutil.copy2(config_path, backup_path)
        print(f"\n💾 Backed up existing config to:\n   {backup_path}")
        
        with open(config_path) as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Existing config file was invalid JSON. Starting fresh (backup saved).")
                config = {}
    
    # Add LawTasksAI server entry
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["lawtasksai"] = {
        "command": "python",
        "args": [server_path],
        "env": {
            "LAWTASKSAI_LICENSE_KEY": license_key
        }
    }
    
    # Write updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    return True


def main():
    print("=" * 50)
    print("  LawTasksAI Installer for Claude Desktop")
    print("=" * 50)
    print()
    print("This installer will:")
    print("  1. Install required Python packages")
    print("  2. Add LawTasksAI to your Claude Desktop config")
    print("     (your existing config is backed up first)")
    print()
    print("After installation, restart Claude Desktop to")
    print("start using 200+ legal research and drafting skills.")
    print()
    
    input("Press Enter to continue (or Ctrl+C to cancel)... ")
    
    # Step 1: Find config
    config_path = get_config_path()
    server_path = get_server_path()
    
    # Step 2: Get license key
    license_key = get_license_key()
    
    # Step 3: Install dependencies
    install_dependencies()
    
    # Step 4: Update config
    print(f"\n⚙️  Adding LawTasksAI to Claude Desktop config...")
    update_config(config_path, server_path, license_key)
    print("   ✅ Config updated.")
    
    # Done
    print()
    print("=" * 50)
    print("  ✅ Installation complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("  1. Restart Claude Desktop")
    print("  2. Ask a legal question, like:")
    print('     "What\'s the statute of limitations for')
    print('      breach of contract in Texas?"')
    print()
    print("Support: hello@lawtasksai.com")
    print("Website: https://lawtasksai.com")


if __name__ == "__main__":
    main()
