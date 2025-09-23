#!/usr/bin/env python3
"""
Fixed Product Analyzer Tool - Command Line Interface with proper page navigation
"""
import asyncio
import argparse
import sys
from pathlib import Path
import json
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fixed_product_analyzer_browser import FixedProductAnalyzerBrowser
from user_journey_mapper import AdvancedUserJourneyMapper
from enhanced_flow_visualizer import EnhancedFlowVisualizer
from inefficiency_dashboard import UserFlowInefficiencyDashboard
from ai_content_analyzer import AIContentAnalyzer


class FixedProductAnalyzerTool:
    """Fixed command-line tool for analyzing websites and generating product documentation."""
    
    def __init__(self):
        self.browser = None
        self.journey_mapper = None
        self.flow_visualizer = None
        self.inefficiency_dashboard = None
        self.ai_analyzer = None
        
    async def analyze_website(self, url: str, max_depth: int = 5, output_dir: str = "analysis_output", headless: bool = True):
        """Analyze a website and generate product documentation."""
        print("🚀 Fixed Product Analyzer Tool")
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
            self.browser = FixedProductAnalyzerBrowser(headless=headless, slow_mo=1000)
            await self.browser.start()
            print("✅ Browser started successfully")

            # Initialize advanced analysis components
            self.journey_mapper = AdvancedUserJourneyMapper(self.browser.browser, output_dir)
            self.flow_visualizer = EnhancedFlowVisualizer()
            self.inefficiency_dashboard = UserFlowInefficiencyDashboard(output_dir)
            self.ai_analyzer = AIContentAnalyzer()
            print("✅ Advanced analysis components initialized")
            print("🧠 AI-powered content analyzer initialized")
            
            # Analyze website
            print("\n🤖 Starting comprehensive analysis...")
            results = await self.browser.analyze_website_for_product_processes(
                url=url, 
                max_depth=max_depth
            )
            
            if results['success']:
                print("✅ Basic analysis completed successfully!")

                # Generate timestamp for file naming
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = url.replace("https://", "").replace("http://", "").split("/")[0]

                # Perform AI-powered intelligent analysis
                print("\n🧠 Starting AI-powered intelligent analysis...")
                ai_analysis = {}
                try:
                    if 'analysis_results' in results and results['analysis_results']:
                        ai_analysis = await self.ai_analyzer.analyze_website_intelligence(url, results['analysis_results'])
                        print("✅ AI analysis completed successfully!")

                        # Replace generic user stories with intelligent ones
                        if ai_analysis.get('intelligent_user_stories'):
                            results['user_stories'] = ai_analysis['intelligent_user_stories']
                            print(f"🎯 Generated {len(ai_analysis['intelligent_user_stories'])} intelligent user stories!")
                    else:
                        print("⚠️ No basic analysis results available for AI enhancement")
                        ai_analysis = {"ai_powered": False, "analysis_quality": "basic"}
                except Exception as e:
                    print(f"⚠️ AI analysis encountered issues: {e}")
                    ai_analysis = {"ai_powered": False, "error": str(e)}

                # Perform advanced user journey mapping (if enabled)
                journey_results = {"journeys": []}  # Default empty results
                enhanced_diagrams = {}
                inefficiency_analysis = {"summary": {"message": "Journey mapping disabled"}}

                try:
                    print("\n🗺️ Starting Advanced User Journey Mapping...")
                    journey_results = await self.journey_mapper.map_user_journeys(url, min(max_depth, 3))  # Limit depth to avoid issues
                    print("✅ User journey mapping completed!")

                    # Generate enhanced visualizations
                    print("\n📊 Creating Enhanced Flow Visualizations...")
                    enhanced_diagrams = self.flow_visualizer.generate_comprehensive_journey_dashboard(journey_results)
                    print("✅ Enhanced visualizations generated!")

                    # Analyze inefficiencies
                    print("\n🔍 Analyzing User Flow Inefficiencies...")
                    inefficiency_analysis = self.inefficiency_dashboard.analyze_flow_inefficiencies(journey_results)
                    print("✅ Inefficiency analysis completed!")
                except Exception as e:
                    print(f"⚠️ Enhanced analysis encountered issues: {e}")
                    print("📋 Continuing with basic analysis...")
                
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

                # Merge AI analysis with basic results
                enhanced_results = convert_sets_to_lists(results)
                if ai_analysis:
                    enhanced_results['ai_analysis'] = ai_analysis

                results_file = output_path / f"analysis_{domain}_{timestamp}.json"
                with open(results_file, 'w') as f:
                    json.dump(enhanced_results, f, indent=2)
                print(f"💾 Enhanced analysis results saved to: {results_file}")

                # Save AI analysis separately for easier access
                if ai_analysis and ai_analysis.get('ai_powered'):
                    ai_file = output_path / f"ai_analysis_{domain}_{timestamp}.json"
                    with open(ai_file, 'w') as f:
                        json.dump(ai_analysis, f, indent=2)
                    print(f"🧠 AI analysis saved to: {ai_file}")
                
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
                
                # Save enhanced diagrams (if generated)
                if enhanced_diagrams:
                    print(f"\n📊 Saving Enhanced Visualizations...")
                    for diagram_type, diagram_content in enhanced_diagrams.items():
                        diagram_file = output_path / f"enhanced_{diagram_type}_{domain}_{timestamp}.md"
                        with open(diagram_file, 'w') as f:
                            f.write(f"# {diagram_type.replace('_', ' ').title()} for {url}\n\n")
                            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                            f.write("```mermaid\n")
                            f.write(diagram_content)
                            f.write("\n```\n")
                        print(f"📊 Enhanced {diagram_type} saved to: {diagram_file}")

                # Save user journey report (if generated)
                if journey_results and journey_results.get("journeys"):
                    try:
                        journey_report_file = await self.journey_mapper.generate_journey_report(journey_results)
                        print(f"🗺️ Journey report saved to: {journey_report_file}")
                    except Exception as e:
                        print(f"⚠️ Could not save journey report: {e}")

                # Save inefficiency dashboard (if analysis was successful)
                if inefficiency_analysis and "summary" in inefficiency_analysis:
                    try:
                        dashboard_json, dashboard_html = self.inefficiency_dashboard.save_dashboard(inefficiency_analysis)
                        print(f"🔍 Inefficiency dashboard saved to: {dashboard_html}")
                        print(f"📋 Dashboard data saved to: {dashboard_json}")
                    except Exception as e:
                        print(f"⚠️ Could not save inefficiency dashboard: {e}")

                # Display and save original Mermaid diagrams
                mermaid_diagrams = results.get('mermaid_diagrams', {})
                if mermaid_diagrams:
                    print(f"\n📊 Generated {len(mermaid_diagrams)} Basic Mermaid Diagrams:")
                    print("=" * 50)

                    for diagram_type, diagram_content in mermaid_diagrams.items():
                        # Save individual diagram files as .md with Mermaid syntax
                        diagram_file = output_path / f"basic_{diagram_type}_{domain}_{timestamp}.md"
                        with open(diagram_file, 'w') as f:
                            f.write(f"# {diagram_type.replace('_', ' ').title()} Diagram for {url}\n\n")
                            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                            f.write("```mermaid\n")
                            f.write(diagram_content)
                            f.write("\n```\n")
                        print(f"📊 Basic {diagram_type} diagram saved to: {diagram_file}")
                else:
                    print("\n📊 No basic Mermaid diagrams generated")

                # Display AI recommendations if available
                if ai_analysis and ai_analysis.get('ai_recommendations'):
                    recommendations = ai_analysis['ai_recommendations']
                    print(f"\n🎯 Generated {len(recommendations)} AI Recommendations:")
                    print("=" * 50)

                    recommendations_file = output_path / f"ai_recommendations_{domain}_{timestamp}.md"
                    with open(recommendations_file, 'w') as f:
                        f.write(f"# AI Recommendations for {url}\n\n")
                        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                        for i, rec in enumerate(recommendations, 1):
                            print(f"\n{i}. {rec.get('title', 'Untitled')}")
                            print(f"   Category: {rec.get('category', 'General')}")
                            print(f"   Impact: {rec.get('impact', 'medium')} | Priority: {rec.get('priority', '3')}")
                            print(f"   Description: {rec.get('description', '')[:100]}...")

                            # Write to file
                            f.write(f"## {i}. {rec.get('title', 'Untitled')}\n\n")
                            f.write(f"**Category:** {rec.get('category', 'General')}\n")
                            f.write(f"**Impact:** {rec.get('impact', 'medium')} | **Priority:** {rec.get('priority', '3')}\n")
                            f.write(f"**Effort:** {rec.get('effort', 'medium')}\n\n")
                            f.write(f"**Description:**\n{rec.get('description', '')}\n\n")
                            f.write("---\n\n")

                    print(f"📋 AI recommendations saved to: {recommendations_file}")
                else:
                    print("\n🎯 No AI recommendations generated")
                
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
                    f.write(f"- **Pages Analyzed:** {len(results.get('analysis_results', []))}\n")
                    f.write(f"- **AI Analysis:** {'Enabled' if ai_analysis.get('ai_powered') else 'Fallback Mode'}\n")
                    if ai_analysis.get('ai_recommendations'):
                        f.write(f"- **AI Recommendations:** {len(ai_analysis['ai_recommendations'])}\n")
                    if ai_analysis.get('business_model'):
                        f.write(f"- **Business Model Detected:** {ai_analysis['business_model'].get('primary_model', 'Unknown')}\n")
                    f.write("\n")
                    
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
                        f.write(f"- `diagram_*_{domain}_{timestamp}.md` - Individual Mermaid diagrams\n")
                        f.write(f"- `all_diagrams_{domain}_{timestamp}.md` - All diagrams combined\n")
                
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
                try:
                    await self.browser.close()
                    print("✅ Browser closed")
                except Exception as e:
                    print(f"⚠️ Browser cleanup warning: {e}")
        
        return True


