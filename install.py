#!/usr/bin/env python3
"""
Quick installation script for Playwright AI Browser.
"""
import subprocess
import sys
import os
from pathlib import Path


def main():
    """Main installation function."""
    print("🚀 Installing Playwright AI Browser...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Install Playwright browsers
    print("🌐 Installing Playwright browsers...")
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
        print("✅ Playwright browsers installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Playwright browsers")
        sys.exit(1)
    
    # Install Claude Code CLI
    print("🤖 Installing Claude Code CLI...")
    try:
        subprocess.run(["npm", "install", "-g", "@anthropic-ai/claude-code"], check=True)
        print("✅ Claude Code CLI installed")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to install Claude Code CLI. Please install manually:")
        print("   npm install -g @anthropic-ai/claude-code")
    
    print("\n🎉 Installation completed!")
    print("\nNext steps:")
    print("1. Set your Claude API key: export CLAUDE_API_KEY='your-key-here'")
    print("2. Run the demo: python examples/demo.py")
    print("3. Or use the CLI: python -m src.main https://example.com")


if __name__ == "__main__":
    main()
