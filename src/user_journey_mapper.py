"""
Advanced User Journey Mapping Module
Provides multi-persona user journey analysis with visual documentation
"""
import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import hashlib


@dataclass
class UserPersona:
    """Represents a user persona for journey mapping."""
    name: str
    type: str  # customer, admin, guest, power_user, etc.
    goals: List[str]
    pain_points: List[str]
    typical_actions: List[str]
    priority: str  # high, medium, low
    demographic: Dict[str, Any]


@dataclass
class JourneyStep:
    """Represents a single step in a user journey."""
    step_number: int
    url: str
    page_title: str
    action_taken: str
    element_interacted: str
    screenshot_path: Optional[str]
    page_type: str
    emotions: List[str]  # frustrated, satisfied, confused, etc.
    time_spent: float
    success: bool
    notes: str
    conversion_event: bool = False
    drop_off_risk: str = "low"  # low, medium, high


@dataclass
class UserJourney:
    """Complete user journey for a specific persona."""
    persona: UserPersona
    journey_id: str
    start_time: float
    end_time: float
    total_duration: float
    steps: List[JourneyStep]
    completion_rate: float
    conversion_events: List[str]
    drop_off_points: List[int]  # step numbers where drop-off occurred
    satisfaction_score: float
    success: bool
    goal_achievement: Dict[str, bool]


