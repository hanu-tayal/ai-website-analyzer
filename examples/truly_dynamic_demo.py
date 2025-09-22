"""
Truly dynamic browser demo that shows real-time action discovery from page content.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from truly_dynamic_browser import TrulyDynamicBrowser


async def truly_dynamic_demo():
    """Demo showing truly dynamic browsing capabilities."""
    
    print("🚀 Truly Dynamic Browser Demo")
    print("=" * 60)
    print("This demo shows real-time action discovery from page content")
    print("No predetermined patterns - everything is discovered dynamically!")
    print("=" * 60)
    
    # Create browser instance
    browser = TrulyDynamicBrowser(
        headless=False,  # Show browser for demo
        slow_mo=2000     # Slow down for visibility
    )
    
    try:
        # Start the browser
        print("🌐 Starting truly dynamic browser...")
        await browser.start()
        
        # Example 1: Truly dynamic website exploration
        print("\n🔍 Example 1: Truly Dynamic Website Exploration")
        print("-" * 50)
        
        website_url = input("Enter a website URL to explore (or press Enter for default): ").strip()
        if not website_url:
            website_url = "https://httpbin.org"
        
        print(f"\n🌐 Exploring: {website_url}")
        print("🔍 Browser will discover all possible actions from page content...")
        
        results = await browser.analyze_and_browse(url=website_url)
        
        print(f"\n✅ Truly dynamic browsing completed: {results['success']}")
        
        if results['success']:
            browsing_steps = results.get('browsing_results', [])
            discovered_actions = results.get('discovered_actions', [])
            
            print(f"\n🔍 Total Actions Discovered: {len(discovered_actions)}")
            print(f"🤖 Actions Executed: {len(browsing_steps)}")
            
            print(f"\n🧠 Action Discovery Process:")
            for i, step in enumerate(browsing_steps, 1):
                discovered = step.get('discovered_actions', [])
                chosen = step.get('chosen_action', {})
                url = step.get('url', 'unknown')
                
                print(f"   Step {i}: {url}")
                print(f"     Discovered {len(discovered)} possible actions")
                if chosen:
                    print(f"     Chose: {chosen.get('description', 'Unknown action')}")
                    print(f"     Type: {chosen.get('type', 'Unknown')}")
                    print(f"     Confidence: {chosen.get('confidence', 0):.2f}")
                print()
            
            # Show action discovery breakdown
            action_types = {}
            for action in discovered_actions:
                action_type = action.get('type', 'unknown')
                action_types[action_type] = action_types.get(action_type, 0) + 1
            
            print("📊 Action Types Discovered:")
            for action_type, count in action_types.items():
                print(f"   {action_type}: {count} actions")
        
        else:
            print(f"❌ Browsing failed: {results.get('error', 'Unknown error')}")
        
        # Save session logs
        print("\n📝 Saving discovery session logs...")
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
    print("🎉 Truly Dynamic Demo completed!")
    print("\nKey features demonstrated:")
    print("✅ Real-time action discovery from page content")
    print("✅ No predetermined patterns or steps")
    print("✅ Intelligent action prioritization")
    print("✅ Dynamic form detection and filling")
    print("✅ Context-aware action selection")
    print("✅ Truly adaptive browsing behavior")
    
    print("\nThis is what makes it truly dynamic:")
    print("- Analyzes actual page content in real-time")
    print("- Discovers all possible interactive elements")
    print("- Categorizes actions by type and priority")
    print("- Chooses actions based on content analysis")
    print("- No hardcoded patterns - everything is discovered!")
    print("- Adapts to any website structure automatically")


async def quick_test():
    """Quick test to verify the truly dynamic browser works."""
    print("🧪 Quick Test - Truly Dynamic Browser")
    print("=" * 40)
    
    browser = TrulyDynamicBrowser(headless=True)
    
    try:
        await browser.start()
        print("✅ Truly dynamic browser started successfully")
        
        # Test action discovery
        test_html = """
        <html>
            <body>
                <h1>Test Page</h1>
                <a href="/about">About Us</a>
                <a href="/contact">Contact</a>
                <button>Click Me</button>
                <form>
                    <input type="email" name="email" placeholder="Email">
                    <input type="password" name="password" placeholder="Password">
                    <button type="submit">Login</button>
                </form>
                <input type="search" name="q" placeholder="Search">
            </body>
        </html>
        """
        
        actions = await browser._discover_page_actions(test_html, "https://example.com")
        print(f"✅ Action discovery completed: {len(actions)} actions found")
        
        for i, action in enumerate(actions[:5], 1):
            print(f"   {i}. {action['type']}: {action['description']}")
        
        await browser.close()
        print("✅ Browser closed successfully")
        print("🎉 Truly dynamic browser is working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


async def main():
    """Main function."""
    print("Choose an option:")
    print("1. Quick test (verify truly dynamic browser)")
    print("2. Truly dynamic demo (full capabilities)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        success = await quick_test()
        if success:
            print("\n✅ Truly dynamic browser verified! You can now run the full demo.")
    elif choice == "2":
        await truly_dynamic_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
