"""
Main orchestrator for the Playwright AI Browser tool.
"""
import asyncio
import argparse
import json
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from .intelligent_browser import IntelligentBrowser, UserCredentials
    INTELLIGENT_BROWSER_AVAILABLE = True
except ImportError:
    INTELLIGENT_BROWSER_AVAILABLE = False

from .simple_browser import SimpleBrowser
from .dynamic_browser import DynamicBrowser
from .smart_browser import SmartBrowser
from .truly_dynamic_browser import TrulyDynamicBrowser


class PlaywrightAIBrowser:
    """Main class that orchestrates the entire AI-powered browsing experience."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000, api_key: Optional[str] = None):
        """Initialize the AI browser.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
            api_key: Claude API key (optional)
        """
        # Use truly dynamic browser that discovers actions from page content
        print("🤖 Using truly dynamic browser")
        self.browser = TrulyDynamicBrowser(headless=headless, slow_mo=slow_mo)
        self.use_ai = True
        
    async def browse_website(self, 
                           url: str, 
                           description: Optional[str] = None,
                           create_account: bool = False,
                           credentials: Optional[UserCredentials] = None,
                           max_steps: int = 20) -> Dict[str, Any]:
        """Browse a website with AI guidance.
        
        Args:
            url: The website URL to browse
            description: Optional description of the website
            create_account: Whether to attempt account creation
            credentials: User credentials for account creation/login
            max_steps: Maximum number of browsing steps
            
        Returns:
            Dictionary containing browsing results
        """
        try:
            # Start the browser
            await self.browser.start()
            
            # Analyze and browse the website
            results = await self.browser.analyze_and_browse(url, description)
            
            if not results["success"]:
                return results
            
            # Create account if requested
            if create_account and credentials:
                print("👤 Attempting to create user account...")
                account_result = await self.browser.create_user_account(credentials)
                results["account_creation"] = account_result
                
                if account_result["success"]:
                    print("✅ Account creation successful")
                else:
                    print(f"❌ Account creation failed: {account_result.get('error', 'Unknown error')}")
            
            # Login if credentials provided and account creation not requested
            elif credentials and not create_account:
                print("🔐 Attempting to login...")
                login_result = await self.browser.login_user(credentials)
                results["login"] = login_result
                
                if login_result["success"]:
                    print("✅ Login successful")
                else:
                    print(f"❌ Login failed: {login_result.get('error', 'Unknown error')}")
            
            # Save session log
            log_path = self.browser.save_session_log()
            results["session_log_path"] = log_path
            print(f"📝 Session log saved to: {log_path}")
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "session_log": self.browser.session_log
            }
        finally:
            # Always close the browser
            await self.browser.close()
    
    async def demo_browsing(self, url: str, description: Optional[str] = None) -> None:
        """Run a demo browsing session.
        
        Args:
            url: The website URL to browse
            description: Optional description of the website
        """
        print("🚀 Starting Playwright AI Browser Demo")
        print("=" * 50)
        
        # Create demo credentials
        demo_credentials = UserCredentials(
            email="demo@example.com",
            password="DemoPassword123!",
            first_name="Demo",
            last_name="User",
            username="demouser"
        )
        
        # Browse the website
        results = await self.browse_website(
            url=url,
            description=description,
            create_account=True,
            credentials=demo_credentials,
            max_steps=15
        )
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 BROWSING RESULTS")
        print("=" * 50)
        
        if results["success"]:
            print("✅ Browsing completed successfully!")
            
            # Display analysis
            analysis = results.get("analysis", {})
            if analysis:
                print(f"\n🔍 Website Analysis:")
                print(f"   Purpose: {analysis.get('purpose', 'Unknown')}")
                print(f"   Key Features: {', '.join(analysis.get('key_features', []))}")
                print(f"   Registration Required: {analysis.get('registration_required', False)}")
            
            # Display browsing steps
            browsing_results = results.get("browsing_results", [])
            print(f"\n🤖 Actions Taken ({len(browsing_results)} steps):")
            for i, step in enumerate(browsing_results, 1):
                action = step.get("analysis", {}).get("next_action", "unknown")
                url = step.get("url", "unknown")
                print(f"   {i}. {action} on {url}")
            
            # Display account creation result
            if "account_creation" in results:
                account_result = results["account_creation"]
                if account_result["success"]:
                    print("\n👤 Account Creation: ✅ Success")
                else:
                    print(f"\n👤 Account Creation: ❌ Failed - {account_result.get('error', 'Unknown error')}")
            
            # Display login result
            if "login" in results:
                login_result = results["login"]
                if login_result["success"]:
                    print("\n🔐 Login: ✅ Success")
                else:
                    print(f"\n🔐 Login: ❌ Failed - {login_result.get('error', 'Unknown error')}")
                    
        else:
            print("❌ Browsing failed!")
            print(f"   Error: {results.get('error', 'Unknown error')}")
        
        print(f"\n📝 Session log saved to: {results.get('session_log_path', 'Not saved')}")
        print("=" * 50)


async def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Playwright AI Browser - Intelligent web browsing with AI")
    parser.add_argument("url", help="Website URL to browse")
    parser.add_argument("-d", "--description", help="Description of the website")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--slow-mo", type=int, default=1000, help="Delay between actions in milliseconds")
    parser.add_argument("--api-key", help="Claude API key (or set CLAUDE_API_KEY environment variable)")
    parser.add_argument("--create-account", action="store_true", help="Attempt to create a user account")
    parser.add_argument("--email", help="Email for account creation/login")
    parser.add_argument("--password", help="Password for account creation/login")
    parser.add_argument("--first-name", help="First name for account creation")
    parser.add_argument("--last-name", help="Last name for account creation")
    parser.add_argument("--username", help="Username for account creation/login")
    parser.add_argument("--max-steps", type=int, default=20, help="Maximum number of browsing steps")
    
    args = parser.parse_args()
    
    # Get API key from environment or argument
    api_key = args.api_key or None
    if not api_key:
        import os
        api_key = os.getenv("CLAUDE_API_KEY")
    
    # Create credentials if provided
    credentials = None
    if args.email and args.password:
        credentials = UserCredentials(
            email=args.email,
            password=args.password,
            first_name=args.first_name or "",
            last_name=args.last_name or "",
            username=args.username or ""
        )
    
    # Create and run the browser
    browser = PlaywrightAIBrowser(
        headless=args.headless,
        slow_mo=args.slow_mo,
        api_key=api_key
    )
    
    # Run the demo
    await browser.demo_browsing(
        url=args.url,
        description=args.description
    )


if __name__ == "__main__":
    asyncio.run(main())