async def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Fixed Product Analyzer Tool - Analyze websites with proper page navigation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fixed_product_analyzer_tool.py https://saleor.io
  python fixed_product_analyzer_tool.py https://saleor.io --depth 3 --output ./my_analysis
  python fixed_product_analyzer_tool.py https://saleor.io --no-headless
        """
    )
    
    parser.add_argument('url', help='Website URL to analyze')
    parser.add_argument('--depth', '-d', type=int, default=5, 
                       help='Maximum analysis depth (number of pages to explore) (default: 5)')
    parser.add_argument('--output', '-o', default='analysis_output',
                       help='Output directory for generated files (default: analysis_output)')
    parser.add_argument('--no-headless', action='store_true',
                       help='Run browser in visible mode (default: headless)')
    parser.add_argument('--enable-journey-mapping', action='store_true', default=True,
                       help='Enable advanced user journey mapping (default: enabled)')
    parser.add_argument('--disable-screenshots', action='store_true',
                       help='Disable screenshot capture during analysis')
    parser.add_argument('--personas', nargs='*', default=['all'],
                       help='Specify personas to analyze (customer, admin, guest, mobile, returning) or "all"')
    parser.add_argument('--version', action='version', version='Fixed Product Analyzer Tool 2.0.0')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Create tool instance
    tool = FixedProductAnalyzerTool()
    
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
