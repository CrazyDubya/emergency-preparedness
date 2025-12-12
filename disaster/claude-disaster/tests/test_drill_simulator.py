#!/usr/bin/env python3
"""
Unit tests for the emergency drill simulator module
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import tempfile
import shutil
import os
from unittest.mock import patch, MagicMock

from emergency_drill_simulator import EmergencyDrillSimulator, DrillScenario, DrillResult
from exceptions import (
    DrillScenarioNotFoundError, DrillValidationError,
    DrillAlreadyRunningError, DatabaseConnectionError
)


class TestDrillScenarioDataclass(unittest.TestCase):
    """Test DrillScenario dataclass"""

    def test_create_scenario(self):
        """Test creating a drill scenario"""
        scenario = DrillScenario(
            id=1,
            name="Test Earthquake Drill",
            disaster_type="earthquake",
            difficulty="intermediate",
            duration_minutes=15,
            objectives=["Drop, cover, hold"],
            decision_points=[{"phase": "initial"}],
            success_criteria={"excellent": {"min_score": 40}},
            family_roles=["Leader", "First Aid"]
        )

        self.assertEqual(scenario.id, 1)
        self.assertEqual(scenario.name, "Test Earthquake Drill")
        self.assertEqual(scenario.disaster_type, "earthquake")


class TestDrillResultDataclass(unittest.TestCase):
    """Test DrillResult dataclass"""

    def test_create_result(self):
        """Test creating a drill result"""
        result = DrillResult(
            scenario_id=1,
            participant_name="John Doe",
            start_time="2024-01-01T10:00:00",
            end_time="2024-01-01T10:15:00",
            decisions_made=[{"choice": "A", "score": 10}],
            objectives_completed=["Objective 1"],
            score=45,
            time_taken=15.0,
            lessons_learned=["Practice more"]
        )

        self.assertEqual(result.scenario_id, 1)
        self.assertEqual(result.participant_name, "John Doe")
        self.assertEqual(result.score, 45)


class TestEmergencyDrillSimulator(unittest.TestCase):
    """Test EmergencyDrillSimulator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_drill.db")
        self.simulator = EmergencyDrillSimulator(db_path=self.db_path)

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_creates_database(self):
        """Test that initialization creates database"""
        self.assertTrue(os.path.exists(self.db_path))

    def test_create_earthquake_drill(self):
        """Test creating earthquake drill scenario"""
        scenario_id = self.simulator.create_earthquake_drill()

        self.assertIsNotNone(scenario_id)
        self.assertIsInstance(scenario_id, int)
        self.assertGreater(scenario_id, 0)

    def test_create_fire_evacuation_drill(self):
        """Test creating fire evacuation drill scenario"""
        scenario_id = self.simulator.create_fire_evacuation_drill()

        self.assertIsNotNone(scenario_id)
        self.assertGreater(scenario_id, 0)

    def test_create_severe_weather_drill(self):
        """Test creating severe weather drill scenario"""
        scenario_id = self.simulator.create_severe_weather_drill()

        self.assertIsNotNone(scenario_id)
        self.assertGreater(scenario_id, 0)

    def test_save_scenario_validates_name(self):
        """Test that save_scenario validates name"""
        with self.assertRaises(DrillValidationError) as ctx:
            self.simulator.save_scenario(
                name="",
                disaster_type="test",
                difficulty="easy",
                duration_minutes=10,
                objectives=["Test"],
                decision_points=[],
                success_criteria={},
                family_roles=[]
            )

        self.assertIn("name", str(ctx.exception.details))

    def test_save_scenario_validates_disaster_type(self):
        """Test that save_scenario validates disaster_type"""
        with self.assertRaises(DrillValidationError) as ctx:
            self.simulator.save_scenario(
                name="Test Drill",
                disaster_type="",
                difficulty="easy",
                duration_minutes=10,
                objectives=["Test"],
                decision_points=[],
                success_criteria={},
                family_roles=[]
            )

        self.assertIn("disaster_type", str(ctx.exception.details))

    def test_save_scenario_validates_duration(self):
        """Test that save_scenario validates duration"""
        with self.assertRaises(DrillValidationError) as ctx:
            self.simulator.save_scenario(
                name="Test Drill",
                disaster_type="test",
                difficulty="easy",
                duration_minutes=0,
                objectives=["Test"],
                decision_points=[],
                success_criteria={},
                family_roles=[]
            )

        self.assertIn("duration", str(ctx.exception.details))

    def test_save_scenario_validates_objectives(self):
        """Test that save_scenario validates objectives"""
        with self.assertRaises(DrillValidationError) as ctx:
            self.simulator.save_scenario(
                name="Test Drill",
                disaster_type="test",
                difficulty="easy",
                duration_minutes=10,
                objectives=[],
                decision_points=[],
                success_criteria={},
                family_roles=[]
            )

        self.assertIn("objective", str(ctx.exception.details))

    def test_run_drill_validates_participant_name(self):
        """Test that run_drill validates participant name"""
        scenario_id = self.simulator.create_earthquake_drill()

        with self.assertRaises(DrillValidationError) as ctx:
            self.simulator.run_drill(scenario_id, "", 4)

        self.assertIn("participant", str(ctx.exception.details))

    def test_run_drill_validates_family_size(self):
        """Test that run_drill validates family size"""
        scenario_id = self.simulator.create_earthquake_drill()

        with self.assertRaises(DrillValidationError) as ctx:
            self.simulator.run_drill(scenario_id, "Test User", 0)

        self.assertIn("family", str(ctx.exception.details))

        with self.assertRaises(DrillValidationError):
            self.simulator.run_drill(scenario_id, "Test User", 25)

    def test_run_drill_scenario_not_found(self):
        """Test that run_drill raises for non-existent scenario"""
        with self.assertRaises(DrillScenarioNotFoundError):
            self.simulator.run_drill(99999, "Test User", 4)

    def test_get_performance_history_empty(self):
        """Test getting performance history for new participant"""
        history = self.simulator.get_performance_history("New User")

        self.assertEqual(history["total_drills"], 0)
        self.assertEqual(history["average_score"], 0)
        self.assertEqual(history["best_score"], 0)

    def test_recommend_next_drill_for_new_user(self):
        """Test drill recommendation for new user"""
        self.simulator.create_earthquake_drill()
        self.simulator.create_fire_evacuation_drill()

        recommendations = self.simulator.recommend_next_drill("New User")

        self.assertIn("recommendations", recommendations)
        self.assertIn("focus_areas", recommendations)

    def test_scenarios_dict_initialized(self):
        """Test that scenarios dictionary is initialized"""
        self.assertIn("earthquake", self.simulator.scenarios)
        self.assertIn("fire", self.simulator.scenarios)
        self.assertIn("flood", self.simulator.scenarios)
        self.assertIn("power_outage", self.simulator.scenarios)
        self.assertIn("tornado", self.simulator.scenarios)

    def test_earthquake_scenario_phases(self):
        """Test earthquake scenario has correct phases"""
        earthquake = self.simulator.scenarios["earthquake"]

        self.assertIn("phases", earthquake)
        self.assertIn("initial_shock", earthquake["phases"])
        self.assertIn("aftershock", earthquake["phases"])

    def test_fire_scenario_time_pressure(self):
        """Test fire scenario has extreme time pressure"""
        fire = self.simulator.scenarios["fire"]

        self.assertEqual(fire["time_pressure"], "extreme")
        self.assertEqual(fire["injury_risk"], "extreme")


class TestDrillSimulatorDatabaseErrors(unittest.TestCase):
    """Test database error handling in drill simulator"""

    def test_init_with_invalid_path_raises_error(self):
        """Test that invalid database path raises appropriate error"""
        # Try to create database in non-existent directory
        invalid_path = "/nonexistent/directory/test.db"

        with self.assertRaises(DatabaseConnectionError):
            EmergencyDrillSimulator(db_path=invalid_path)


if __name__ == "__main__":
    unittest.main()
