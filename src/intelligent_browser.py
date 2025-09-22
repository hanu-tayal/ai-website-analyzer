"""
Intelligent browser that combines Playwright automation with Claude Code SDK for AI-guided navigation.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
import json
import time
from pathlib import Path
from dataclasses import dataclass

from .browser_automation import BrowserAutomation
from .website_analyzer import WebsiteAnalyzer


@dataclass
class UserCredentials:
    """Container for user account credentials."""
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""
    username: str = ""


class IntelligentBrowser:
    """Main class that orchestrates intelligent web browsing using AI."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000, api_key: Optional[str] = None):
        """Initialize the intelligent browser.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
            api_key: Claude API key (optional)
        """
        self.browser = BrowserAutomation(headless=headless, slow_mo=slow_mo)
        self.analyzer = WebsiteAnalyzer(api_key=api_key)
        self.credentials = UserCredentials("", "")
        self.session_log = []
        self.current_analysis = None
        
    async def start(self) -> None:
        """Start the browser and initialize the session."""
        await self.browser.start_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_started",
            "details": "Browser automation started"
        })
        
    async def close(self) -> None:
        """Close the browser and cleanup resources."""
        await self.browser.close_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_closed",
            "details": "Browser automation stopped"
        })
        
    async def analyze_and_browse(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website and begin intelligent browsing.
        
        Args:
            url: The website URL to browse
            description: Optional description of the website
            
        Returns:
            Dictionary containing browsing results and analysis
        """
        try:
            # Step 1: Analyze the website
            print(f"🔍 Analyzing website: {url}")
            self.current_analysis = await self.analyzer.analyze_website(url, description)
            
            # Step 2: Navigate to the website
            print(f"🌐 Navigating to: {url}")
            page_info = await self.browser.navigate_to(url)
            
            if 'error' in page_info:
                return {
                    "success": False,
                    "error": f"Failed to navigate to {url}: {page_info['error']}",
                    "analysis": self.current_analysis
                }
            
            # Step 3: Begin intelligent browsing
            print("🤖 Starting intelligent browsing...")
            browsing_results = await self._intelligent_browsing_loop()
            
            return {
                "success": True,
                "analysis": self.current_analysis,
                "browsing_results": browsing_results,
                "session_log": self.session_log
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": self.current_analysis,
                "session_log": self.session_log
            }
    
    async def _intelligent_browsing_loop(self, max_steps: int = 20) -> List[Dict[str, Any]]:
        """Main intelligent browsing loop that uses AI to guide navigation.
        
        Args:
            max_steps: Maximum number of steps to take
            
        Returns:
            List of actions taken during browsing
        """
        actions_taken = []
        step_count = 0
        
        while step_count < max_steps:
            try:
                # Get current page information
                current_url = await self.browser.get_current_url()
                page_content = await self.browser.get_page_content()
                
                # Use AI to analyze the current page and decide next action
                print(f"🧠 Analyzing page {step_count + 1}: {current_url}")
                analysis = await self.analyzer.get_page_analysis(
                    page_content, 
                    current_url, 
                    f"Step {step_count + 1}"
                )
                
                # Log the analysis
                self.session_log.append({
                    "timestamp": time.time(),
                    "action": "page_analysis",
                    "url": current_url,
                    "analysis": analysis
                })
                
                # Execute the suggested action
                action_result = await self._execute_action(analysis, current_url)
                actions_taken.append({
                    "step": step_count + 1,
                    "url": current_url,
                    "analysis": analysis,
                    "action_result": action_result
                })
                
                # Check if we should continue or stop
                if not action_result.get("continue", True):
                    print("🛑 Stopping browsing based on AI recommendation")
                    break
                    
                # Wait a bit before next step
                await asyncio.sleep(2)
                step_count += 1
                
            except Exception as e:
                print(f"❌ Error in browsing loop step {step_count + 1}: {e}")
                actions_taken.append({
                    "step": step_count + 1,
                    "error": str(e),
                    "action_result": {"continue": False}
                })
                break
                
        return actions_taken
    
    async def _execute_action(self, analysis: Dict[str, Any], current_url: str) -> Dict[str, Any]:
        """Execute the action suggested by AI analysis.
        
        Args:
            analysis: AI analysis of the current page
            current_url: Current page URL
            
        Returns:
            Result of the action execution
        """
        try:
            next_action = analysis.get("next_action", "wait")
            target_elements = analysis.get("target_elements", [])
            form_data = analysis.get("form_data", {})
            page_type = analysis.get("page_type", "unknown")
            
            print(f"🎯 Executing action: {next_action}")
            
            if next_action == "click" and target_elements:
                # Try to click on suggested elements
                for element in target_elements:
                    if await self.browser.click_element(element):
                        print(f"✅ Clicked element: {element}")
                        return {"success": True, "action": "click", "element": element, "continue": True}
                        
            elif next_action == "fill_form" and form_data:
                # Fill out a form
                if await self.browser.fill_form(form_data):
                    print(f"✅ Filled form with data: {list(form_data.keys())}")
                    # Try to submit the form
                    if await self.browser.submit_form():
                        print("✅ Form submitted")
                        return {"success": True, "action": "form_submit", "continue": True}
                    else:
                        return {"success": True, "action": "form_filled", "continue": True}
                        
            elif next_action == "navigate" and target_elements:
                # Navigate to a specific URL or click a link
                for element in target_elements:
                    if element.startswith("http"):
                        # Direct URL navigation
                        page_info = await self.browser.navigate_to(element)
                        if "error" not in page_info:
                            print(f"✅ Navigated to: {element}")
                            return {"success": True, "action": "navigate", "url": element, "continue": True}
                    else:
                        # Click a link
                        if await self.browser.click_element(element):
                            print(f"✅ Clicked link: {element}")
                            return {"success": True, "action": "click_link", "element": element, "continue": True}
                            
            elif next_action == "wait":
                print("⏳ Waiting for page to load...")
                await asyncio.sleep(3)
                return {"success": True, "action": "wait", "continue": True}
                
            elif next_action == "stop":
                print("🛑 AI recommended stopping")
                return {"success": True, "action": "stop", "continue": False}
            
            # If no specific action worked, try to find and click common elements
            return await self._try_common_actions(page_type)
            
        except Exception as e:
            print(f"❌ Error executing action: {e}")
            return {"success": False, "error": str(e), "continue": False}
    
    async def _try_common_actions(self, page_type: str) -> Dict[str, Any]:
        """Try common actions based on page type.
        
        Args:
            page_type: Type of page (login, signup, dashboard, etc.)
            
        Returns:
            Result of the action attempt
        """
        try:
            if page_type in ["login", "signin"]:
                # Look for login form or sign in button
                login_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Sign In")',
                    'button:has-text("Login")',
                    'a:has-text("Sign In")',
                    'a:has-text("Login")'
                ]
                
                for selector in login_selectors:
                    if await self.browser.click_element(selector):
                        print(f"✅ Clicked login element: {selector}")
                        return {"success": True, "action": "click_login", "continue": True}
                        
            elif page_type in ["signup", "register"]:
                # Look for signup form or register button
                signup_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Sign Up")',
                    'button:has-text("Register")',
                    'button:has-text("Create Account")',
                    'a:has-text("Sign Up")',
                    'a:has-text("Register")'
                ]
                
                for selector in signup_selectors:
                    if await self.browser.click_element(selector):
                        print(f"✅ Clicked signup element: {selector}")
                        return {"success": True, "action": "click_signup", "continue": True}
                        
            elif page_type == "homepage":
                # Look for common navigation elements
                nav_selectors = [
                    'nav a',
                    '.menu a',
                    '.navigation a',
                    'a[href*="/about"]',
                    'a[href*="/features"]',
                    'a[href*="/pricing"]'
                ]
                
                for selector in nav_selectors:
                    if await self.browser.click_element(selector):
                        print(f"✅ Clicked navigation element: {selector}")
                        return {"success": True, "action": "click_nav", "continue": True}
            
            # Default: wait and continue
            print("⏳ No specific action found, waiting...")
            await asyncio.sleep(3)
            return {"success": True, "action": "wait", "continue": True}
            
        except Exception as e:
            print(f"❌ Error in common actions: {e}")
            return {"success": False, "error": str(e), "continue": False}
    
    async def create_user_account(self, credentials: UserCredentials) -> Dict[str, Any]:
        """Create a user account on the current website.
        
        Args:
            credentials: User credentials for account creation
            
        Returns:
            Result of account creation attempt
        """
        try:
            self.credentials = credentials
            
            # Look for signup/register form
            page_content = await self.browser.get_page_content()
            analysis = await self.analyzer.get_page_analysis(
                page_content, 
                await self.browser.get_current_url(), 
                "Looking for account creation form"
            )
            
            if analysis.get("page_type") in ["signup", "register"]:
                # Prepare form data
                form_data = {
                    "email": credentials.email,
                    "password": credentials.password,
                    "first_name": credentials.first_name,
                    "last_name": credentials.last_name,
                    "username": credentials.username or credentials.email.split("@")[0]
                }
                
                # Fill and submit the form
                if await self.browser.fill_form(form_data):
                    if await self.browser.submit_form():
                        print("✅ Account creation form submitted")
                        return {"success": True, "message": "Account creation form submitted"}
                    else:
                        return {"success": False, "error": "Failed to submit form"}
                else:
                    return {"success": False, "error": "Failed to fill form"}
            else:
                # Look for signup link
                signup_selectors = [
                    'a:has-text("Sign Up")',
                    'a:has-text("Register")',
                    'a:has-text("Create Account")',
                    'button:has-text("Sign Up")'
                ]
                
                for selector in signup_selectors:
                    if await self.browser.click_element(selector):
                        print(f"✅ Clicked signup link: {selector}")
                        # Wait for page to load and try again
                        await asyncio.sleep(3)
                        return await self.create_user_account(credentials)
                
                return {"success": False, "error": "No signup form or link found"}
                
        except Exception as e:
            print(f"❌ Error creating account: {e}")
            return {"success": False, "error": str(e)}
    
    async def login_user(self, credentials: UserCredentials) -> Dict[str, Any]:
        """Login with user credentials.
        
        Args:
            credentials: User credentials for login
            
        Returns:
            Result of login attempt
        """
        try:
            # Look for login form
            page_content = await self.browser.get_page_content()
            analysis = await self.analyzer.get_page_analysis(
                page_content, 
                await self.browser.get_current_url(), 
                "Looking for login form"
            )
            
            if analysis.get("page_type") in ["login", "signin"]:
                # Prepare login data
                form_data = {
                    "email": credentials.email,
                    "password": credentials.password,
                    "username": credentials.username or credentials.email
                }
                
                # Fill and submit the form
                if await self.browser.fill_form(form_data):
                    if await self.browser.submit_form():
                        print("✅ Login form submitted")
                        return {"success": True, "message": "Login form submitted"}
                    else:
                        return {"success": False, "error": "Failed to submit login form"}
                else:
                    return {"success": False, "error": "Failed to fill login form"}
            else:
                # Look for login link
                login_selectors = [
                    'a:has-text("Sign In")',
                    'a:has-text("Login")',
                    'button:has-text("Sign In")',
                    'button:has-text("Login")'
                ]
                
                for selector in login_selectors:
                    if await self.browser.click_element(selector):
                        print(f"✅ Clicked login link: {selector}")
                        # Wait for page to load and try again
                        await asyncio.sleep(3)
                        return await self.login_user(credentials)
                
                return {"success": False, "error": "No login form or link found"}
                
        except Exception as e:
            print(f"❌ Error logging in: {e}")
            return {"success": False, "error": str(e)}
    
    def save_session_log(self, filename: str = None) -> str:
        """Save the session log to a file.
        
        Args:
            filename: Optional filename for the log
            
        Returns:
            Path to the saved log file
        """
        if not filename:
            timestamp = int(time.time())
            filename = f"browsing_session_{timestamp}.json"
            
        log_path = Path(filename)
        with open(log_path, 'w') as f:
            json.dump(self.session_log, f, indent=2)
            
        return str(log_path)
