"""
Smart browser demo that shows dynamic, context-aware browsing without requiring Claude Code SDK.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from smart_browser import SmartBrowser


async def smart_demo():
    """Demo showing smart dynamic browsing capabilities."""
    
    print("🚀 Smart Dynamic Browser Demo")
    print("=" * 60)
    print("This demo shows intelligent, context-aware web browsing")
    print("Uses advanced heuristics and pattern matching for dynamic decisions")
    print("No Claude Code SDK required - works out of the box!")
    print("=" * 60)
    
    # Create browser instance
    browser = SmartBrowser(
        headless=False,  # Show browser for demo
        slow_mo=2000     # Slow down for visibility
    )
    
    try:
        # Start the browser
        print("🌐 Starting smart browser...")
        await browser.start()
        
        # Example 1: Smart website exploration
        print("\n🔍 Example 1: Smart Website Exploration")
        print("-" * 50)
        
        website_url = input("Enter a website URL to explore (or press Enter for default): ").strip()
        if not website_url:
            website_url = "https://httpbin.org"
        
        website_description = input("Enter a description of the website (optional): ").strip()
        if not website_description:
            website_description = None
        
        print(f"\n🌐 Exploring: {website_url}")
        print("🧠 Smart browser will analyze each page and make intelligent decisions...")
        
        results = await browser.analyze_and_browse(
            url=website_url,
            description=website_description
        )
        
        print(f"\n✅ Smart browsing completed: {results['success']}")
        
        if results['success']:
            analysis = results.get('analysis', {})
            print(f"\n📊 Website Analysis:")
            print(f"   Purpose: {analysis.get('purpose', 'Unknown')}")
            print(f"   Key Features: {', '.join(analysis.get('key_features', [])[:3])}")
            print(f"   Interaction Strategy: {analysis.get('interaction_strategy', 'N/A')}")
            
            browsing_steps = results.get('browsing_results', [])
            print(f"\n🧠 Smart Actions Taken ({len(browsing_steps)} steps):")
            
            for i, step in enumerate(browsing_steps, 1):
                analysis_data = step.get('analysis', {})
                action = analysis_data.get('next_action', 'unknown')
                reasoning = analysis_data.get('reasoning', 'No reasoning provided')
                confidence = analysis_data.get('confidence', 0.0)
                page_type = analysis_data.get('page_type', 'unknown')
                url = step.get('url', 'unknown')
                
                print(f"   {i}. {action} on {page_type} page")
                print(f"      URL: {url}")
                print(f"      Reasoning: {reasoning}")
                print(f"      Confidence: {confidence:.2f}")
                print()
            
            # Show smart decision making process
            print("🧠 Smart Decision Making Process:")
            print("   - Each page is analyzed using advanced heuristics")
            print("   - Page type is classified based on content patterns")
            print("   - Actions are chosen based on page type and context")
            print("   - Confidence scores help prioritize actions")
            print("   - No predetermined steps - everything is dynamic!")
        
        else:
            print(f"❌ Browsing failed: {results.get('error', 'Unknown error')}")
        
        # Save session logs
        print("\n📝 Saving smart session logs...")
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
    print("🎉 Smart Dynamic Demo completed!")
    print("\nKey features demonstrated:")
    print("✅ Advanced page type classification")
    print("✅ Context-aware action selection")
    print("✅ Intelligent reasoning for each action")
    print("✅ Dynamic decision making based on content")
    print("✅ No predetermined steps - truly dynamic!")
    print("✅ Works without Claude Code SDK")
    
    print("\nThis is what makes it truly dynamic:")
    print("- Analyzes each page individually using heuristics")
    print("- Classifies page types (login, search, product, article, etc.)")
    print("- Chooses appropriate actions based on page type")
    print("- Provides reasoning for each decision")
    print("- Adapts to different website types automatically")
    print("- No hardcoded steps - everything is context-aware!")


async def quick_test():
    """Quick test to verify the smart browser works."""
    print("🧪 Quick Test - Smart Browser")
    print("=" * 40)
    
    browser = SmartBrowser(headless=True)
    
    try:
        await browser.start()
        print("✅ Smart browser started successfully")
        
        # Test website analysis
        analysis = browser._analyze_website_smart("https://example.com", "Test website")
        print(f"✅ Website analysis completed: {analysis['purpose']}")
        
        # Test page analysis
        page_analysis = browser._analyze_page_smart("<html><body><h1>Test</h1><a href='/about'>About</a></body></html>", "https://example.com", 0)
        print(f"✅ Page analysis completed: {page_analysis['next_action']}")
        print(f"   Page type: {page_analysis['page_type']}")
        print(f"   Reasoning: {page_analysis['reasoning']}")
        
        await browser.close()
        print("✅ Browser closed successfully")
        print("🎉 Smart browser is working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


async def main():
    """Main function."""
    print("Choose an option:")
    print("1. Quick test (verify smart browser)")
    print("2. Smart demo (full capabilities)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        success = await quick_test()
        if success:
            print("\n✅ Smart browser verified! You can now run the full demo.")
    elif choice == "2":
        await smart_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