class AdvancedUserJourneyMapper:
    """Advanced user journey mapping with multi-persona analysis."""

    def __init__(self, browser_automation, output_dir: str = "analysis_output"):
        """Initialize the user journey mapper.

        Args:
            browser_automation: BrowserAutomation instance
            output_dir: Directory to save journey documentation
        """
        self.browser = browser_automation
        self.output_dir = Path(output_dir)
        self.journeys: List[UserJourney] = []
        self.personas = self._initialize_default_personas()
        self.conversion_funnels: Dict[str, List[str]] = {}
        self.screenshots_dir = self.output_dir / "screenshots"
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def _initialize_default_personas(self) -> List[UserPersona]:
        """Initialize default user personas."""
        return [
            UserPersona(
                name="New Customer",
                type="customer",
                goals=["Find products", "Make purchase", "Create account"],
                pain_points=["Complex checkout", "Unclear pricing", "Registration required"],
                typical_actions=["browse", "search", "add_to_cart", "checkout"],
                priority="high",
                demographic={"age_group": "25-45", "tech_savvy": "medium"}
            ),
            UserPersona(
                name="Returning Customer",
                type="returning_customer",
                goals=["Quick purchase", "Check account", "Reorder items"],
                pain_points=["Forgot password", "Changed interface", "Out of stock"],
                typical_actions=["login", "browse", "quick_buy", "check_orders"],
                priority="high",
                demographic={"age_group": "30-55", "tech_savvy": "high"}
            ),
            UserPersona(
                name="Guest User",
                type="guest",
                goals=["Browse content", "Get information", "Avoid registration"],
                pain_points=["Forced registration", "Limited access", "Pop-ups"],
                typical_actions=["browse", "read", "search", "exit"],
                priority="medium",
                demographic={"age_group": "18-65", "tech_savvy": "mixed"}
            ),
            UserPersona(
                name="Administrator",
                type="admin",
                goals=["Manage content", "Monitor users", "System maintenance"],
                pain_points=["Complex interface", "Slow loading", "Limited permissions"],
                typical_actions=["login", "navigate_admin", "manage", "monitor"],
                priority="high",
                demographic={"age_group": "25-50", "tech_savvy": "high"}
            ),
            UserPersona(
                name="Mobile User",
                type="mobile_customer",
                goals=["Quick browsing", "Easy checkout", "Touch-friendly interface"],
                pain_points=["Small buttons", "Slow loading", "Desktop-only features"],
                typical_actions=["swipe", "tap", "pinch_zoom", "quick_actions"],
                priority="high",
                demographic={"age_group": "16-40", "tech_savvy": "high", "device": "mobile"}
            )
        ]

    async def map_user_journeys(self, url: str, max_depth: int = 5) -> Dict[str, Any]:
        """Map user journeys for all personas.

        Args:
            url: Starting URL for journey mapping
            max_depth: Maximum depth of navigation per journey

        Returns:
            Dictionary containing all journey analysis results
        """
        print("🗺️ Starting Advanced User Journey Mapping")
        print("=" * 60)

        results = {
            "journeys": [],
            "personas": [asdict(p) for p in self.personas],
            "conversion_funnels": {},
            "drop_off_analysis": {},
            "journey_comparison": {},
            "recommendations": []
        }

        # Map journeys for each persona
        for persona in self.personas:
            print(f"\n👤 Mapping journey for: {persona.name} ({persona.type})")

            try:
                journey = await self._map_persona_journey(persona, url, max_depth)
                if journey:
                    self.journeys.append(journey)
                    results["journeys"].append(asdict(journey))
                    print(f"✅ Journey completed for {persona.name}")
                else:
                    print(f"❌ Journey failed for {persona.name}")

            except Exception as e:
                print(f"❌ Error mapping journey for {persona.name}: {e}")

        # Analyze conversion funnels
        results["conversion_funnels"] = self._analyze_conversion_funnels()

        # Identify drop-off points
        results["drop_off_analysis"] = self._analyze_drop_off_points()

        # Compare journeys
        results["journey_comparison"] = self._compare_journeys()

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations()

        return results

    async def _map_persona_journey(self, persona: UserPersona, url: str, max_depth: int) -> Optional[UserJourney]:
        """Map a journey for a specific persona.

        Args:
            persona: User persona to simulate
            url: Starting URL
            max_depth: Maximum navigation depth

        Returns:
            Complete UserJourney object or None if failed
        """
        journey_id = self._generate_journey_id(persona, url)
        start_time = time.time()
        steps = []

        try:
            # Navigate to starting URL
            await self.browser.navigate_to(url)
            current_step = 1

            # Set up persona-specific browser context
            await self._setup_persona_context(persona)

            while current_step <= max_depth:
                # Capture current page state
                current_url = await self.browser.get_current_url()
                page_title = await self.browser.get_page_title()

                # Take screenshot
                screenshot_path = await self._capture_screenshot(
                    f"{persona.name}_step_{current_step}", current_url
                )

                # Analyze page for persona-specific actions
                page_analysis = await self._analyze_page_for_persona(persona, current_url)

                # Choose persona-appropriate action
                action_result = await self._execute_persona_action(persona, page_analysis)

                # Create journey step
                step = JourneyStep(
                    step_number=current_step,
                    url=current_url,
                    page_title=page_title,
                    action_taken=action_result.get("action", "none"),
                    element_interacted=action_result.get("element", "none"),
                    screenshot_path=str(screenshot_path) if screenshot_path else None,
                    page_type=page_analysis.get("page_type", "unknown"),
                    emotions=self._analyze_user_emotions(persona, page_analysis, action_result),
                    time_spent=action_result.get("time_spent", 2.0),
                    success=action_result.get("success", False),
                    notes=action_result.get("notes", ""),
                    conversion_event=self._is_conversion_event(action_result, page_analysis),
                    drop_off_risk=self._assess_drop_off_risk(persona, page_analysis, action_result)
                )

                steps.append(step)

                # Check if journey should continue
                if not action_result.get("continue", True):
                    break

                current_step += 1
                await asyncio.sleep(1)  # Simulate user thinking time

        except Exception as e:
            print(f"Error in persona journey: {e}")
            return None

        end_time = time.time()

        # Create complete journey
        journey = UserJourney(
            persona=persona,
            journey_id=journey_id,
            start_time=start_time,
            end_time=end_time,
            total_duration=end_time - start_time,
            steps=steps,
            completion_rate=self._calculate_completion_rate(steps, persona),
            conversion_events=self._extract_conversion_events(steps),
            drop_off_points=self._identify_drop_off_points(steps),
            satisfaction_score=self._calculate_satisfaction_score(steps, persona),
            success=self._determine_journey_success(steps, persona),
            goal_achievement=self._assess_goal_achievement(steps, persona)
        )

        return journey

    def _generate_journey_id(self, persona: UserPersona, url: str) -> str:
        """Generate a unique journey ID."""
        content = f"{persona.name}_{persona.type}_{url}_{int(time.time())}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    async def _setup_persona_context(self, persona: UserPersona) -> None:
        """Set up browser context specific to the persona."""
        try:
            if persona.type == "mobile_customer":
                # Set mobile viewport
                await self.browser.page.set_viewport_size({'width': 375, 'height': 667})
            else:
                # Set desktop viewport
                await self.browser.page.set_viewport_size({'width': 1280, 'height': 720})
        except Exception as e:
            print(f"⚠️ Could not set viewport for {persona.name}: {e}")
            # Continue without viewport change

    async def _capture_screenshot(self, filename: str, url: str) -> Optional[Path]:
        """Capture screenshot of current page."""
        try:
            timestamp = datetime.now().strftime("%H%M%S")
            safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
            screenshot_path = self.screenshots_dir / f"{safe_filename}_{timestamp}.png"

            await self.browser.page.screenshot(path=str(screenshot_path), full_page=True)
            return screenshot_path
        except Exception as e:
            print(f"Screenshot capture failed: {e}")
            return None

    async def _analyze_page_for_persona(self, persona: UserPersona, url: str) -> Dict[str, Any]:
        """Analyze current page from persona's perspective."""
        page_content = await self.browser.get_page_content()

        return {
            "page_type": self._classify_page_type(page_content),
            "relevant_elements": await self._find_persona_relevant_elements(persona),
            "barriers": self._identify_persona_barriers(persona, page_content),
            "opportunities": self._identify_persona_opportunities(persona, page_content)
        }

    async def _find_persona_relevant_elements(self, persona: UserPersona) -> List[Dict[str, str]]:
        """Find elements relevant to the specific persona."""
        elements = []

        if persona.type in ["customer", "returning_customer"]:
            # Look for shopping-related elements
            selectors = [
                "button:has-text('Add to Cart')",
                "button:has-text('Buy Now')",
                "a:has-text('Shop')",
                ".cart, .shopping-cart",
                ".checkout",
                ".price"
            ]
        elif persona.type == "admin":
            # Look for admin-related elements
            selectors = [
                "a:has-text('Admin')",
                "a:has-text('Dashboard')",
                "button:has-text('Manage')",
                ".admin-panel",
                ".settings"
            ]
        else:  # guest
            # Look for information and content
            selectors = [
                "a:has-text('Learn More')",
                "button:has-text('Get Started')",
                ".content",
                ".about",
                "nav a"
            ]

        for selector in selectors:
            try:
                elements_found = await self.browser.page.query_selector_all(selector)
                for element in elements_found[:3]:  # Limit to first 3
                    text = await element.text_content()
                    if text:
                        elements.append({
                            "selector": selector,
                            "text": text.strip(),
                            "type": "actionable"
                        })
            except Exception:
                continue

        return elements

    def _identify_persona_barriers(self, persona: UserPersona, content: str) -> List[str]:
        """Identify barriers for the specific persona."""
        barriers = []
        content_lower = content.lower()

        for pain_point in persona.pain_points:
            if any(word in content_lower for word in pain_point.lower().split()):
                barriers.append(pain_point)

        # Universal barriers
        if "sign up required" in content_lower or "registration required" in content_lower:
            if persona.type == "guest":
                barriers.append("Forced registration detected")

        return barriers

    def _identify_persona_opportunities(self, persona: UserPersona, content: str) -> List[str]:
        """Identify opportunities for the specific persona."""
        opportunities = []
        content_lower = content.lower()

        for goal in persona.goals:
            if any(word in content_lower for word in goal.lower().split()):
                opportunities.append(f"Goal achievable: {goal}")

        return opportunities

    async def _execute_persona_action(self, persona: UserPersona, page_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action appropriate for the persona."""
        relevant_elements = page_analysis.get("relevant_elements", [])

        if not relevant_elements:
            return {
                "action": "observe",
                "element": "page",
                "success": True,
                "continue": False,
                "notes": "No relevant elements found for persona",
                "time_spent": 2.0
            }

        # Choose most relevant element based on persona goals
        chosen_element = self._choose_persona_element(persona, relevant_elements)

        try:
            # Simulate persona-specific action
            if "Add to Cart" in chosen_element.get("text", ""):
                action_type = "click_add_to_cart"
            elif "Buy Now" in chosen_element.get("text", ""):
                action_type = "click_buy_now"
            elif any(word in chosen_element.get("text", "").lower() for word in ["login", "sign in"]):
                action_type = "attempt_login"
            else:
                action_type = "click_navigate"

            # Execute the action
            success = await self._simulate_action(chosen_element, persona)

            return {
                "action": action_type,
                "element": chosen_element.get("text", "unknown"),
                "success": success,
                "continue": success,
                "notes": f"Persona {persona.name} performed {action_type}",
                "time_spent": self._calculate_persona_time(persona, action_type)
            }

        except Exception as e:
            return {
                "action": "failed_action",
                "element": "unknown",
                "success": False,
                "continue": False,
                "notes": f"Action failed: {e}",
                "time_spent": 1.0
            }

    def _choose_persona_element(self, persona: UserPersona, elements: List[Dict[str, str]]) -> Dict[str, str]:
        """Choose the most appropriate element for the persona."""
        if not elements:
            return {"text": "none", "selector": "none"}

        # Score elements based on persona preferences
        scored_elements = []
        for element in elements:
            score = 0
            text = element.get("text", "").lower()

            # Score based on persona goals
            for goal in persona.goals:
                for word in goal.lower().split():
                    if word in text:
                        score += 2

            # Score based on typical actions
            for action in persona.typical_actions:
                if action in text:
                    score += 1

            scored_elements.append((score, element))

        # Return highest scoring element
        scored_elements.sort(reverse=True, key=lambda x: x[0])
        return scored_elements[0][1] if scored_elements else elements[0]

    async def _simulate_action(self, element: Dict[str, str], persona: UserPersona) -> bool:
        """Simulate performing the action."""
        try:
            selector = element.get("selector", "")
            if selector and selector != "none":
                # Try to click the element using simpler selector
                try:
                    # First try with the original selector
                    element_handle = await self.browser.page.query_selector(selector)
                    if element_handle:
                        await element_handle.click()
                        await asyncio.sleep(1)  # Wait for page response
                        return True
                except Exception:
                    # If that fails, try a simpler approach
                    text = element.get("text", "")
                    if text:
                        # Try clicking by text content
                        simple_selector = f"text='{text[:30]}'"  # Truncate long text
                        try:
                            await self.browser.page.click(simple_selector, timeout=2000)
                            await asyncio.sleep(1)
                            return True
                        except Exception:
                            pass
            return False
        except Exception as e:
            print(f"Action simulation failed: {e}")
            return False

    def _calculate_persona_time(self, persona: UserPersona, action_type: str) -> float:
        """Calculate time spent based on persona characteristics."""
        base_time = 2.0

        # Adjust based on tech savviness
        tech_level = persona.demographic.get("tech_savvy", "medium")
        if tech_level == "low":
            base_time *= 1.5
        elif tech_level == "high":
            base_time *= 0.8

        # Adjust based on action complexity
        if action_type in ["attempt_login", "click_buy_now"]:
            base_time *= 1.3

        return base_time

    def _analyze_user_emotions(self, persona: UserPersona, page_analysis: Dict[str, Any],
                              action_result: Dict[str, Any]) -> List[str]:
        """Analyze likely user emotions at this step."""
        emotions = []

        barriers = page_analysis.get("barriers", [])
        opportunities = page_analysis.get("opportunities", [])
        success = action_result.get("success", False)

        if barriers:
            emotions.extend(["frustrated", "confused"])

        if opportunities:
            emotions.extend(["interested", "motivated"])

        if success:
            emotions.append("satisfied")
        else:
            emotions.extend(["frustrated", "disappointed"])

        # Remove duplicates
        return list(set(emotions))

    def _is_conversion_event(self, action_result: Dict[str, Any], page_analysis: Dict[str, Any]) -> bool:
        """Determine if this step is a conversion event."""
        action = action_result.get("action", "")
        conversion_actions = ["click_buy_now", "click_add_to_cart", "complete_checkout", "sign_up"]
        return action in conversion_actions

    def _assess_drop_off_risk(self, persona: UserPersona, page_analysis: Dict[str, Any],
                             action_result: Dict[str, Any]) -> str:
        """Assess the risk of user drop-off at this step."""
        barriers = len(page_analysis.get("barriers", []))
        success = action_result.get("success", False)

        if barriers >= 2 or not success:
            return "high"
        elif barriers == 1:
            return "medium"
        else:
            return "low"

    def _classify_page_type(self, content: str) -> str:
        """Classify the page type based on content."""
        content_lower = content.lower()

        if any(word in content_lower for word in ["add to cart", "buy now", "price", "shopping"]):
            return "ecommerce_product"
        elif any(word in content_lower for word in ["login", "sign in", "password"]):
            return "authentication"
        elif any(word in content_lower for word in ["sign up", "register", "create account"]):
            return "registration"
        elif any(word in content_lower for word in ["dashboard", "admin", "manage"]):
            return "dashboard"
        elif any(word in content_lower for word in ["checkout", "cart", "payment"]):
            return "checkout"
        else:
            return "content"

    def _calculate_completion_rate(self, steps: List[JourneyStep], persona: UserPersona) -> float:
        """Calculate journey completion rate."""
        if not steps:
            return 0.0

        successful_steps = sum(1 for step in steps if step.success)
        return (successful_steps / len(steps)) * 100

    def _extract_conversion_events(self, steps: List[JourneyStep]) -> List[str]:
        """Extract conversion events from journey steps."""
        events = []
        for step in steps:
            if step.conversion_event:
                events.append(f"Step {step.step_number}: {step.action_taken}")
        return events

    def _identify_drop_off_points(self, steps: List[JourneyStep]) -> List[int]:
        """Identify steps where drop-off occurred or risk is high."""
        drop_off_points = []
        for step in steps:
            if step.drop_off_risk == "high" or not step.success:
                drop_off_points.append(step.step_number)
        return drop_off_points

    def _calculate_satisfaction_score(self, steps: List[JourneyStep], persona: UserPersona) -> float:
        """Calculate overall satisfaction score for the journey."""
        if not steps:
            return 0.0

        total_score = 0
        for step in steps:
            step_score = 5.0  # Base score

            # Reduce score for negative emotions
            if "frustrated" in step.emotions:
                step_score -= 2
            if "confused" in step.emotions:
                step_score -= 1

            # Increase score for positive emotions
            if "satisfied" in step.emotions:
                step_score += 1
            if "motivated" in step.emotions:
                step_score += 0.5

            # Adjust for success
            if not step.success:
                step_score -= 1

            total_score += max(0, step_score)

        return min(10.0, total_score / len(steps))

    def _determine_journey_success(self, steps: List[JourneyStep], persona: UserPersona) -> bool:
        """Determine if the journey was successful overall."""
        if not steps:
            return False

        # Check if major goals were achieved
        conversion_events = sum(1 for step in steps if step.conversion_event)
        completion_rate = self._calculate_completion_rate(steps, persona)

        return conversion_events > 0 and completion_rate >= 60

    def _assess_goal_achievement(self, steps: List[JourneyStep], persona: UserPersona) -> Dict[str, bool]:
        """Assess which persona goals were achieved."""
        achievements = {}

        for goal in persona.goals:
            achieved = False
            goal_keywords = goal.lower().split()

            for step in steps:
                step_text = f"{step.action_taken} {step.notes}".lower()
                if any(keyword in step_text for keyword in goal_keywords):
                    achieved = True
                    break

            achievements[goal] = achieved

        return achievements

    def _analyze_conversion_funnels(self) -> Dict[str, Any]:
        """Analyze conversion funnels across all journeys."""
        funnels = {}

        for journey in self.journeys:
            persona_type = journey.persona.type
            if persona_type not in funnels:
                funnels[persona_type] = {
                    "total_journeys": 0,
                    "conversion_steps": [],
                    "drop_off_analysis": {},
                    "average_steps_to_conversion": 0
                }

            funnels[persona_type]["total_journeys"] += 1

            # Analyze conversion steps
            for step in journey.steps:
                if step.conversion_event:
                    funnels[persona_type]["conversion_steps"].append({
                        "step_number": step.step_number,
                        "action": step.action_taken,
                        "page_type": step.page_type
                    })

        return funnels

    def _analyze_drop_off_points(self) -> Dict[str, Any]:
        """Analyze drop-off points across all journeys."""
        drop_off_analysis = {
            "common_drop_off_points": {},
            "drop_off_by_persona": {},
            "critical_issues": []
        }

        for journey in self.journeys:
            persona_type = journey.persona.type

            if persona_type not in drop_off_analysis["drop_off_by_persona"]:
                drop_off_analysis["drop_off_by_persona"][persona_type] = []

            for drop_off_step in journey.drop_off_points:
                drop_off_analysis["drop_off_by_persona"][persona_type].append(drop_off_step)

                # Track common drop-off points
                key = f"step_{drop_off_step}"
                if key not in drop_off_analysis["common_drop_off_points"]:
                    drop_off_analysis["common_drop_off_points"][key] = 0
                drop_off_analysis["common_drop_off_points"][key] += 1

        return drop_off_analysis

    def _compare_journeys(self) -> Dict[str, Any]:
        """Compare journeys across different personas."""
        if len(self.journeys) < 2:
            return {"message": "Need at least 2 journeys for comparison"}

        comparison = {
            "persona_performance": {},
            "journey_length_comparison": {},
            "satisfaction_comparison": {},
            "goal_achievement_comparison": {}
        }

        for journey in self.journeys:
            persona_name = journey.persona.name
            comparison["persona_performance"][persona_name] = {
                "completion_rate": journey.completion_rate,
                "satisfaction_score": journey.satisfaction_score,
                "total_steps": len(journey.steps),
                "conversion_events": len(journey.conversion_events),
                "success": journey.success
            }

        return comparison

    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate recommendations based on journey analysis."""
        recommendations = []

        if not self.journeys:
            return recommendations

        # Analyze common issues
        high_drop_off_journeys = [j for j in self.journeys if len(j.drop_off_points) >= 2]
        low_satisfaction_journeys = [j for j in self.journeys if j.satisfaction_score < 5.0]

        if high_drop_off_journeys:
            recommendations.append({
                "type": "critical",
                "title": "High Drop-off Rates Detected",
                "description": f"{len(high_drop_off_journeys)} persona journeys show high drop-off rates",
                "action": "Review and simplify user flows, reduce friction points"
            })

        if low_satisfaction_journeys:
            recommendations.append({
                "type": "improvement",
                "title": "Low User Satisfaction",
                "description": f"{len(low_satisfaction_journeys)} personas show low satisfaction scores",
                "action": "Improve UX design, reduce barriers, enhance user guidance"
            })

        # Check for mobile-specific issues
        mobile_journeys = [j for j in self.journeys if j.persona.type == "mobile_customer"]
        if mobile_journeys and any(not j.success for j in mobile_journeys):
            recommendations.append({
                "type": "mobile",
                "title": "Mobile Experience Issues",
                "description": "Mobile users experiencing difficulties",
                "action": "Optimize mobile interface, improve touch targets, reduce loading times"
            })

        return recommendations

    async def generate_journey_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive journey mapping report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"user_journey_report_{timestamp}.md"

        report_content = self._build_journey_report(results)

        with open(report_file, 'w') as f:
            f.write(report_content)

        return str(report_file)

    def _build_journey_report(self, results: Dict[str, Any]) -> str:
        """Build the journey report content."""
        report = []
        report.append("# Advanced User Journey Mapping Report\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Executive Summary
        report.append("## Executive Summary\n")
        total_journeys = len(results.get("journeys", []))
        successful_journeys = sum(1 for j in results.get("journeys", []) if j.get("success", False))
        report.append(f"- **Total Journeys Analyzed:** {total_journeys}\n")
        report.append(f"- **Successful Journeys:** {successful_journeys}\n")
        if total_journeys > 0:
            report.append(f"- **Success Rate:** {(successful_journeys/total_journeys)*100:.1f}%\n\n")
        else:
            report.append(f"- **Success Rate:** 0.0%\n\n")

        # Persona Analysis
        report.append("## Persona Journey Analysis\n")
        for journey_data in results.get("journeys", []):
            persona_name = journey_data.get("persona", {}).get("name", "Unknown")
            completion_rate = journey_data.get("completion_rate", 0)
            satisfaction_score = journey_data.get("satisfaction_score", 0)

            report.append(f"### {persona_name}\n")
            report.append(f"- **Completion Rate:** {completion_rate:.1f}%\n")
            report.append(f"- **Satisfaction Score:** {satisfaction_score:.1f}/10\n")
            report.append(f"- **Total Steps:** {len(journey_data.get('steps', []))}\n")
            report.append(f"- **Conversion Events:** {len(journey_data.get('conversion_events', []))}\n\n")

        # Recommendations
        recommendations = results.get("recommendations", [])
        if recommendations:
            report.append("## Recommendations\n")
            for i, rec in enumerate(recommendations, 1):
                report.append(f"{i}. **{rec.get('title', 'Recommendation')}** ({rec.get('type', 'general')})\n")
                report.append(f"   - {rec.get('description', '')}\n")
                report.append(f"   - **Action:** {rec.get('action', '')}\n\n")

        return "".join(report)