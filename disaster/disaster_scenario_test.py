#!/usr/bin/env python3
"""
Disaster Scenario Test Script
Tests the system's information and reliability against various disaster scenarios.
"""

import unittest
import sys
sys.path.append('claude-disaster')
from integrated_preparedness_system import IntegratedPreparednessSystem

class DisasterScenarioTest(unittest.TestCase):

    def setUp(self):
        """Set up the test environment"""
        self.system = IntegratedPreparednessSystem()

    def run_scenario_test(self, scenario_name, search_term, expected_plan_keyword, expected_solution_keyword):
        """Helper function to run a standard set of tests for a given scenario."""
        print(f"\n--- Testing {scenario_name} Scenario ---")

        # Test Knowledge Base Search
        print(f"Testing Knowledge Base Search for '{search_term}'...")
        kb_results = self.system.knowledge_base.search(search_term)
        self.assertGreater(len(kb_results), 0, f"Knowledge base should return results for '{search_term}'")
        self.assertTrue(any(search_term in result['title'].lower() or any(search_term in section['content'].lower() for section in result['sections']) for result in kb_results), f"At least one result should have '{search_term}' in the title or content")
        print(f"Knowledge Base Search for '{search_term}' PASSED")

        # Test Scenario Planning
        print(f"Testing Scenario Planning for '{scenario_name}'...")
        scenario_plans = self.system.scenario_planner.create_realistic_scenarios()
        scenario_plan = scenario_plans.get(scenario_name)
        self.assertIsNotNone(scenario_plan, f"Scenario planner should have a plan for '{scenario_name}'")
        self.assertIn(expected_plan_keyword, scenario_plan['description'].lower(), f"{scenario_name} plan should include {expected_plan_keyword} instructions")
        print(f"Scenario Planning for '{scenario_name}' PASSED")

        # Test Simple Engineering Solutions
        print(f"Testing Simple Engineering Solutions for '{scenario_name}'...")
        engineering_solutions = self.system.engineering_solutions.find_solutions_by_scenario(search_term)
        self.assertGreater(len(engineering_solutions), 0, f"Engineering solutions should have suggestions for '{search_term}'")
        self.assertTrue(any(expected_solution_keyword in solution['name'].lower() for solution in engineering_solutions), f"At least one solution should be related to {expected_solution_keyword}")
        print(f"Simple Engineering Solutions for '{scenario_name}' PASSED")

    def test_scenarios(self):
        """Run tests for all 10 disaster scenarios."""
        scenarios = [
            {"name": "Winter Storm Cascade", "search": "winter storm", "plan_keyword": "power outage", "solution_keyword": "heating"},
            {"name": "Economic Shock Wave", "search": "economic downturn", "plan_keyword": "emergency fund", "solution_keyword": "financial"},
            {"name": "Health Crisis Cluster", "search": "health crisis", "plan_keyword": "childcare", "solution_keyword": "medical"},
            {"name": "Infrastructure Domino Effect", "search": "blackout", "plan_keyword": "offline communication", "solution_keyword": "backup"},
            {"name": "Security Escalation", "search": "home break-in", "plan_keyword": "security measures", "solution_keyword": "security"}
        ]

        for scenario in scenarios:
            self.run_scenario_test(scenario["name"], scenario["search"], scenario["plan_keyword"], scenario["solution_keyword"])

if __name__ == '__main__':
    unittest.main()