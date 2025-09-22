"""
Demo script for the Playwright AI Browser.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from intelligent_browser import IntelligentBrowser, UserCredentials


async def demo_website_browsing():
    """Demo function showing how to use the AI browser."""
    
    # Example 1: Browse a simple website
    print("🌐 Demo 1: Basic Website Browsing")
    print("=" * 50)
    
    browser = IntelligentBrowser(headless=False, slow_mo=2000)  # Slow down for demo
    
    try:
        await browser.start()
        
        # Browse a website
        results = await browser.analyze_and_browse(
            url="https://example.com",
            description="A simple example website"
        )
        
        print(f"✅ Browsing completed: {results['success']}")
        if results['success']:
            analysis = results.get('analysis', {})
            print(f"   Purpose: {analysis.get('purpose', 'Unknown')}")
            print(f"   Features: {analysis.get('key_features', [])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await browser.close()
    
    print("\n" + "=" * 50)
    
    # Example 2: Browse with account creation
    print("👤 Demo 2: Website Browsing with Account Creation")
    print("=" * 50)
    
    browser2 = IntelligentBrowser(headless=False, slow_mo=2000)
    
    try:
        await browser2.start()
        
        # Create demo credentials
        credentials = UserCredentials(
            email="demo@example.com",
            password="DemoPassword123!",
            first_name="Demo",
            last_name="User",
            username="demouser"
        )
        
        # Browse a website that might have account creation
        results = await browser2.analyze_and_browse(
            url="https://github.com",
            description="GitHub - a code hosting platform"
        )
        
        print(f"✅ Browsing completed: {results['success']}")
        
        # Try to create an account (this will likely fail for demo purposes)
        if results['success']:
            print("🔐 Attempting account creation...")
            account_result = await browser2.create_user_account(credentials)
            print(f"   Account creation: {'✅ Success' if account_result['success'] else '❌ Failed'}")
            if not account_result['success']:
                print(f"   Error: {account_result.get('error', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await browser2.close()


async def demo_with_custom_website():
    """Demo with a custom website URL."""
    
    print("🎯 Demo 3: Custom Website Browsing")
    print("=" * 50)
    
    # Get website URL from user input
    website_url = input("Enter a website URL to browse (or press Enter for default): ").strip()
    if not website_url:
        website_url = "https://httpbin.org"
    
    website_description = input("Enter a description of the website (optional): ").strip()
    if not website_description:
        website_description = None
    
    browser = IntelligentBrowser(headless=False, slow_mo=1500)
    
    try:
        await browser.start()
        
        results = await browser.analyze_and_browse(
            url=website_url,
            description=website_description
        )
        
        print(f"\n📊 Results:")
        print(f"   Success: {results['success']}")
        
        if results['success']:
            analysis = results.get('analysis', {})
            print(f"   Purpose: {analysis.get('purpose', 'Unknown')}")
            print(f"   Registration Required: {analysis.get('registration_required', False)}")
            
            browsing_steps = results.get('browsing_results', [])
            print(f"   Steps Taken: {len(browsing_steps)}")
            
            for i, step in enumerate(browsing_steps[:5], 1):  # Show first 5 steps
                action = step.get('analysis', {}).get('next_action', 'unknown')
                url = step.get('url', 'unknown')
                print(f"     {i}. {action} on {url}")
            
            if len(browsing_steps) > 5:
                print(f"     ... and {len(browsing_steps) - 5} more steps")
        else:
            print(f"   Error: {results.get('error', 'Unknown error')}")
        
        # Save session log
        log_path = browser.save_session_log()
        print(f"\n📝 Session log saved to: {log_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await browser.close()


async def main():
    """Main demo function."""
    print("🚀 Playwright AI Browser Demo")
    print("=" * 50)
    print("This demo shows how to use the AI-powered browser to:")
    print("1. Analyze websites using Claude Code SDK")
    print("2. Navigate websites intelligently")
    print("3. Create user accounts automatically")
    print("4. Follow natural user journeys")
    print("=" * 50)
    
    # Check if Claude API key is available
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        print("⚠️  Warning: CLAUDE_API_KEY environment variable not set.")
        print("   The AI analysis will not work without a valid API key.")
        print("   You can still run the demo to see the browser automation.")
        print()
    
    try:
        # Run demos
        await demo_website_browsing()
        await demo_with_custom_website()
        
        print("\n🎉 Demo completed!")
        print("=" * 50)
        print("To use this tool with your own websites:")
        print("1. Set your Claude API key: export CLAUDE_API_KEY='your-key-here'")
        print("2. Run: python -m src.main <website-url>")
        print("3. Or use the examples in the examples/ directory")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
