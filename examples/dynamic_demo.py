"""
Dynamic AI browser demo that shows real-time AI decision making.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dynamic_browser import DynamicBrowser


async def dynamic_demo():
    """Demo showing dynamic AI-powered browsing."""
    
    print("🚀 Dynamic AI Browser Demo")
    print("=" * 60)
    print("This demo shows real-time AI decision making for web browsing")
    print("The AI analyzes each page and makes intelligent decisions about what to do next")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        print("⚠️  Warning: CLAUDE_API_KEY not set.")
        print("   The AI analysis will use fallback pattern matching.")
        print("   For full AI capabilities, set: export CLAUDE_API_KEY='your-key-here'")
        print()
    
    # Create browser instance
    browser = DynamicBrowser(
        headless=False,  # Show browser for demo
        slow_mo=2000,    # Slow down for visibility
        api_key=api_key
    )
    
    try:
        # Start the browser
        print("🌐 Starting dynamic AI browser...")
        await browser.start()
        
        # Example 1: Dynamic website exploration
        print("\n🔍 Example 1: Dynamic Website Exploration")
        print("-" * 50)
        
        website_url = input("Enter a website URL to explore (or press Enter for default): ").strip()
        if not website_url:
            website_url = "https://httpbin.org"
        
        website_description = input("Enter a description of the website (optional): ").strip()
        if not website_description:
            website_description = None
        
        print(f"\n🌐 Exploring: {website_url}")
        print("🤖 AI will analyze each page and decide what to do next...")
        
        results = await browser.analyze_and_browse(
            url=website_url,
            description=website_description
        )
        
        print(f"\n✅ Dynamic browsing completed: {results['success']}")
        
        if results['success']:
            analysis = results.get('analysis', {})
            print(f"\n📊 Website Analysis:")
            print(f"   Purpose: {analysis.get('purpose', 'Unknown')}")
            print(f"   Key Features: {', '.join(analysis.get('key_features', [])[:3])}")
            print(f"   Interaction Strategy: {analysis.get('interaction_strategy', 'N/A')}")
            
            browsing_steps = results.get('browsing_results', [])
            print(f"\n🤖 AI Actions Taken ({len(browsing_steps)} steps):")
            
            for i, step in enumerate(browsing_steps, 1):
                analysis_data = step.get('analysis', {})
                action = analysis_data.get('next_action', 'unknown')
                reasoning = analysis_data.get('reasoning', 'No reasoning provided')
                confidence = analysis_data.get('confidence', 0.0)
                url = step.get('url', 'unknown')
                
                print(f"   {i}. {action} on {url}")
                print(f"      Reasoning: {reasoning}")
                print(f"      Confidence: {confidence:.2f}")
                print()
            
            # Show AI decision making process
            print("🧠 AI Decision Making Process:")
            print("   - Each page is analyzed in real-time")
            print("   - AI considers context, content, and user intent")
            print("   - Decisions are based on what would be most interesting/useful")
            print("   - No predetermined steps - everything is dynamic!")
        
        else:
            print(f"❌ Browsing failed: {results.get('error', 'Unknown error')}")
        
        # Save session logs
        print("\n📝 Saving AI session logs...")
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
    print("🎉 Dynamic AI Demo completed!")
    print("\nKey features demonstrated:")
    print("✅ Real-time AI analysis of each page")
    print("✅ Dynamic decision making based on content")
    print("✅ Context-aware action selection")
    print("✅ Intelligent reasoning for each action")
    print("✅ No predetermined steps - truly dynamic!")
    
    print("\nThis is what makes it truly AI-powered:")
    print("- AI analyzes each page individually")
    print("- Makes decisions based on actual content")
    print("- Considers context and user intent")
    print("- Adapts to different website types")
    print("- Provides reasoning for each action")


async def quick_test():
    """Quick test to verify the dynamic browser works."""
    print("🧪 Quick Test - Dynamic AI Browser")
    print("=" * 40)
    
    browser = DynamicBrowser(headless=True, api_key=os.getenv("CLAUDE_API_KEY"))
    
    try:
        await browser.start()
        print("✅ Dynamic browser started successfully")
        
        # Test AI analysis
        analysis = await browser._analyze_website_ai("https://example.com", "Test website")
        print(f"✅ AI analysis completed: {analysis['purpose']}")
        
        # Test page analysis
        page_analysis = await browser._analyze_page_ai("<html><body><h1>Test</h1></body></html>", "https://example.com", "Test")
        print(f"✅ Page analysis completed: {page_analysis['next_action']}")
        
        await browser.close()
        print("✅ Browser closed successfully")
        print("🎉 Dynamic AI browser is working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


async def main():
    """Main function."""
    print("Choose an option:")
    print("1. Quick test (verify dynamic AI browser)")
    print("2. Dynamic AI demo (full capabilities)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        success = await quick_test()
        if success:
            print("\n✅ Dynamic AI browser verified! You can now run the full demo.")
    elif choice == "2":
        await dynamic_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
