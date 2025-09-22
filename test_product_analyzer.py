#!/usr/bin/env python3
"""
Test the Product Analyzer Browser with a complex website
"""
import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from product_analyzer_browser import ProductAnalyzerBrowser


async def test_complex_website():
    """Test the product analyzer with a complex website."""
    print("🚀 Testing Product Analyzer with Complex Website")
    print("=" * 60)
    
    browser = ProductAnalyzerBrowser(headless=True)
    
    try:
        await browser.start()
        print("✅ Product analyzer browser started")
        
        # Test with a more complex website
        website_url = "https://httpbin.org"
        print(f"🔍 Analyzing: {website_url}")
        
        results = await browser.analyze_website_for_product_processes(
            url=website_url, 
            max_depth=3
        )
        
        if results['success']:
            print("✅ Analysis completed successfully!")
            
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
            
            print("\n🎉 Product analysis completed successfully!")
            print("\nKey achievements:")
            print("✅ Analyzed website structure and features")
            print("✅ Generated user stories for product development")
            print("✅ Created Mermaid diagrams for process visualization")
            print("✅ Mapped user flows and page types")
            print("✅ Saved results for further analysis")
            
        else:
            print(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
        
        await browser.close()
        print("✅ Browser closed")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_complex_website())
