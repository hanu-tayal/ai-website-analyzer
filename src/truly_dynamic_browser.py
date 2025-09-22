"""
Truly dynamic browser that analyzes page content and discovers actionable steps in real-time.
No predetermined patterns - everything is based on actual page analysis.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import time
import re
from urllib.parse import urlparse, urljoin

from .browser_automation import BrowserAutomation


class TrulyDynamicBrowser:
    """Truly dynamic browser that discovers actionable steps from page content."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000):
        """Initialize the truly dynamic browser.
        
        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Delay between actions in milliseconds
        """
        self.browser = BrowserAutomation(headless=headless, slow_mo=slow_mo)
        self.session_log = []
        self.browsing_context = {
            "visited_urls": set(),
            "discovered_actions": [],
            "session_start": time.time(),
            "tried_actions": set(),  # Track actions we've already tried
            "action_history": [],    # Track action history to detect loops
            "consecutive_same_actions": 0,  # Track consecutive identical actions
        }
        
    async def start(self) -> None:
        """Start the browser and initialize the session."""
        await self.browser.start_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_started",
            "details": "Truly dynamic browser automation started"
        })
        
    async def close(self) -> None:
        """Close the browser and cleanup resources."""
        await self.browser.close_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_closed",
            "details": "Truly dynamic browser automation stopped"
        })
        
    async def analyze_and_browse(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website and begin truly dynamic browsing.
        
        Args:
            url: The website URL to browse
            description: Optional description of the website
            
        Returns:
            Dictionary containing browsing results and analysis
        """
        try:
            # Step 1: Navigate to the website
            print(f"🌐 Navigating to: {url}")
            page_info = await self.browser.navigate_to(url)
            
            if 'error' in page_info:
                return {
                    "success": False,
                    "error": f"Failed to navigate to {url}: {page_info['error']}",
                }
            
            # Add to visited URLs
            self.browsing_context["visited_urls"].add(url)
            
            # Step 2: Begin truly dynamic browsing
            print("🤖 Starting truly dynamic browsing...")
            browsing_results = await self._truly_dynamic_browsing_loop()
            
            return {
                "success": True,
                "browsing_results": browsing_results,
                "session_log": self.session_log,
                "discovered_actions": self.browsing_context["discovered_actions"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "session_log": self.session_log
            }
    
    async def _truly_dynamic_browsing_loop(self, max_steps: int = 30) -> List[Dict[str, Any]]:
        """Main truly dynamic browsing loop that discovers actions from page content.
        
        Args:
            max_steps: Maximum number of steps to take
            
        Returns:
            List of actions taken during browsing
        """
        actions_taken = []
        step_count = 0
        consecutive_failures = 0
        
        while step_count < max_steps and consecutive_failures < 5:
            try:
                # Get current page information
                current_url = await self.browser.get_current_url()
                page_content = await self.browser.get_page_content()
                
                # Discover all possible actions from the page content
                print(f"🔍 Discovering actions on page {step_count + 1}: {current_url}")
                discovered_actions = await self._discover_page_actions(page_content, current_url)
                
                # Log the discovered actions
                self.session_log.append({
                    "timestamp": time.time(),
                    "action": "action_discovery",
                    "url": current_url,
                    "discovered_actions": discovered_actions
                })
                
                # Choose the best action from discovered options
                chosen_action = self._choose_best_action(discovered_actions, step_count)
                
                # Execute the chosen action
                action_result = await self._execute_discovered_action(chosen_action, current_url)
                actions_taken.append({
                    "step": step_count + 1,
                    "url": current_url,
                    "discovered_actions": discovered_actions,
                    "chosen_action": chosen_action,
                    "action_result": action_result
                })
                
                # Track failures
                if action_result.get("success", False):
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                
                # Check if we should continue
                if not action_result.get("continue", True):
                    print("🛑 No more viable actions found")
                    break
                
                # Add to visited URLs
                self.browsing_context["visited_urls"].add(current_url)
                
                # Reset consecutive same actions if we successfully navigated to a new page
                if action_result.get("success", False) and action_result.get("action") == "click":
                    new_url = await self.browser.get_current_url()
                    if new_url != current_url:
                        print("🆕 Successfully navigated to new page - resetting action tracking")
                        self.browsing_context["consecutive_same_actions"] = 0
                    
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
                consecutive_failures += 1
                break
                
        return actions_taken
    
    async def _discover_page_actions(self, page_content: str, current_url: str) -> List[Dict[str, Any]]:
        """Discover all possible actions from page content.
        
        Args:
            page_content: The HTML content of the current page
            current_url: The URL of the current page
            
        Returns:
            List of discovered actions with details
        """
        actions = []
        
        try:
            # Extract all interactive elements
            interactive_elements = self._extract_interactive_elements(page_content)
            
            # Discover clickable elements
            clickable_actions = self._discover_clickable_actions(interactive_elements, current_url)
            actions.extend(clickable_actions)
            
            # Discover form actions
            form_actions = self._discover_form_actions(interactive_elements, current_url)
            actions.extend(form_actions)
            
            # Discover navigation actions
            nav_actions = self._discover_navigation_actions(interactive_elements, current_url)
            actions.extend(nav_actions)
            
            # Discover search actions
            search_actions = self._discover_search_actions(interactive_elements, current_url)
            actions.extend(search_actions)
            
            # Discover content exploration actions
            content_actions = self._discover_content_actions(interactive_elements, current_url)
            actions.extend(content_actions)
            
            # Store discovered actions
            self.browsing_context["discovered_actions"].extend(actions)
            
            print(f"   Found {len(actions)} possible actions:")
            for i, action in enumerate(actions[:5], 1):  # Show first 5
                print(f"     {i}. {action['type']}: {action['description']}")
            if len(actions) > 5:
                print(f"     ... and {len(actions) - 5} more actions")
            
            return actions
            
        except Exception as e:
            print(f"Error discovering actions: {e}")
            return []
    
    def _extract_interactive_elements(self, page_content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all interactive elements from page content."""
        elements = {
            "links": [],
            "buttons": [],
            "forms": [],
            "inputs": [],
            "selects": [],
            "textareas": []
        }
        
        try:
            # Extract links
            link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
            links = re.findall(link_pattern, page_content, re.IGNORECASE | re.DOTALL)
            for href, text in links:
                if href and text.strip():
                    # Clean HTML entities
                    clean_href = href.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                    clean_text = re.sub(r'<[^>]+>', '', text).strip()  # Remove HTML tags from text
                    
                    if clean_text:  # Only add if there's actual text content
                        elements["links"].append({
                            "href": clean_href,
                            "text": clean_text,
                            "selector": f'a[href="{clean_href}"]'
                        })
            
            # Extract buttons
            button_pattern = r'<button[^>]*>(.*?)</button>'
            buttons = re.findall(button_pattern, page_content, re.IGNORECASE | re.DOTALL)
            for i, text in enumerate(buttons):
                if text.strip():
                    # Clean HTML tags and entities from button text
                    clean_text = re.sub(r'<[^>]+>', '', text).strip()  # Remove HTML tags
                    clean_text = clean_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                    
                    # Only add if there's meaningful text (not just HTML)
                    if clean_text and len(clean_text) < 100:  # Reasonable length
                        elements["buttons"].append({
                            "text": clean_text,
                            "selector": f'button:has-text("{clean_text}")',
                            "index": i
                        })
            
            # Extract input elements
            input_pattern = r'<input[^>]*>'
            inputs = re.findall(input_pattern, page_content, re.IGNORECASE)
            for i, input_tag in enumerate(inputs):
                input_type = self._extract_attribute(input_tag, "type") or "text"
                input_name = self._extract_attribute(input_tag, "name") or f"input_{i}"
                input_placeholder = self._extract_attribute(input_tag, "placeholder") or ""
                
                elements["inputs"].append({
                    "type": input_type,
                    "name": input_name,
                    "placeholder": input_placeholder,
                    "selector": f'input[name="{input_name}"]' if input_name else f'input:nth-of-type({i+1})'
                })
            
            # Extract forms
            form_pattern = r'<form[^>]*>(.*?)</form>'
            forms = re.findall(form_pattern, page_content, re.IGNORECASE | re.DOTALL)
            for i, form_content in enumerate(forms):
                form_action = self._extract_attribute(f'<form {form_content}>', "action") or ""
                form_method = self._extract_attribute(f'<form {form_content}>', "method") or "get"
                
                elements["forms"].append({
                    "action": form_action,
                    "method": form_method,
                    "content": form_content,
                    "selector": f'form:nth-of-type({i+1})'
                })
            
            # Extract select elements
            select_pattern = r'<select[^>]*>(.*?)</select>'
            selects = re.findall(select_pattern, page_content, re.IGNORECASE | re.DOTALL)
            for i, select_content in enumerate(selects):
                select_name = self._extract_attribute(f'<select {select_content}>', "name") or f"select_{i}"
                elements["selects"].append({
                    "name": select_name,
                    "content": select_content,
                    "selector": f'select[name="{select_name}"]'
                })
            
            # Extract textareas
            textarea_pattern = r'<textarea[^>]*>(.*?)</textarea>'
            textareas = re.findall(textarea_pattern, page_content, re.IGNORECASE | re.DOTALL)
            for i, textarea_content in enumerate(textareas):
                textarea_name = self._extract_attribute(f'<textarea {textarea_content}>', "name") or f"textarea_{i}"
                elements["textareas"].append({
                    "name": textarea_name,
                    "content": textarea_content,
                    "selector": f'textarea[name="{textarea_name}"]'
                })
            
        except Exception as e:
            print(f"Error extracting interactive elements: {e}")
        
        return elements
    
    def _extract_attribute(self, tag: str, attribute: str) -> Optional[str]:
        """Extract attribute value from HTML tag."""
        pattern = rf'{attribute}=["\']([^"\']*)["\']'
        match = re.search(pattern, tag, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _create_robust_selectors(self, href: str, text: str) -> List[str]:
        """Create multiple robust selector options for an element."""
        selectors = []
        
        # Clean the href for better matching
        clean_href = href.replace("&amp;", "&")
        
        # Skip accessibility elements that are not meant to be clicked
        if any(skip_word in text.lower() for skip_word in ["jump to", "skip to", "skip content", "skip navigation"]):
            return []  # Don't create selectors for accessibility skip links
        
        # 1. Text-based selector (most reliable)
        if text and len(text.strip()) > 0 and len(text.strip()) < 50:
            # Clean and escape text for CSS selector
            clean_text = text.strip()
            clean_text = re.sub(r'<[^>]+>', '', clean_text)  # Remove HTML tags
            clean_text = clean_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            clean_text = clean_text.replace('"', '\\"').replace("'", "\\'")
            
            # Only use if it's reasonable text
            if clean_text and len(clean_text) < 50 and not any(char in clean_text for char in ['<', '>', '{', '}']):
                selectors.append(f'a:has-text("{clean_text}")')
        
        # 2. Partial href match
        if clean_href:
            # Try exact href match
            selectors.append(f'a[href="{clean_href}"]')
            # Try partial href match
            if "/" in clean_href:
                href_parts = clean_href.split("/")
                if len(href_parts) > 1:
                    domain_part = href_parts[2] if len(href_parts) > 2 else href_parts[1]
                    selectors.append(f'a[href*="{domain_part}"]')
        
        # 3. Generic link selectors (only for meaningful links)
        if clean_href and not clean_href.startswith("#"):
            selectors.append('a[href]')
        
        # 4. Text-based fallbacks for important links
        if text and any(word in text.lower() for word in ["about", "contact", "home", "login", "sign", "products", "news", "company"]):
            selectors.append(f'a:has-text("{text[:20]}")')  # First 20 chars
        
        return selectors
    
    def _discover_clickable_actions(self, elements: Dict[str, List[Dict[str, Any]]], current_url: str) -> List[Dict[str, Any]]:
        """Discover clickable actions from page elements."""
        actions = []
        
        # Process links
        for link in elements["links"]:
            href = link["href"]
            text = link["text"]
            
            # Create more robust selectors
            selectors = self._create_robust_selectors(href, text)
            
            # Determine action type based on href
            if href.startswith("http"):
                action_type = "navigate_external"
                description = f"Navigate to external link: {text} -> {href}"
            elif href.startswith("/") or href.startswith("#"):
                action_type = "navigate_internal"
                description = f"Navigate to internal link: {text} -> {href}"
            else:
                action_type = "navigate_relative"
                description = f"Navigate to relative link: {text} -> {href}"
            
            # Only add action if we have valid selectors
            if selectors:
                actions.append({
                    "type": action_type,
                    "action": "click",
                    "selectors": selectors,  # Multiple selector options
                    "description": description,
                    "target_url": href,
                    "confidence": 0.8,
                    "priority": 1 if "home" in text.lower() or "main" in text.lower() else 2
                })
        
        # Process buttons
        for button in elements["buttons"]:
            text = button["text"]
            selector = button["selector"]
            
            # Determine action type based on button text
            if any(word in text.lower() for word in ["submit", "send", "go", "search"]):
                action_type = "form_submit"
                description = f"Submit form: {text}"
                priority = 1
            elif any(word in text.lower() for word in ["login", "sign in", "enter"]):
                action_type = "authentication"
                description = f"Authentication action: {text}"
                priority = 1
            elif any(word in text.lower() for word in ["sign up", "register", "create"]):
                action_type = "registration"
                description = f"Registration action: {text}"
                priority = 1
            else:
                action_type = "interaction"
                description = f"Interactive button: {text}"
                priority = 3
            
            actions.append({
                "type": action_type,
                "action": "click",
                "selector": selector,
                "description": description,
                "confidence": 0.7,
                "priority": priority
            })
        
        return actions
    
    def _discover_form_actions(self, elements: Dict[str, List[Dict[str, Any]]], current_url: str) -> List[Dict[str, Any]]:
        """Discover form-related actions from page elements."""
        actions = []
        
        # Process forms
        for form in elements["forms"]:
            form_selector = form["selector"]
            form_method = form["method"]
            form_action = form["action"]
            
            # Find inputs within this form
            form_inputs = []
            for input_elem in elements["inputs"]:
                if input_elem["name"]:
                    form_inputs.append(input_elem)
            
            if form_inputs:
                # Determine form type based on input fields
                input_types = [inp["type"] for inp in form_inputs]
                input_names = [inp["name"] for inp in form_inputs]
                
                if "password" in input_types:
                    if "email" in input_names or "username" in input_names:
                        form_type = "login"
                        description = "Fill and submit login form"
                        priority = 1
                    else:
                        form_type = "registration"
                        description = "Fill and submit registration form"
                        priority = 1
                elif "search" in input_types or "q" in input_names:
                    form_type = "search"
                    description = "Perform search"
                    priority = 2
                else:
                    form_type = "general"
                    description = "Fill and submit general form"
                    priority = 3
                
                actions.append({
                    "type": f"form_{form_type}",
                    "action": "fill_and_submit",
                    "selector": form_selector,
                    "description": description,
                    "form_inputs": form_inputs,
                    "confidence": 0.9,
                    "priority": priority
                })
        
        return actions
    
    def _discover_navigation_actions(self, elements: Dict[str, List[Dict[str, Any]]], current_url: str) -> List[Dict[str, Any]]:
        """Discover navigation actions from page elements."""
        actions = []
        
        # Look for navigation patterns
        nav_keywords = ["home", "about", "contact", "services", "products", "blog", "news", "help", "support"]
        
        for link in elements["links"]:
            text = link["text"].lower()
            href = link["href"]
            
            if any(keyword in text for keyword in nav_keywords):
                actions.append({
                    "type": "navigation",
                    "action": "click",
                    "selector": link["selector"],
                    "description": f"Navigate to {link['text']} section",
                    "target_url": href,
                    "confidence": 0.8,
                    "priority": 2
                })
        
        return actions
    
    def _discover_search_actions(self, elements: Dict[str, List[Dict[str, Any]]], current_url: str) -> List[Dict[str, Any]]:
        """Discover search actions from page elements."""
        actions = []
        
        # Look for search inputs
        for input_elem in elements["inputs"]:
            if input_elem["type"] == "search" or "search" in input_elem["name"].lower() or "q" in input_elem["name"].lower():
                actions.append({
                    "type": "search",
                    "action": "search",
                    "selector": input_elem["selector"],
                    "description": f"Perform search using {input_elem['name']} field",
                    "input_name": input_elem["name"],
                    "confidence": 0.9,
                    "priority": 2
                })
        
        return actions
    
    def _discover_content_actions(self, elements: Dict[str, List[Dict[str, Any]]], current_url: str) -> List[Dict[str, Any]]:
        """Discover content exploration actions from page elements."""
        actions = []
        
        # Look for content-related links
        content_keywords = ["read more", "learn more", "details", "view", "see", "explore", "discover"]
        
        for link in elements["links"]:
            text = link["text"].lower()
            href = link["href"]
            
            if any(keyword in text for keyword in content_keywords):
                actions.append({
                    "type": "content_exploration",
                    "action": "click",
                    "selector": link["selector"],
                    "description": f"Explore content: {link['text']}",
                    "target_url": href,
                    "confidence": 0.7,
                    "priority": 3
                })
        
        return actions
    
    def _choose_best_action(self, discovered_actions: List[Dict[str, Any]], step_count: int) -> Optional[Dict[str, Any]]:
        """Choose the best action from discovered options."""
        if not discovered_actions:
            return None
        
        # Filter out actions we've already tried
        available_actions = []
        for action in discovered_actions:
            action_key = f"{action.get('type', '')}_{action.get('target_url', '')}_{action.get('description', '')}"
            
            # Skip if we've tried this exact action before
            if action_key in self.browsing_context["tried_actions"]:
                continue
                
            # Skip if this action would create a loop
            if self._would_create_loop(action, step_count):
                continue
                
            available_actions.append(action)
        
        if not available_actions:
            print("🛑 No new actions available - all actions have been tried or would create loops")
            return None
        
        # Sort by priority and confidence
        available_actions.sort(key=lambda x: (x.get("priority", 5), -x.get("confidence", 0)))
        
        # Choose the best action
        chosen_action = available_actions[0]
        action_key = f"{chosen_action.get('type', '')}_{chosen_action.get('target_url', '')}_{chosen_action.get('description', '')}"
        
        # Mark as tried
        self.browsing_context["tried_actions"].add(action_key)
        self.browsing_context["action_history"].append({
            "step": step_count,
            "action": chosen_action,
            "timestamp": time.time()
        })
        
        # Check for consecutive same actions
        if (len(self.browsing_context["action_history"]) >= 2 and 
            self.browsing_context["action_history"][-1]["action"]["description"] == 
            self.browsing_context["action_history"][-2]["action"]["description"]):
            self.browsing_context["consecutive_same_actions"] += 1
        else:
            self.browsing_context["consecutive_same_actions"] = 0
        
        print(f"🎯 Chosen action: {chosen_action['description']}")
        print(f"   Type: {chosen_action['type']}")
        print(f"   Confidence: {chosen_action.get('confidence', 0):.2f}")
        print(f"   Priority: {chosen_action.get('priority', 5)}")
        print(f"   Consecutive same actions: {self.browsing_context['consecutive_same_actions']}")
        
        return chosen_action
    
    def _would_create_loop(self, action: Dict[str, Any], step_count: int) -> bool:
        """Check if an action would create a loop."""
        # Check for consecutive same actions
        if self.browsing_context["consecutive_same_actions"] >= 3:
            print(f"🔄 Loop detected: {self.browsing_context['consecutive_same_actions']} consecutive same actions")
            return True
        
        # Check if we've visited this URL recently
        target_url = action.get("target_url", "")
        if target_url and target_url in self.browsing_context["visited_urls"]:
            # Check if we visited it in the last 3 steps
            recent_steps = self.browsing_context["action_history"][-3:]
            for step in recent_steps:
                if step["action"].get("target_url") == target_url:
                    print(f"🔄 Loop detected: Would revisit URL {target_url}")
                    return True
        
        # Check for action repetition pattern
        if len(self.browsing_context["action_history"]) >= 4:
            recent_actions = [step["action"]["description"] for step in self.browsing_context["action_history"][-4:]]
            if len(set(recent_actions)) <= 2:  # Only 2 unique actions in last 4 steps
                print(f"🔄 Loop detected: Repetitive action pattern")
                return True
        
        return False
    
    async def _execute_discovered_action(self, action: Dict[str, Any], current_url: str) -> Dict[str, Any]:
        """Execute a discovered action."""
        if not action:
            return {"success": False, "error": "No action to execute", "continue": False}
        
        try:
            action_type = action.get("type", "")
            action_method = action.get("action", "")
            selector = action.get("selector", "")
            
            if action_method == "click":
                # Try multiple selectors if available
                selectors_to_try = action.get("selectors", [selector])
                
                for i, sel in enumerate(selectors_to_try):
                    try:
                        if await self.browser.click_element(sel):
                            print(f"✅ Successfully clicked: {action['description']} (selector {i+1})")
                            return {"success": True, "action": "click", "continue": True}
                    except Exception as e:
                        print(f"   Selector {i+1} failed: {e}")
                        continue
                
                print(f"❌ Failed to click: {action['description']} (tried {len(selectors_to_try)} selectors)")
                return {"success": False, "error": "All selectors failed", "continue": True}
            
            elif action_method == "fill_and_submit":
                form_inputs = action.get("form_inputs", [])
                form_data = {}
                
                # Generate appropriate form data based on input types
                for input_elem in form_inputs:
                    input_name = input_elem["name"]
                    input_type = input_elem["type"]
                    
                    if input_type == "email":
                        form_data[input_name] = "demo@example.com"
                    elif input_type == "password":
                        form_data[input_name] = "password123"
                    elif input_type == "search" or "search" in input_name.lower():
                        form_data[input_name] = "artificial intelligence"
                    elif input_type == "text":
                        if "name" in input_name.lower():
                            form_data[input_name] = "Demo User"
                        elif "message" in input_name.lower():
                            form_data[input_name] = "Hello from AI browser"
                        else:
                            form_data[input_name] = "demo"
                    else:
                        form_data[input_name] = "demo"
                
                if await self.browser.fill_form(form_data):
                    if await self.browser.submit_form():
                        print(f"✅ Successfully filled and submitted form: {action['description']}")
                        return {"success": True, "action": "form_submit", "continue": True}
                    else:
                        print(f"✅ Filled form but couldn't submit: {action['description']}")
                        return {"success": True, "action": "form_filled", "continue": True}
                else:
                    print(f"❌ Failed to fill form: {action['description']}")
                    return {"success": False, "error": "Form fill failed", "continue": True}
            
            elif action_method == "search":
                input_name = action.get("input_name", "q")
                search_data = {input_name: "artificial intelligence"}
                
                if await self.browser.fill_form(search_data):
                    if await self.browser.submit_form():
                        print(f"✅ Successfully performed search: {action['description']}")
                        return {"success": True, "action": "search", "continue": True}
                    else:
                        print(f"✅ Filled search but couldn't submit: {action['description']}")
                        return {"success": True, "action": "search_filled", "continue": True}
                else:
                    print(f"❌ Failed to fill search: {action['description']}")
                    return {"success": False, "error": "Search fill failed", "continue": True}
            
            else:
                print(f"❌ Unknown action method: {action_method}")
                return {"success": False, "error": "Unknown action method", "continue": True}
                
        except Exception as e:
            print(f"❌ Error executing action: {e}")
            return {"success": False, "error": str(e), "continue": True}
    
    def save_session_log(self, filename: str = None) -> str:
        """Save the session log to a file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"browsing_session_{timestamp}.json"
            
        log_path = Path(filename)
        with open(log_path, 'w') as f:
            json.dump({
                "session_log": self.session_log,
                "browsing_context": {
                    "visited_urls": list(self.browsing_context["visited_urls"]),
                    "discovered_actions": self.browsing_context["discovered_actions"],
                    "action_history": self.browsing_context["action_history"],
                    "session_start": self.browsing_context["session_start"]
                }
            }, f, indent=2)
            
        return str(log_path)
