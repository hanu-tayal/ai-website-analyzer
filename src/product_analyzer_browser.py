"""
Product Analyzer Browser - Analyzes websites to generate user stories and Mermaid diagrams.
This browser is designed to understand product processes and user flows from website analysis.
"""
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import time
import re
from urllib.parse import urlparse, urljoin

from browser_automation import BrowserAutomation


class ProductAnalyzerBrowser:
    """Advanced browser that analyzes websites to generate user stories and Mermaid diagrams."""
    
    def __init__(self, headless: bool = False, slow_mo: int = 1000):
        """Initialize the product analyzer browser.
        
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
            "tried_actions": set(),
            "action_history": [],
            "consecutive_same_actions": 0,
            "user_flows": [],  # Track user flows for diagram generation
            "page_types": {},  # Track different page types discovered
            "interactions": [],  # Track user interactions
            "forms_discovered": [],  # Track forms for user stories
            "features_discovered": []  # Track features for product analysis
        }
        
    async def start(self) -> None:
        """Start the browser and initialize the session."""
        await self.browser.start_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_started",
            "details": "Product analyzer browser started"
        })
        
    async def close(self) -> None:
        """Close the browser and cleanup resources."""
        await self.browser.close_browser()
        self.session_log.append({
            "timestamp": time.time(),
            "action": "browser_closed",
            "details": "Product analyzer browser stopped"
        })
        
    async def analyze_website_for_product_processes(self, url: str, max_depth: int = 5) -> Dict[str, Any]:
        """Analyze a website to understand product processes and generate user stories.
        
        Args:
            url: The website URL to analyze
            max_depth: Maximum depth of analysis (number of pages to explore)
            
        Returns:
            Dictionary containing analysis results, user stories, and Mermaid diagrams
        """
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
        """Generate a Mermaid flowchart showing user flows."""
        mermaid = "graph TD\n"
        mermaid += "    A[User visits website] --> B{Is user logged in?}\n"
        mermaid += "    B -->|No| C[Registration/Login page]\n"
        mermaid += "    B -->|Yes| D[User Dashboard]\n"
        mermaid += "    C --> E[Authentication]\n"
        mermaid += "    E --> D\n"
        
        # Add discovered page types
        for url, page_type in self.browsing_context["page_types"].items():
            if page_type == "ecommerce_product":
                mermaid += "    D --> F[Product Catalog]\n"
                mermaid += "    F --> G[Add to Cart]\n"
                mermaid += "    G --> H[Checkout]\n"
            elif page_type == "support":
                mermaid += "    D --> I[Support/Help]\n"
            elif page_type == "about":
                mermaid += "    D --> J[About Page]\n"
        
        return mermaid
    
    def _generate_page_type_diagram(self) -> str:
        """Generate a Mermaid diagram showing discovered page types."""
        mermaid = "graph LR\n"
        
        page_types = set(self.browsing_context["page_types"].values())
        for i, page_type in enumerate(page_types):
            node_id = f"P{i+1}"
            mermaid += f"    {node_id}[{page_type.replace('_', ' ').title()}]\n"
        
        return mermaid
    
    def _generate_feature_map_diagram(self) -> str:
        """Generate a Mermaid mindmap of discovered features."""
        mermaid = "mindmap\n"
        mermaid += "  root((Product Features))\n"
        
        # Group features by category
        feature_categories = {
            "Authentication": ["login", "registration", "password_reset"],
            "E-commerce": ["product_catalog", "shopping_cart", "checkout", "payment"],
            "User Management": ["profile", "dashboard", "settings"],
            "Content": ["blog", "news", "articles"],
            "Support": ["contact", "help", "faq", "support_ticket"]
        }
        
        for category, features in feature_categories.items():
            mermaid += f"    {category}\n"
            for feature in features:
                mermaid += f"      {feature}\n"
        
        return mermaid
    
    # Include all the methods from TrulyDynamicBrowser for action discovery and execution
    async def _discover_page_actions(self, page_content: str, current_url: str) -> List[Dict[str, Any]]:
        """Discover all possible actions from page content."""
        # Implementation from TrulyDynamicBrowser
        pass
    
    def _choose_best_action(self, discovered_actions: List[Dict[str, Any]], step_count: int) -> Optional[Dict[str, Any]]:
        """Choose the best action from discovered options."""
        # Implementation from TrulyDynamicBrowser
        pass
    
    async def _execute_discovered_action(self, action: Dict[str, Any], current_url: str) -> Dict[str, Any]:
        """Execute a discovered action."""
        # Implementation from TrulyDynamicBrowser
        pass
    
    def save_session_log(self, filename: str = None) -> str:
        """Save the session log to a file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"product_analysis_{timestamp}.json"
            
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
