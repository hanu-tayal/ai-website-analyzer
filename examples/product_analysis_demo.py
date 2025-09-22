"""
Product Analysis Demo - Analyzes websites to generate user stories and Mermaid diagrams.
"""
import asyncio
import os
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from product_analyzer_browser import ProductAnalyzerBrowser


async def product_analysis_demo():
    """Demo showing product analysis capabilities."""
    
    print("🚀 Product Analyzer Browser Demo")
    print("=" * 60)
    print("This demo analyzes websites to generate:")
    print("✅ User stories for product development")
    print("✅ Mermaid diagrams for process visualization")
    print("✅ Feature maps and user flows")
    print("=" * 60)
    
    # Create browser instance
    browser = ProductAnalyzerBrowser(
        headless=False,  # Show browser for demo
        slow_mo=2000     # Slow down for visibility
    )
    
    try:
        # Start the browser
        print("🌐 Starting product analyzer browser...")
        await browser.start()
        
        # Example: Analyze a complex website
        print("\n🔍 Example: Product Analysis")
        print("-" * 50)
        
        website_url = input("Enter a website URL to analyze (or press Enter for default): ").strip()
        if not website_url:
            website_url = "https://httpbin.org"
        
        print(f"\n🌐 Analyzing: {website_url}")
        print("🔍 Browser will analyze the website for product processes...")
        
        results = await browser.analyze_website_for_product_processes(url=website_url, max_depth=3)
        
        print(f"\n✅ Product analysis completed: {results['success']}")
        
        if results['success']:
            # Display user stories
            user_stories = results.get('user_stories', [])
            print(f"\n📝 Generated {len(user_stories)} User Stories:")
            print("=" * 50)
            
            for i, story in enumerate(user_stories, 1):
                print(f"\n{i}. {story['title']}")
                print(f"   Story: {story['story']}")
                print(f"   Priority: {story['priority']}")
                print(f"   Page Type: {story['page_type']}")
                print("   Acceptance Criteria:")
                for criteria in story['acceptance_criteria']:
                    print(f"     - {criteria}")
            
            # Display Mermaid diagrams
            mermaid_diagrams = results.get('mermaid_diagrams', {})
            print(f"\n📊 Generated {len(mermaid_diagrams)} Mermaid Diagrams:")
            print("=" * 50)
            
            for diagram_type, diagram_content in mermaid_diagrams.items():
                print(f"\n{diagram_type.upper().replace('_', ' ')} DIAGRAM:")
                print("-" * 30)
                print(diagram_content)
                print()
            
            # Save results
            print("\n💾 Saving analysis results...")
            log_path = browser.save_session_log()
            print(f"   Analysis saved to: {log_path}")
            
            # Save Mermaid diagrams to separate files
            for diagram_type, diagram_content in mermaid_diagrams.items():
                diagram_file = f"mermaid_{diagram_type}.mmd"
                with open(diagram_file, 'w') as f:
                    f.write(diagram_content)
                print(f"   {diagram_type} diagram saved to: {diagram_file}")
        
        else:
            print(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
        
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
    print("🎉 Product Analysis Demo completed!")
    print("\nKey features demonstrated:")
    print("✅ Website analysis for product processes")
    print("✅ User story generation")
    print("✅ Mermaid diagram creation")
    print("✅ Feature mapping")
    print("✅ User flow visualization")
    
    print("\nThis tool helps you understand:")
    print("- What users can do on a website")
    print("- How the product is structured")
    print("- What features are available")
    print("- How users navigate through the product")


async def quick_test():
    """Quick test to verify the product analyzer works."""
    print("🧪 Quick Test - Product Analyzer Browser")
    print("=" * 40)
    
    browser = ProductAnalyzerBrowser(headless=True)
    
    try:
        await browser.start()
        print("✅ Product analyzer browser started successfully")
        
        # Test with a simple website
        results = await browser.analyze_website_for_product_processes("https://httpbin.org", max_depth=2)
        
        if results['success']:
            user_stories = results.get('user_stories', [])
            mermaid_diagrams = results.get('mermaid_diagrams', {})
            
            print(f"✅ Analysis completed: {len(user_stories)} user stories, {len(mermaid_diagrams)} diagrams")
            
            # Show a sample user story
            if user_stories:
                story = user_stories[0]
                print(f"\nSample User Story:")
                print(f"  Title: {story['title']}")
                print(f"  Story: {story['story']}")
            
            # Show a sample diagram
            if mermaid_diagrams:
                diagram_type = list(mermaid_diagrams.keys())[0]
                print(f"\nSample {diagram_type} diagram:")
                print(mermaid_diagrams[diagram_type][:200] + "...")
        
        await browser.close()
        print("✅ Browser closed successfully")
        print("🎉 Product analyzer browser is working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


async def main():
    """Main function."""
    print("Choose an option:")
    print("1. Quick test (verify product analyzer)")
    print("2. Full product analysis demo")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        success = await quick_test()
        if success:
            print("\n✅ Product analyzer verified! You can now run the full demo.")
    elif choice == "2":
        await product_analysis_demo()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
