"""
AI-Powered Content Analyzer using Claude Code SDK
Provides intelligent analysis of website content, business models, and user journeys
"""
import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re
from urllib.parse import urlparse


try:
    from claude_code_sdk import ClaudeSDKClient
    CLAUDE_AVAILABLE = True
except ImportError:
    print("⚠️ Claude Code SDK not available. Install with: pip install claude-code-sdk")
    CLAUDE_AVAILABLE = False


@dataclass
class BusinessModel:
    """Represents the discovered business model of a website."""
    primary_model: str  # freemium, subscription, marketplace, education, etc.
    revenue_streams: List[str]
    target_audience: List[str]
    value_proposition: str
    conversion_funnels: List[str]
    competitive_advantages: List[str]
    pricing_strategy: str


@dataclass
class WebsitePurpose:
    """Represents the understood purpose and type of a website."""
    primary_purpose: str  # education, ecommerce, saas, content, community, etc.
    secondary_purposes: List[str]
    industry: str
    user_types: List[str]
    key_features: List[str]
    unique_selling_points: List[str]


@dataclass
class UserInsight:
    """Represents insights about user behavior and needs."""
    user_goals: List[str]
    pain_points: List[str]
    user_journey_stages: List[str]
    emotional_drivers: List[str]
    success_metrics: List[str]


