"""
User Flow Inefficiency Dashboard
Identifies and visualizes where user flows are inefficient and why
"""
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import statistics


@dataclass
class InefficiencyIssue:
    """Represents a specific inefficiency issue in user flow."""
    issue_id: str
    severity: str  # critical, high, medium, low
    category: str  # navigation, performance, ux, content, technical
    title: str
    description: str
    affected_personas: List[str]
    step_numbers: List[int]
    frequency: int
    impact_score: float
    root_cause: str
    suggested_fixes: List[str]
    business_impact: str
    user_quotes: List[str]  # Simulated user feedback


@dataclass
class FlowMetrics:
    """Metrics for analyzing flow efficiency."""
    total_steps: int
    successful_steps: int
    failed_steps: int
    average_time_per_step: float
    total_time: float
    bounce_rate: float
    conversion_rate: float
    user_effort_score: float
    cognitive_load_score: float


class UserFlowInefficiencyDashboard:
    """Dashboard for identifying and analyzing user flow inefficiencies."""

    def __init__(self, output_dir: str = "analysis_output"):
        """Initialize the inefficiency dashboard."""
        self.output_dir = Path(output_dir)
        self.inefficiencies: List[InefficiencyIssue] = []
        self.flow_metrics: Dict[str, FlowMetrics] = {}

        # Define inefficiency patterns
        self.inefficiency_patterns = {
            "excessive_steps": {
                "threshold": 8,
                "severity": "high",
                "description": "User journey requires too many steps to complete basic tasks"
            },
            "high_drop_off": {
                "threshold": 0.3,  # 30% drop-off rate
                "severity": "critical",
                "description": "Significant user abandonment at specific steps"
            },
            "low_success_rate": {
                "threshold": 0.6,  # Below 60% success
                "severity": "high",
                "description": "Users frequently fail to complete intended actions"
            },
            "slow_progression": {
                "threshold": 10.0,  # More than 10 seconds per step
                "severity": "medium",
                "description": "Users spend excessive time on individual steps"
            },
            "repeated_failures": {
                "threshold": 2,  # 2+ failed attempts
                "severity": "high",
                "description": "Users repeatedly attempt the same failed actions"
            },
            "emotional_distress": {
                "emotions": ["frustrated", "confused", "angry"],
                "severity": "medium",
                "description": "Users experience negative emotions during journey"
            }
        }

    def analyze_flow_inefficiencies(self, journey_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user flows to identify inefficiencies."""
        print("🔍 Analyzing User Flow Inefficiencies")
        print("=" * 50)

        journeys = journey_results.get("journeys", [])

        if not journeys:
            return {"error": "No journey data available for analysis"}

        # Calculate flow metrics for each journey
        self._calculate_flow_metrics(journeys)

        # Identify inefficiency patterns
        self._identify_inefficiencies(journeys)

        # Analyze cross-persona issues
        cross_persona_issues = self._analyze_cross_persona_issues(journeys)

        # Generate priority matrix
        priority_matrix = self._create_priority_matrix()

        # Create efficiency recommendations
        recommendations = self._generate_efficiency_recommendations()

        dashboard_data = {
            "summary": self._create_inefficiency_summary(),
            "flow_metrics": {k: asdict(v) for k, v in self.flow_metrics.items()},
            "inefficiencies": [asdict(issue) for issue in self.inefficiencies],
            "cross_persona_issues": cross_persona_issues,
            "priority_matrix": priority_matrix,
            "recommendations": recommendations,
            "efficiency_score": self._calculate_overall_efficiency_score(),
            "benchmark_comparison": self._create_benchmark_comparison()
        }

        return dashboard_data

    def _calculate_flow_metrics(self, journeys: List[Dict[str, Any]]) -> None:
        """Calculate detailed metrics for each user flow."""
        for journey in journeys:
            persona_name = journey.get("persona", {}).get("name", "Unknown")
            steps = journey.get("steps", [])

            if not steps:
                continue

            total_steps = len(steps)
            successful_steps = sum(1 for step in steps if step.get("success", False))
            failed_steps = total_steps - successful_steps

            # Calculate timing metrics
            total_time = sum(step.get("time_spent", 0) for step in steps)
            avg_time_per_step = total_time / total_steps if total_steps > 0 else 0

            # Calculate bounce rate (early exits)
            expected_journey_length = max(5, total_steps)  # Baseline expectation
            bounce_rate = max(0, (expected_journey_length - total_steps) / expected_journey_length)

            # Calculate conversion rate
            conversion_events = sum(1 for step in steps if step.get("conversion_event", False))
            conversion_rate = conversion_events / total_steps if total_steps > 0 else 0

            # Calculate user effort score (1-10, lower is better)
            effort_factors = [
                failed_steps * 2,  # Failed attempts increase effort
                max(0, total_steps - 5),  # Extra steps beyond 5
                max(0, avg_time_per_step - 3)  # Time beyond 3 seconds per step
            ]
            user_effort_score = min(10, sum(effort_factors))

            # Calculate cognitive load score (1-10, based on complexity)
            cognitive_factors = []
            for step in steps:
                page_type = step.get("page_type", "")
                emotions = step.get("emotions", [])

                if page_type in ["checkout", "authentication", "registration"]:
                    cognitive_factors.append(2)
                elif "confused" in emotions or "frustrated" in emotions:
                    cognitive_factors.append(3)
                else:
                    cognitive_factors.append(1)

            cognitive_load_score = min(10, sum(cognitive_factors) / len(cognitive_factors) if cognitive_factors else 1)

            self.flow_metrics[persona_name] = FlowMetrics(
                total_steps=total_steps,
                successful_steps=successful_steps,
                failed_steps=failed_steps,
                average_time_per_step=avg_time_per_step,
                total_time=total_time,
                bounce_rate=bounce_rate,
                conversion_rate=conversion_rate,
                user_effort_score=user_effort_score,
                cognitive_load_score=cognitive_load_score
            )

    def _identify_inefficiencies(self, journeys: List[Dict[str, Any]]) -> None:
        """Identify specific inefficiency patterns in user journeys."""
        issue_counter = 1

        for journey in journeys:
            persona_name = journey.get("persona", {}).get("name", "Unknown")
            persona_type = journey.get("persona", {}).get("type", "unknown")
            steps = journey.get("steps", [])

            if not steps:
                continue

            # Check for excessive steps
            if len(steps) > self.inefficiency_patterns["excessive_steps"]["threshold"]:
                self._add_inefficiency(
                    issue_id=f"INF_{issue_counter:03d}",
                    severity="high",
                    category="navigation",
                    title="Excessive Journey Length",
                    description=f"{persona_name} requires {len(steps)} steps to complete journey (recommended: ≤{self.inefficiency_patterns['excessive_steps']['threshold']})",
                    affected_personas=[persona_name],
                    step_numbers=list(range(self.inefficiency_patterns["excessive_steps"]["threshold"] + 1, len(steps) + 1)),
                    frequency=1,
                    impact_score=7.5,
                    root_cause="Complex navigation structure or missing shortcuts",
                    suggested_fixes=[
                        "Add quick actions or shortcuts",
                        "Consolidate similar steps",
                        "Implement progressive disclosure",
                        "Add 'skip' options for optional steps"
                    ],
                    business_impact="Increased abandonment rate, reduced conversion",
                    user_quotes=[
                        "This is taking too long...",
                        "Why do I need so many steps for this?",
                        "I just want to get this done quickly"
                    ]
                )
                issue_counter += 1

            # Check for high drop-off points
            drop_off_points = journey.get("drop_off_points", [])
            if drop_off_points:
                drop_off_rate = len(drop_off_points) / len(steps)
                if drop_off_rate > self.inefficiency_patterns["high_drop_off"]["threshold"]:
                    self._add_inefficiency(
                        issue_id=f"INF_{issue_counter:03d}",
                        severity="critical",
                        category="ux",
                        title="High Drop-off Rate",
                        description=f"{persona_name} shows {drop_off_rate*100:.1f}% drop-off rate at steps: {drop_off_points}",
                        affected_personas=[persona_name],
                        step_numbers=drop_off_points,
                        frequency=len(drop_off_points),
                        impact_score=9.0,
                        root_cause="Barriers, confusion, or friction at critical steps",
                        suggested_fixes=[
                            "Simplify forms and interactions",
                            "Add progress indicators",
                            "Provide help text and guidance",
                            "Remove unnecessary fields",
                            "Improve error messaging"
                        ],
                        business_impact="Direct revenue loss, poor user experience",
                        user_quotes=[
                            "This is confusing, I'm leaving",
                            "Too complicated, not worth it",
                            "What am I supposed to do here?"
                        ]
                    )
                    issue_counter += 1

            # Check for low success rate
            metrics = self.flow_metrics.get(persona_name)
            if metrics and metrics.successful_steps / metrics.total_steps < self.inefficiency_patterns["low_success_rate"]["threshold"]:
                success_rate = metrics.successful_steps / metrics.total_steps
                self._add_inefficiency(
                    issue_id=f"INF_{issue_counter:03d}",
                    severity="high",
                    category="technical",
                    title="Low Action Success Rate",
                    description=f"{persona_name} has only {success_rate*100:.1f}% success rate in completing actions",
                    affected_personas=[persona_name],
                    step_numbers=list(range(1, metrics.total_steps + 1)),
                    frequency=metrics.failed_steps,
                    impact_score=8.0,
                    root_cause="Technical issues, broken functionality, or poor usability",
                    suggested_fixes=[
                        "Fix broken interactive elements",
                        "Improve button and link visibility",
                        "Add loading indicators",
                        "Test across different browsers/devices",
                        "Implement better error handling"
                    ],
                    business_impact="Poor user experience, loss of trust",
                    user_quotes=[
                        "Nothing happens when I click this",
                        "Is this website broken?",
                        "Why isn't this working?"
                    ]
                )
                issue_counter += 1

            # Check for slow progression
            if metrics and metrics.average_time_per_step > self.inefficiency_patterns["slow_progression"]["threshold"]:
                self._add_inefficiency(
                    issue_id=f"INF_{issue_counter:03d}",
                    severity="medium",
                    category="performance",
                    title="Slow User Progression",
                    description=f"{persona_name} spends {metrics.average_time_per_step:.1f}s per step (recommended: ≤{self.inefficiency_patterns['slow_progression']['threshold']}s)",
                    affected_personas=[persona_name],
                    step_numbers=list(range(1, metrics.total_steps + 1)),
                    frequency=metrics.total_steps,
                    impact_score=6.0,
                    root_cause="Slow page loading, confusing interface, or information overload",
                    suggested_fixes=[
                        "Optimize page loading speed",
                        "Simplify interface design",
                        "Reduce cognitive load",
                        "Add visual cues and guidance",
                        "Implement auto-save features"
                    ],
                    business_impact="Reduced efficiency, potential abandonment",
                    user_quotes=[
                        "This is taking forever to load",
                        "I need time to figure this out",
                        "Where do I click next?"
                    ]
                )
                issue_counter += 1

            # Check for emotional distress
            negative_emotions = []
            for step in steps:
                emotions = step.get("emotions", [])
                step_negative = [e for e in emotions if e in self.inefficiency_patterns["emotional_distress"]["emotions"]]
                if step_negative:
                    negative_emotions.extend([(step.get("step_number"), e) for e in step_negative])

            if len(negative_emotions) >= 2:  # Multiple instances of negative emotions
                self._add_inefficiency(
                    issue_id=f"INF_{issue_counter:03d}",
                    severity="medium",
                    category="ux",
                    title="User Emotional Distress",
                    description=f"{persona_name} experiences negative emotions: {', '.join([e[1] for e in negative_emotions[:3]])}",
                    affected_personas=[persona_name],
                    step_numbers=[e[0] for e in negative_emotions],
                    frequency=len(negative_emotions),
                    impact_score=7.0,
                    root_cause="Poor UX design, unclear instructions, or system limitations",
                    suggested_fixes=[
                        "Improve user interface clarity",
                        "Add better onboarding and help",
                        "Provide clear feedback messages",
                        "Simplify complex processes",
                        "Add progress indicators"
                    ],
                    business_impact="Negative brand perception, reduced loyalty",
                    user_quotes=[
                        "This is so frustrating!",
                        "I don't understand what's happening",
                        "Why is this so difficult?"
                    ]
                )
                issue_counter += 1

    def _add_inefficiency(self, issue_id: str, severity: str, category: str, title: str,
                         description: str, affected_personas: List[str], step_numbers: List[int],
                         frequency: int, impact_score: float, root_cause: str,
                         suggested_fixes: List[str], business_impact: str, user_quotes: List[str]) -> None:
        """Add an inefficiency issue to the tracking list."""
        issue = InefficiencyIssue(
            issue_id=issue_id,
            severity=severity,
            category=category,
            title=title,
            description=description,
            affected_personas=affected_personas,
            step_numbers=step_numbers,
            frequency=frequency,
            impact_score=impact_score,
            root_cause=root_cause,
            suggested_fixes=suggested_fixes,
            business_impact=business_impact,
            user_quotes=user_quotes
        )
        self.inefficiencies.append(issue)

    def _analyze_cross_persona_issues(self, journeys: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify issues that affect multiple personas."""
        cross_issues = []

        # Group similar issues across personas
        issue_patterns = {}

        for issue in self.inefficiencies:
            pattern_key = f"{issue.category}_{issue.title.lower().replace(' ', '_')}"
            if pattern_key not in issue_patterns:
                issue_patterns[pattern_key] = []
            issue_patterns[pattern_key].append(issue)

        # Find patterns that affect multiple personas
        for pattern, issues in issue_patterns.items():
            if len(issues) > 1:
                all_personas = []
                total_impact = 0
                combined_steps = []

                for issue in issues:
                    all_personas.extend(issue.affected_personas)
                    total_impact += issue.impact_score
                    combined_steps.extend(issue.step_numbers)

                cross_issues.append({
                    "pattern": pattern,
                    "title": issues[0].title,
                    "affected_personas": list(set(all_personas)),
                    "persona_count": len(set(all_personas)),
                    "total_impact": total_impact,
                    "average_impact": total_impact / len(issues),
                    "affected_steps": list(set(combined_steps)),
                    "frequency": sum(issue.frequency for issue in issues),
                    "severity": self._determine_cross_issue_severity(issues),
                    "description": f"This issue affects {len(set(all_personas))} different persona types"
                })

        # Sort by impact
        cross_issues.sort(key=lambda x: x["total_impact"], reverse=True)
        return cross_issues

    def _determine_cross_issue_severity(self, issues: List[InefficiencyIssue]) -> str:
        """Determine severity for cross-persona issues."""
        severity_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        max_severity = max(severity_scores.get(issue.severity, 1) for issue in issues)

        severity_map = {4: "critical", 3: "high", 2: "medium", 1: "low"}
        return severity_map[max_severity]

    def _create_priority_matrix(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create a priority matrix for addressing inefficiencies."""
        matrix = {
            "critical_urgent": [],    # High impact, high frequency
            "critical_important": [], # High impact, lower frequency
            "optimize": [],          # Medium impact, high frequency
            "monitor": []            # Lower impact, lower frequency
        }

        for issue in self.inefficiencies:
            impact = issue.impact_score
            frequency = issue.frequency

            if impact >= 8 and frequency >= 3:
                matrix["critical_urgent"].append(asdict(issue))
            elif impact >= 7:
                matrix["critical_important"].append(asdict(issue))
            elif frequency >= 3:
                matrix["optimize"].append(asdict(issue))
            else:
                matrix["monitor"].append(asdict(issue))

        return matrix

    def _generate_efficiency_recommendations(self) -> List[Dict[str, Any]]:
        """Generate specific recommendations for improving efficiency."""
        recommendations = []

        # Analyze patterns in inefficiencies
        category_counts = {}
        for issue in self.inefficiencies:
            category_counts[issue.category] = category_counts.get(issue.category, 0) + 1

        # Generate category-specific recommendations
        if category_counts.get("navigation", 0) >= 2:
            recommendations.append({
                "priority": "high",
                "category": "Navigation",
                "title": "Simplify Navigation Structure",
                "description": "Multiple navigation issues detected across user journeys",
                "actions": [
                    "Conduct navigation tree analysis",
                    "Implement breadcrumbs and clear navigation paths",
                    "Add search functionality",
                    "Create user-friendly menu structure"
                ],
                "expected_impact": "25-40% reduction in journey length",
                "effort": "medium"
            })

        if category_counts.get("ux", 0) >= 2:
            recommendations.append({
                "priority": "high",
                "category": "User Experience",
                "title": "Improve User Experience Design",
                "description": "UX issues causing emotional distress and drop-offs",
                "actions": [
                    "Redesign problematic interfaces",
                    "Add progress indicators and feedback",
                    "Implement user testing sessions",
                    "Create consistent design patterns"
                ],
                "expected_impact": "30-50% improvement in user satisfaction",
                "effort": "high"
            })

        if category_counts.get("technical", 0) >= 1:
            recommendations.append({
                "priority": "critical",
                "category": "Technical",
                "title": "Fix Technical Issues",
                "description": "Technical problems preventing successful user actions",
                "actions": [
                    "Debug and fix broken functionality",
                    "Improve error handling and messaging",
                    "Optimize performance and loading times",
                    "Test across multiple devices and browsers"
                ],
                "expected_impact": "50-70% improvement in success rates",
                "effort": "medium"
            })

        return recommendations

    def _calculate_overall_efficiency_score(self) -> Dict[str, Any]:
        """Calculate an overall efficiency score for the website."""
        if not self.flow_metrics:
            return {"score": 0, "grade": "F", "description": "No data available"}

        # Calculate component scores
        metrics_values = list(self.flow_metrics.values())

        success_rate = statistics.mean([m.successful_steps / m.total_steps for m in metrics_values])
        time_efficiency = statistics.mean([min(1, 3 / m.average_time_per_step) for m in metrics_values])  # 3s baseline
        conversion_rate = statistics.mean([m.conversion_rate for m in metrics_values])
        effort_score = 1 - (statistics.mean([m.user_effort_score for m in metrics_values]) / 10)
        cognitive_score = 1 - (statistics.mean([m.cognitive_load_score for m in metrics_values]) / 10)

        # Weight the components
        overall_score = (
            success_rate * 0.3 +
            time_efficiency * 0.2 +
            conversion_rate * 0.2 +
            effort_score * 0.15 +
            cognitive_score * 0.15
        ) * 100

        # Assign grade
        if overall_score >= 90:
            grade = "A+"
        elif overall_score >= 85:
            grade = "A"
        elif overall_score >= 80:
            grade = "B+"
        elif overall_score >= 75:
            grade = "B"
        elif overall_score >= 70:
            grade = "C+"
        elif overall_score >= 65:
            grade = "C"
        elif overall_score >= 60:
            grade = "D"
        else:
            grade = "F"

        return {
            "score": round(overall_score, 1),
            "grade": grade,
            "components": {
                "success_rate": round(success_rate * 100, 1),
                "time_efficiency": round(time_efficiency * 100, 1),
                "conversion_rate": round(conversion_rate * 100, 1),
                "user_effort": round(effort_score * 100, 1),
                "cognitive_load": round(cognitive_score * 100, 1)
            },
            "description": self._get_score_description(overall_score, grade)
        }

    def _get_score_description(self, score: float, grade: str) -> str:
        """Get description for the efficiency score."""
        if score >= 85:
            return "Excellent user flow efficiency with minimal friction"
        elif score >= 75:
            return "Good user flow with some areas for improvement"
        elif score >= 65:
            return "Moderate efficiency with several optimization opportunities"
        elif score >= 50:
            return "Below average efficiency requiring significant improvements"
        else:
            return "Poor user flow efficiency with critical issues requiring immediate attention"

    def _create_benchmark_comparison(self) -> Dict[str, Any]:
        """Create benchmark comparison with industry standards."""
        if not self.flow_metrics:
            return {}

        metrics_values = list(self.flow_metrics.values())

        # Industry benchmarks (approximate)
        benchmarks = {
            "average_steps": {"benchmark": 5, "good": 3, "excellent": 2},
            "success_rate": {"benchmark": 0.75, "good": 0.85, "excellent": 0.95},
            "time_per_step": {"benchmark": 5.0, "good": 3.0, "excellent": 2.0},
            "conversion_rate": {"benchmark": 0.15, "good": 0.25, "excellent": 0.35},
            "bounce_rate": {"benchmark": 0.4, "good": 0.25, "excellent": 0.15}
        }

        # Calculate current performance
        current = {
            "average_steps": statistics.mean([m.total_steps for m in metrics_values]),
            "success_rate": statistics.mean([m.successful_steps / m.total_steps for m in metrics_values]),
            "time_per_step": statistics.mean([m.average_time_per_step for m in metrics_values]),
            "conversion_rate": statistics.mean([m.conversion_rate for m in metrics_values]),
            "bounce_rate": statistics.mean([m.bounce_rate for m in metrics_values])
        }

        comparison = {}
        for metric, value in current.items():
            benchmark_data = benchmarks[metric]

            if metric in ["average_steps", "time_per_step", "bounce_rate"]:  # Lower is better
                if value <= benchmark_data["excellent"]:
                    performance = "excellent"
                elif value <= benchmark_data["good"]:
                    performance = "good"
                elif value <= benchmark_data["benchmark"]:
                    performance = "benchmark"
                else:
                    performance = "below_benchmark"
            else:  # Higher is better
                if value >= benchmark_data["excellent"]:
                    performance = "excellent"
                elif value >= benchmark_data["good"]:
                    performance = "good"
                elif value >= benchmark_data["benchmark"]:
                    performance = "benchmark"
                else:
                    performance = "below_benchmark"

            comparison[metric] = {
                "current": round(value, 2),
                "benchmark": benchmark_data["benchmark"],
                "performance": performance,
                "gap": round(value - benchmark_data["benchmark"], 2)
            }

        return comparison

    def _create_inefficiency_summary(self) -> Dict[str, Any]:
        """Create a summary of all identified inefficiencies."""
        if not self.inefficiencies:
            return {"message": "No inefficiencies detected"}

        summary = {
            "total_issues": len(self.inefficiencies),
            "by_severity": {},
            "by_category": {},
            "top_issues": [],
            "affected_personas": set()
        }

        for issue in self.inefficiencies:
            # Count by severity
            summary["by_severity"][issue.severity] = summary["by_severity"].get(issue.severity, 0) + 1

            # Count by category
            summary["by_category"][issue.category] = summary["by_category"].get(issue.category, 0) + 1

            # Track affected personas
            summary["affected_personas"].update(issue.affected_personas)

        # Get top 5 issues by impact
        top_issues = sorted(self.inefficiencies, key=lambda x: x.impact_score, reverse=True)[:5]
        summary["top_issues"] = [
            {
                "title": issue.title,
                "severity": issue.severity,
                "impact_score": issue.impact_score,
                "affected_personas": issue.affected_personas
            }
            for issue in top_issues
        ]

        summary["affected_personas"] = list(summary["affected_personas"])

        return summary

    def generate_dashboard_html(self, dashboard_data: Dict[str, Any]) -> str:
        """Generate an HTML dashboard for inefficiency analysis."""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>User Flow Inefficiency Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .dashboard {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px; }}
                .metric-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .metric-value {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
                .critical {{ color: #e74c3c; }}
                .high {{ color: #f39c12; }}
                .medium {{ color: #f1c40f; }}
                .low {{ color: #27ae60; }}
                .issues-list {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .issue-item {{ border-left: 4px solid #bdc3c7; padding: 15px; margin: 10px 0; }}
                .issue-item.critical {{ border-color: #e74c3c; }}
                .issue-item.high {{ border-color: #f39c12; }}
                .issue-item.medium {{ border-color: #f1c40f; }}
                .issue-item.low {{ border-color: #27ae60; }}
                .recommendations {{ background: white; padding: 20px; border-radius: 8px; }}
                .efficiency-score {{ text-align: center; font-size: 3em; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>🔍 User Flow Inefficiency Dashboard</h1>
                    <p>Comprehensive analysis of user journey bottlenecks and optimization opportunities</p>
                    <p>Generated: {timestamp}</p>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Overall Efficiency Score</h3>
                        <div class="metric-value efficiency-score {score_class}">{efficiency_score}/100</div>
                        <div>Grade: {efficiency_grade}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Total Issues Identified</h3>
                        <div class="metric-value">{total_issues}</div>
                        <div>Across {persona_count} personas</div>
                    </div>
                    <div class="metric-card">
                        <h3>Critical Issues</h3>
                        <div class="metric-value critical">{critical_issues}</div>
                        <div>Requiring immediate attention</div>
                    </div>
                    <div class="metric-card">
                        <h3>Avg Success Rate</h3>
                        <div class="metric-value">{success_rate}%</div>
                        <div>User action completion</div>
                    </div>
                </div>

                <div class="issues-list">
                    <h2>🚨 Top Priority Issues</h2>
                    {issues_html}
                </div>

                <div class="recommendations">
                    <h2>💡 Optimization Recommendations</h2>
                    {recommendations_html}
                </div>
            </div>
        </body>
        </html>
        """

        # Extract data for template
        efficiency_data = dashboard_data.get("efficiency_score", {})
        summary = dashboard_data.get("summary", {})

        efficiency_score = efficiency_data.get("score", 0)
        efficiency_grade = efficiency_data.get("grade", "F")
        score_class = "high" if efficiency_score >= 75 else "medium" if efficiency_score >= 50 else "critical"

        total_issues = summary.get("total_issues", 0)
        critical_issues = summary.get("by_severity", {}).get("critical", 0)
        persona_count = len(summary.get("affected_personas", []))

        # Calculate average success rate
        flow_metrics = dashboard_data.get("flow_metrics", {})
        if flow_metrics:
            success_rates = [metrics.get("successful_steps", 0) / max(metrics.get("total_steps", 1), 1) * 100
                           for metrics in flow_metrics.values()]
            success_rate = round(statistics.mean(success_rates), 1) if success_rates else 0
        else:
            success_rate = 0

        # Generate issues HTML
        issues_html = ""
        top_issues = summary.get("top_issues", [])
        for issue in top_issues:
            issues_html += f"""
            <div class="issue-item {issue['severity']}">
                <h4>{issue['title']} <span class="{issue['severity']}">[{issue['severity'].upper()}]</span></h4>
                <p>Impact Score: {issue['impact_score']}/10</p>
                <p>Affected Personas: {', '.join(issue['affected_personas'])}</p>
            </div>
            """

        # Generate recommendations HTML
        recommendations_html = ""
        recommendations = dashboard_data.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            recommendations_html += f"""
            <div class="issue-item {rec['priority']}">
                <h4>{i}. {rec['title']} <span class="{rec['priority']}">[{rec['priority'].upper()}]</span></h4>
                <p>{rec['description']}</p>
                <p><strong>Expected Impact:</strong> {rec['expected_impact']}</p>
                <p><strong>Effort:</strong> {rec['effort']}</p>
            </div>
            """

        # Fill in template
        html_content = html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            efficiency_score=efficiency_score,
            efficiency_grade=efficiency_grade,
            score_class=score_class,
            total_issues=total_issues,
            persona_count=persona_count,
            critical_issues=critical_issues,
            success_rate=success_rate,
            issues_html=issues_html,
            recommendations_html=recommendations_html
        )

        return html_content

    def save_dashboard(self, dashboard_data: Dict[str, Any]) -> Tuple[str, str]:
        """Save dashboard data and HTML report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save JSON data
        json_file = self.output_dir / f"inefficiency_dashboard_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2, default=str)

        # Save HTML dashboard
        html_content = self.generate_dashboard_html(dashboard_data)
        html_file = self.output_dir / f"inefficiency_dashboard_{timestamp}.html"
        with open(html_file, 'w') as f:
            f.write(html_content)

        return str(json_file), str(html_file)