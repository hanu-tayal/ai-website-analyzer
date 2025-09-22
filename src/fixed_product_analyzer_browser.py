"""
Fixed Product Analyzer Browser - Properly implements page navigation and action discovery.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import time
import re
from urllib.parse import urlparse, urljoin

from browser_automation import BrowserAutomation


class FixedProductAnalyzerBrowser:
    """Fixed browser that properly analyzes websites and navigates between pages."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000):
        """Initialize the fixed product analyzer browser."""
        self.browser = BrowserAutomation(headless=headless, slow_mo=slow_mo)
        self.session_log = []
        self.browsing_context = {
            "visited_urls": set(),
            "discovered_actions": [],
            "session_start": time.time(),
            "tried_actions": set(),
            "action_history": [],
            "consecutive_same_actions": 0,
            "user_flows": [],
            "page_types": {},
            "interactions": [],
            "forms_discovered": [],
            "features_discovered": []
        }
        
    async def start(self) -> None:
        """Start the browser and initialize the session."""
        await self.browser.start_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_started",
            "details": "Fixed product analyzer browser started"
        })
        
    async def close(self) -> None:
        """Close the browser and cleanup resources."""
        await self.browser.close_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_closed",
            "details": "Fixed product analyzer browser stopped"
        })
        
    async def analyze_website_for_product_processes(self, url: str, max_depth: int = 5) -> Dict[str, Any]:
        """Analyze a website to understand product processes and generate user stories."""
        try:
            print(f"🔍 Starting product analysis of: {url}")
            print(f"📊 Max depth: {max_depth} pages")
            
            # Step 1: Navigate to the website
            page_info = await self.browser.navigate_to(url)
            
            if 'error' in page_info:
                return {
                    "success": False,
                    "error": f"Failed to navigate to {url}: {page_info['error']}",
                }
            
            # Step 2: Begin comprehensive analysis
            print("🤖 Starting comprehensive product analysis...")
            analysis_results = await self._comprehensive_analysis_loop(max_depth)
            
            # Step 3: Generate user stories and diagrams
            print("📝 Generating user stories and Mermaid diagrams...")
            user_stories = self._generate_user_stories()
            mermaid_diagrams = self._generate_mermaid_diagrams()
            
            return {
                "success": True,
                "analysis_results": analysis_results,
                "user_stories": user_stories,
                "mermaid_diagrams": mermaid_diagrams,
                "session_log": self.session_log,
                "browsing_context": self.browsing_context
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "session_log": self.session_log
            }
    
    async def _comprehensive_analysis_loop(self, max_depth: int) -> List[Dict[str, Any]]:
        """Comprehensive analysis loop that explores the website in detail."""
        analysis_steps = []
        step_count = 0
        consecutive_failures = 0
        
        while step_count < max_depth and consecutive_failures < 3:
            try:
                # Get current page information
                current_url = await self.browser.get_current_url()
                page_content = await self.browser.get_page_content()
                
                print(f"🔍 Analyzing page {step_count + 1}: {current_url}")
                
                # Comprehensive page analysis
                page_analysis = await self._analyze_page_comprehensively(page_content, current_url)
                
                # Discover and categorize actions
                discovered_actions = await self._discover_page_actions(page_content, current_url)
                
                # Choose the best action for exploration
                chosen_action = self._choose_best_action(discovered_actions, step_count)
                
                # Execute the chosen action
                action_result = await self._execute_discovered_action(chosen_action, current_url)
                
                # Record analysis step
                analysis_steps.append({
                    "step": step_count + 1,
                    "url": current_url,
                    "page_analysis": page_analysis,
                    "discovered_actions": discovered_actions,
                    "chosen_action": chosen_action,
                    "action_result": action_result
                })
                
                # Track failures
                if action_result.get("success", False):
                    consecutive_failures = 0
                    # Reset consecutive same actions if we successfully navigated to a new page
                    if action_result.get("action") == "click":
                        new_url = await self.browser.get_current_url()
                        if new_url != current_url:
                            print("🆕 Successfully navigated to new page - resetting action tracking")
                            self.browsing_context["consecutive_same_actions"] = 0
                else:
                    consecutive_failures += 1
                
                # Check if we should continue
                if not action_result.get("continue", True):
                    print("🛑 Analysis complete - no more viable actions found")
                    break
                
                # Add to visited URLs
                self.browsing_context["visited_urls"].add(current_url)
                    
                # Wait before next step
                await asyncio.sleep(2)
                step_count += 1
                
            except Exception as e:
                print(f"❌ Error in analysis step {step_count + 1}: {e}")
                analysis_steps.append({
                    "step": step_count + 1,
                    "error": str(e),
                    "action_result": {"continue": False}
                })
                consecutive_failures += 1
                break
                
        return analysis_steps
    
    async def _analyze_page_comprehensively(self, page_content: str, current_url: str) -> Dict[str, Any]:
        """Comprehensive analysis of a page to understand its purpose and features."""
        analysis = {
            "url": current_url,
            "page_type": self._classify_page_type(page_content, current_url),
            "features": self._extract_features(page_content),
            "forms": self._extract_forms(page_content),
            "navigation": self._extract_navigation(page_content),
            "content_sections": self._extract_content_sections(page_content),
            "user_interactions": self._identify_user_interactions(page_content),
            "business_goals": self._infer_business_goals(page_content, current_url)
        }
        
        # Store page type for diagram generation
        self.browsing_context["page_types"][current_url] = analysis["page_type"]
        
        # Store features for diagram generation
        if analysis["features"]:
            self.browsing_context["features_discovered"].append(analysis["features"])
        
        return analysis
    
    def _classify_page_type(self, content: str, url: str) -> str:
        """Classify the page type based on content analysis."""
        content_lower = content.lower()
        
        # E-commerce patterns
        if any(word in content_lower for word in ["add to cart", "buy now", "price", "shopping", "checkout", "cart"]):
            return "ecommerce_product"
        elif any(word in content_lower for word in ["login", "sign in", "password", "email"]):
            return "authentication"
        elif any(word in content_lower for word in ["sign up", "register", "create account", "join"]):
            return "registration"
        elif any(word in content_lower for word in ["dashboard", "profile", "account", "settings"]):
            return "user_dashboard"
        elif any(word in content_lower for word in ["about", "company", "team", "mission"]):
            return "about"
        elif any(word in content_lower for word in ["contact", "support", "help", "faq"]):
            return "support"
        elif any(word in content_lower for word in ["blog", "news", "article", "post"]):
            return "content"
        elif any(word in content_lower for word in ["pricing", "plans", "subscription", "billing"]):
            return "pricing"
        elif any(word in content_lower for word in ["api", "documentation", "docs", "endpoint"]):
            return "api_docs"
        else:
            return "general"
    
    def _extract_features(self, content: str) -> List[str]:
        """Extract features and functionality from page content."""
        features = []
        content_lower = content.lower()
        
        # Common web features
        feature_patterns = {
            "search": ["search", "find", "lookup", "query"],
            "filter": ["filter", "sort", "category", "tag"],
            "sharing": ["share", "social", "facebook", "twitter", "linkedin"],
            "notifications": ["notification", "alert", "reminder", "subscribe"],
            "messaging": ["message", "chat", "contact", "support"],
            "file_upload": ["upload", "attach", "file", "document"],
            "payment": ["payment", "billing", "credit card", "paypal", "stripe"],
            "calendar": ["calendar", "schedule", "booking", "appointment"],
            "maps": ["map", "location", "address", "directions"],
            "video": ["video", "youtube", "stream", "play"]
        }
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                features.append(feature)
        
        return features
    
    def _extract_forms(self, content: str) -> List[Dict[str, Any]]:
        """Extract forms and their fields for user story generation."""
        forms = []
        
        # Extract form patterns
        form_pattern = r'<form[^>]*>(.*?)</form>'
        form_matches = re.findall(form_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for i, form_content in enumerate(form_matches):
            form_data = {
                "form_id": i + 1,
                "fields": [],
                "purpose": "unknown"
            }
            
            # Extract input fields
            input_pattern = r'<input[^>]*name=["\']([^"\']*)["\'][^>]*>'
            inputs = re.findall(input_pattern, form_content, re.IGNORECASE)
            
            for input_name in inputs:
                form_data["fields"].append(input_name)
            
            # Determine form purpose
            if any(word in form_content.lower() for word in ["login", "sign in", "password"]):
                form_data["purpose"] = "authentication"
            elif any(word in form_content.lower() for word in ["sign up", "register", "create"]):
                form_data["purpose"] = "registration"
            elif any(word in form_content.lower() for word in ["contact", "message", "inquiry"]):
                form_data["purpose"] = "contact"
            elif any(word in form_content.lower() for word in ["search", "query", "find"]):
                form_data["purpose"] = "search"
            
            forms.append(form_data)
        
        # Store forms for user story generation
        self.browsing_context["forms_discovered"].extend(forms)
        
        return forms
    
    def _extract_navigation(self, content: str) -> List[Dict[str, str]]:
        """Extract navigation elements and their purposes."""
        navigation = []
        
        # Extract navigation links
        nav_pattern = r'<nav[^>]*>(.*?)</nav>'
        nav_matches = re.findall(nav_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for nav_content in nav_matches:
            link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
            links = re.findall(link_pattern, nav_content, re.IGNORECASE | re.DOTALL)
            
            for href, text in links:
                clean_text = re.sub(r'<[^>]+>', '', text).strip()
                if clean_text:
                    navigation.append({
                        "text": clean_text,
                        "href": href,
                        "type": "navigation"
                    })
        
        return navigation
    
    def _extract_content_sections(self, content: str) -> List[str]:
        """Extract main content sections for understanding page structure."""
        sections = []
        
        # Common section patterns
        section_patterns = [
            r'<header[^>]*>(.*?)</header>',
            r'<main[^>]*>(.*?)</main>',
            r'<section[^>]*>(.*?)</section>',
            r'<article[^>]*>(.*?)</article>',
            r'<aside[^>]*>(.*?)</aside>',
            r'<footer[^>]*>(.*?)</footer>'
        ]
        
        for pattern in section_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract text content
                text_content = re.sub(r'<[^>]+>', '', match).strip()
                if text_content and len(text_content) > 20:
                    sections.append(text_content[:100] + "..." if len(text_content) > 100 else text_content)
        
        return sections
    
    def _identify_user_interactions(self, content: str) -> List[str]:
        """Identify possible user interactions on the page."""
        interactions = []
        content_lower = content.lower()
        
        # Common interaction patterns
        interaction_patterns = {
            "click": ["button", "link", "click", "tap"],
            "form_fill": ["input", "textarea", "select", "form"],
            "upload": ["upload", "file", "attach", "browse"],
            "download": ["download", "save", "export"],
            "search": ["search", "filter", "sort"],
            "navigate": ["menu", "navigation", "breadcrumb"],
            "share": ["share", "social", "like", "follow"]
        }
        
        for interaction, keywords in interaction_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                interactions.append(interaction)
        
        return interactions
    
    def _infer_business_goals(self, content: str, url: str) -> List[str]:
        """Infer business goals from page content and URL."""
        goals = []
        content_lower = content.lower()
        
        # Business goal patterns
        if any(word in content_lower for word in ["sell", "buy", "purchase", "price", "cart"]):
            goals.append("revenue_generation")
        if any(word in content_lower for word in ["sign up", "register", "join", "subscribe"]):
            goals.append("user_acquisition")
        if any(word in content_lower for word in ["login", "dashboard", "profile", "account"]):
            goals.append("user_retention")
        if any(word in content_lower for word in ["contact", "support", "help", "faq"]):
            goals.append("customer_support")
        if any(word in content_lower for word in ["blog", "news", "content", "article"]):
            goals.append("content_marketing")
        if any(word in content_lower for word in ["api", "documentation", "developers"]):
            goals.append("developer_engagement")
        
        return goals
    
    async def _discover_page_actions(self, page_content: str, current_url: str) -> List[Dict[str, Any]]:
        """Discover all possible actions from page content."""
        actions = []
        
        try:
            # Extract all interactive elements
            interactive_elements = self._extract_interactive_elements(page_content)
            
            # Discover clickable actions
            clickable_actions = self._discover_clickable_actions(interactive_elements, current_url)
            actions.extend(clickable_actions)
            
            # Discover form actions
            form_actions = self._discover_form_actions(interactive_elements, current_url)
            actions.extend(form_actions)
            
            # Discover navigation actions
            nav_actions = self._discover_navigation_actions(interactive_elements, current_url)
            actions.extend(nav_actions)
            
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
            
        except Exception as e:
            print(f"Error extracting interactive elements: {e}")
        
        return elements
    
    def _extract_attribute(self, tag: str, attribute: str) -> Optional[str]:
        """Extract attribute value from HTML tag."""
        pattern = rf'{attribute}=["\']([^"\']*)["\']'
        match = re.search(pattern, tag, re.IGNORECASE)
        return match.group(1) if match else None
    
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
                # Add dropdown-aware selectors for navigation elements
                dropdown_selectors = self._create_dropdown_selectors(href, text)
                all_selectors = selectors + dropdown_selectors
                
                # Add parent navigation hover actions for dropdown menus
                if any(nav_word in text.lower() for nav_word in ["product", "feature", "solution", "resource", "about", "contact"]):
                    # Add a special action to hover over parent navigation first
                    parent_hover_action = {
                        "type": f"hover_{action_type}",
                        "action": "hover_then_click",
                        "selectors": all_selectors,
                        "description": f"Hover over navigation then click: {text} -> {href}",
                        "target_url": href,
                        "confidence": 0.9,
                        "priority": 1  # Higher priority for navigation elements
                    }
                    actions.append(parent_hover_action)
                
                actions.append({
                    "type": action_type,
                    "action": "click",
                    "selectors": all_selectors,  # Multiple selector options including dropdown-aware ones
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
                selectors = self._create_robust_selectors(href, link["text"])
                if selectors:
                    actions.append({
                        "type": "navigation",
                        "action": "click",
                        "selectors": selectors,
                        "description": f"Navigate to {link['text']} section",
                        "target_url": href,
                        "confidence": 0.8,
                        "priority": 2
                    })
        
        return actions
    
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
    
    def _create_dropdown_selectors(self, href: str, text: str) -> List[str]:
        """Create selectors that work with dropdown menus."""
        selectors = []
        
        # Clean the href for better matching
        clean_href = href.replace("&amp;", "&")
        
        # Skip accessibility elements
        if any(skip_word in text.lower() for skip_word in ["jump to", "skip to", "skip content", "skip navigation"]):
            return []
        
        # 1. Try to find parent navigation elements that might need to be hovered first
        if clean_href and not clean_href.startswith("#"):
            # Look for common navigation patterns
            if any(nav_word in text.lower() for nav_word in ["product", "feature", "solution", "resource", "about", "contact"]):
                # Try parent navigation elements
                selectors.append(f'nav a[href="{clean_href}"]')
                selectors.append(f'[role="navigation"] a[href="{clean_href}"]')
                selectors.append(f'.nav a[href="{clean_href}"]')
                selectors.append(f'.menu a[href="{clean_href}"]')
                selectors.append(f'.dropdown a[href="{clean_href}"]')
                
                # Try to find the parent dropdown trigger
                if "product" in text.lower() or "feature" in text.lower():
                    selectors.append(f'button:has-text("Product") + * a[href="{clean_href}"]')
                    selectors.append(f'[data-testid*="product"] a[href="{clean_href}"]')
                elif "resource" in text.lower():
                    selectors.append(f'button:has-text("Resources") + * a[href="{clean_href}"]')
                    selectors.append(f'[data-testid*="resource"] a[href="{clean_href}"]')
        
        return selectors
    
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
                        # First try normal click
                        if await self.browser.click_element(sel):
                            print(f"✅ Successfully clicked: {action['description']} (selector {i+1})")
                            return {"success": True, "action": "click", "continue": True}
                    except Exception as e:
                        print(f"   Selector {i+1} failed: {e}")
                        
                        # Try force click for hidden elements
                        try:
                            if await self._force_click_element(sel):
                                print(f"✅ Successfully force-clicked: {action['description']} (selector {i+1})")
                                return {"success": True, "action": "force_click", "continue": True}
                        except Exception as force_e:
                            print(f"   Force click {i+1} also failed: {force_e}")
                            
                        # Try hover then click for dropdown elements
                        try:
                            if await self._hover_and_click_element(sel):
                                print(f"✅ Successfully hover-clicked: {action['description']} (selector {i+1})")
                                return {"success": True, "action": "hover_click", "continue": True}
                        except Exception as hover_e:
                            print(f"   Hover-click {i+1} also failed: {hover_e}")
                        
                        continue
                
                print(f"❌ Failed to click: {action['description']} (tried {len(selectors_to_try)} selectors)")
                return {"success": False, "error": "All selectors failed", "continue": True}
            
            elif action_method == "hover_then_click":
                # Try multiple selectors if available
                selectors_to_try = action.get("selectors", [selector])
                
                for i, sel in enumerate(selectors_to_try):
                    try:
                        if await self._hover_and_click_element(sel):
                            print(f"✅ Successfully hover-clicked: {action['description']} (selector {i+1})")
                            return {"success": True, "action": "hover_click", "continue": True}
                    except Exception as e:
                        print(f"   Hover-click selector {i+1} failed: {e}")
                        continue
                
                print(f"❌ Failed to hover-click: {action['description']} (tried {len(selectors_to_try)} selectors)")
                return {"success": False, "error": "All hover-click selectors failed", "continue": True}
            
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
            
            else:
                print(f"❌ Unknown action method: {action_method}")
                return {"success": False, "error": "Unknown action method", "continue": True}
                
        except Exception as e:
            print(f"❌ Error executing action: {e}")
            return {"success": False, "error": str(e), "continue": True}
    
    def _generate_user_stories(self) -> List[Dict[str, Any]]:
        """Generate user stories based on discovered features and interactions."""
        user_stories = []
        
        # Generate stories from forms
        for form in self.browsing_context["forms_discovered"]:
            if form["purpose"] == "authentication":
                user_stories.append({
                    "title": "User Authentication",
                    "story": f"As a user, I want to log in to my account so that I can access personalized features",
                    "acceptance_criteria": [
                        "I can enter my email/username and password",
                        "I can click a login button to authenticate",
                        "I am redirected to my dashboard upon successful login",
                        "I see an error message for invalid credentials"
                    ],
                    "priority": "high",
                    "page_type": "authentication"
                })
            elif form["purpose"] == "registration":
                user_stories.append({
                    "title": "User Registration",
                    "story": f"As a new user, I want to create an account so that I can use the service",
                    "acceptance_criteria": [
                        "I can fill in required registration fields",
                        "I can submit the registration form",
                        "I receive confirmation of successful registration",
                        "I can verify my email address if required"
                    ],
                    "priority": "high",
                    "page_type": "registration"
                })
        
        # Generate stories from page types
        for url, page_type in self.browsing_context["page_types"].items():
            if page_type == "ecommerce_product":
                user_stories.append({
                    "title": "Product Purchase",
                    "story": "As a customer, I want to view product details and add items to cart so that I can make a purchase",
                    "acceptance_criteria": [
                        "I can see product information and pricing",
                        "I can add products to my shopping cart",
                        "I can proceed to checkout",
                        "I can complete the payment process"
                    ],
                    "priority": "high",
                    "page_type": "ecommerce_product"
                })
            elif page_type == "user_dashboard":
                user_stories.append({
                    "title": "Dashboard Access",
                    "story": "As a logged-in user, I want to access my dashboard so that I can manage my account and activities",
                    "acceptance_criteria": [
                        "I can see my personal information",
                        "I can navigate to different sections",
                        "I can update my settings",
                        "I can view my activity history"
                    ],
                    "priority": "medium",
                    "page_type": "user_dashboard"
                })
        
        return user_stories
    
    def _generate_mermaid_diagrams(self) -> Dict[str, str]:
        """Generate Mermaid diagrams for different aspects of the product."""
        diagrams = {}
        
        # User Flow Diagram
        diagrams["user_flow"] = self._generate_user_flow_diagram()
        
        # Page Type Diagram
        diagrams["page_types"] = self._generate_page_type_diagram()
        
        # Feature Map Diagram
        diagrams["feature_map"] = self._generate_feature_map_diagram()
        
        return diagrams
    
    def _generate_user_flow_diagram(self) -> str:
        """Generate a Mermaid flowchart showing user flows based on actual website content."""
        mermaid = "graph TD\n"
        mermaid += "    A[User visits website] --> B{Is user logged in?}\n"
        mermaid += "    B -->|No| C[Registration/Login page]\n"
        mermaid += "    B -->|Yes| D[User Dashboard]\n"
        mermaid += "    C --> E[Authentication]\n"
        mermaid += "    E --> D\n"
        
        # Build flow based on actual discovered page types and actions
        page_flows = {}
        for url, page_type in self.browsing_context["page_types"].items():
            if page_type not in page_flows:
                page_flows[page_type] = []
            page_flows[page_type].append(url)
        
        # Add discovered page flows
        node_counter = 1
        for page_type, urls in page_flows.items():
            if page_type == "ecommerce_product":
                mermaid += "    D --> F[Product Catalog]\n"
                mermaid += "    F --> G[Add to Cart]\n"
                mermaid += "    G --> H[Checkout]\n"
            elif page_type == "authentication":
                mermaid += "    D --> I[Login/Register]\n"
            elif page_type == "support":
                mermaid += "    D --> J[Support/Help]\n"
            elif page_type == "about":
                mermaid += "    D --> K[About Page]\n"
            elif page_type == "pricing":
                mermaid += "    D --> L[Pricing Plans]\n"
            elif page_type == "api_docs":
                mermaid += "    D --> M[API Documentation]\n"
            elif page_type == "content":
                mermaid += "    D --> N[Blog/Content]\n"
            elif page_type == "user_dashboard":
                mermaid += "    D --> O[User Dashboard]\n"
        
        # Add discovered features from actual content
        features = set()
        for analysis in self.browsing_context.get("features_discovered", []):
            features.update(analysis)
        
        if "search" in features:
            mermaid += "    D --> P[Search]\n"
        if "contact" in features:
            mermaid += "    D --> Q[Contact Form]\n"
        if "file_upload" in features:
            mermaid += "    D --> R[File Upload]\n"
        
        return mermaid
    
    def _generate_page_type_diagram(self) -> str:
        """Generate a Mermaid diagram showing discovered page types."""
        mermaid = "graph LR\n"
        
        # Get actual discovered page types
        page_types = set(self.browsing_context["page_types"].values())
        
        if not page_types:
            mermaid += "    P1[General Page]\n"
            return mermaid
        
        # Create nodes for each discovered page type
        for i, page_type in enumerate(sorted(page_types)):
            node_id = f"P{i+1}"
            display_name = page_type.replace('_', ' ').title()
            mermaid += f"    {node_id}[{display_name}]\n"
        
        # Add connections between related page types
        if "authentication" in page_types and "user_dashboard" in page_types:
            mermaid += "    P1 --> P2\n"  # Auth leads to Dashboard
        
        return mermaid
    
    def _generate_feature_map_diagram(self) -> str:
        """Generate a Mermaid mindmap of discovered features."""
        mermaid = "mindmap\n"
        mermaid += "  root((Website Features))\n"
        
        # Collect all discovered features from analysis
        all_features = set()
        for analysis in self.browsing_context.get("features_discovered", []):
            if isinstance(analysis, list):
                all_features.update(analysis)
            elif isinstance(analysis, dict) and "features" in analysis:
                all_features.update(analysis["features"])
        
        # Also collect features from page analysis
        for url, page_type in self.browsing_context["page_types"].items():
            if page_type == "ecommerce_product":
                all_features.update(["product_catalog", "shopping_cart", "checkout", "payment"])
            elif page_type == "authentication":
                all_features.update(["login", "registration", "password_reset"])
            elif page_type == "support":
                all_features.update(["contact", "help", "faq", "support_ticket"])
            elif page_type == "api_docs":
                all_features.update(["api_documentation", "endpoints", "authentication"])
            elif page_type == "pricing":
                all_features.update(["pricing_plans", "subscription", "billing"])
        
        # Group features by category based on what was actually discovered
        feature_categories = {}
        
        # Authentication features
        auth_features = [f for f in all_features if f in ["login", "registration", "password_reset", "authentication"]]
        if auth_features:
            feature_categories["Authentication"] = auth_features
        
        # E-commerce features
        ecommerce_features = [f for f in all_features if f in ["product_catalog", "shopping_cart", "checkout", "payment", "cart", "buy"]]
        if ecommerce_features:
            feature_categories["E-commerce"] = ecommerce_features
        
        # User Management features
        user_features = [f for f in all_features if f in ["profile", "dashboard", "settings", "account", "user_management"]]
        if user_features:
            feature_categories["User Management"] = user_features
        
        # Content features
        content_features = [f for f in all_features if f in ["blog", "news", "articles", "content", "blog", "news"]]
        if content_features:
            feature_categories["Content"] = content_features
        
        # Support features
        support_features = [f for f in all_features if f in ["contact", "help", "faq", "support_ticket", "support", "contact"]]
        if support_features:
            feature_categories["Support"] = support_features
        
        # API features
        api_features = [f for f in all_features if f in ["api_documentation", "endpoints", "api", "documentation", "developers"]]
        if api_features:
            feature_categories["API & Development"] = api_features
        
        # Other discovered features
        other_features = [f for f in all_features if f not in 
                         auth_features + ecommerce_features + user_features + 
                         content_features + support_features + api_features]
        if other_features:
            feature_categories["Other Features"] = other_features
        
        # Generate the mindmap
        for category, features in feature_categories.items():
            mermaid += f"    {category}\n"
            for feature in sorted(features):
                mermaid += f"      {feature.replace('_', ' ').title()}\n"
        
        # If no features were discovered, show a generic structure
        if not feature_categories:
            mermaid += "    General Website\n"
            mermaid += "      Navigation\n"
            mermaid += "      Content\n"
        
        return mermaid
    
    def save_session_log(self, filename: str = None) -> str:
        """Save the session log to a file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"fixed_product_analysis_{timestamp}.json"
            
        log_path = Path(filename)
        with open(log_path, 'w') as f:
            json.dump({
                "session_log": self.session_log,
                "browsing_context": {
                    "visited_urls": list(self.browsing_context["visited_urls"]),
                    "discovered_actions": self.browsing_context["discovered_actions"],
                    "action_history": self.browsing_context["action_history"],
                    "page_types": self.browsing_context["page_types"],
                    "forms_discovered": self.browsing_context["forms_discovered"],
                    "features_discovered": self.browsing_context["features_discovered"],
                    "session_start": self.browsing_context["session_start"]
                }
            }, f, indent=2)
            
        return str(log_path)
    
    async def _force_click_element(self, selector: str) -> bool:
        """Force click an element even if it's hidden."""
        try:
            page = self.browser.page
            element = await page.query_selector(selector)
            if element:
                await element.click(force=True)
                return True
            return False
        except Exception as e:
            print(f"Force click error: {e}")
            return False
    
    async def _hover_and_click_element(self, selector: str) -> bool:
        """Hover over an element then click it (useful for dropdowns)."""
        try:
            page = self.browser.page
            
            # Check if page is still valid
            if not page or page.is_closed():
                print("Page is closed, cannot perform hover-click")
                return False
            
            # First try to find the parent navigation element that might need to be hovered
            parent_selectors = [
                'nav', '[role="navigation"]', '.nav', '.menu', '.dropdown',
                'button:has-text("Product")', 'button:has-text("Resources")',
                '[data-testid*="product"]', '[data-testid*="resource"]'
            ]
            
            # Try to hover over parent elements first
            for parent_selector in parent_selectors:
                try:
                    if page.is_closed():
                        print("Page closed during parent element search")
                        return False
                        
                    parent_element = await page.query_selector(parent_selector)
                    if parent_element:
                        await parent_element.hover()
                        await asyncio.sleep(0.5)  # Wait for dropdown to appear
                        break
                except Exception as e:
                    print(f"Parent hover failed for {parent_selector}: {e}")
                    continue
            
            # Now try to find and click the target element
            if page.is_closed():
                print("Page closed before target element search")
                return False
                
            element = await page.query_selector(selector)
            if element:
                # Try to make it visible first
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(0.2)
                
                # Check if element is now visible
                is_visible = await element.is_visible()
                if is_visible:
                    await element.click()
                    return True
                else:
                    # Try force click as fallback
                    await element.click(force=True)
                    return True
            return False
        except Exception as e:
            print(f"Hover-click error: {e}")
            return False
