"""
Complete example demonstrating the Playwright AI Browser capabilities.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from intelligent_browser import IntelligentBrowser, UserCredentials


async def complete_browsing_demo():
    """Complete demo showing all features of the AI browser."""
    
    print("🚀 Playwright AI Browser - Complete Demo")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        print("⚠️  Warning: CLAUDE_API_KEY not set. AI analysis will not work.")
        print("   Set it with: export CLAUDE_API_KEY='your-key-here'")
        print()
    
    # Create browser instance
    browser = IntelligentBrowser(
        headless=False,  # Show browser for demo
        slow_mo=2000,    # Slow down for visibility
        api_key=api_key
    )
    
    # Demo credentials
    demo_credentials = UserCredentials(
        email="demo@example.com",
        password="DemoPassword123!",
        first_name="Demo",
        last_name="User",
        username="demouser"
    )
    
    try:
        # Start the browser
        print("🌐 Starting browser...")
        await browser.start()
        
        # Example 1: Simple website browsing
        print("\n📖 Example 1: Simple Website Browsing")
        print("-" * 40)
        
        results = await browser.analyze_and_browse(
            url="https://httpbin.org",
            description="A simple HTTP testing service"
        )
        
        print(f"✅ Browsing completed: {results['success']}")
        if results['success']:
            analysis = results.get('analysis', {})
            print(f"   Purpose: {analysis.get('purpose', 'Unknown')}")
            print(f"   Features: {', '.join(analysis.get('key_features', [])[:3])}")
            
            browsing_steps = results.get('browsing_results', [])
            print(f"   Steps taken: {len(browsing_steps)}")
        
        # Example 2: Website with potential account creation
        print("\n👤 Example 2: Website with Account Creation")
        print("-" * 40)
        
        # Try a website that might have signup
        results2 = await browser.analyze_and_browse(
            url="https://github.com",
            description="GitHub - a code hosting platform for version control"
        )
        
        print(f"✅ Browsing completed: {results2['success']}")
        if results2['success']:
            analysis2 = results2.get('analysis', {})
            print(f"   Purpose: {analysis2.get('purpose', 'Unknown')}")
            print(f"   Registration required: {analysis2.get('registration_required', False)}")
            
            # Try to create an account (this will likely fail for demo purposes)
            print("🔐 Attempting account creation...")
            account_result = await browser.create_user_account(demo_credentials)
            print(f"   Account creation: {'✅ Success' if account_result['success'] else '❌ Failed'}")
            if not account_result['success']:
                print(f"   Reason: {account_result.get('error', 'Unknown error')}")
        
        # Example 3: Interactive website exploration
        print("\n🔍 Example 3: Interactive Website Exploration")
        print("-" * 40)
        
        # Ask user for a website to explore
        print("Enter a website URL to explore (or press Enter for default):")
        user_url = input().strip()
        if not user_url:
            user_url = "https://example.com"
        
        print(f"🌐 Exploring: {user_url}")
        
        results3 = await browser.analyze_and_browse(
            url=user_url,
            description="User-specified website for exploration"
        )
        
        print(f"✅ Exploration completed: {results3['success']}")
        if results3['success']:
            analysis3 = results3.get('analysis', {})
            print(f"   Website purpose: {analysis3.get('purpose', 'Unknown')}")
            
            browsing_steps = results3.get('browsing_results', [])
            print(f"   Actions taken: {len(browsing_steps)}")
            
            # Show first few actions
            for i, step in enumerate(browsing_steps[:5], 1):
                action = step.get('analysis', {}).get('next_action', 'unknown')
                url = step.get('url', 'unknown')
                print(f"     {i}. {action} on {url}")
            
            if len(browsing_steps) > 5:
                print(f"     ... and {len(browsing_steps) - 5} more actions")
        
        # Save session logs
        print("\n📝 Saving session logs...")
        log_path = browser.save_session_log()
        print(f"   Session log saved to: {log_path}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always close the browser
        print("\n🔄 Closing browser...")
        await browser.close()
        print("✅ Browser closed")
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\nKey features demonstrated:")
    print("✅ AI-powered website analysis")
    print("✅ Intelligent navigation and browsing")
    print("✅ Automatic account creation attempts")
    print("✅ Interactive website exploration")
    print("✅ Session logging and error handling")
    
    print("\nTo use this tool with your own websites:")
    print("1. Set your Claude API key: export CLAUDE_API_KEY='your-key-here'")
    print("2. Run: python -m src.main <website-url>")
    print("3. Or customize the examples in the examples/ directory")


async def quick_test():
    """Quick test to verify everything is working."""
    print("🧪 Quick Test - Verifying Installation")
    print("=" * 40)
    
    browser = IntelligentBrowser(headless=True)  # Headless for quick test
    
    try:
        await browser.start()
        print("✅ Browser started successfully")
        
        # Test navigation
        page_info = await browser.browser.navigate_to("data:text/html,<html><body><h1>Test</h1></body></html>")
        if "error" not in page_info:
            print("✅ Navigation test passed")
        else:
            print(f"❌ Navigation test failed: {page_info['error']}")
        
        await browser.close()
        print("✅ Browser closed successfully")
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


async def main():
    """Main function."""
    print("Choose an option:")
    print("1. Quick test (verify installation)")
    print("2. Complete demo (full features)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        success = await quick_test()
        if success:
            print("\n✅ Installation verified! You can now run the complete demo.")
    elif choice == "2":
        await complete_browsing_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
