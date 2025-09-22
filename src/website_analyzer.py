"""
Website analysis module that uses Claude Code SDK to understand website structure and purpose.
"""
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock


class WebsiteAnalyzer:
    """Analyzes websites using Claude Code SDK to understand their structure and purpose."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the website analyzer.
        
        Args:
            api_key: Claude API key (optional, can be set via environment variable)
        """
        self.api_key = api_key
        
    async def analyze_website(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a website to understand its purpose and structure.
        
        Args:
            url: The website URL to analyze
            description: Optional description of what the website is about
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = self._build_analysis_prompt(url, description)
        
        analysis_result = {
            "url": url,
            "description": description,
            "purpose": "",
            "key_features": [],
            "user_flows": [],
            "registration_required": False,
            "login_flow": {},
            "main_navigation": [],
            "suggested_user_journey": []
        }
        
        try:
            # Try to use Claude Code SDK with proper options
            options = ClaudeCodeOptions(
                system_prompt="You are an expert web analyst. Analyze websites to understand their purpose, structure, and user flows.",
                max_turns=1
            )
            
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            # Parse the response and extract structured information
                            analysis_result.update(self._parse_analysis_response(block.text))
                            
        except Exception as e:
            print(f"Error analyzing website with Claude Code SDK: {e}")
            # Fallback to basic analysis without AI
            analysis_result.update(self._fallback_analysis(url, description))
            
        return analysis_result
    
    def _build_analysis_prompt(self, url: str, description: Optional[str] = None) -> str:
        """Build the analysis prompt for Claude."""
        base_prompt = f"""
        Please analyze the website at {url} and provide a comprehensive analysis.
        
        If provided, here's what I know about this website: {description or "No description provided"}
        
        Please analyze the website and provide the following information in a structured format:
        
        1. **Purpose**: What is the main purpose of this website?
        2. **Key Features**: List the main features and functionalities
        3. **User Flows**: Describe the typical user journeys on this site
        4. **Registration Required**: Does the site require user registration?
        5. **Login Flow**: If registration is required, describe the login/signup process
        6. **Main Navigation**: List the main navigation elements and pages
        7. **Suggested User Journey**: Recommend a logical sequence of actions a user should take
        
        Please format your response as JSON with the following structure:
        {{
            "purpose": "string",
            "key_features": ["feature1", "feature2", ...],
            "user_flows": ["flow1", "flow2", ...],
            "registration_required": boolean,
            "login_flow": {{
                "signup_url": "string",
                "login_url": "string",
                "required_fields": ["field1", "field2", ...]
            }},
            "main_navigation": ["nav1", "nav2", ...],
            "suggested_user_journey": ["step1", "step2", ...]
        }}
        """
        return base_prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response and extract structured data."""
        try:
            # Try to extract JSON from the response
            import re
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
            "suggested_user_journey": []
        }
    
    async def get_page_analysis(self, page_content: str, current_url: str, action_taken: str = "") -> Dict[str, Any]:
        """Analyze a specific page to determine next actions.
        
        Args:
            page_content: The HTML content of the current page
            current_url: The URL of the current page
            action_taken: Description of the last action taken
            
        Returns:
            Dictionary with analysis and suggested next actions
        """
        prompt = f"""
        Analyze this webpage and suggest the next action to take.
        
        Current URL: {current_url}
        Last Action: {action_taken or "Initial page load"}
        
        Page Content (first 2000 characters):
        {page_content[:2000]}...
        
        Based on this page content, suggest:
        1. What type of page this is (homepage, login, signup, dashboard, etc.)
        2. What the next logical action should be
        3. Any specific elements to interact with (buttons, forms, links)
        4. Whether we need to fill out forms and what information to provide
        
        Respond in JSON format:
        {{
            "page_type": "string",
            "next_action": "string",
            "target_elements": ["element1", "element2"],
            "form_data": {{"field1": "value1", "field2": "value2"}},
            "confidence": 0.8
        }}
        """
        
        try:
            options = ClaudeCodeOptions(
                system_prompt="You are an expert web automation assistant. Analyze web pages and suggest the next logical action to take.",
                max_turns=1
            )
            
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            return self._parse_analysis_response(block.text)
        except Exception as e:
            print(f"Error analyzing page with Claude Code SDK: {e}")
            # Fallback to basic page analysis
            return self._fallback_page_analysis(page_content, current_url, action_taken)
            
        return {
            "page_type": "unknown",
            "next_action": "wait",
            "target_elements": [],
            "form_data": {},
            "confidence": 0.0
        }
    
    def _fallback_analysis(self, url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Fallback analysis when Claude Code SDK is not available.
        
        Args:
            url: The website URL
            description: Optional description
            
        Returns:
            Basic analysis results
        """
        # Basic analysis based on URL patterns and description
        purpose = "Unknown website"
        key_features = []
        registration_required = False
        
        if description:
            purpose = description
        elif "github.com" in url:
            purpose = "Code hosting and version control platform"
            key_features = ["Repository management", "Code collaboration", "Issue tracking"]
            registration_required = True
        elif "google.com" in url:
            purpose = "Search engine and web services"
            key_features = ["Web search", "Email", "Cloud services"]
            registration_required = False
        elif "example.com" in url:
            purpose = "Example website for testing"
            key_features = ["Basic web content"]
            registration_required = False
        
        return {
            "purpose": purpose,
            "key_features": key_features,
            "user_flows": ["Browse content", "Search", "Navigate"],
            "registration_required": registration_required,
            "login_flow": {},
            "main_navigation": ["Home", "About", "Contact"],
            "suggested_user_journey": ["Visit homepage", "Explore content", "Look for features"]
        }
    
    def _fallback_page_analysis(self, page_content: str, current_url: str, action_taken: str = "") -> Dict[str, Any]:
        """Fallback page analysis when Claude Code SDK is not available.
        
        Args:
            page_content: The HTML content of the current page
            current_url: The URL of the current page
            action_taken: Description of the last action taken
            
        Returns:
            Basic page analysis results
        """
        import re
        
        # Basic page type detection
        page_type = "unknown"
        next_action = "wait"
        target_elements = []
        form_data = {}
        confidence = 0.3
        
        # Detect page type based on content patterns
        content_lower = page_content.lower()
        
        if "login" in content_lower or "sign in" in content_lower:
            page_type = "login"
            next_action = "fill_form"
            target_elements = ['input[name="email"]', 'input[name="username"]', 'input[type="password"]']
            form_data = {"email": "demo@example.com", "password": "password123"}
            confidence = 0.7
            
        elif "signup" in content_lower or "register" in content_lower or "create account" in content_lower:
            page_type = "signup"
            next_action = "fill_form"
            target_elements = ['input[name="email"]', 'input[name="password"]', 'input[name="first_name"]']
            form_data = {"email": "demo@example.com", "password": "password123", "first_name": "Demo"}
            confidence = 0.7
            
        elif "search" in content_lower and "input" in content_lower:
            page_type = "search"
            next_action = "click"
            target_elements = ['input[type="search"]', 'input[name="q"]', 'button[type="submit"]']
            confidence = 0.6
            
        elif "form" in content_lower:
            page_type = "form"
            next_action = "fill_form"
            target_elements = ['form input', 'form textarea', 'form select']
            confidence = 0.5
            
        elif "button" in content_lower or "link" in content_lower:
            page_type = "navigation"
            next_action = "click"
            target_elements = ['a', 'button', 'input[type="submit"]']
            confidence = 0.4
            
        else:
            page_type = "content"
            next_action = "click"
            target_elements = ['a', 'button']
            confidence = 0.3
        
        return {
            "page_type": page_type,
            "next_action": next_action,
            "target_elements": target_elements,
            "form_data": form_data,
            "confidence": confidence
        }
