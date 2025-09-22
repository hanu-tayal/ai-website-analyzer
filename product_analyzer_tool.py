#!/usr/bin/env python3
"""
Product Analyzer Tool - Command Line Interface
Analyzes websites to generate user stories and Mermaid diagrams for product development.
"""
import asyncio
import argparse
import sys
from pathlib import Path
import json
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from product_analyzer_browser import ProductAnalyzerBrowser


class ProductAnalyzerTool:
    """Command-line tool for analyzing websites and generating product documentation."""
    
    def __init__(self):
        self.browser = None
        
    async def analyze_website(self, url: str, max_depth: int = 5, output_dir: str = "analysis_output", headless: bool = True):
        """Analyze a website and generate product documentation.
        
        Args:
            url: Website URL to analyze
            max_depth: Maximum depth of analysis (number of pages to explore)
            output_dir: Directory to save output files
            headless: Whether to run browser in headless mode
        """
        print("🚀 Product Analyzer Tool")
        print("=" * 60)
        print(f"🔍 Analyzing: {url}")
        print(f"📊 Max depth: {max_depth} pages")
        print(f"📁 Output directory: {output_dir}")
        print("=" * 60)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        try:
            # Initialize browser
            self.browser = ProductAnalyzerBrowser(headless=headless, slow_mo=1000)
            await self.browser.start()
            print("✅ Browser started successfully")
            
            # Analyze website
            print("\n🤖 Starting comprehensive analysis...")
            results = await self.browser.analyze_website_for_product_processes(
                url=url, 
                max_depth=max_depth
            )
            
            if results['success']:
                print("✅ Analysis completed successfully!")
                
                # Generate timestamp for file naming
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = url.replace("https://", "").replace("http://", "").split("/")[0]
                
                # Save comprehensive results (convert sets to lists for JSON serialization)
                def convert_sets_to_lists(obj):
                    if isinstance(obj, set):
                        return list(obj)
                    elif isinstance(obj, dict):
                        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convert_sets_to_lists(item) for item in obj]
                    else:
                        return obj
                
                serializable_results = convert_sets_to_lists(results)
                results_file = output_path / f"analysis_{domain}_{timestamp}.json"
                with open(results_file, 'w') as f:
                    json.dump(serializable_results, f, indent=2)
                print(f"💾 Analysis results saved to: {results_file}")
                
                # Display and save user stories
                user_stories = results.get('user_stories', [])
                if user_stories:
                    print(f"\n📝 Generated {len(user_stories)} User Stories:")
                    print("=" * 50)
                    
                    stories_file = output_path / f"user_stories_{domain}_{timestamp}.md"
                    with open(stories_file, 'w') as f:
                        f.write(f"# User Stories for {url}\n\n")
                        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        
                        for i, story in enumerate(user_stories, 1):
                            print(f"\n{i}. {story['title']}")
                            print(f"   Story: {story['story']}")
                            print(f"   Priority: {story['priority']}")
                            print(f"   Page Type: {story['page_type']}")
                            print("   Acceptance Criteria:")
                            for criteria in story['acceptance_criteria']:
                                print(f"     - {criteria}")
                            
                            # Write to file
                            f.write(f"## {i}. {story['title']}\n\n")
                            f.write(f"**Story:** {story['story']}\n\n")
                            f.write(f"**Priority:** {story['priority']}\n\n")
                            f.write(f"**Page Type:** {story['page_type']}\n\n")
                            f.write("**Acceptance Criteria:**\n")
                            for criteria in story['acceptance_criteria']:
                                f.write(f"- {criteria}\n")
                            f.write("\n---\n\n")
                    
                    print(f"📄 User stories saved to: {stories_file}")
                else:
                    print("\n📝 No user stories generated (website may be too simple)")
                
                # Display and save Mermaid diagrams
                mermaid_diagrams = results.get('mermaid_diagrams', {})
                if mermaid_diagrams:
                    print(f"\n📊 Generated {len(mermaid_diagrams)} Mermaid Diagrams:")
                    print("=" * 50)
                    
                    for diagram_type, diagram_content in mermaid_diagrams.items():
                        print(f"\n{diagram_type.upper().replace('_', ' ')} DIAGRAM:")
                        print("-" * 30)
                        print(diagram_content)
                        print()
                        
                        # Save individual diagram files
                        diagram_file = output_path / f"diagram_{diagram_type}_{domain}_{timestamp}.mmd"
                        with open(diagram_file, 'w') as f:
                            f.write(f"<!-- {diagram_type.upper().replace('_', ' ')} DIAGRAM for {url} -->\n")
                            f.write(f"<!-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
                            f.write(diagram_content)
                        print(f"📊 {diagram_type} diagram saved to: {diagram_file}")
                    
                    # Create combined diagram file
                    combined_file = output_path / f"all_diagrams_{domain}_{timestamp}.mmd"
                    with open(combined_file, 'w') as f:
                        f.write(f"<!-- ALL DIAGRAMS for {url} -->\n")
                        f.write(f"<!-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
                        for diagram_type, diagram_content in mermaid_diagrams.items():
                            f.write(f"%% {diagram_type.upper().replace('_', ' ')} DIAGRAM\n")
                            f.write(diagram_content)
                            f.write("\n\n")
                    print(f"📊 Combined diagrams saved to: {combined_file}")
                else:
                    print("\n📊 No Mermaid diagrams generated")
                
                # Generate summary report
                summary_file = output_path / f"summary_{domain}_{timestamp}.md"
                with open(summary_file, 'w') as f:
                    f.write(f"# Product Analysis Summary for {url}\n\n")
                    f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"**Website:** {url}\n")
                    f.write(f"**Analysis Depth:** {max_depth} pages\n\n")
                    
                    f.write("## Analysis Results\n\n")
                    f.write(f"- **User Stories Generated:** {len(user_stories)}\n")
                    f.write(f"- **Mermaid Diagrams Generated:** {len(mermaid_diagrams)}\n")
                    f.write(f"- **Pages Analyzed:** {len(results.get('analysis_results', []))}\n\n")
                    
                    if user_stories:
                        f.write("## User Stories Overview\n\n")
                        for i, story in enumerate(user_stories, 1):
                            f.write(f"{i}. **{story['title']}** ({story['priority']} priority)\n")
                        f.write("\n")
                    
                    if mermaid_diagrams:
                        f.write("## Generated Diagrams\n\n")
                        for diagram_type in mermaid_diagrams.keys():
                            f.write(f"- {diagram_type.replace('_', ' ').title()}\n")
                        f.write("\n")
                    
                    f.write("## Files Generated\n\n")
                    f.write(f"- `analysis_{domain}_{timestamp}.json` - Complete analysis data\n")
                    if user_stories:
                        f.write(f"- `user_stories_{domain}_{timestamp}.md` - User stories in Markdown\n")
                    if mermaid_diagrams:
                        f.write(f"- `diagram_*_{domain}_{timestamp}.mmd` - Individual Mermaid diagrams\n")
                        f.write(f"- `all_diagrams_{domain}_{timestamp}.mmd` - All diagrams combined\n")
                
                print(f"📋 Summary report saved to: {summary_file}")
                
                print("\n🎉 Analysis completed successfully!")
                print(f"📁 All files saved to: {output_path.absolute()}")
                
            else:
                print(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if self.browser:
                await self.browser.close()
                print("✅ Browser closed")
        
        return True


async def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Product Analyzer Tool - Analyze websites to generate user stories and Mermaid diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python product_analyzer_tool.py https://example.com
  python product_analyzer_tool.py https://httpbin.org --depth 3 --output ./my_analysis
  python product_analyzer_tool.py https://jsonplaceholder.typicode.com --no-headless
        """
    )
    
    parser.add_argument('url', help='Website URL to analyze')
    parser.add_argument('--depth', '-d', type=int, default=5, 
                       help='Maximum analysis depth (number of pages to explore) (default: 5)')
    parser.add_argument('--output', '-o', default='analysis_output',
                       help='Output directory for generated files (default: analysis_output)')
    parser.add_argument('--no-headless', action='store_true',
                       help='Run browser in visible mode (default: headless)')
    parser.add_argument('--version', action='version', version='Product Analyzer Tool 1.0.0')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Create tool instance
    tool = ProductAnalyzerTool()
    
    # Run analysis
    success = await tool.analyze_website(
        url=args.url,
        max_depth=args.depth,
        output_dir=args.output,
        headless=not args.no_headless
    )
    
    if success:
        print("\n✅ Product analysis completed successfully!")
        print("📁 Check the output directory for generated files")
        sys.exit(0)
    else:
        print("\n❌ Product analysis failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
