#!/usr/bin/env python3
"""
Setup script for Playwright AI Browser.
This script helps users set up the environment and dependencies.
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.10 or higher.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def check_node_js():
    """Check if Node.js is installed."""
    print("📦 Checking Node.js installation...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Node.js {result.stdout.strip()} is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is not installed. Please install Node.js from https://nodejs.org/")
        return False


def install_python_dependencies():
    """Install Python dependencies."""
    print("📚 Installing Python dependencies...")
    
    # Check if requirements.txt exists
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        print("❌ requirements.txt not found. Please run this script from the project root.")
        return False
    
    # Install dependencies
    return run_command("pip install -r requirements.txt", "Installing Python packages")


def install_playwright_browsers():
    """Install Playwright browsers."""
    print("🌐 Installing Playwright browsers...")
    return run_command("playwright install", "Installing Playwright browsers")


def install_claude_code_cli():
    """Install Claude Code CLI."""
    print("🤖 Installing Claude Code CLI...")
    return run_command("npm install -g @anthropic-ai/claude-code", "Installing Claude Code CLI")


def check_claude_api_key():
    """Check if Claude API key is set."""
    print("🔑 Checking Claude API key...")
    api_key = os.getenv("CLAUDE_API_KEY")
    if api_key:
        print("✅ Claude API key is set")
        return True
    else:
        print("⚠️  Claude API key is not set")
        print("   Please set it with: export CLAUDE_API_KEY='your-key-here'")
        print("   Or add it to your shell profile (.bashrc, .zshrc, etc.)")
        return False


def create_example_config():
    """Create an example configuration file."""
    print("📝 Creating example configuration...")
    
    config_content = """# Playwright AI Browser Configuration
# Copy this file to .env and fill in your values

# Required: Claude API Key
CLAUDE_API_KEY=your_claude_api_key_here

# Optional: Browser settings
PLAYWRIGHT_HEADLESS=false
PLAYWRIGHT_SLOW_MO=1000

# Optional: Logging
LOG_LEVEL=INFO
LOG_FILE=browser.log
"""
    
    try:
        with open(".env.example", "w") as f:
            f.write(config_content)
        print("✅ Created .env.example file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env.example: {e}")
        return False


def run_tests():
    """Run basic tests to verify installation."""
    print("🧪 Running basic tests...")
    
    # Test Python imports
    try:
        import playwright
        import anyio
        print("✅ Python dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Python dependencies: {e}")
        return False
    
    # Test Playwright
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        print("✅ Playwright browser test passed")
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        return False
    
    return True


def main():
    """Main setup function."""
    print("🚀 Playwright AI Browser Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("src").exists() or not Path("requirements.txt").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    success = True
    
    # Check system requirements
    if not check_python_version():
        success = False
    
    if not check_node_js():
        success = False
    
    if not success:
        print("\n❌ System requirements not met. Please install the missing dependencies.")
        sys.exit(1)
    
    # Install dependencies
    if not install_python_dependencies():
        success = False
    
    if not install_playwright_browsers():
        success = False
    
    if not install_claude_code_cli():
        success = False
    
    # Check configuration
    check_claude_api_key()
    
    # Create example files
    create_example_config()
    
    # Run tests
    if not run_tests():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Set your Claude API key: export CLAUDE_API_KEY='your-key-here'")
        print("2. Run the demo: python examples/demo.py")
        print("3. Or use the CLI: python -m src.main https://example.com")
    else:
        print("❌ Setup completed with errors. Please check the messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