class AIContentAnalyzer:
    """AI-powered website content analyzer using Claude Code SDK."""

    def __init__(self):
        """Initialize the AI content analyzer."""
        if not CLAUDE_AVAILABLE:
            raise Exception("Claude Code SDK is not installed. Install with: pip install claude-code-sdk")

        try:
            self.claude = ClaudeSDKClient()
            print("✅ Claude Code SDK initialized")
        except Exception as e:
            print(f"❌ Could not initialize Claude SDK: {e}")
            raise e


    async def analyze_website_intelligence(self, url: str, pages_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive AI analysis of website content."""
        print(f"🧠 Starting AI-powered analysis of {url}")

        # Combine all page content for analysis
        combined_content = self._prepare_content_for_analysis(pages_content)

        return await self._ai_powered_analysis(url, combined_content, pages_content)

    def _prepare_content_for_analysis(self, pages_content: List[Dict[str, Any]]) -> str:
        """Prepare and clean content for AI analysis."""
        content_parts = []

        for page in pages_content[:5]:  # Analyze first 5 pages to avoid token limits
            if 'page_analysis' in page:
                analysis = page['page_analysis']

                # Extract key information
                url = analysis.get('url', '')
                content_parts.append(f"Page: {url}")

                # Add navigation info
                nav_items = analysis.get('navigation', [])[:10]  # First 10 nav items
                if nav_items:
                    nav_text = ', '.join([item.get('text', '') for item in nav_items])
                    content_parts.append(f"Navigation: {nav_text}")

                # Add form information
                forms = analysis.get('forms', [])
                if forms:
                    form_info = []
                    for form in forms:
                        purpose = form.get('purpose', 'unknown')
                        fields = len(form.get('fields', []))
                        form_info.append(f"{purpose} form ({fields} fields)")
                    content_parts.append(f"Forms: {', '.join(form_info)}")

                # Add features
                features = analysis.get('features', [])
                if features:
                    content_parts.append(f"Features: {', '.join(features)}")

                content_parts.append("---")

        return '\n'.join(content_parts)

    async def _ai_powered_analysis(self, url: str, content: str, pages_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform AI-powered analysis using Claude."""
        print("🤖 Using Claude AI for intelligent analysis...")

        try:
            # Connect to Claude SDK
            await self.claude.connect()
            print("🔗 Connected to Claude SDK")
            # Skip business model analysis
            business_model = None

            # Understand website purpose
            website_purpose = await self._analyze_website_purpose(url, content)

            # Generate user insights
            user_insights = await self._analyze_user_insights(url, content)

            # Generate intelligent user stories
            user_stories = await self._generate_intelligent_user_stories(url, website_purpose, user_insights)

            # Create enhanced feature analysis
            features = await self._analyze_features_intelligently(url, content)

            # Generate actionable recommendations
            recommendations = await self._generate_ai_recommendations(url, None, user_insights)

            result = {
                "ai_powered": True,
                "business_model": asdict(business_model) if business_model else None,
                "website_purpose": asdict(website_purpose) if website_purpose else None,
                "user_insights": asdict(user_insights) if user_insights else None,
                "intelligent_user_stories": user_stories,
                "intelligent_features": features,
                "ai_recommendations": recommendations,
                "analysis_quality": "high",
                "timestamp": datetime.now().isoformat()
            }

            # Disconnect from Claude SDK
            await self.claude.disconnect()
            print("🔌 Disconnected from Claude SDK")

            return result

        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            raise e

    async def _analyze_business_model(self, url: str, content: str) -> Optional[BusinessModel]:
        """Analyze business model using Claude AI."""
        try:
            prompt = f"""
            Analyze the business model of this website: {url}

            Website Content Summary:
            {content[:2000]}  # Limit content to avoid token limits

            Please identify:
            1. Primary business model (freemium, subscription, marketplace, education, etc.)
            2. Revenue streams
            3. Target audience segments
            4. Value proposition
            5. Conversion funnels
            6. Competitive advantages
            7. Pricing strategy

            Respond ONLY with valid JSON format using these exact keys: primary_model, revenue_streams, target_audience, value_proposition, conversion_funnels, competitive_advantages, pricing_strategy. Do not include any other text or markdown.
            """

            await self.claude.query(prompt)

            # Collect the streaming response
            response_parts = []
            async for message in self.claude.receive_response():
                if hasattr(message, 'content') and message.content:
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_parts.append(content_block.text)

            response = ''.join(response_parts)

            # Parse AI response
            try:
                cleaned_response = self._clean_json_response(response)
                ai_analysis = json.loads(cleaned_response)
                return BusinessModel(
                    primary_model=ai_analysis.get('primary_model', 'unknown'),
                    revenue_streams=ai_analysis.get('revenue_streams', []),
                    target_audience=ai_analysis.get('target_audience', []),
                    value_proposition=ai_analysis.get('value_proposition', ''),
                    conversion_funnels=ai_analysis.get('conversion_funnels', []),
                    competitive_advantages=ai_analysis.get('competitive_advantages', []),
                    pricing_strategy=ai_analysis.get('pricing_strategy', 'unknown')
                )
            except json.JSONDecodeError:
                # If JSON parsing fails, extract key information from text
                return self._extract_business_model_from_text(response)

        except Exception as e:
            print(f"⚠️ Business model analysis failed: {e}")
            return None

    async def _analyze_website_purpose(self, url: str, content: str) -> Optional[WebsitePurpose]:
        """Analyze website purpose using Claude AI."""
        try:
            prompt = f"""
            Analyze the purpose and type of this website: {url}

            Website Content:
            {content[:2000]}

            Identify:
            1. Primary purpose (education, ecommerce, saas, content, community, etc.)
            2. Secondary purposes
            3. Industry/vertical
            4. User types who would use this site
            5. Key features and functionality
            6. Unique selling points

            Respond ONLY with valid JSON format using these exact keys: primary_purpose, secondary_purposes, industry, user_types, key_features, unique_selling_points. Do not include any other text or markdown.
            """

            await self.claude.query(prompt)

            # Collect the streaming response
            response_parts = []
            async for message in self.claude.receive_response():
                if hasattr(message, 'content') and message.content:
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_parts.append(content_block.text)

            response = ''.join(response_parts)

            try:
                cleaned_response = self._clean_json_response(response)
                ai_analysis = json.loads(cleaned_response)
                return WebsitePurpose(
                    primary_purpose=ai_analysis.get('primary_purpose', 'unknown'),
                    secondary_purposes=ai_analysis.get('secondary_purposes', []),
                    industry=ai_analysis.get('industry', 'unknown'),
                    user_types=ai_analysis.get('user_types', []),
                    key_features=ai_analysis.get('key_features', []),
                    unique_selling_points=ai_analysis.get('unique_selling_points', [])
                )
            except json.JSONDecodeError:
                return self._extract_website_purpose_from_text(response)

        except Exception as e:
            print(f"⚠️ Website purpose analysis failed: {e}")
            return None

    async def _analyze_user_insights(self, url: str, content: str) -> Optional[UserInsight]:
        """Analyze user insights using Claude AI."""
        try:
            prompt = f"""
            Analyze user behavior and needs for this website: {url}

            Website Content:
            {content[:2000]}

            Identify:
            1. What are users trying to accomplish (goals)?
            2. What problems/pain points might they have?
            3. What stages do users go through in their journey?
            4. What emotions drive user decisions?
            5. How should success be measured?

            Respond ONLY with valid JSON format using these exact keys: user_goals, pain_points, user_journey_stages, emotional_drivers, success_metrics. Do not include any other text or markdown.
            """

            await self.claude.query(prompt)

            # Collect the streaming response
            response_parts = []
            async for message in self.claude.receive_response():
                if hasattr(message, 'content') and message.content:
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_parts.append(content_block.text)

            response = ''.join(response_parts)

            try:
                cleaned_response = self._clean_json_response(response)
                ai_analysis = json.loads(cleaned_response)
                return UserInsight(
                    user_goals=ai_analysis.get('user_goals', []),
                    pain_points=ai_analysis.get('pain_points', []),
                    user_journey_stages=ai_analysis.get('user_journey_stages', []),
                    emotional_drivers=ai_analysis.get('emotional_drivers', []),
                    success_metrics=ai_analysis.get('success_metrics', [])
                )
            except json.JSONDecodeError:
                return self._extract_user_insights_from_text(response)

        except Exception as e:
            print(f"⚠️ User insights analysis failed: {e}")
            return None

    async def _generate_intelligent_user_stories(self, url: str, purpose: Optional[WebsitePurpose],
                                               insights: Optional[UserInsight]) -> List[Dict[str, Any]]:
        """Generate intelligent, website-specific user stories."""
        try:
            # Prepare context for AI
            purpose_text = ""
            if purpose:
                purpose_text = f"Website Purpose: {purpose.primary_purpose}\nTarget Users: {', '.join(purpose.user_types)}\nKey Features: {', '.join(purpose.key_features)}"

            insights_text = ""
            if insights:
                insights_text = f"User Goals: {', '.join(insights.user_goals)}\nPain Points: {', '.join(insights.pain_points)}"

            prompt = f"""
            Generate 5-7 specific, actionable user stories for this website: {url}

            Context:
            {purpose_text}
            {insights_text}

            Create user stories that are:
            1. Specific to this website's actual functionality
            2. Based on real user needs and goals
            3. Include realistic acceptance criteria
            4. Prioritized by business value
            5. Different from generic templates

            Format each story as:
            {{
                "title": "Brief title",
                "story": "As a [user type], I want to [action] so that [benefit]",
                "priority": "high/medium/low",
                "page_type": "specific page type",
                "acceptance_criteria": ["criterion 1", "criterion 2", ...],
                "business_value": "explanation of business impact"
            }}

            Respond ONLY with a valid JSON array. Do not include any markdown or other text.
            """

            await self.claude.query(prompt)

            # Collect the streaming response
            response_parts = []
            async for message in self.claude.receive_response():
                if hasattr(message, 'content') and message.content:
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_parts.append(content_block.text)

            response = ''.join(response_parts)

            try:
                cleaned_response = self._clean_json_response(response)
                stories = json.loads(cleaned_response)
                return stories if isinstance(stories, list) else []
            except json.JSONDecodeError:
                # Fallback: extract stories from text response
                return self._extract_user_stories_from_text(response)

        except Exception as e:
            print(f"⚠️ User story generation failed: {e}")
            return []

    async def _analyze_features_intelligently(self, url: str, content: str) -> List[Dict[str, str]]:
        """Analyze features intelligently using AI."""
        try:
            prompt = f"""
            Identify and categorize the actual features of this website: {url}

            Content:
            {content[:2000]}

            For each feature found:
            1. Feature name
            2. Category (navigation, content, interaction, commerce, etc.)
            3. Purpose/benefit
            4. User type who would use it

            Return as JSON array of objects with keys: name, category, purpose, target_user
            """

            await self.claude.query(prompt)

            # Collect the streaming response
            response_parts = []
            async for message in self.claude.receive_response():
                if hasattr(message, 'content') and message.content:
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_parts.append(content_block.text)

            response = ''.join(response_parts)

            try:
                cleaned_response = self._clean_json_response(response)
                features = json.loads(cleaned_response)
                return features if isinstance(features, list) else []
            except json.JSONDecodeError:
                return self._extract_features_from_text(response)

        except Exception as e:
            print(f"⚠️ Feature analysis failed: {e}")
            return []

    async def _generate_ai_recommendations(self, url: str, business_model: Optional[Any],
                                         insights: Optional[UserInsight]) -> List[Dict[str, str]]:
        """Generate AI-powered recommendations for improvement."""
        try:
            context = f"URL: {url}\n"
            if insights:
                context += f"User Goals: {', '.join(insights.user_goals[:3])}\n"

            prompt = f"""
            Based on this website analysis, provide 5-7 specific, actionable recommendations for improvement:

            {context}

            Focus on:
            1. User experience improvements
            2. Conversion optimization
            3. Business growth opportunities
            4. Technical enhancements
            5. Content strategy

            Format each recommendation as:
            {{
                "category": "UX/Conversion/Growth/Technical/Content",
                "title": "Brief title",
                "description": "Detailed recommendation",
                "impact": "high/medium/low",
                "effort": "high/medium/low",
                "priority": "1-5"
            }}

            Respond ONLY with a valid JSON array. Do not include any markdown or other text.
            """

            await self.claude.query(prompt)

            # Collect the streaming response
            response_parts = []
            async for message in self.claude.receive_response():
                if hasattr(message, 'content') and message.content:
                    for content_block in message.content:
                        if hasattr(content_block, 'text'):
                            response_parts.append(content_block.text)

            response = ''.join(response_parts)

            try:
                # Clean and fix common JSON issues
                cleaned_response = self._clean_json_response(response)
                recommendations = json.loads(cleaned_response)
                return recommendations if isinstance(recommendations, list) else []
            except json.JSONDecodeError:
                return self._extract_recommendations_from_text(response)

        except Exception as e:
            print(f"⚠️ Recommendations generation failed: {e}")
            return []


    # Helper methods for parsing text responses when JSON fails
    def _extract_business_model_from_text(self, text: str) -> BusinessModel:
        """Extract business model info from text response."""
        return BusinessModel(
            primary_model=self._extract_field_from_text(text, "primary_model", "unknown"),
            revenue_streams=self._extract_list_from_text(text, "revenue"),
            target_audience=self._extract_list_from_text(text, "audience"),
            value_proposition=self._extract_field_from_text(text, "value", ""),
            conversion_funnels=self._extract_list_from_text(text, "funnel"),
            competitive_advantages=self._extract_list_from_text(text, "advantage"),
            pricing_strategy=self._extract_field_from_text(text, "pricing", "unknown")
        )

    def _extract_website_purpose_from_text(self, text: str) -> WebsitePurpose:
        """Extract website purpose from text response."""
        return WebsitePurpose(
            primary_purpose=self._extract_field_from_text(text, "purpose", "unknown"),
            secondary_purposes=self._extract_list_from_text(text, "secondary"),
            industry=self._extract_field_from_text(text, "industry", "unknown"),
            user_types=self._extract_list_from_text(text, "user"),
            key_features=self._extract_list_from_text(text, "feature"),
            unique_selling_points=self._extract_list_from_text(text, "unique")
        )

    def _extract_user_insights_from_text(self, text: str) -> UserInsight:
        """Extract user insights from text response."""
        return UserInsight(
            user_goals=self._extract_list_from_text(text, "goal"),
            pain_points=self._extract_list_from_text(text, "pain"),
            user_journey_stages=self._extract_list_from_text(text, "journey"),
            emotional_drivers=self._extract_list_from_text(text, "emotion"),
            success_metrics=self._extract_list_from_text(text, "metric")
        )

    def _extract_field_from_text(self, text: str, field_name: str, default: str) -> str:
        """Extract a specific field value from text."""
        pattern = rf"{field_name}[:\-\s]+(.*?)(?:\n|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    def _extract_list_from_text(self, text: str, field_name: str) -> List[str]:
        """Extract a list of items from text."""
        items = []
        lines = text.split('\n')

        for line in lines:
            if field_name.lower() in line.lower():
                # Look for bullet points or numbered lists
                if '-' in line or '•' in line or re.match(r'^\d+\.', line.strip()):
                    item = re.sub(r'^[-•\d\.]\s*', '', line.strip())
                    if item:
                        items.append(item)

        return items[:5] if items else [f"inferred {field_name}"]

    def _extract_user_stories_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract user stories from text response."""
        stories = []
        story_blocks = text.split('\n\n')

        for block in story_blocks:
            if 'as a' in block.lower() and 'i want' in block.lower():
                stories.append({
                    "title": "AI Generated Story",
                    "story": block.strip()[:200],
                    "priority": "medium",
                    "page_type": "general",
                    "acceptance_criteria": ["AI generated criteria"],
                    "business_value": "Identified by AI"
                })

        return stories[:7] if stories else []

    def _extract_features_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract features from text response."""
        features = []
        lines = text.split('\n')

        for line in lines:
            if any(word in line.lower() for word in ['feature', 'functionality', 'capability']):
                if '-' in line or '•' in line:
                    feature_name = re.sub(r'^[-•\d\.]\s*', '', line.strip())
                    if feature_name:
                        features.append({
                            "name": feature_name[:50],
                            "category": "general",
                            "purpose": "identified by AI",
                            "target_user": "general users"
                        })

        return features[:10] if features else []

    def _extract_recommendations_from_text(self, text: str) -> List[Dict[str, str]]:
        """Extract recommendations from text response."""
        recommendations = []
        lines = text.split('\n')

        for line in lines:
            if '-' in line or '•' in line or re.match(r'^\d+\.', line.strip()):
                rec = re.sub(r'^[-•\d\.]\s*', '', line.strip())
                if rec:
                    recommendations.append({
                        "category": "General",
                        "title": rec[:100],
                        "description": rec,
                        "impact": "medium",
                        "effort": "medium",
                        "priority": "3"
                    })

        return recommendations[:7] if recommendations else []

    def _clean_json_response(self, response: str) -> str:
        """Clean and fix common JSON formatting issues from AI responses."""
        # Remove leading/trailing whitespace and common prefixes
        cleaned = response.strip()

        # Remove common markdown code block markers
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)

        # Fix escaped quotes in strings that should be JSON
        # Look for patterns like "\"field\": \"value\"" and fix them
        cleaned = re.sub(r'\"\\\"([^"]+)\\\":', r'"\1":', cleaned)
        cleaned = re.sub(r':\\s*\\\"([^"]*?)\\\"', r': "\1"', cleaned)

        # Remove trailing commas before closing brackets
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)

        # Try to extract JSON array/object if it's embedded in text
        json_match = re.search(r'(\[.*\]|\{.*\})', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(1)

        return cleaned