"""
Smart browser that provides dynamic, context-aware browsing without requiring Claude Code SDK.
Uses advanced pattern matching, content analysis, and heuristics to make intelligent decisions.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import time
import re
from urllib.parse import urlparse, urljoin

from .browser_automation import BrowserAutomation


class SmartBrowser:
    """Smart browser that provides dynamic, context-aware browsing."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000):
        """Initialize the smart browser.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
        """
        self.browser = BrowserAutomation(headless=headless, slow_mo=slow_mo)
        self.session_log = []
        self.current_analysis = None
        self.browsing_context = {
            "visited_urls": set(),
            "current_goal": "explore",
            "interests": [],
            "session_start": time.time()
        }
        
    async def start(self) -> None:
        """Start the browser and initialize the session."""
        await self.browser.start_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_started",
            "details": "Smart browser automation started"
        })
        
    async def close(self) -> None:
        """Close the browser and cleanup resources."""
        await self.browser.close_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_closed",
            "details": "Smart browser automation stopped"
        })
        
    async def analyze_and_browse(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website and begin smart browsing.
        
        Args:
            url: The website URL to browse
            description: Optional description of the website
            
        Returns:
            Dictionary containing browsing results and analysis
        """
        try:
            # Step 1: Analyze the website
            print(f"🔍 Analyzing website: {url}")
            self.current_analysis = self._analyze_website_smart(url, description)
            
            # Step 2: Navigate to the website
            print(f"🌐 Navigating to: {url}")
            page_info = await self.browser.navigate_to(url)
            
            if 'error' in page_info:
                return {
                    "success": False,
                    "error": f"Failed to navigate to {url}: {page_info['error']}",
                    "analysis": self.current_analysis
                }
            
            # Add to visited URLs
            self.browsing_context["visited_urls"].add(url)
            
            # Step 3: Begin smart browsing
            print("🤖 Starting smart dynamic browsing...")
            browsing_results = await self._smart_browsing_loop()
            
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
    
    def _analyze_website_smart(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website using smart heuristics and pattern matching.
        
        Args:
            url: The website URL to analyze
            description: Optional description of the website
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "url": url,
            "description": description,
            "purpose": "Website exploration",
            "key_features": [],
            "user_flows": [],
            "registration_required": False,
            "login_flow": {},
            "main_navigation": [],
            "suggested_user_journey": [],
            "interaction_strategy": "Explore and interact with interesting elements"
        }
        
        # Smart analysis based on URL patterns and domain knowledge
        domain = urlparse(url).netloc.lower()
        
        if "github.com" in domain:
            analysis.update({
                "purpose": "Code hosting and version control platform",
                "key_features": ["Repository management", "Code collaboration", "Issue tracking", "Pull requests", "Actions"],
                "user_flows": ["Browse repositories", "View code", "Check issues", "Explore trending projects"],
                "registration_required": False,  # Can browse without account
                "main_navigation": ["Repositories", "Issues", "Pull requests", "Actions", "Packages"],
                "suggested_user_journey": ["Explore trending repos", "Check out popular projects", "Look at issues", "Browse code"],
                "interaction_strategy": "Focus on repositories, trending projects, and interesting code"
            })
            
        elif "google.com" in domain:
            analysis.update({
                "purpose": "Search engine and web services",
                "key_features": ["Web search", "Images", "Maps", "Gmail", "Drive"],
                "user_flows": ["Search", "Browse results", "Click on interesting links"],
                "registration_required": False,
                "main_navigation": ["Search", "Images", "Maps", "Gmail", "Drive"],
                "suggested_user_journey": ["Perform searches", "Explore search results", "Click on interesting links"],
                "interaction_strategy": "Search for interesting topics and explore results"
            })
            
        elif "httpbin.org" in domain:
            analysis.update({
                "purpose": "HTTP testing and debugging service",
                "key_features": ["HTTP method testing", "Request inspection", "Response testing", "Webhook testing"],
                "user_flows": ["Test HTTP methods", "Inspect requests", "Try different endpoints"],
                "registration_required": False,
                "main_navigation": ["GET", "POST", "PUT", "DELETE", "PATCH"],
                "suggested_user_journey": ["Test different HTTP methods", "Inspect request details", "Try various endpoints"],
                "interaction_strategy": "Test different HTTP methods and explore the API"
            })
            
        elif "example.com" in domain:
            analysis.update({
                "purpose": "Example website for testing and demonstration",
                "key_features": ["Basic web content", "Example pages", "Test functionality"],
                "user_flows": ["Browse content", "Navigate pages", "Test features"],
                "registration_required": False,
                "main_navigation": ["Home", "About", "Contact", "Services"],
                "suggested_user_journey": ["Read content", "Navigate to different pages", "Test interactive elements"],
                "interaction_strategy": "Explore all available pages and test functionality"
            })
            
        else:
            # Generic analysis with smart heuristics
            if description:
                analysis["purpose"] = description
                analysis["interaction_strategy"] = f"Explore {description} and find interesting content"
            
            # Analyze URL patterns
            if "blog" in domain or "/blog" in url:
                analysis.update({
                    "purpose": "Blog or content website",
                    "key_features": ["Articles", "Content", "Navigation"],
                    "interaction_strategy": "Read articles and explore content"
                })
            elif "shop" in domain or "store" in domain or "ecommerce" in domain:
                analysis.update({
                    "purpose": "E-commerce website",
                    "key_features": ["Products", "Shopping cart", "Categories"],
                    "interaction_strategy": "Browse products and explore categories"
                })
            elif "news" in domain or "news" in url:
                analysis.update({
                    "purpose": "News website",
                    "key_features": ["Articles", "Headlines", "Categories"],
                    "interaction_strategy": "Read news articles and explore different sections"
                })
        
        return analysis
    
    async def _smart_browsing_loop(self, max_steps: int = 25) -> List[Dict[str, Any]]:
        """Main smart browsing loop that makes dynamic decisions.
        
        Args:
            max_steps: Maximum number of steps to take
            
        Returns:
            List of actions taken during browsing
        """
        actions_taken = []
        step_count = 0
        consecutive_failures = 0
        
        while step_count < max_steps and consecutive_failures < 3:
            try:
                # Get current page information
                current_url = await self.browser.get_current_url()
                page_content = await self.browser.get_page_content()
                
                # Smart analysis of the current page
                print(f"🧠 Smart analyzing page {step_count + 1}: {current_url}")
                analysis = self._analyze_page_smart(page_content, current_url, step_count)
                
                # Log the analysis
                self.session_log.append({
                    "timestamp": time.time(),
                    "action": "smart_page_analysis",
                    "url": current_url,
                    "analysis": analysis
                })
                
                # Execute the smart-suggested action
                action_result = await self._execute_smart_action(analysis, current_url, step_count)
                actions_taken.append({
                    "step": step_count + 1,
                    "url": current_url,
                    "analysis": analysis,
                    "action_result": action_result
                })
                
                # Track failures
                if action_result.get("success", False):
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                
                # Check if we should continue or stop
                if not action_result.get("continue", True):
                    print("🛑 Smart analysis suggests stopping browsing")
                    break
                
                # Add to visited URLs
                self.browsing_context["visited_urls"].add(current_url)
                    
                # Wait a bit before next step
                await asyncio.sleep(2)
                step_count += 1
                
            except Exception as e:
                print(f"❌ Error in smart browsing step {step_count + 1}: {e}")
                actions_taken.append({
                    "step": step_count + 1,
                    "error": str(e),
                    "action_result": {"continue": False}
                })
                consecutive_failures += 1
                break
                
        return actions_taken
    
    def _analyze_page_smart(self, page_content: str, current_url: str, step_count: int) -> Dict[str, Any]:
        """Smart analysis of a specific page using advanced heuristics.
        
        Args:
            page_content: The HTML content of the current page
            current_url: The URL of the current page
            step_count: Current step number
            
        Returns:
            Dictionary with smart analysis and suggested next actions
        """
        content_lower = page_content.lower()
        
        # Extract key information from the page
        page_info = self._extract_page_info(page_content)
        
        # Determine page type and appropriate action
        page_type = self._classify_page_type(content_lower, page_info)
        next_action = self._determine_next_action(page_type, page_info, step_count)
        target_elements = self._find_target_elements(page_type, page_info, content_lower)
        form_data = self._generate_form_data(page_type, page_info)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(page_type, next_action, page_info, step_count)
        
        return {
            "page_type": page_type,
            "next_action": next_action,
            "target_elements": target_elements,
            "form_data": form_data,
            "reasoning": reasoning,
            "confidence": self._calculate_confidence(page_type, next_action, page_info),
            "continue": self._should_continue(step_count, page_type, page_info)
        }
    
    def _extract_page_info(self, page_content: str) -> Dict[str, Any]:
        """Extract useful information from page content."""
        info = {
            "title": "",
            "headings": [],
            "links": [],
            "forms": [],
            "buttons": [],
            "images": [],
            "text_content": ""
        }
        
        try:
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', page_content, re.IGNORECASE | re.DOTALL)
            if title_match:
                info["title"] = title_match.group(1).strip()
            
            # Extract headings
            headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', page_content, re.IGNORECASE | re.DOTALL)
            info["headings"] = [h.strip() for h in headings if h.strip()]
            
            # Extract links
            links = re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', page_content, re.IGNORECASE | re.DOTALL)
            info["links"] = [(href, text.strip()) for href, text in links if text.strip()]
            
            # Extract forms
            forms = re.findall(r'<form[^>]*>(.*?)</form>', page_content, re.IGNORECASE | re.DOTALL)
            info["forms"] = forms
            
            # Extract buttons
            buttons = re.findall(r'<button[^>]*>(.*?)</button>', page_content, re.IGNORECASE | re.DOTALL)
            info["buttons"] = [b.strip() for b in buttons if b.strip()]
            
            # Extract text content (simplified)
            text_content = re.sub(r'<[^>]+>', ' ', page_content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            info["text_content"] = text_content[:500]  # First 500 chars
            
        except Exception as e:
            print(f"Error extracting page info: {e}")
        
        return info
    
    def _classify_page_type(self, content_lower: str, page_info: Dict[str, Any]) -> str:
        """Classify the page type based on content analysis."""
        
        # Check for specific page types
        if "login" in content_lower or "sign in" in content_lower:
            return "login"
        elif "signup" in content_lower or "register" in content_lower or "create account" in content_lower:
            return "signup"
        elif "search" in content_lower and ("input" in content_lower or "form" in content_lower):
            return "search"
        elif "error" in content_lower or "not found" in content_lower or "404" in content_lower:
            return "error"
        elif "dashboard" in content_lower or "admin" in content_lower:
            return "dashboard"
        elif "product" in content_lower or "item" in content_lower:
            return "product"
        elif "article" in content_lower or "post" in content_lower or "blog" in content_lower:
            return "article"
        elif "form" in content_lower and "input" in content_lower:
            return "form"
        elif "results" in content_lower or "search results" in content_lower:
            return "search_results"
        elif "httpbin" in content_lower or "api" in content_lower or "endpoint" in content_lower:
            return "api_docs"
        elif "home" in content_lower or "welcome" in content_lower or len(page_info["headings"]) == 0:
            return "homepage"
        else:
            return "content"
    
    def _determine_next_action(self, page_type: str, page_info: Dict[str, Any], step_count: int) -> str:
        """Determine the next action based on page type and context."""
        
        if page_type == "login":
            return "fill_form"
        elif page_type == "signup":
            return "fill_form"
        elif page_type == "search":
            return "search"
        elif page_type == "form":
            return "fill_form"
        elif page_type == "error":
            return "navigate"
        elif page_type == "search_results":
            return "click"
        elif page_type == "product":
            return "click"
        elif page_type == "article":
            return "click"
        elif page_type == "api_docs":
            return "click"  # API docs usually have links to different endpoints
        elif page_type == "homepage":
            if step_count < 3:
                return "click"
            else:
                return "search"
        else:
            # For content pages, vary the action
            if step_count % 3 == 0:
                return "search"
            else:
                return "click"
    
    def _find_target_elements(self, page_type: str, page_info: Dict[str, Any], content_lower: str) -> List[str]:
        """Find target elements based on page type and content."""
        elements = []
        
        if page_type == "login":
            elements = ['input[name="email"]', 'input[name="username"]', 'input[type="password"]', 'button[type="submit"]']
        elif page_type == "signup":
            elements = ['input[name="email"]', 'input[name="password"]', 'input[name="first_name"]', 'button[type="submit"]']
        elif page_type == "search":
            elements = ['input[type="search"]', 'input[name="q"]', 'button[type="submit"]']
        elif page_type == "search_results":
            elements = ['a[href*="http"]', 'h3 a', 'h2 a', '.result a']
        elif page_type == "product":
            elements = ['a[href*="product"]', '.product a', 'button']
        elif page_type == "article":
            elements = ['a[href*="article"]', '.article a', 'a[href*="post"]']
        elif page_type == "api_docs":
            elements = ['a[href*="http"]', 'a[href*="/"]', '.endpoint a', 'a[href*="api"]']
        elif page_type == "form":
            elements = ['form input', 'form textarea', 'form select', 'button[type="submit"]']
        else:
            # General content page
            elements = ['a', 'button', 'input[type="submit"]']
        
        # Filter elements that actually exist on the page
        existing_elements = []
        for element in elements:
            if self._element_exists_in_content(element, content_lower):
                existing_elements.append(element)
        
        return existing_elements[:5]  # Limit to 5 elements
    
    def _element_exists_in_content(self, selector: str, content_lower: str) -> bool:
        """Check if an element exists in the page content."""
        if 'input[name="email"]' in selector:
            return 'name="email"' in content_lower
        elif 'input[name="username"]' in selector:
            return 'name="username"' in content_lower
        elif 'input[type="password"]' in selector:
            return 'type="password"' in content_lower
        elif 'input[type="search"]' in selector:
            return 'type="search"' in content_lower
        elif 'input[name="q"]' in selector:
            return 'name="q"' in content_lower
        elif 'button[type="submit"]' in selector:
            return 'type="submit"' in content_lower
        elif 'a' in selector:
            return '<a ' in content_lower
        elif 'button' in selector:
            return '<button' in content_lower
        else:
            return True
    
    def _generate_form_data(self, page_type: str, page_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate appropriate form data based on page type."""
        if page_type == "login":
            return {"email": "demo@example.com", "password": "password123"}
        elif page_type == "signup":
            return {"email": "demo@example.com", "password": "password123", "first_name": "Demo"}
        elif page_type == "search":
            return {"q": "artificial intelligence", "search": "artificial intelligence"}
        elif page_type == "form":
            return {"email": "demo@example.com", "message": "Hello from smart browser"}
        else:
            return {}
    
    def _generate_reasoning(self, page_type: str, next_action: str, page_info: Dict[str, Any], step_count: int) -> str:
        """Generate human-readable reasoning for the action."""
        if page_type == "login":
            return "Login page detected - attempting to fill login form"
        elif page_type == "signup":
            return "Signup page detected - attempting to fill registration form"
        elif page_type == "search":
            return "Search page detected - performing a search query"
        elif page_type == "search_results":
            return "Search results page - clicking on interesting results"
        elif page_type == "product":
            return "Product page detected - exploring product details"
        elif page_type == "article":
            return "Article page detected - looking for related content"
        elif page_type == "api_docs":
            return "API documentation page detected - exploring different endpoints"
        elif page_type == "homepage":
            return f"Homepage detected (step {step_count}) - exploring navigation elements"
        elif page_type == "error":
            return "Error page detected - trying to navigate back to working content"
        else:
            return f"Content page detected - exploring available elements (step {step_count})"
    
    def _calculate_confidence(self, page_type: str, next_action: str, page_info: Dict[str, Any]) -> float:
        """Calculate confidence in the suggested action."""
        base_confidence = 0.5
        
        if page_type in ["login", "signup", "search"]:
            base_confidence = 0.8
        elif page_type in ["search_results", "product", "article"]:
            base_confidence = 0.7
        elif page_type == "error":
            base_confidence = 0.9
        elif page_type == "homepage":
            base_confidence = 0.6
        else:
            base_confidence = 0.5
        
        # Adjust based on available elements
        if page_info.get("forms") and next_action == "fill_form":
            base_confidence += 0.1
        if page_info.get("links") and next_action == "click":
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _should_continue(self, step_count: int, page_type: str, page_info: Dict[str, Any]) -> bool:
        """Determine if browsing should continue."""
        if step_count >= 20:
            return False
        if page_type == "error" and step_count > 5:
            return False
        if len(self.browsing_context["visited_urls"]) > 15:
            return False
        
        # Stop if we're stuck on the same page type for too long
        if step_count > 10 and page_type in ["content", "article"]:
            return False
            
        return True
    
    async def _execute_smart_action(self, analysis: Dict[str, Any], current_url: str, step_count: int) -> Dict[str, Any]:
        """Execute the smart-suggested action."""
        try:
            next_action = analysis.get("next_action", "wait")
            target_elements = analysis.get("target_elements", [])
            form_data = analysis.get("form_data", {})
            reasoning = analysis.get("reasoning", "")
            confidence = analysis.get("confidence", 0.0)
            
            print(f"🎯 Smart Action: {next_action}")
            print(f"   Reasoning: {reasoning}")
            print(f"   Confidence: {confidence:.2f}")
            
            if next_action == "click" and target_elements:
                # Try to click on suggested elements
                for element in target_elements:
                    if await self.browser.click_element(element):
                        print(f"✅ Clicked element: {element}")
                        return {"success": True, "action": "click", "element": element, "continue": True}
                        
            elif next_action == "fill_form" and form_data:
                # Fill out a form with suggested data
                if await self.browser.fill_form(form_data):
                    print(f"✅ Filled form with data: {list(form_data.keys())}")
                    # Try to submit the form
                    if await self.browser.submit_form():
                        print("✅ Form submitted")
                        return {"success": True, "action": "form_submit", "continue": True}
                    else:
                        return {"success": True, "action": "form_filled", "continue": True}
                        
            elif next_action == "search" and form_data:
                # Perform a search
                if await self.browser.fill_form(form_data):
                    if await self.browser.submit_form():
                        print(f"✅ Searched for: {form_data.get('q', form_data.get('search', 'query'))}")
                        return {"success": True, "action": "search", "continue": True}
                        
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
                print("⏳ Smart analysis suggests waiting...")
                await asyncio.sleep(3)
                return {"success": True, "action": "wait", "continue": True}
            
            # If no specific action worked, try to find and click common elements
            return await self._try_smart_fallback(analysis)
            
        except Exception as e:
            print(f"❌ Error executing smart action: {e}")
            return {"success": False, "error": str(e), "continue": False}
    
    async def _try_smart_fallback(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Try smart fallback actions."""
        try:
            page_type = analysis.get("page_type", "unknown")
            target_elements = analysis.get("target_elements", [])
            
            # Try the suggested elements first
            for element in target_elements:
                if await self.browser.click_element(element):
                    print(f"✅ Clicked fallback element: {element}")
                    return {"success": True, "action": "click", "element": element, "continue": True}
            
            # Try common elements based on page type
            if page_type in ["login", "signin"]:
                selectors = ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Sign In")']
            elif page_type in ["signup", "register"]:
                selectors = ['button[type="submit"]', 'input[type="submit"]', 'button:has-text("Sign Up")']
            elif page_type == "search":
                selectors = ['input[type="search"]', 'input[name="q"]', 'button[type="submit"]']
            else:
                selectors = ['a', 'button', 'input[type="submit"]']
            
            for selector in selectors:
                if await self.browser.click_element(selector):
                    print(f"✅ Clicked generic element: {selector}")
                    return {"success": True, "action": "click", "element": selector, "continue": True}
            
            # Default: wait and continue
            print("⏳ No actionable elements found, waiting...")
            await asyncio.sleep(3)
            return {"success": True, "action": "wait", "continue": True}
            
        except Exception as e:
            print(f"❌ Error in smart fallback: {e}")
            return {"success": False, "error": str(e), "continue": False}
    
    async def create_user_account(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Create a user account on the current website.
        
        Args:
            credentials: User credentials for account creation
            
        Returns:
            Result of account creation attempt
        """
        try:
            # Look for signup/register form
            page_content = await self.browser.get_page_content()
            analysis = self._analyze_page_smart(page_content, await self.browser.get_current_url(), "Looking for account creation form")
            
            if analysis.get("page_type") in ["signup", "register"]:
                # Prepare form data
                form_data = {
                    "email": credentials.get("email", "demo@example.com"),
                    "password": credentials.get("password", "password123"),
                    "first_name": credentials.get("first_name", "Demo"),
                    "last_name": credentials.get("last_name", "User"),
                    "username": credentials.get("username", credentials.get("email", "demo").split("@")[0])
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
    
    async def login_user(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Login with user credentials.
        
        Args:
            credentials: User credentials for login
            
        Returns:
            Result of login attempt
        """
        try:
            # Look for login form
            page_content = await self.browser.get_page_content()
            analysis = self._analyze_page_smart(page_content, await self.browser.get_current_url(), "Looking for login form")
            
            if analysis.get("page_type") in ["login", "signin"]:
                # Prepare login data
                form_data = {
                    "email": credentials.get("email", "demo@example.com"),
                    "password": credentials.get("password", "password123"),
                    "username": credentials.get("username", credentials.get("email", "demo"))
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
        """Save the session log to a file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"smart_browsing_session_{timestamp}.json"
            
        log_path = Path(filename)
        with open(log_path, 'w') as f:
            json.dump(self.session_log, f, indent=2)
            
        return str(log_path)
