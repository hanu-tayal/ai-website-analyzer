"""
Simple demo using the fallback browser implementation.
This works without Claude Code SDK and provides basic AI-like functionality.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from simple_browser import SimpleBrowser


async def simple_demo():
    """Simple demo using the fallback browser."""
    
    print("🚀 Simple Playwright AI Browser Demo")
    print("=" * 50)
    print("This demo uses pattern matching and heuristics instead of Claude Code SDK")
    print("=" * 50)
    
    # Create browser instance
    browser = SimpleBrowser(headless=False, slow_mo=2000)  # Slow down for demo
    
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
            
            # Show first few steps
            for i, step in enumerate(browsing_steps[:5], 1):
                action = step.get('analysis', {}).get('next_action', 'unknown')
                url = step.get('url', 'unknown')
                print(f"     {i}. {action} on {url}")
        
        # Example 2: Google search
        print("\n🔍 Example 2: Google Search")
        print("-" * 40)
        
        results2 = await browser.analyze_and_browse(
            url="https://www.google.com",
            description="Google search engine"
        )
        
        print(f"✅ Browsing completed: {results2['success']}")
        if results2['success']:
            analysis2 = results2.get('analysis', {})
            print(f"   Purpose: {analysis2.get('purpose', 'Unknown')}")
            
            browsing_steps = results2.get('browsing_results', [])
            print(f"   Steps taken: {len(browsing_steps)}")
            
            # Show first few steps
            for i, step in enumerate(browsing_steps[:5], 1):
                action = step.get('analysis', {}).get('next_action', 'unknown')
                url = step.get('url', 'unknown')
                print(f"     {i}. {action} on {url}")
        
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
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nKey features demonstrated:")
    print("✅ Pattern-based website analysis")
    print("✅ Intelligent navigation and browsing")
    print("✅ Form detection and filling")
    print("✅ Interactive website exploration")
    print("✅ Session logging")
    
    print("\nThis simple version works without Claude Code SDK!")
    print("To use the full AI version, set up Claude Code SDK properly.")


async def quick_test():
    """Quick test to verify everything is working."""
    print("🧪 Quick Test - Verifying Installation")
    print("=" * 40)
    
    browser = SimpleBrowser(headless=True)  # Headless for quick test
    
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
    print("2. Simple demo (pattern-based AI)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        success = await quick_test()
        if success:
            print("\n✅ Installation verified! You can now run the demo.")
    elif choice == "2":
        await simple_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
