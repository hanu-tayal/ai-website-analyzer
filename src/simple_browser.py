"""
Simplified browser implementation that works without Claude Code SDK.
This provides basic AI-like functionality using pattern matching and heuristics.
"""
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import time
import re

from .browser_automation import BrowserAutomation


class SimpleBrowser:
    """Simplified browser that provides AI-like functionality without Claude Code SDK."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000):
        """Initialize the simple browser.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
        """
        self.browser = BrowserAutomation(headless=headless, slow_mo=slow_mo)
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
            self.current_analysis = self._analyze_website(url, description)
            
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
    
    def _analyze_website(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website using pattern matching and heuristics.
        
        Args:
            url: The website URL to analyze
            description: Optional description of the website
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "url": url,
            "description": description,
            "purpose": "Unknown website",
            "key_features": [],
            "user_flows": [],
            "registration_required": False,
            "login_flow": {},
            "main_navigation": [],
            "suggested_user_journey": []
        }
        
        # Analyze based on URL patterns
        url_lower = url.lower()
        
        if "github.com" in url_lower:
            analysis.update({
                "purpose": "Code hosting and version control platform",
                "key_features": ["Repository management", "Code collaboration", "Issue tracking", "Pull requests"],
                "user_flows": ["Browse repositories", "Create account", "Clone repositories", "Create issues"],
                "registration_required": True,
                "login_flow": {
                    "signup_url": "https://github.com/signup",
                    "login_url": "https://github.com/login",
                    "required_fields": ["username", "email", "password"]
                },
                "main_navigation": ["Repositories", "Issues", "Pull requests", "Marketplace"],
                "suggested_user_journey": ["Visit homepage", "Sign up", "Create repository", "Explore features"]
            })
            
        elif "google.com" in url_lower:
            analysis.update({
                "purpose": "Search engine and web services",
                "key_features": ["Web search", "Email (Gmail)", "Cloud storage", "Maps"],
                "user_flows": ["Search", "Sign in", "Use services"],
                "registration_required": False,
                "main_navigation": ["Search", "Images", "Maps", "Gmail"],
                "suggested_user_journey": ["Search", "Explore results", "Click on links"]
            })
            
        elif "example.com" in url_lower:
            analysis.update({
                "purpose": "Example website for testing",
                "key_features": ["Basic web content", "Example pages"],
                "user_flows": ["Browse content", "Navigate pages"],
                "registration_required": False,
                "main_navigation": ["Home", "About", "Contact"],
                "suggested_user_journey": ["Visit homepage", "Read content", "Navigate to other pages"]
            })
            
        elif "httpbin.org" in url_lower:
            analysis.update({
                "purpose": "HTTP testing service",
                "key_features": ["HTTP request testing", "API testing", "Webhook testing"],
                "user_flows": ["Test HTTP methods", "View request details", "Test responses"],
                "registration_required": False,
                "main_navigation": ["GET", "POST", "PUT", "DELETE"],
                "suggested_user_journey": ["Test GET request", "Test POST request", "View response"]
            })
            
        else:
            # Generic analysis based on description
            if description:
                analysis["purpose"] = description
                analysis["key_features"] = ["Web content", "Navigation", "User interaction"]
                analysis["user_flows"] = ["Browse content", "Navigate", "Interact"]
                analysis["main_navigation"] = ["Home", "About", "Contact", "Services"]
                analysis["suggested_user_journey"] = ["Visit homepage", "Explore content", "Look for features"]
            
            # Check for common patterns in URL
            if "login" in url_lower or "signin" in url_lower:
                analysis["registration_required"] = True
                analysis["login_flow"] = {"login_url": url}
            elif "signup" in url_lower or "register" in url_lower:
                analysis["registration_required"] = True
                analysis["login_flow"] = {"signup_url": url}
        
        return analysis
    
    async def _intelligent_browsing_loop(self, max_steps: int = 15) -> List[Dict[str, Any]]:
        """Main intelligent browsing loop using pattern matching.
        
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
                
                # Analyze the current page
                print(f"🧠 Analyzing page {step_count + 1}: {current_url}")
                analysis = self._analyze_page(page_content, current_url, f"Step {step_count + 1}")
                
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
                    print("🛑 Stopping browsing based on analysis")
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
    
    def _analyze_page(self, page_content: str, current_url: str, action_taken: str = "") -> Dict[str, Any]:
        """Analyze a specific page using pattern matching.
        
        Args:
            page_content: The HTML content of the current page
            current_url: The URL of the current page
            action_taken: Description of the last action taken
            
        Returns:
            Dictionary with analysis and suggested next actions
        """
        content_lower = page_content.lower()
        
        # Basic page type detection
        page_type = "unknown"
        next_action = "wait"
        target_elements = []
        form_data = {}
        confidence = 0.3
        
        # Detect page type based on content patterns
        if "login" in content_lower or "sign in" in content_lower:
            page_type = "login"
            next_action = "fill_form"
            target_elements = ['input[name="email"]', 'input[name="username"]', 'input[type="password"]']
            form_data = {"email": "demo@example.com", "password": "password123"}
            confidence = 0.8
            
        elif "signup" in content_lower or "register" in content_lower or "create account" in content_lower:
            page_type = "signup"
            next_action = "fill_form"
            target_elements = ['input[name="email"]', 'input[name="password"]', 'input[name="first_name"]']
            form_data = {"email": "demo@example.com", "password": "password123", "first_name": "Demo"}
            confidence = 0.8
            
        elif "search" in content_lower and ("input" in content_lower or "form" in content_lower):
            page_type = "search"
            next_action = "click"
            target_elements = ['input[type="search"]', 'input[name="q"]', 'button[type="submit"]']
            confidence = 0.7
            
        elif "form" in content_lower and "input" in content_lower:
            page_type = "form"
            next_action = "fill_form"
            target_elements = ['form input', 'form textarea', 'form select']
            form_data = {"email": "demo@example.com", "message": "Hello from AI browser"}
            confidence = 0.6
            
        elif "button" in content_lower or "link" in content_lower:
            page_type = "navigation"
            next_action = "click"
            target_elements = ['a', 'button', 'input[type="submit"]']
            confidence = 0.5
            
        elif "error" in content_lower or "not found" in content_lower:
            page_type = "error"
            next_action = "navigate"
            target_elements = ['a[href="/"]', 'a[href*="home"]']
            confidence = 0.9
            
        else:
            page_type = "content"
            next_action = "click"
            target_elements = ['a', 'button']
            confidence = 0.4
        
        # Special handling for specific domains
        if "google.com" in current_url.lower():
            if "search" in current_url.lower():
                page_type = "search_results"
                next_action = "click"
                target_elements = ['a[href*="http"]', 'h3 a']
                confidence = 0.8
            else:
                page_type = "search"
                next_action = "fill_form"
                target_elements = ['input[name="q"]', 'input[type="search"]']
                form_data = {"q": "artificial intelligence"}
                confidence = 0.7
        
        return {
            "page_type": page_type,
            "next_action": next_action,
            "target_elements": target_elements,
            "form_data": form_data,
            "confidence": confidence
        }
    
    async def _execute_action(self, analysis: Dict[str, Any], current_url: str) -> Dict[str, Any]:
        """Execute the action suggested by analysis.
        
        Args:
            analysis: Analysis of the current page
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
