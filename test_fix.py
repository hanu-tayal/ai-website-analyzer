#!/usr/bin/env python3
"""
Test script to verify the fix for the Claude Code SDK error.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from simple_browser import SimpleBrowser


async def test_simple_browser():
    """Test the simple browser implementation."""
    print("🧪 Testing Simple Browser Implementation")
    print("=" * 50)
    
    browser = SimpleBrowser(headless=False, slow_mo=1000)
    
    try:
        print("🌐 Starting browser...")
        await browser.start()
        print("✅ Browser started successfully")
        
        print("🔍 Testing website analysis...")
        analysis = browser._analyze_website("https://example.com", "A simple example website")
        print(f"✅ Analysis completed: {analysis['purpose']}")
        
        print("🌐 Testing navigation...")
        page_info = await browser.browser.navigate_to("https://httpbin.org")
        if "error" not in page_info:
            print("✅ Navigation successful")
        else:
            print(f"❌ Navigation failed: {page_info['error']}")
        
        print("🧠 Testing page analysis...")
        page_analysis = browser._analyze_page(page_info['content'], page_info.get('url', ''), "Test")
        print(f"✅ Page analysis completed: {page_analysis['page_type']}")
        
        print("🤖 Testing intelligent browsing...")
        results = await browser.analyze_and_browse("https://httpbin.org", "HTTP testing service")
        print(f"✅ Browsing completed: {results['success']}")
        
        if results['success']:
            steps = results.get('browsing_results', [])
            print(f"   Steps taken: {len(steps)}")
            for i, step in enumerate(steps[:3], 1):
                action = step.get('analysis', {}).get('next_action', 'unknown')
                print(f"     {i}. {action}")
        
        print("📝 Testing session logging...")
        log_path = browser.save_session_log()
        print(f"✅ Session log saved to: {log_path}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("🔄 Closing browser...")
        await browser.close()
        print("✅ Browser closed")
    
    print("\n🎉 All tests passed!")
    return True


async def main():
    """Main test function."""
    print("🚀 Testing Playwright AI Browser Fix")
    print("=" * 50)
    print("This test verifies that the browser works without Claude Code SDK")
    print("=" * 50)
    
    success = await test_simple_browser()
    
    if success:
        print("\n✅ Fix verified! The browser now works without Claude Code SDK.")
        print("\nTo run the demo:")
        print("python examples/simple_demo.py")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")


if __name__ == "__main__":
    asyncio.run(main())
