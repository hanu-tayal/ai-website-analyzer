"""
Enhanced Flow Visualizer for User Journey Mapping
Creates advanced Mermaid diagrams and visualizations
"""
from typing import Dict, List, Any, Optional
from dataclasses import asdict
import json


class EnhancedFlowVisualizer:
    """Creates enhanced visualizations for user journey analysis."""

    def __init__(self):
        """Initialize the enhanced flow visualizer."""
        self.color_scheme = {
            "customer": "#4CAF50",
            "returning_customer": "#2196F3",
            "guest": "#FF9800",
            "admin": "#9C27B0",
            "mobile_customer": "#E91E63"
        }

    def generate_persona_journey_diagram(self, journeys: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive persona journey diagram."""
        diagram = ["sequenceDiagram"]
        diagram.append("    participant W as Website")

        # Add participants for each persona
        persona_map = {}
        for i, journey in enumerate(journeys):
            persona_name = journey.get("persona", {}).get("name", f"User{i}")
            persona_key = f"U{i+1}"
            persona_map[persona_name] = persona_key
            diagram.append(f"    participant {persona_key} as {persona_name}")

        diagram.append("")

        # Add journey flows
        for journey in journeys:
            persona_name = journey.get("persona", {}).get("name", "User")
            persona_key = persona_map.get(persona_name, "U1")
            steps = journey.get("steps", [])

            diagram.append(f"    Note over {persona_key}: {persona_name} Journey")

            for step in steps:
                step_num = step.get("step_number", 1)
                action = step.get("action_taken", "unknown")
                success = step.get("success", False)

                if success:
                    diagram.append(f"    {persona_key}->>+W: Step {step_num}: {action}")
                    diagram.append(f"    W-->>-{persona_key}: Success")
                else:
                    diagram.append(f"    {persona_key}->>+W: Step {step_num}: {action}")
                    diagram.append(f"    W-->>-{persona_key}: Failed/Blocked")

                # Add emotions as notes
                emotions = step.get("emotions", [])
                if emotions:
                    emotion_text = ", ".join(emotions)
                    diagram.append(f"    Note right of {persona_key}: Feels: {emotion_text}")

            diagram.append("")

        return "\n".join(diagram)

    def generate_conversion_funnel_diagram(self, conversion_analysis: Dict[str, Any]) -> str:
        """Generate a conversion funnel visualization."""
        diagram = ["graph TD"]
        diagram.append("    subgraph \"Conversion Funnel Analysis\"")

        node_counter = 1
        for persona_type, funnel_data in conversion_analysis.items():
            total_journeys = funnel_data.get("total_journeys", 0)
            conversion_steps = funnel_data.get("conversion_steps", [])

            if total_journeys > 0:
                # Start node
                start_node = f"A{node_counter}"
                diagram.append(f"    {start_node}[\"{persona_type}<br/>{total_journeys} Users\"]")

                # Conversion steps
                prev_node = start_node
                for i, step in enumerate(conversion_steps):
                    step_node = f"B{node_counter}_{i}"
                    action = step.get("action", "unknown")
                    diagram.append(f"    {step_node}[\"{action}\"]")
                    diagram.append(f"    {prev_node} --> {step_node}")
                    prev_node = step_node

                # End node
                end_node = f"C{node_counter}"
                conversion_rate = len(conversion_steps) / total_journeys * 100
                diagram.append(f"    {end_node}[\"Converted<br/>{conversion_rate:.1f}%\"]")
                diagram.append(f"    {prev_node} --> {end_node}")

                node_counter += 1

        diagram.append("    end")

        # Add styling
        diagram.extend([
            "",
            "    classDef success fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef warning fill:#FF9800,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef error fill:#f44336,stroke:#333,stroke-width:2px,color:#fff"
        ])

        return "\n".join(diagram)

    def generate_drop_off_heatmap(self, drop_off_analysis: Dict[str, Any]) -> str:
        """Generate a drop-off point heatmap visualization."""
        common_drops = drop_off_analysis.get("common_drop_off_points", {})

        diagram = ["graph LR"]
        diagram.append("    subgraph \"Drop-off Heatmap\"")

        # Sort drop-off points by frequency
        sorted_drops = sorted(common_drops.items(), key=lambda x: x[1], reverse=True)

        for i, (step_key, frequency) in enumerate(sorted_drops[:10]):  # Top 10
            node_id = f"D{i+1}"

            # Determine heat level
            if frequency >= 3:
                heat_class = "critical"
                heat_emoji = "🔥"
            elif frequency >= 2:
                heat_class = "warning"
                heat_emoji = "⚠️"
            else:
                heat_class = "low"
                heat_emoji = "📊"

            diagram.append(f"    {node_id}[\"{heat_emoji} {step_key}<br/>Drop-offs: {frequency}\"]")

        diagram.append("    end")

        # Add styling for heat levels
        diagram.extend([
            "",
            "    classDef critical fill:#f44336,stroke:#333,stroke-width:3px,color:#fff",
            "    classDef warning fill:#FF9800,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef low fill:#4CAF50,stroke:#333,stroke-width:1px,color:#fff"
        ])

        return "\n".join(diagram)

    def generate_persona_satisfaction_radar(self, journeys: List[Dict[str, Any]]) -> str:
        """Generate a radar chart showing persona satisfaction levels."""
        # Note: Mermaid doesn't support radar charts directly, so we'll create a conceptual diagram
        diagram = ["graph TB"]
        diagram.append("    subgraph \"Persona Satisfaction Analysis\"")

        center_node = "CENTER[\"Satisfaction<br/>Analysis\"]"
        diagram.append(f"    {center_node}")

        for i, journey in enumerate(journeys):
            persona_name = journey.get("persona", {}).get("name", f"User{i}")
            satisfaction = journey.get("satisfaction_score", 0)
            completion_rate = journey.get("completion_rate", 0)

            node_id = f"P{i+1}"

            # Determine satisfaction level
            if satisfaction >= 7:
                sat_level = "High"
                sat_class = "high"
                sat_emoji = "😊"
            elif satisfaction >= 4:
                sat_level = "Medium"
                sat_class = "medium"
                sat_emoji = "😐"
            else:
                sat_level = "Low"
                sat_class = "low"
                sat_emoji = "😞"

            diagram.append(f"    {node_id}[\"{sat_emoji} {persona_name}<br/>Satisfaction: {satisfaction:.1f}/10<br/>Completion: {completion_rate:.1f}%\"]")
            diagram.append(f"    {center_node} --- {node_id}")

        diagram.append("    end")

        # Add styling
        diagram.extend([
            "",
            "    classDef high fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef medium fill:#FF9800,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef low fill:#f44336,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef center fill:#2196F3,stroke:#333,stroke-width:3px,color:#fff"
        ])

        return "\n".join(diagram)

    def generate_user_flow_with_emotions(self, journeys: List[Dict[str, Any]]) -> str:
        """Generate user flow diagram with emotional states."""
        diagram = ["flowchart TD"]
        diagram.append("    subgraph \"Emotional User Journey\"")

        for journey_idx, journey in enumerate(journeys):
            persona_name = journey.get("persona", {}).get("name", f"User{journey_idx}")
            steps = journey.get("steps", [])

            if not steps:
                continue

            # Start node
            start_id = f"S{journey_idx}"
            diagram.append(f"    {start_id}[\"🚀 {persona_name}<br/>Starts Journey\"]")

            prev_node = start_id

            for step_idx, step in enumerate(steps):
                node_id = f"N{journey_idx}_{step_idx}"
                action = step.get("action_taken", "unknown")
                emotions = step.get("emotions", [])
                success = step.get("success", False)
                page_type = step.get("page_type", "unknown")

                # Choose emoji based on emotions and success
                if "satisfied" in emotions:
                    emoji = "✅"
                elif "frustrated" in emotions:
                    emoji = "❌"
                elif "confused" in emotions:
                    emoji = "❓"
                elif "interested" in emotions:
                    emoji = "👀"
                else:
                    emoji = "➡️"

                # Create node
                emotion_text = ", ".join(emotions[:2])  # Limit to 2 emotions
                diagram.append(f"    {node_id}[\"{emoji} {action}<br/>({page_type})<br/>{emotion_text}\"]")

                # Connect nodes
                if success:
                    diagram.append(f"    {prev_node} --> {node_id}")
                else:
                    diagram.append(f"    {prev_node} -.-> {node_id}")

                prev_node = node_id

            # End node
            end_id = f"E{journey_idx}"
            journey_success = journey.get("success", False)
            if journey_success:
                diagram.append(f"    {end_id}[\"🎉 Journey<br/>Completed\"]")
            else:
                diagram.append(f"    {end_id}[\"🚫 Journey<br/>Abandoned\"]")

            diagram.append(f"    {prev_node} --> {end_id}")

        diagram.append("    end")

        # Add styling
        diagram.extend([
            "",
            "    classDef success fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef failure fill:#f44336,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef neutral fill:#9E9E9E,stroke:#333,stroke-width:1px,color:#fff"
        ])

        return "\n".join(diagram)

    def generate_goal_achievement_matrix(self, journeys: List[Dict[str, Any]]) -> str:
        """Generate a goal achievement matrix visualization."""
        diagram = ["graph LR"]
        diagram.append("    subgraph \"Goal Achievement Matrix\"")

        for journey_idx, journey in enumerate(journeys):
            persona_name = journey.get("persona", {}).get("name", f"User{journey_idx}")
            goals = journey.get("persona", {}).get("goals", [])
            goal_achievement = journey.get("goal_achievement", {})

            persona_node = f"P{journey_idx}[\"{persona_name}\"]"
            diagram.append(f"    {persona_node}")

            for goal_idx, goal in enumerate(goals):
                goal_node = f"G{journey_idx}_{goal_idx}"
                achieved = goal_achievement.get(goal, False)

                if achieved:
                    achievement_emoji = "✅"
                    goal_class = "achieved"
                else:
                    achievement_emoji = "❌"
                    goal_class = "not_achieved"

                diagram.append(f"    {goal_node}[\"{achievement_emoji} {goal}\"]")
                diagram.append(f"    {persona_node} --> {goal_node}")

        diagram.append("    end")

        # Add styling
        diagram.extend([
            "",
            "    classDef achieved fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef not_achieved fill:#f44336,stroke:#333,stroke-width:2px,color:#fff",
            "    classDef persona fill:#2196F3,stroke:#333,stroke-width:3px,color:#fff"
        ])

        return "\n".join(diagram)

    def generate_comprehensive_journey_dashboard(self, results: Dict[str, Any]) -> Dict[str, str]:
        """Generate a comprehensive set of journey visualizations."""
        journeys = results.get("journeys", [])
        conversion_funnels = results.get("conversion_funnels", {})
        drop_off_analysis = results.get("drop_off_analysis", {})

        diagrams = {}

        # Generate all visualization types
        if journeys:
            diagrams["persona_journeys"] = self.generate_persona_journey_diagram(journeys)
            diagrams["satisfaction_analysis"] = self.generate_persona_satisfaction_radar(journeys)
            diagrams["emotional_flow"] = self.generate_user_flow_with_emotions(journeys)
            diagrams["goal_achievement"] = self.generate_goal_achievement_matrix(journeys)

        if conversion_funnels:
            diagrams["conversion_funnel"] = self.generate_conversion_funnel_diagram(conversion_funnels)

        if drop_off_analysis:
            diagrams["drop_off_heatmap"] = self.generate_drop_off_heatmap(drop_off_analysis)

        return diagrams

    def create_journey_summary_diagram(self, results: Dict[str, Any]) -> str:
        """Create a high-level summary diagram of all journeys."""
        journeys = results.get("journeys", [])

        diagram = ["mindmap"]
        diagram.append("  root((User Journey Analysis))")

        # Personas branch
        diagram.append("    Personas")
        for journey in journeys:
            persona_name = journey.get("persona", {}).get("name", "Unknown")
            satisfaction = journey.get("satisfaction_score", 0)
            success = journey.get("success", False)

            status = "✅ Success" if success else "❌ Issues"
            diagram.append(f"      {persona_name}")
            diagram.append(f"        Satisfaction: {satisfaction:.1f}/10")
            diagram.append(f"        Status: {status}")

        # Key Insights branch
        recommendations = results.get("recommendations", [])
        if recommendations:
            diagram.append("    Key Insights")
            for rec in recommendations[:3]:  # Top 3 recommendations
                rec_type = rec.get("type", "general")
                title = rec.get("title", "Recommendation")
                diagram.append(f"      {rec_type.title()}")
                diagram.append(f"        {title}")

        # Metrics branch
        if journeys:
            total_success = sum(1 for j in journeys if j.get("success", False))
            success_rate = (total_success / len(journeys)) * 100
            avg_satisfaction = sum(j.get("satisfaction_score", 0) for j in journeys) / len(journeys)

            diagram.append("    Metrics")
            diagram.append(f"      Success Rate: {success_rate:.1f}%")
            diagram.append(f"      Avg Satisfaction: {avg_satisfaction:.1f}/10")
            diagram.append(f"      Total Journeys: {len(journeys)}")

        return "\n".join(diagram)