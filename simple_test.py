#!/usr/bin/env python3
"""
Simple test to verify basic components work
"""
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing module imports...")

    try:
        from user_journey_mapper import AdvancedUserJourneyMapper
        print("✅ AdvancedUserJourneyMapper imported")
    except Exception as e:
        print(f"❌ AdvancedUserJourneyMapper failed: {e}")

    try:
        from enhanced_flow_visualizer import EnhancedFlowVisualizer
        print("✅ EnhancedFlowVisualizer imported")
    except Exception as e:
        print(f"❌ EnhancedFlowVisualizer failed: {e}")

    try:
        from inefficiency_dashboard import UserFlowInefficiencyDashboard
        print("✅ UserFlowInefficiencyDashboard imported")
    except Exception as e:
        print(f"❌ UserFlowInefficiencyDashboard failed: {e}")

    print("✅ All imports successful!")


def test_dashboard_creation():
    """Test creating a dashboard with sample data."""
    print("\n🎯 Testing dashboard creation...")

    try:
        from inefficiency_dashboard import UserFlowInefficiencyDashboard

        # Create sample data
        sample_data = {
            "journeys": [
                {
                    "persona": {"name": "Test User", "type": "customer", "goals": ["test"]},
                    "steps": [
                        {
                            "step_number": 1,
                            "success": True,
                            "time_spent": 2.0,
                            "emotions": ["satisfied"],
                            "page_type": "content",
                            "conversion_event": False,
                            "drop_off_risk": "low"
                        }
                    ],
                    "completion_rate": 100.0,
                    "satisfaction_score": 8.0,
                    "success": True,
                    "drop_off_points": [],
                    "conversion_events": [],
                    "goal_achievement": {"test": True}
                }
            ]
        }

        # Create dashboard
        dashboard = UserFlowInefficiencyDashboard("test_simple_output")
        result = dashboard.analyze_flow_inefficiencies(sample_data)

        print(f"✅ Dashboard analysis completed")
        print(f"   📊 Efficiency Score: {result.get('efficiency_score', {}).get('score', 'N/A')}")
        print(f"   🎯 Issues Found: {len(result.get('inefficiencies', []))}")

        return True

    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🔧 Simple Component Test")
    print("=" * 30)

    test_imports()
    success = test_dashboard_creation()

    if success:
        print("\n✅ Basic components are working!")
    else:
        print("\n❌ Issues found in basic components")