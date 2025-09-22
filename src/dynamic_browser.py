"""
Dynamic AI-powered browser that uses Claude Code SDK for real-time intelligent decision making.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import time
import re

from .browser_automation import BrowserAutomation


class DynamicBrowser:
    """Dynamic browser that uses AI for real-time decision making."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000, api_key: Optional[str] = None):
        """Initialize the dynamic browser.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
            api_key: Claude API key (optional)
        """
        self.browser = BrowserAutomation(headless=headless, slow_mo=slow_mo)
        self.api_key = api_key
        self.session_log = []
        self.current_analysis = None
        self.use_ai = False
        
        # Try to initialize Claude Code SDK
        self._initialize_ai()
        
    def _initialize_ai(self):
        """Initialize AI capabilities."""
        try:
            from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock
            self.query = query
            self.ClaudeCodeOptions = ClaudeCodeOptions
            self.AssistantMessage = AssistantMessage
            self.TextBlock = TextBlock
            self.use_ai = True
            print("✅ Claude Code SDK initialized successfully")
        except ImportError as e:
            print(f"⚠️  Claude Code SDK not available: {e}")
            print("   Using fallback pattern-based analysis")
            self.use_ai = False
        except Exception as e:
            print(f"⚠️  Error initializing Claude Code SDK: {e}")
            print("   Using fallback pattern-based analysis")
            self.use_ai = False
        
    async def start(self) -> None:
        """Start the browser and initialize the session."""
        await self.browser.start_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_started",
            "details": "Dynamic browser automation started"
        })
        
    async def close(self) -> None:
        """Close the browser and cleanup resources."""
        await self.browser.close_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_closed",
            "details": "Dynamic browser automation stopped"
        })
        
    async def analyze_and_browse(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website and begin dynamic AI-powered browsing.
        
        Args:
            url: The website URL to browse
            description: Optional description of the website
            
        Returns:
            Dictionary containing browsing results and analysis
        """
        try:
            # Step 1: Analyze the website
            print(f"🔍 Analyzing website: {url}")
            self.current_analysis = await self._analyze_website_ai(url, description)
            
            # Step 2: Navigate to the website
            print(f"🌐 Navigating to: {url}")
            page_info = await self.browser.navigate_to(url)
            
            if 'error' in page_info:
                return {
                    "success": False,
                    "error": f"Failed to navigate to {url}: {page_info['error']}",
                    "analysis": self.current_analysis
                }
            
            # Step 3: Begin dynamic AI browsing
            print("🤖 Starting dynamic AI browsing...")
            browsing_results = await self._dynamic_browsing_loop()
            
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
    
    async def _analyze_website_ai(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website using AI.
        
        Args:
            url: The website URL to analyze
            description: Optional description of the website
            
        Returns:
            Dictionary containing analysis results
        """
        if not self.use_ai:
            return self._fallback_website_analysis(url, description)
        
        prompt = f"""
        You are an expert web analyst. Analyze the website at {url} and provide a comprehensive analysis.
        
        Description: {description or "No description provided"}
        
        Please analyze this website and provide the following information in a structured JSON format:
        
        {{
            "purpose": "What is the main purpose of this website?",
            "key_features": ["List the main features and functionalities"],
            "user_flows": ["Describe typical user journeys on this site"],
            "registration_required": true/false,
            "login_flow": {{
                "signup_url": "URL for signup if available",
                "login_url": "URL for login if available",
                "required_fields": ["List required fields for registration"]
            }},
            "main_navigation": ["List main navigation elements"],
            "suggested_user_journey": ["Recommend a logical sequence of actions a user should take"],
            "interaction_strategy": "How should an AI browser interact with this site? What should it focus on?"
        }}
        
        Be specific and actionable. Focus on what an AI browser should do to explore this website effectively.
        """
        
        try:
            options = self.ClaudeCodeOptions(
                system_prompt="You are an expert web analyst. Provide detailed, actionable analysis of websites for AI browser automation.",
                max_turns=1
            )
            
            analysis_result = {
                "url": url,
                "description": description,
                "purpose": "",
                "key_features": [],
                "user_flows": [],
                "registration_required": False,
                "login_flow": {},
                "main_navigation": [],
                "suggested_user_journey": [],
                "interaction_strategy": ""
            }
            
            async for message in self.query(prompt=prompt, options=options):
                if isinstance(message, self.AssistantMessage):
                    for block in message.content:
                        if isinstance(block, self.TextBlock):
                            # Parse the AI response
                            parsed = self._parse_ai_response(block.text)
                            analysis_result.update(parsed)
                            
            return analysis_result
            
        except Exception as e:
            print(f"Error in AI website analysis: {e}")
            return self._fallback_website_analysis(url, description)
    
    async def _dynamic_browsing_loop(self, max_steps: int = 20) -> List[Dict[str, Any]]:
        """Main dynamic browsing loop that uses AI for real-time decisions.
        
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
                print(f"🧠 AI analyzing page {step_count + 1}: {current_url}")
                analysis = await self._analyze_page_ai(page_content, current_url, f"Step {step_count + 1}")
                
                # Log the analysis
                self.session_log.append({
                    "timestamp": time.time(),
                    "action": "ai_page_analysis",
                    "url": current_url,
                    "analysis": analysis
                })
                
                # Execute the AI-suggested action
                action_result = await self._execute_ai_action(analysis, current_url)
                actions_taken.append({
                    "step": step_count + 1,
                    "url": current_url,
                    "analysis": analysis,
                    "action_result": action_result
                })
                
                # Check if AI suggests stopping
                if not action_result.get("continue", True):
                    print("🛑 AI recommended stopping browsing")
                    break
                    
                # Wait a bit before next step
                await asyncio.sleep(2)
                step_count += 1
                
            except Exception as e:
                print(f"❌ Error in dynamic browsing step {step_count + 1}: {e}")
                actions_taken.append({
                    "step": step_count + 1,
                    "error": str(e),
                    "action_result": {"continue": False}
                })
                break
                
        return actions_taken
    
    async def _analyze_page_ai(self, page_content: str, current_url: str, context: str = "") -> Dict[str, Any]:
        """Use AI to analyze a specific page and determine next actions.
        
        Args:
            page_content: The HTML content of the current page
            current_url: The URL of the current page
            context: Context about what we're trying to do
            
        Returns:
            Dictionary with AI analysis and suggested next actions
        """
        if not self.use_ai:
            return self._fallback_page_analysis(page_content, current_url, context)
        
        # Truncate content to avoid token limits
        content_preview = page_content[:3000] + "..." if len(page_content) > 3000 else page_content
        
        prompt = f"""
        You are an expert web automation AI. Analyze this webpage and suggest the next intelligent action to take.
        
        Current URL: {current_url}
        Context: {context}
        
        Page Content Preview:
        {content_preview}
        
        Based on this page content, provide a JSON response with:
        {{
            "page_type": "Type of page (homepage, login, signup, dashboard, search_results, product_page, etc.)",
            "next_action": "Specific action to take (click, fill_form, navigate, search, wait, stop)",
            "target_elements": ["CSS selectors for elements to interact with"],
            "form_data": {{"field_name": "value"}} if filling forms,
            "search_query": "query to search for" if searching,
            "reasoning": "Why this action makes sense",
            "confidence": 0.0-1.0,
            "continue": true/false
        }}
        
        Be intelligent and context-aware. Consider:
        - What would a human user naturally do next?
        - What's the most interesting or useful action?
        - Are there any forms to fill, buttons to click, or links to explore?
        - Should we stop browsing or continue exploring?
        
        Make decisions that would lead to meaningful exploration of the website.
        """
        
        try:
            options = self.ClaudeCodeOptions(
                system_prompt="You are an expert web automation AI. Make intelligent, context-aware decisions about web browsing actions.",
                max_turns=1
            )
            
            async for message in self.query(prompt=prompt, options=options):
                if isinstance(message, self.AssistantMessage):
                    for block in message.content:
                        if isinstance(block, self.TextBlock):
                            return self._parse_ai_response(block.text)
                            
        except Exception as e:
            print(f"Error in AI page analysis: {e}")
            return self._fallback_page_analysis(page_content, current_url, context)
        
        return {
            "page_type": "unknown",
            "next_action": "wait",
            "target_elements": [],
            "form_data": {},
            "reasoning": "AI analysis failed",
            "confidence": 0.0,
            "continue": True
        }
    
    async def _execute_ai_action(self, analysis: Dict[str, Any], current_url: str) -> Dict[str, Any]:
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
            search_query = analysis.get("search_query", "")
            reasoning = analysis.get("reasoning", "")
            confidence = analysis.get("confidence", 0.0)
            
            print(f"🎯 AI Action: {next_action}")
            print(f"   Reasoning: {reasoning}")
            print(f"   Confidence: {confidence:.2f}")
            
            if next_action == "click" and target_elements:
                # Try to click on AI-suggested elements
                for element in target_elements:
                    if await self.browser.click_element(element):
                        print(f"✅ Clicked element: {element}")
                        return {"success": True, "action": "click", "element": element, "continue": True}
                        
            elif next_action == "fill_form" and form_data:
                # Fill out a form with AI-suggested data
                if await self.browser.fill_form(form_data):
                    print(f"✅ Filled form with data: {list(form_data.keys())}")
                    # Try to submit the form
                    if await self.browser.submit_form():
                        print("✅ Form submitted")
                        return {"success": True, "action": "form_submit", "continue": True}
                    else:
                        return {"success": True, "action": "form_filled", "continue": True}
                        
            elif next_action == "search" and search_query:
                # Perform a search
                search_data = {"q": search_query, "search": search_query}
                if await self.browser.fill_form(search_data):
                    if await self.browser.submit_form():
                        print(f"✅ Searched for: {search_query}")
                        return {"success": True, "action": "search", "query": search_query, "continue": True}
                        
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
                print("⏳ AI suggests waiting...")
                await asyncio.sleep(3)
                return {"success": True, "action": "wait", "continue": True}
                
            elif next_action == "stop":
                print("🛑 AI recommends stopping browsing")
                return {"success": True, "action": "stop", "continue": False}
            
            # If no specific action worked, try to find and click common elements
            return await self._try_smart_actions(analysis)
            
        except Exception as e:
            print(f"❌ Error executing AI action: {e}")
            return {"success": False, "error": str(e), "continue": False}
    
    async def _try_smart_actions(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Try smart actions based on AI analysis.
        
        Args:
            analysis: AI analysis of the current page
            
        Returns:
            Result of the action attempt
        """
        try:
            page_type = analysis.get("page_type", "unknown")
            target_elements = analysis.get("target_elements", [])
            
            # Try the AI-suggested elements first
            for element in target_elements:
                if await self.browser.click_element(element):
                    print(f"✅ Clicked AI-suggested element: {element}")
                    return {"success": True, "action": "click", "element": element, "continue": True}
            
            # Fallback to common actions based on page type
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
                    print(f"✅ Clicked fallback element: {selector}")
                    return {"success": True, "action": "click", "element": selector, "continue": True}
            
            # Default: wait and continue
            print("⏳ No actionable elements found, waiting...")
            await asyncio.sleep(3)
            return {"success": True, "action": "wait", "continue": True}
            
        except Exception as e:
            print(f"❌ Error in smart actions: {e}")
            return {"success": False, "error": str(e), "continue": False}
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data."""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError):
            pass
        
        # Fallback: return basic structure if JSON parsing fails
        return {
            "purpose": "Analysis in progress",
            "key_features": [],
            "user_flows": [],
            "registration_required": False,
            "login_flow": {},
            "main_navigation": [],
            "suggested_user_journey": [],
            "interaction_strategy": "Continue exploring"
        }
    
    def _fallback_website_analysis(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Fallback website analysis when AI is not available."""
        return {
            "url": url,
            "description": description,
            "purpose": description or "Website exploration",
            "key_features": ["Web content", "Navigation", "User interaction"],
            "user_flows": ["Browse content", "Navigate", "Interact"],
            "registration_required": False,
            "login_flow": {},
            "main_navigation": ["Home", "About", "Contact"],
            "suggested_user_journey": ["Visit homepage", "Explore content", "Look for features"],
            "interaction_strategy": "Explore and interact with available elements"
        }
    
    def _fallback_page_analysis(self, page_content: str, current_url: str, context: str = "") -> Dict[str, Any]:
        """Fallback page analysis when AI is not available."""
        content_lower = page_content.lower()
        
        if "login" in content_lower or "sign in" in content_lower:
            return {
                "page_type": "login",
                "next_action": "fill_form",
                "target_elements": ['input[name="email"]', 'input[name="username"]', 'input[type="password"]'],
                "form_data": {"email": "demo@example.com", "password": "password123"},
                "reasoning": "Login page detected",
                "confidence": 0.7,
                "continue": True
            }
        elif "search" in content_lower and "input" in content_lower:
            return {
                "page_type": "search",
                "next_action": "search",
                "target_elements": ['input[type="search"]', 'input[name="q"]'],
                "search_query": "artificial intelligence",
                "reasoning": "Search page detected",
                "confidence": 0.6,
                "continue": True
            }
        else:
            return {
                "page_type": "content",
                "next_action": "click",
                "target_elements": ['a', 'button'],
                "reasoning": "General content page",
                "confidence": 0.4,
                "continue": True
            }
    
    def save_session_log(self, filename: str = None) -> str:
        """Save the session log to a file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"dynamic_browsing_session_{timestamp}.json"
            
        log_path = Path(filename)
        with open(log_path, 'w') as f:
            json.dump(self.session_log, f, indent=2)
            
        return str(log_path)
