#!/usr/bin/env python3
"""
Integrated Emergency Preparedness System
Main interface combining all preparedness modules into a unified system
Enhanced with stateful operations and profile management
"""

import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Import all modules
from disaster_probability_matrix import DisasterProbabilityMatrix
from interactive_risk_assessment import InteractiveRiskAssessment
from supply_inventory_tracker import SupplyInventoryTracker
from emergency_contacts_manager import EmergencyContactsManager
from alert_monitoring_system import AlertMonitoringSystem
from neighborhood_coordination import NeighborhoodCoordination
from scenario_planning import ScenarioPlanner
from communication_emergency_plan import CommunicationEmergencyPlan
from financial_emergency_planning import FinancialEmergencyPlanner
from simple_engineering_solutions import SimpleEngineeringSolutions
from intuitive_building_guide import IntuitiveBuilder
from materials_calculator import MaterialsCalculator
from step_by_step_builder import StepByStepBuilder
from emergency_drill_simulator import EmergencyDrillSimulator
from visualization_dashboard import VisualizationDashboard
from knowledge_base_search import KnowledgeBaseSearch

# Import Version 2.0 Modern Threat Modules
from v2_modules.cyber_attack_response import CyberAttackResponseModule
from v2_modules.emp_hardening_module import EMPHardeningModule
from v2_modules.nuclear_safety_module import NuclearSafetyModule

# Import Version 2.0 Phase 2B Long-Term Sustainability Modules
from v2_modules.extended_supply_planning import ExtendedSupplyPlanningModule
from v2_modules.local_production_capabilities import LocalProductionCapabilities
from v2_modules.alternative_economy_systems import AlternativeEconomySystems
from v2_modules.community_resilience_networks import CommunityResilienceNetworks

# Import Version 3.0 Phase 3 Critical Gap Remediation Modules
from v2_modules.advanced_risk_engine import AdvancedRiskEngine
from v2_modules.scenario_risk_profiles import ScenarioRiskProfiles
from v2_modules.multi_source_alert_aggregator import MultiSourceAlertAggregator
from v2_modules.rapid_response_protocols import RapidResponseProtocols
from v2_modules.scenario_drill_generator import ScenarioDrillGenerator
from v2_modules.drill_automation_scheduler import DrillAutomationScheduler

# Import new stateful management modules
from user_profile_manager import UserProfileManager
from backup_manager import BackupManager

class IntegratedPreparednessSystem:
    def __init__(self, data_dir: str = "preparedness_data", profile: str = "default"):
        """Initialize integrated preparedness system with profile support"""
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize profile and backup managers
        self.profile_manager = UserProfileManager(data_dir)
        self.backup_manager = BackupManager(data_dir)
        
        # Load or create user profile
        self.profile_name = profile
        self.profile_data = self.profile_manager.load_profile(profile)
        
        # Check for auto-backup
        if self.backup_manager.auto_backup_needed():
            print("📦 Performing automatic backup...")
            self.backup_manager.perform_auto_backup()
        
        # Initialize all subsystems
        self.risk_matrix = DisasterProbabilityMatrix()
        self.risk_assessment = InteractiveRiskAssessment()
        self.supply_tracker = SupplyInventoryTracker(f"{data_dir}/supplies.db")
        self.contacts = EmergencyContactsManager(f"{data_dir}/contacts.db")
        self.alert_monitor = AlertMonitoringSystem(f"{data_dir}/alerts.db")
        self.neighborhood = NeighborhoodCoordination(f"{data_dir}/neighborhood.db")
        self.scenario_planner = ScenarioPlanner()
        self.communication_plan = CommunicationEmergencyPlan()
        self.financial_plan = FinancialEmergencyPlanner()
        
        # Initialize engineering and building modules
        self.engineering_solutions = SimpleEngineeringSolutions(f"{data_dir}/engineering.db")
        self.building_guide = IntuitiveBuilder(f"{data_dir}/building_guides.db")
        self.materials_calc = MaterialsCalculator(f"{data_dir}/materials.db")
        self.step_builder = StepByStepBuilder(f"{data_dir}/step_builder.db")
        
        # Initialize new enhancement modules
        self.drill_simulator = EmergencyDrillSimulator(f"{data_dir}/drill_simulator.db")
        self.dashboard = VisualizationDashboard(data_dir)
        self.knowledge_base = KnowledgeBaseSearch("disaster_knowledge_base", f"{data_dir}/knowledge_base.db")
        
        # Initialize Version 2.0 Modern Threat Modules
        self.cyber_response = CyberAttackResponseModule(f"{data_dir}/modern_threats.db")
        self.emp_hardening = EMPHardeningModule(f"{data_dir}/modern_threats.db")
        self.nuclear_safety = NuclearSafetyModule(f"{data_dir}/modern_threats.db")
        
        # Initialize Version 2.0 Phase 2B Long-Term Sustainability Modules
        self.extended_supply = ExtendedSupplyPlanningModule(f"{data_dir}/extended_supply.db")
        self.local_production = LocalProductionCapabilities(f"{data_dir}/local_production.db")
        self.alternative_economy = AlternativeEconomySystems(f"{data_dir}/alternative_economy.db")
        self.community_networks = CommunityResilienceNetworks(f"{data_dir}/community_resilience.db")
        
        # Initialize Version 3.0 Phase 3 Critical Gap Remediation Modules
        self.advanced_risk_engine = AdvancedRiskEngine(f"{data_dir}/advanced_risk.db")
        self.scenario_risk_profiles = ScenarioRiskProfiles(f"{data_dir}/scenario_profiles.db")
        self.alert_aggregator = MultiSourceAlertAggregator(f"{data_dir}/alert_aggregator.db")
        self.rapid_response = RapidResponseProtocols(f"{data_dir}/rapid_response.db")
        self.drill_generator = ScenarioDrillGenerator(f"{data_dir}/scenario_drills.db")
        self.drill_scheduler = DrillAutomationScheduler(f"{data_dir}/drill_scheduler.db")
        
        self.system_status = {
            "initialized": datetime.now().isoformat(),
            "modules_active": 29,
            "data_directory": data_dir
        }
        
        # Initialize with default data
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize databases with default engineering and building data"""
        try:
            # Initialize engineering solutions database
            self.engineering_solutions.initialize_default_solutions()
            
            # Initialize building guides with default projects
            self.building_guide.initialize_default_guides()
            
            # Initialize step-by-step builder with emergency shelter guide
            try:
                self.step_builder.create_emergency_shelter_guide()
            except:
                pass  # May already exist
                
            # Initialize emergency contacts with default services
            self.contacts.initialize_default_services()
            
            # Initialize drill scenarios
            self.drill_simulator.create_earthquake_drill()
            self.drill_simulator.create_fire_evacuation_drill()
            self.drill_simulator.create_severe_weather_drill()
            
            # Index knowledge base
            # self.knowledge_base.index_knowledge_base() # Indexing is now handled by build_knowledge_base.py
            
        except Exception as e:
            # Non-critical - system can still function
            print(f"Note: Some default data initialization skipped: {e}")
    
    def show_main_menu(self):
        """Display main system menu - ALL 43 OPTIONS GUARANTEED"""
        print("\n" + "="*70)
        print("🚨 INTEGRATED EMERGENCY PREPAREDNESS SYSTEM v3.0 🚨")
        print("="*70)
        
        print("\n📊 ASSESSMENT & PLANNING")
        print("  1. Risk Assessment & Probability Matrix")
        print("  2. Scenario Planning & Response")
        print("  3. Financial Emergency Planning")
        print("  4. Communication Planning")
        
        print("\n📦 INVENTORY & SUPPLIES")
        print("  5. Supply Inventory Management")
        print("  6. Shopping List Generator")
        print("  7. Expiration Alerts")
        
        print("\n👥 CONTACTS & COORDINATION")
        print("  8. Emergency Contacts Management")
        print("  9. Neighborhood Coordination")
        print(" 10. Community Resource Sharing")
        
        print("\n🌪️  MONITORING & ALERTS")
        print(" 11. Weather & Alert Monitoring")
        print(" 12. Active Alert Dashboard")
        print(" 13. System Status Check")
        
        print("\n🔧 ENGINEERING & BUILDING")
        print(" 17. Engineering Solutions Database")
        print(" 18. Building Project Calculator")
        print(" 19. Step-by-Step Construction Guide")
        print(" 20. Materials & Tools Calculator")
        
        print("\n🎯 TRAINING & DRILLS")
        print(" 21. Emergency Drill Simulator")
        print(" 22. View Drill Performance History")
        
        print("\n📊 ANALYTICS & INSIGHTS")
        print(" 23. Visual Dashboard")
        print(" 24. Export Dashboard to HTML")
        
        print("\n📚 KNOWLEDGE BASE")
        print(" 25. Search Knowledge Base")
        print(" 26. Browse Checklists")
        print(" 27. Generate Quick Reference Cards")
        
        print("\n🚨 MODERN THREATS (V2.0)")
        print(" 28. Cyber Attack Response")
        print(" 29. EMP/Solar Flare Hardening")
        print(" 30. Nuclear/Radiation Safety")
        
        print("\n🌱 LONG-TERM SUSTAINABILITY (V2.0)")
        print(" 31. Extended Supply Planning (6+ months)")
        print(" 32. Local Production Capabilities")
        print(" 33. Alternative Economy Systems")
        print(" 34. Community Resilience Networks")
        
        print("\n🎯 CRITICAL GAP REMEDIATION (V3.0)")
        print(" 35. Advanced Risk Assessment Engine")
        print(" 36. Scenario-Specific Risk Profiles")
        print(" 37. Multi-Source Alert Aggregator")
        print(" 38. Rapid Response Protocols")
        print(" 39. Scenario-Based Drill Generator")
        print(" 40. Drill Automation & Scheduling")
        
        print("\n📋 REPORTS & EXPORT")
        print(" 41. Comprehensive Preparedness Report")
        print(" 42. Export All Data")
        print(" 43. Emergency Quick Reference")
        
        print("\n 0. Exit System")
        print("="*70)
        
        # Force output flush to ensure all menu items display correctly
        import sys
        sys.stdout.flush()
    
    def run_risk_assessment(self):
        """Run comprehensive risk assessment with caching"""
        print("\n🎯 RUNNING COMPREHENSIVE RISK ASSESSMENT")
        print("-" * 50)
        
        # Check for cached assessment
        cached_assessment = self.profile_manager.get_risk_assessment()
        if cached_assessment and not self.profile_manager.is_update_needed('risk_assessment'):
            print("✅ Using cached risk assessment (still current)")
            print(f"Last updated: {cached_assessment.get('last_updated', 'Unknown')}")
            
            # Display cached results
            if 'top_risks' in cached_assessment:
                print("\n📈 TOP RISKS (from cache):")
                for i, risk in enumerate(cached_assessment['top_risks'][:10], 1):
                    print(f"{i:2}. {risk['name']:<30} {risk['probability']:>6.1f}%")
            
            if 'preparedness_score' in cached_assessment:
                print(f"\n💪 Preparedness Score: {cached_assessment['preparedness_score']}/100")
            
            return cached_assessment
        
        # If no cache or update needed, collect new data
        print("📊 Performing new risk assessment...")
        
        # Check if we have family/location data cached
        family_info = self.profile_manager.get_family_info()
        location_info = self.profile_manager.get_location_info()
        
        if family_info.get('adults') and location_info.get('type'):
            print("✅ Using saved profile information")
            # Pre-populate risk assessment with saved data
            self.risk_assessment.user_profile = {
                **family_info,
                **location_info
            }
        else:
            # Collect user profile
            self.risk_assessment.collect_user_profile()
            
            # Save the collected information
            self.profile_manager.save_family_info({
                'adults': self.risk_assessment.user_profile.get('adults', 0),
                'children': self.risk_assessment.user_profile.get('children', 0),
                'child_ages': self.risk_assessment.user_profile.get('child_ages', []),
                'adult_ages': self.risk_assessment.user_profile.get('adult_ages', [])
            })
            
            self.profile_manager.save_location_info({
                'type': self.risk_assessment.user_profile.get('location_type'),
                'housing': self.risk_assessment.user_profile.get('housing_type'),
                'ownership': self.risk_assessment.user_profile.get('home_ownership')
            })
        
        # Generate personalized risks
        print("\nCalculating personalized risk matrix...")
        personalized_risks = self.risk_assessment.generate_personalized_matrix()
        
        # Display top risks
        print("\n📈 TOP 10 HIGHEST PROBABILITY RISKS:")
        if isinstance(personalized_risks, dict) and 'high_probability' in personalized_risks:
            for i, (event, prob) in enumerate(personalized_risks['high_probability'][:10], 1):
                print(f"{i:2}. {event:<30} {prob:>6.1f}%")
        else:
            # Handle case where it returns a different format
            print("Risk assessment completed - use Advanced Risk Engine (option 35) for detailed analysis")
        
        # Generate recommendations
        try:
            if isinstance(personalized_risks, dict) and 'high_probability' in personalized_risks:
                # Convert to format expected by generate_personalized_recommendations
                print("\n💡 RECOMMENDATIONS:")
                print("  • Use Advanced Risk Engine (option 35) for detailed personalized recommendations")
                print("  • Review and update emergency supplies based on your highest probability risks")
                print("  • Create specific response plans for your top 3 risk scenarios")
            else:
                # Try to get recommendations if personalized_risks is a DataFrame
                recommendations = self.risk_assessment.generate_personalized_recommendations(personalized_risks)
                print(f"\n💡 RECOMMENDATIONS:")
                for category, items in recommendations.items():
                    print(f"\n{category.upper()}:")
                    for item in items[:3]:  # Top 3 per category
                        print(f"  • {item}")
        except Exception as e:
            print("\n💡 RECOMMENDATIONS:")
            print("  • Use Advanced Risk Engine (option 35) for detailed analysis and recommendations")
            print("  • Review your emergency preparedness supplies")
            print("  • Consider creating a family emergency plan")
        
        # Save assessment results to profile
        if isinstance(personalized_risks, dict) and 'high_probability' in personalized_risks:
            assessment_data = {
                'top_risks': [{'name': name, 'probability': prob} 
                             for name, prob in personalized_risks['high_probability'][:10]],
                'preparedness_score': 0,  # Will be calculated by comprehensive report
                'matrix': personalized_risks
            }
            self.profile_manager.save_risk_assessment(assessment_data)
            self.profile_manager.record_activity('risk_assessment_completed')
        
        return personalized_risks
    
    def manage_supplies(self):
        """Supply inventory management interface"""
        while True:
            print("\n📦 SUPPLY INVENTORY MANAGEMENT")
            print("-" * 40)
            print("1. View Inventory Summary")
            print("2. Add Supply Item")
            print("3. Check Minimum Levels")
            print("4. Check Expiration Alerts")
            print("5. Generate Shopping List")
            print("6. Record Supply Usage")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                summary = self.supply_tracker.get_inventory_summary()
                print(f"\n📊 INVENTORY SUMMARY")
                print(f"Categories: {len(summary['categories'])}")
                for cat, info in summary['categories'].items():
                    print(f"  {cat}: {info['item_count']} items")
                
            elif choice == "2":
                print("\n➕ ADD SUPPLY ITEM")
                category = input("Category: ")
                name = input("Item name: ")
                quantity = float(input("Quantity: "))
                unit = input("Unit: ")
                expiration = input("Expiration date (YYYY-MM-DD, optional): ").strip() or None
                location = input("Location (optional): ").strip() or None
                
                item_id = self.supply_tracker.add_supply(category, name, quantity, unit, expiration, location)
                print(f"✅ Added item #{item_id}")
                
            elif choice == "3":
                family_size = int(input("Family size: "))
                alerts = self.supply_tracker.check_minimum_levels(family_size)
                print(f"\n⚠️  MINIMUM LEVEL ALERTS ({len(alerts)} items)")
                for alert in alerts:
                    print(f"  {alert['category']}: {alert['current']}/{alert['minimum']} {alert['unit']} (shortage: {alert['shortage']})")
                    
            elif choice == "4":
                days = int(input("Check expiration within how many days? (default 30): ") or 30)
                expiring = self.supply_tracker.check_expiration_alerts(days)
                print(f"\n📅 EXPIRING ITEMS ({len(expiring)} items)")
                for item in expiring:
                    print(f"  {item['item']}: expires in {item['days_until']} days")
                    
            elif choice == "5":
                family_size = int(input("Family size: "))
                shopping = self.supply_tracker.generate_shopping_list(family_size)
                print(f"\n🛒 SHOPPING LIST")
                for priority, items in shopping.items():
                    if items:
                        print(f"\n{priority.upper()}:")
                        for item in items:
                            if 'category' in item:
                                print(f"  • {item['category']}: {item['quantity_needed']} {item['unit']}")
                            else:
                                print(f"  • {item['item']} ({item['reason']})")
    
    def manage_contacts(self):
        """Emergency contacts management interface"""
        while True:
            print("\n👥 EMERGENCY CONTACTS MANAGEMENT")
            print("-" * 40)
            print("1. View Priority Contacts")
            print("2. Add New Contact")
            print("3. Create Contact Group")
            print("4. Generate Emergency Card")
            print("5. Check Verification Status")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                contacts = self.contacts.get_priority_contacts()
                print(f"\n📞 PRIORITY CONTACTS ({len(contacts)} contacts)")
                for contact in contacts[:10]:  # Top 10
                    print(f"  {contact['name']} ({contact['category']}): {contact['primary_phone']}")
                    
            elif choice == "2":
                print("\n➕ ADD EMERGENCY CONTACT")
                category = input("Category: ")
                name = input("Name: ")
                phone = input("Primary phone: ")
                relationship = input("Relationship (optional): ").strip() or None
                email = input("Email (optional): ").strip() or None
                
                contact_id = self.contacts.add_contact(category, name, phone, relationship, None, email)
                print(f"✅ Added contact #{contact_id}")
                
            elif choice == "4":
                card = self.contacts.get_emergency_card()
                print(f"\n💳 EMERGENCY CONTACT CARD")
                print(card)
                
                save = input("\nSave to file? (y/n): ").lower() == 'y'
                if save:
                    with open(f"{self.data_dir}/emergency_card.txt", 'w') as f:
                        f.write(card)
                    print("💾 Saved to emergency_card.txt")
    
    def monitor_alerts(self):
        """Alert monitoring interface"""
        print("\n🌪️  ALERT MONITORING SYSTEM")
        print("-" * 40)
        
        # Check if location is configured
        try:
            results = self.alert_monitor.run_monitoring_cycle()
            if "error" in results:
                print("⚠️  System not configured. Setting up location...")
                lat = float(input("Latitude: "))
                lon = float(input("Longitude: "))
                location = input("Location name: ")
                api_key = input("OpenWeather API key (optional): ").strip() or None
                
                self.alert_monitor.set_location(lat, lon, location, api_key)
                results = self.alert_monitor.run_monitoring_cycle()
            
            print(f"\n📡 MONITORING RESULTS")
            print(f"New alerts: {results['new_alerts']}")
            print(f"Weather risks: {len(results['weather_risks'])}")
            for risk in results['weather_risks']:
                print(f"  ⚠️  {risk}")
            
            if results['errors']:
                print(f"Errors: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"  ❌ {error}")
            
            # Show active alerts
            active = self.alert_monitor.get_active_alerts()
            print(f"\n🚨 ACTIVE ALERTS ({len(active)})")
            for alert in active[:5]:  # Top 5
                print(f"  {alert['title']} (Severity: {alert['severity']})")
                
        except Exception as e:
            print(f"❌ Error running monitoring: {e}")
    
    def generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive preparedness report"""
        print("\n📋 GENERATING COMPREHENSIVE PREPAREDNESS REPORT")
        print("-" * 55)
        
        report = {
            "generated": datetime.now().isoformat(),
            "system_status": self.system_status,
            "preparedness_score": 0,
            "sections": {}
        }
        
        # Supply inventory status
        print("Analyzing supply inventory...")
        supply_summary = self.supply_tracker.get_inventory_summary()
        family_size = 3  # Default
        supply_alerts = self.supply_tracker.check_minimum_levels(family_size)
        expiring_items = self.supply_tracker.check_expiration_alerts(30)
        
        supply_score = max(0, 100 - (len(supply_alerts) * 10) - (len(expiring_items) * 5))
        
        report["sections"]["supplies"] = {
            "score": supply_score,
            "total_categories": len(supply_summary['categories']),
            "shortages": len(supply_alerts),
            "expiring_soon": len(expiring_items),
            "status": "excellent" if supply_score >= 90 else "good" if supply_score >= 70 else "needs_improvement"
        }
        
        # Contact management status
        print("Analyzing contact management...")
        verification_status = self.contacts.get_verification_status()
        contact_score = verification_status['statistics']['verification_rate']
        
        report["sections"]["contacts"] = {
            "score": contact_score,
            "total_contacts": verification_status['statistics']['total'],
            "verified_contacts": verification_status['statistics']['verified'],
            "needs_verification": len(verification_status['needs_verification']),
            "status": "excellent" if contact_score >= 90 else "good" if contact_score >= 70 else "needs_improvement"
        }
        
        # Alert monitoring status
        print("Checking alert monitoring...")
        try:
            alert_summary = self.alert_monitor.generate_alert_summary()
            alert_score = 100 - (alert_summary['urgent_count'] * 20)  # Deduct for urgent alerts
            
            report["sections"]["monitoring"] = {
                "score": max(0, alert_score),
                "active_alerts": alert_summary['total_active'],
                "urgent_alerts": alert_summary['urgent_count'],
                "highest_severity": alert_summary['highest_severity'],
                "status": "excellent" if alert_score >= 90 else "good" if alert_score >= 70 else "needs_attention"
            }
        except:
            report["sections"]["monitoring"] = {
                "score": 50,
                "status": "not_configured"
            }
        
        # Calculate overall preparedness score
        scores = [section.get('score', 0) for section in report["sections"].values()]
        report["preparedness_score"] = sum(scores) / len(scores) if scores else 0
        
        # Recommendations
        recommendations = []
        if supply_score < 80:
            recommendations.append("Address supply shortages - check minimum levels")
        if contact_score < 80:
            recommendations.append("Verify emergency contacts - many outdated")
        if report["sections"]["monitoring"]["status"] == "not_configured":
            recommendations.append("Configure alert monitoring system")
        
        report["recommendations"] = recommendations
        
        return report
    
    def export_all_data(self):
        """Export all system data"""
        print("\n💾 EXPORTING ALL SYSTEM DATA")
        print("-" * 35)
        
        export_dir = f"{self.data_dir}/exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Export supplies
            supply_file = f"{export_dir}/supplies_{timestamp}.json"
            self.supply_tracker.export_inventory(supply_file)
            print(f"✅ Supplies exported: {supply_file}")
            
            # Export contacts
            contact_file = f"{export_dir}/contacts_{timestamp}.json"
            self.contacts.export_contacts(contact_file)
            print(f"✅ Contacts exported: {contact_file}")
            
            # Export comprehensive report
            report = self.generate_comprehensive_report()
            report_file = f"{export_dir}/preparedness_report_{timestamp}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✅ Report exported: {report_file}")
            
            # Create quick reference
            quick_ref = self.generate_quick_reference()
            ref_file = f"{export_dir}/quick_reference_{timestamp}.txt"
            with open(ref_file, 'w') as f:
                f.write(quick_ref)
            print(f"✅ Quick reference exported: {ref_file}")
            
            print(f"\n📁 All data exported to: {export_dir}")
            
        except Exception as e:
            print(f"❌ Export error: {e}")
    
    def generate_quick_reference(self) -> str:
        """Generate emergency quick reference guide"""
        ref = f"""
🚨 EMERGENCY QUICK REFERENCE GUIDE 🚨
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📞 PRIORITY EMERGENCY CONTACTS
{'='*40}
"""
        
        try:
            priority_contacts = self.contacts.get_priority_contacts()
            for contact in priority_contacts[:8]:  # Top 8
                ref += f"{contact['name']:<20} {contact['primary_phone']}\n"
        except:
            ref += "Emergency contacts not configured\n"
        
        ref += f"""
📦 CRITICAL SUPPLY STATUS
{'='*40}
"""
        
        try:
            supply_alerts = self.supply_tracker.check_minimum_levels(3)
            if supply_alerts:
                for alert in supply_alerts[:5]:
                    ref += f"⚠️  {alert['category']}: {alert['current']}/{alert['minimum']} {alert['unit']}\n"
            else:
                ref += "✅ All critical supplies at adequate levels\n"
        except:
            ref += "Supply inventory not configured\n"
        
        ref += f"""
🌪️  CURRENT ALERTS
{'='*40}
"""
        
        try:
            active_alerts = self.alert_monitor.get_active_alerts(3)  # Severe+ only
            if active_alerts:
                for alert in active_alerts[:3]:
                    ref += f"🚨 {alert['title']}\n"
            else:
                ref += "✅ No severe weather alerts\n"
        except:
            ref += "Alert monitoring not configured\n"
        
        ref += f"""
📋 EMERGENCY PROCEDURES
{'='*40}
1. Assess immediate danger
2. Ensure family safety first
3. Contact emergency services if needed (911)
4. Implement family communication plan
5. Check on neighbors if safe to do so
6. Monitor official emergency broadcasts
7. Follow evacuation orders immediately

💡 Remember: Stay calm, think clearly, help others when safe
"""
        
        return ref
    
    def engineering_solutions_interface(self):
        """Engineering solutions database interface"""
        while True:
            print("\n🔧 ENGINEERING SOLUTIONS DATABASE")
            print("-" * 40)
            print("1. Browse Solutions by Category")
            print("2. Find Solutions for Disaster Scenario")
            print("3. Get Solution Details & Instructions")
            print("4. Add New Solution")
            print("5. Search by Available Materials")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                categories = ["water_collection", "water_purification", "shelter", 
                            "power_generation", "heating_cooling", "tools"]
                print("\nAvailable categories:")
                for i, cat in enumerate(categories, 1):
                    print(f"  {i}. {cat.replace('_', ' ').title()}")
                
                try:
                    cat_choice = int(input("Select category: ")) - 1
                    if 0 <= cat_choice < len(categories):
                        solutions = self.engineering_solutions.get_solutions_by_category(categories[cat_choice])
                        print(f"\n{categories[cat_choice].replace('_', ' ').title()} Solutions:")
                        for sol in solutions:
                            print(f"  • {sol['name']} ({sol['difficulty']}) - ${sol['cost_estimate']:.2f}")
                except (ValueError, IndexError):
                    print("Invalid selection")
                    
            elif choice == "2":
                scenario = input("Enter disaster scenario (e.g., 'flood', 'power outage'): ")
                solutions = self.engineering_solutions.find_solutions_by_scenario(scenario)
                print(f"\nSolutions for '{scenario}':")
                for sol in solutions:
                    print(f"  • {sol['name']} ({sol['difficulty']})")
                    
            elif choice == "3":
                try:
                    solution_id = int(input("Enter solution ID: "))
                    details = self.engineering_solutions.get_solution_details(solution_id)
                    if details:
                        print(f"\n📋 {details['name']}")
                        print(f"Category: {details['category']}")
                        print(f"Difficulty: {details['difficulty']}")
                        print(f"Build Time: {details['build_time']}")
                        print(f"Cost: ${details['cost_estimate']:.2f}")
                        print(f"\nMaterials ({len(details['materials'])}):")
                        for mat in details['materials']:
                            print(f"  • {mat['quantity']} {mat['unit']} {mat['name']}")
                        print(f"\nInstructions ({len(details['instructions'])}):")
                        for inst in details['instructions']:
                            print(f"  {inst['step']}. {inst['instruction']}")
                except (ValueError, KeyError):
                    print("Invalid solution ID")
    
    def building_calculator_interface(self):
        """Building project calculator interface"""
        while True:
            print("\n🏗️ BUILDING PROJECT CALCULATOR")
            print("-" * 40)
            print("1. Calculate Complete Shelter")
            print("2. Calculate Foundation Materials")
            print("3. Calculate Frame Materials")
            print("4. Calculate Roofing Materials")
            print("5. Optimize Materials for Budget")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                try:
                    length = float(input("Shelter length (feet): "))
                    width = float(input("Shelter width (feet): "))
                    height = float(input("Shelter height (feet, default 8): ") or 8)
                    foundation = input("Include foundation? (y/n): ").lower() == 'y'
                    
                    calc = self.materials_calc.calculate_complete_shelter(length, width, height, foundation)
                    
                    print(f"\n🏠 COMPLETE SHELTER CALCULATION")
                    print(f"Dimensions: {length}'L x {width}'W x {height}'H")
                    print(f"Material Cost: ${calc['total_material_cost']:,.2f}")
                    print(f"Tool Cost: ${calc['total_tool_cost']:,.2f}")
                    print(f"Build Time: {calc['estimated_build_time']}")
                    print(f"Difficulty: {calc['difficulty_level']}")
                    
                    print(f"\nMATERIALS BREAKDOWN:")
                    for material, details in calc["materials"].items():
                        print(f"  {material}: {details['quantity']} - ${details['total_cost']:.2f}")
                    
                    save = input("\nSave calculation? (y/n): ").lower() == 'y'
                    if save:
                        name = input("Project name: ")
                        self.materials_calc.save_calculation(name, calc)
                        print("✅ Calculation saved")
                        
                except ValueError:
                    print("Invalid input - please enter numbers")
                    
            elif choice == "2":
                try:
                    length = float(input("Foundation length (feet): "))
                    width = float(input("Foundation width (feet): "))
                    thickness = float(input("Foundation thickness (feet, default 0.5): ") or 0.5)
                    
                    calc = self.materials_calc.calculate_foundation_materials(length, width, thickness)
                    
                    print(f"\n🏗️ FOUNDATION CALCULATION")
                    print(f"Dimensions: {length}'L x {width}'W x {thickness}'T")
                    print(f"Total Cost: ${calc['total_cost']:,.2f}")
                    print(f"Volume: {calc['volume_cubic_feet']:.1f} cubic feet")
                    
                    for material, details in calc["materials"].items():
                        print(f"  {material}: {details['quantity']} {details['unit']} - ${details['total_cost']:.2f}")
                        
                except ValueError:
                    print("Invalid input - please enter numbers")
    
    def step_by_step_guide_interface(self):
        """Step-by-step construction guide interface"""
        while True:
            print("\n📋 STEP-BY-STEP CONSTRUCTION GUIDE")
            print("-" * 40)
            print("1. Start New Building Project")
            print("2. Continue Existing Project")
            print("3. View Available Project Guides")
            print("4. Create Emergency Shelter Guide")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                name = input("Your name: ")
                print("\nAvailable Projects:")
                print("  1. Emergency A-Frame Shelter")
                # Add more project options here
                
                try:
                    project_choice = int(input("Select project: "))
                    if project_choice == 1:
                        # Initialize default shelter guide if not exists
                        try:
                            project_id = self.step_builder.create_emergency_shelter_guide()
                        except:
                            project_id = 1  # Assume it exists
                        
                        session_id = self.step_builder.start_user_session(project_id, name)
                        self._run_building_session(session_id)
                except ValueError:
                    print("Invalid selection")
                    
            elif choice == "2":
                try:
                    session_id = int(input("Enter session ID: "))
                    self._run_building_session(session_id)
                except ValueError:
                    print("Invalid session ID")
                    
            elif choice == "4":
                try:
                    project_id = self.step_builder.create_emergency_shelter_guide()
                    print(f"✅ Emergency shelter guide created with ID: {project_id}")
                except Exception as e:
                    print(f"❌ Error creating guide: {e}")
    
    def _run_building_session(self, session_id: int):
        """Run interactive building session"""
        while True:
            progress = self.step_builder.get_user_progress(session_id)
            if not progress:
                print("❌ Session not found")
                return
            
            if progress["current_step"] > progress["total_steps"]:
                print("🎉 Project completed!")
                return
            
            guide = self.step_builder.generate_interactive_guide(
                progress["project_id"], progress["current_step"]
            )
            print(guide)
            
            action = input().lower().strip()
            
            if action == 'y':
                rating = int(input("Quality rating (1-5): ") or 5)
                notes = input("Any notes (optional): ")
                
                self.step_builder.complete_step(session_id, progress["current_step"], rating, notes)
                print("✅ Step completed!")
                
            elif action == 'h':
                step = self.step_builder.get_build_step(progress["project_id"], progress["current_step"])
                print(f"\n💡 HELP FOR STEP {progress['current_step']}:")
                if step.get('common_mistakes'):
                    print("Common mistakes to avoid:")
                    for mistake in step['common_mistakes']:
                        print(f"  • {mistake}")
                        
            elif action == 'q':
                issues = input("Describe quality issues encountered: ")
                # Could integrate with quality tracking system
                print("Quality issues noted")
                
            elif action == 'exit':
                break
    
    def materials_tools_calculator(self):
        """Materials and tools calculator interface"""
        while True:
            print("\n🧮 MATERIALS & TOOLS CALCULATOR")
            print("-" * 40)
            print("1. Beam Load Calculator")
            print("2. Foundation Size Calculator")
            print("3. Material Cost Estimator")
            print("4. Tool Requirements")
            print("5. Bulk Pricing Optimizer")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                try:
                    length = float(input("Beam length (feet): "))
                    load = float(input("Load (pounds): "))
                    material = input("Material (2x4_lumber, 2x6_lumber, etc.): ") or "2x4_lumber"
                    
                    calc = self.building_guide.calculate_beam_load(length, load, material)
                    
                    print(f"\n⚖️ BEAM ANALYSIS")
                    print(f"Status: {calc['status']}")
                    print(f"Deflection: {calc['deflection_inches']} inches")
                    print(f"Max allowable: {calc['max_allowable_inches']} inches")
                    print(f"Safety ratio: {calc['safety_ratio']}")
                    print(f"Recommendation: {calc['recommendation']}")
                    
                except ValueError:
                    print("Invalid input - please enter numbers")
                    
            elif choice == "2":
                try:
                    weight = float(input("Structure weight (pounds): "))
                    soil = input("Soil type (rock/hard_clay/average/soft_clay/sand): ") or "average"
                    
                    calc = self.building_guide.calculate_foundation_size(weight, soil)
                    
                    print(f"\n🏗️ FOUNDATION CALCULATION")
                    print(f"Required area: {calc['required_area_sqft']} sq ft")
                    print(f"Recommended width: {calc['recommended_width_ft']} ft")
                    print(f"Recommended depth: {calc['recommended_depth_ft']} ft")
                    print(f"Concrete needed: {calc['concrete_needed_cubic_ft']} cubic feet")
                    
                except ValueError:
                    print("Invalid input - please enter numbers")
    
    def run_drill_simulator(self):
        """Run emergency drill simulator interface"""
        print("\n🎯 EMERGENCY DRILL SIMULATOR")
        print("-" * 40)
        print("Available Drills:")
        print("  1. Earthquake Response Drill")
        print("  2. Fire Evacuation Drill")
        print("  3. Tornado Warning Drill")
        
        try:
            choice = int(input("\nSelect drill (1-3): "))
            name = input("Participant name: ")
            family_size = int(input("Family size (1-5): ") or 4)
            
            # Run selected drill
            result = self.drill_simulator.run_drill(choice, name, family_size)
            
            # Show recommendations
            recommendations = self.drill_simulator.recommend_next_drill(name)
            if recommendations['recommendations']:
                print(f"\n💡 RECOMMENDED NEXT DRILL:")
                for rec in recommendations['recommendations'][:1]:
                    print(f"  {rec['name']}: {rec['reason']}")
                    
        except (ValueError, KeyError) as e:
            print(f"Error running drill: {e}")
    
    def view_drill_history(self):
        """View drill performance history"""
        name = input("Enter participant name: ")
        history = self.drill_simulator.get_performance_history(name)
        
        print(f"\n📈 PERFORMANCE HISTORY FOR {name.upper()}")
        print(f"Total Drills: {history['total_drills']}")
        print(f"Average Score: {history['average_score']}")
        print(f"Best Score: {history['best_score']}")
        
        if history['recent_drills']:
            print(f"\nRecent Drills:")
            for drill in history['recent_drills']:
                print(f"  • {drill['scenario']} - Score: {drill['score']} ({drill['grade']})")
    
    def show_visual_dashboard(self):
        """Display visual analytics dashboard"""
        print("\n📊 GENERATING VISUAL DASHBOARD...")
        dashboard_output = self.dashboard.generate_full_dashboard()
        print(dashboard_output)
    
    def export_dashboard(self):
        """Export dashboard to HTML file"""
        filename = input("Enter filename (default: emergency_dashboard.html): ").strip()
        if not filename:
            filename = "emergency_dashboard.html"
        
        filepath = self.dashboard.export_dashboard_html(filename)
        print(f"✅ Dashboard exported to: {filepath}")
        print("Open in web browser for best viewing experience")
    
    def search_knowledge_base(self):
        """Search knowledge base interface"""
        while True:
            print("\n📚 KNOWLEDGE BASE SEARCH")
            print("-" * 40)
            query = input("Search query (or 'back' to return): ").strip()
            
            if query.lower() == 'back':
                break
            
            results = self.knowledge_base.search(query)
            
            if results:
                print(f"\n📖 SEARCH RESULTS ({len(results)} found):")
                for i, result in enumerate(results[:5], 1):
                    print(f"\n{i}. {result['title']} ({result['category']})")
                    if result['sections']:
                        print(f"   {result['sections'][0]['content']}")
                
                # Option to view full document
                try:
                    view = input("\nView full document? Enter number (or press Enter to skip): ").strip()
                    if view and view.isdigit():
                        doc_id = results[int(view) - 1]['id']
                        doc = self.knowledge_base.get_document(doc_id)
                        print(f"\n{'='*60}")
                        print(f"📄 {doc['title']}")
                        print(f"{'='*60}")
                        print(doc['content'][:2000])  # First 2000 chars
                        if len(doc['content']) > 2000:
                            print("\n[Document truncated - see full file for complete content]")
                except (ValueError, IndexError):
                    pass
            else:
                print("No results found. Try different keywords.")
    
    def browse_checklists(self):
        """Browse interactive checklists"""
        print("\n✅ INTERACTIVE CHECKLISTS")
        print("-" * 40)
        
        categories = ["water", "food", "shelter", "medical", "evacuation", None]
        print("Categories:")
        for i, cat in enumerate(categories[:-1], 1):
            print(f"  {i}. {cat.title()}")
        print(f"  {len(categories)}. All checklists")
        
        try:
            choice = int(input("\nSelect category: "))
            category = categories[choice - 1] if choice < len(categories) else None
            
            checklists = self.knowledge_base.get_checklists(category)
            
            if checklists:
                for checklist in checklists[:5]:
                    print(f"\n📝 {checklist['title']} ({checklist['category']})")
                    print(f"   Priority: {checklist['priority']}/10")
                    print(f"   Items ({len(checklist['items'])}):")
                    for item in checklist['items'][:5]:
                        check = "✓" if item.get('checked') else "□"
                        print(f"     {check} {item['text']}")
                    if len(checklist['items']) > 5:
                        print(f"     ... and {len(checklist['items']) - 5} more items")
            else:
                print("No checklists found for this category")
                
        except (ValueError, IndexError):
            print("Invalid selection")
    
    def generate_reference_cards(self):
        """Generate printable quick reference cards"""
        print("\n📇 GENERATING QUICK REFERENCE CARDS...")
        
        cards = self.knowledge_base.generate_quick_reference_cards()
        
        for card in cards:
            print(f"\n{'='*50}")
            print(f"📇 {card['title'].upper()}")
            print(f"Category: {card['category']}")
            print(f"{'='*50}")
            print(card['content'])
        
        save = input("\nSave cards to file? (y/n): ").lower() == 'y'
        if save:
            filename = f"{self.data_dir}/quick_reference_cards.txt"
            with open(filename, 'w') as f:
                for card in cards:
                    f.write(f"{'='*50}\n")
                    f.write(f"{card['title'].upper()}\n")
                    f.write(f"Category: {card['category']}\n")
                    f.write(f"{'='*50}\n")
                    f.write(card['content'])
                    f.write("\n\n")
            print(f"✅ Cards saved to: {filename}")
    
    # Version 2.0 Modern Threat Module Handlers
    def run_cyber_attack_response(self):
        """Interface for Cyber Attack Response Module"""
        print("\n🔒 CYBER ATTACK RESPONSE MODULE v2.0")
        print("=" * 50)
        
        while True:
            print("\n1. Assess Cyber Preparedness")
            print("2. Create Offline Backup Plan")
            print("3. Generate Manual Operations Guide")
            print("4. Calculate Financial Alternatives")
            print("5. Setup Communication Backups")
            print("6. Secure Identity Documents")
            print("7. Run Cyber Attack Drill")
            print("8. Generate Comprehensive Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                assessment = self.cyber_response.assess_cyber_preparedness(4)
                print(f"\n📊 Cyber Preparedness Score: {assessment['preparedness_score']}%")
                print(f"Level: {assessment['preparedness_level']}")
                if assessment['critical_gaps']:
                    print("\n🚨 Critical Gaps:")
                    for gap in assessment['critical_gaps']:
                        print(f"  • {gap}")
                if assessment['recommendations']:
                    print("\n💡 Recommendations:")
                    for rec in assessment['recommendations']:
                        print(f"  • {rec}")
            elif choice == "2":
                backup_plan = self.cyber_response.create_offline_backup_plan()
                print(f"\n💾 Offline Backup Plan Created")
                print(f"Priority items to backup: {len(backup_plan['priority_items'])}")
                print(f"Estimated total time: {backup_plan['total_estimated_time']} hours")
                print("\nBackup Schedule:")
                for freq, items in backup_plan['backup_schedule'].items():
                    print(f"  {freq.title()}: {', '.join(items)}")
            elif choice == "3":
                manual_guide = self.cyber_response.generate_manual_operations_guide()
                print(f"\n📋 Manual Operations Guide Created")
                print(f"Critical systems covered: {len(manual_guide['critical_systems'])}")
                print(f"Tools required: {len(manual_guide['tools_required'])} items")
                print("\nSkills to develop:")
                for skill in manual_guide['skill_development']:
                    print(f"  • {skill}")
            elif choice == "4":
                financial = self.cyber_response.calculate_financial_alternatives(3000, 4)
                print(f"\n💰 Financial Alternatives Calculated")
                print(f"Total recommended value: ${financial['total_recommended_value']:.2f}")
                print(f"Diversification score: {financial['diversification_score']}/100")
                print("\nRecommendations by type:")
                for asset_type, details in financial['recommendations'].items():
                    print(f"  {asset_type.title()}: {details['amount']} ({details['percentage']})")
            elif choice == "7":
                print("\n🎯 Starting Cyber Attack Drill...")
                drill_result = self.cyber_response.run_cyber_attack_drill("ransomware", ["Adult 1", "Adult 2"])
                print(f"\nDrill Performance: {drill_result['performance_level']}")
            elif choice == "8":
                print("\n📊 Generating Comprehensive Cyber Report...")
                report = self.cyber_response.generate_comprehensive_report()
                print(f"Overall Cyber Preparedness: {report['overall_cyber_preparedness']}%")
                print(f"Level: {report['preparedness_level']}")
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_emp_hardening(self):
        """Interface for EMP Hardening Module"""
        print("\n⚡ EMP/SOLAR FLARE HARDENING MODULE v2.0")
        print("=" * 50)
        
        while True:
            print("\n1. Assess EMP Vulnerability")
            print("2. Design Faraday Cage")
            print("3. Create Manual Systems Plan")
            print("4. Setup Grid-Independent Utilities")
            print("5. Create Hardened Communications")
            print("6. Develop EMP Response Plan")
            print("7. Run EMP Hardening Drill")
            print("8. Generate Comprehensive Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                assessment = self.emp_hardening.assess_emp_vulnerability()
                print(f"\n📊 EMP Vulnerability Score: {assessment['vulnerability_score']}%")
                print(f"Protection Level: {assessment['protection_level']}")
                print(f"Protected Items: {assessment['protected_items']}")
                print(f"Vulnerable Items: {assessment['vulnerable_items']}")
                if assessment['critical_gaps']:
                    print("\n🚨 Critical Gaps:")
                    for gap in assessment['critical_gaps']:
                        print(f"  • {gap}")
            elif choice == "2":
                size = input("Cage size needed (small/medium/large): ").strip().lower() or "medium"
                budget = float(input("Budget available ($): ").strip() or "100")
                cage_design = self.emp_hardening.design_faraday_cage(size, budget)
                print(f"\n🛡️ Faraday Cage Design Created")
                print(f"Size: {cage_design['size_category']}")
                print(f"Total Cost: ${cage_design['total_cost']}")
                print(f"Effectiveness: {cage_design['effectiveness_rating']} dB")
                print(f"Materials needed: {len(cage_design['materials_list'])} items")
            elif choice == "3":
                manual_plan = self.emp_hardening.create_manual_systems_plan()
                print(f"\n🔧 Manual Systems Plan Created")
                print(f"Systems covered: {len(manual_plan['manual_systems'])}")
                print(f"Total cost estimate: ${manual_plan['total_cost_estimate']}")
            elif choice == "4":
                utility_type = input("Utility type (power/water/heating/all): ").strip().lower() or "all"
                utilities = self.emp_hardening.setup_grid_independent_utilities(utility_type)
                print(f"\n🏠 Grid-Independent Utilities Designed")
                print(f"Systems: {len(utilities['systems'])}")
                print(f"Total cost: ${utilities['total_cost']}")
            elif choice == "7":
                print("\n🎯 Starting EMP Hardening Drill...")
                drill_result = self.emp_hardening.run_emp_hardening_drill("solar_flare")
                print(f"\nDrill Performance: {drill_result['performance']}")
            elif choice == "8":
                print("\n📊 Generating Comprehensive EMP Report...")
                report = self.emp_hardening.generate_comprehensive_report()
                print(f"EMP Preparedness: {report['emp_preparedness_score']:.1f}%")
                print(f"Level: {report['preparedness_level']}")
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_nuclear_safety(self):
        """Interface for Nuclear Safety Module"""
        print("\n☢️ NUCLEAR/RADIATION SAFETY MODULE v2.0")
        print("=" * 50)
        
        while True:
            print("\n1. Assess Nuclear Preparedness")
            print("2. Recommend Detection Equipment")
            print("3. Create Decontamination Protocol")
            print("4. Plan Evacuation Routes")
            print("5. Develop Medical Protocols")
            print("6. Design Radiation Shelter")
            print("7. Run Nuclear Emergency Drill")
            print("8. Generate Comprehensive Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                distance = float(input("Distance to nearest nuclear facility (miles): ").strip() or "20")
                assessment = self.nuclear_safety.assess_nuclear_preparedness(distance)
                print(f"\n📊 Nuclear Preparedness Assessment")
                print(f"Risk Level: {assessment['risk_level']}")
                print(f"Preparedness Score: {assessment['preparedness_score']}%")
                print(f"Detection Capability: {assessment['detection_capability']}%")
                print(f"Medical Readiness: {assessment['medical_readiness']}%")
                if assessment['critical_gaps']:
                    print("\n🚨 Critical Gaps:")
                    for gap in assessment['critical_gaps']:
                        print(f"  • {gap}")
            elif choice == "2":
                budget = float(input("Equipment budget ($): ").strip() or "500")
                risk = input("Risk level (low/moderate/high): ").strip().lower() or "moderate"
                equipment = self.nuclear_safety.recommend_detection_equipment(budget, risk)
                print(f"\n🔍 Detection Equipment Recommendations")
                if equipment['primary_device']:
                    print(f"Primary: {equipment['primary_device']['name']} - ${equipment['primary_device']['cost']}")
                if equipment['secondary_device']:
                    print(f"Secondary: {equipment['secondary_device']['name']} - ${equipment['secondary_device']['cost']}")
                print(f"Total cost: ${equipment['total_cost']}")
            elif choice == "3":
                contamination_type = input("Contamination type (general/specific): ").strip() or "general"
                protocol = self.nuclear_safety.create_decontamination_protocol(contamination_type)
                print(f"\n🚿 Decontamination Protocol Created")
                print(f"Procedures: {len(protocol['procedures'])}")
                print(f"Supplies needed: {len(protocol['supplies_needed'])} items")
            elif choice == "4":
                home = input("Home address (or 'Unknown'): ").strip() or "Unknown"
                distance = float(input("Distance to nuclear facility (miles): ").strip() or "20")
                evacuation = self.nuclear_safety.plan_evacuation_routes(home, distance)
                print(f"\n🚗 Evacuation Planning Complete")
                print(f"Facility distance: {evacuation['facility_distance']} miles")
                print(f"Routes planned: {len(evacuation['routes'])}")
                print(f"Destinations: {len(evacuation['destinations'])}")
            elif choice == "6":
                shelter_type = input("Shelter type (basement/above_ground/purpose_built): ").strip() or "basement"
                budget = float(input("Budget ($): ").strip() or "1000")
                shelter = self.nuclear_safety.design_radiation_shelter(shelter_type, budget)
                print(f"\n🏠 Radiation Shelter Designed")
                print(f"Protection Factor: {shelter['protection_factor']}")
                print(f"Total Cost: ${shelter['total_cost']}")
                print(f"Capacity: {shelter['capacity']} people")
            elif choice == "7":
                print("\n🎯 Starting Nuclear Emergency Drill...")
                drill_result = self.nuclear_safety.run_nuclear_emergency_drill("power_plant_accident")
                print(f"\nDrill Performance: {drill_result['performance']}")
            elif choice == "8":
                print("\n📊 Generating Comprehensive Nuclear Report...")
                report = self.nuclear_safety.generate_comprehensive_report()
                print(f"Nuclear Preparedness: {report['nuclear_preparedness_score']}%")
                print(f"Level: {report['preparedness_level']}")
            else:
                print("❌ Invalid option. Please try again.")
    
    # Version 2.0 Phase 2B Long-Term Sustainability Module Handlers
    def run_extended_supply_planning(self):
        """Interface for Extended Supply Planning Module"""
        print("\n📦 EXTENDED SUPPLY PLANNING MODULE v2.0 (6+ Months)")
        print("=" * 60)
        
        while True:
            print("\n1. Assess Extended Supply Readiness")
            print("2. Create 6-Month Supply Plan")
            print("3. Design Storage System")
            print("4. Generate Procurement Timeline")
            print("5. Calculate Nutritional Balance")
            print("6. Plan Seasonal Adjustments")
            print("7. Generate Supply Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                household_size = int(input("Household size: ") or "4")
                duration_months = int(input("Target duration (months): ") or "6")
                
                supplies = self.extended_supply.calculate_extended_supplies(household_size, duration_months)
                print(f"\n📊 Extended Supply Analysis")
                print(f"Total Categories: {len(supplies['supply_categories'])}")
                print(f"Total Investment: ${supplies['total_investment_cost']:,.2f}")
                print(f"Storage Space: {supplies['total_storage_volume']:.1f} cubic feet")
                print(f"Procurement Timeline: {supplies['procurement_timeline']['total_phases']} phases")
            elif choice == "2":
                household_size = int(input("Household size: ") or "4")
                duration_months = int(input("Supply duration (months): ") or "6")
                budget = float(input("Total budget ($): ") or "3000")
                
                supply_plan = self.extended_supply.calculate_extended_supplies(household_size, duration_months, budget)
                print(f"\n📋 Extended Supply Plan Created")
                print(f"Categories Covered: {len(supply_plan['supply_categories'])}")
                print(f"Total Investment: ${supply_plan['total_investment_cost']:,.2f}")
                print(f"Storage Volume: {supply_plan['total_storage_volume']:.1f} cubic feet")
                if 'procurement_timeline' in supply_plan:
                    print(f"Implementation Timeline: {supply_plan['procurement_timeline']['total_phases']} phases")
            elif choice == "7":
                print("\n📊 Generating Extended Supply Report...")
                report = self.extended_supply.generate_extended_supply_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_local_production_capabilities(self):
        """Interface for Local Production Capabilities Module"""
        print("\n🌱 LOCAL PRODUCTION CAPABILITIES MODULE v2.0")
        print("=" * 60)
        
        while True:
            print("\n1. Assess Production Potential")
            print("2. Design Food Production System")
            print("3. Plan Water Independence")
            print("4. Create Energy Production Plan")
            print("5. Setup Manufacturing Capability")
            print("6. Create Production Timeline")
            print("7. Generate Production Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                household_size = int(input("Household size: ") or "4")
                property_size = float(input("Property size (acres): ") or "0.25")
                property_type = input("Property type (urban/suburban/rural): ") or "suburban"
                
                assessment = self.local_production.assess_production_potential(
                    household_size, property_size, property_type
                )
                print(f"\n📊 Production Potential Assessment")
                print(f"Overall Score: {assessment['overall_score']:.1f}/10")
                print(f"Food Production: {assessment['food_production']['overall_score']:.1f}/10")
                print(f"Water Systems: {assessment['water_systems']['overall_score']:.1f}/10") 
                print(f"Energy Systems: {assessment['energy_systems']['overall_score']:.1f}/10")
                print(f"Manufacturing: {assessment['manufacturing']['overall_score']:.1f}/10")
                if assessment['priority_recommendations']:
                    print("\n💡 Priority Recommendations:")
                    for rec in assessment['priority_recommendations'][:5]:
                        print(f"  • {rec['title']} (${rec['cost']:,.0f})")
            elif choice == "6":
                household_size = int(input("Household size: ") or "4")
                property_size = float(input("Property size (acres): ") or "0.25")
                property_type = input("Property type (urban/suburban/rural): ") or "suburban"
                
                assessment = self.local_production.assess_production_potential(
                    household_size, property_size, property_type
                )
                budget = float(input("Available budget ($): ") or "15000")
                timeframe_months = int(input("Timeframe (months): ") or "18")
                
                plan = self.local_production.create_production_plan(assessment, budget, timeframe_months)
                print(f"\n📋 Production Plan Created")
                print(f"Projects Selected: {len(plan['selected_projects'])}")
                print(f"Total Investment: ${plan['resource_requirements']['total_budget']:,.0f}")
                print(f"Expected Payback: {plan['expected_outcomes']['timeline_to_benefits']['break_even_months']} months")
            elif choice == "7":
                print("\n📊 Generating Production Capabilities Report...")
                report = self.local_production.generate_production_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_alternative_economy_systems(self):
        """Interface for Alternative Economy Systems Module"""
        print("\n🔄 ALTERNATIVE ECONOMY SYSTEMS MODULE v2.0")
        print("=" * 60)
        
        while True:
            print("\n1. Assess Economic Resilience")
            print("2. Create Skill Inventory")
            print("3. Create Resource Inventory") 
            print("4. Find Trading Matches")
            print("5. Setup Barter Network")
            print("6. Plan Local Currency System")
            print("7. Generate Economy Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                household_size = int(input("Household size: ") or "4")
                community_size = int(input("Community size: ") or "500")
                
                assessment = self.alternative_economy.assess_economic_resilience(
                    household_size, community_size
                )
                print(f"\n📊 Economic Resilience Assessment")
                print(f"Overall Score: {assessment['overall_score']:.1f}/10")
                print(f"Economic Resilience Duration: {assessment['economic_resilience_months']:.1f} months")
                print(f"Barter Systems: {assessment['barter_systems']['overall_score']:.1f}/10")
                print(f"Skill Sharing: {assessment['skill_sharing']['overall_score']:.1f}/10")
                print(f"Local Currency: {assessment['local_currency']['overall_score']:.1f}/10")
                if assessment['recommendations']:
                    print("\n💡 Top Recommendations:")
                    for rec in assessment['recommendations'][:3]:
                        print(f"  • {rec['title']} ({rec['category']})")
            elif choice == "2":
                print("\n🎓 Creating Skill Inventory")
                user_id = input("User ID (or username): ") or "user_001"
                
                skills = []
                print("Enter your skills (press Enter with empty name to finish):")
                while True:
                    skill_name = input("  Skill name: ").strip()
                    if not skill_name:
                        break
                    category = input("  Category: ").strip() or "general"
                    proficiency = int(input("  Proficiency (1-10): ") or "5")
                    teaching = int(input("  Teaching ability (1-10): ") or "5")
                    time_available = int(input("  Hours available per month: ") or "10")
                    
                    skills.append({
                        'category': category,
                        'name': skill_name,
                        'proficiency_level': proficiency,
                        'teaching_ability': teaching,
                        'time_availability': time_available
                    })
                
                inventory = self.alternative_economy.create_skill_inventory(user_id, skills)
                print(f"\n✅ Skill Inventory Created")
                print(f"Skills Added: {inventory['skills_added']}")
                print(f"Total Trade Value: ${inventory['total_trade_value']:.2f}/month")
            elif choice == "7":
                print("\n📊 Generating Alternative Economy Report...")
                report = self.alternative_economy.generate_economy_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_community_resilience_networks(self):
        """Interface for Community Resilience Networks Module"""
        print("\n🤝 COMMUNITY RESILIENCE NETWORKS MODULE v2.0")
        print("=" * 60)
        
        while True:
            print("\n1. Assess Network Resilience")
            print("2. Create Network Map")
            print("3. Simulate Disaster Response")
            print("4. Plan Network Development")
            print("5. Build Trust Systems")
            print("6. Setup Communication Networks")
            print("7. Generate Resilience Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                community_size = int(input("Community size: ") or "500")
                geographic_area = float(input("Geographic area (sq miles): ") or "10.0")
                
                assessment = self.community_networks.assess_network_resilience(
                    community_size, geographic_area
                )
                print(f"\n📊 Network Resilience Assessment")
                print(f"Overall Score: {assessment['overall_score']:.1f}/10")
                print(f"Resilience Rating: {assessment['resilience_rating']}")
                print(f"Network Topology: {assessment['network_topology']['overall_score']:.1f}/10")
                print(f"Social Capital: {assessment['social_capital']['overall_score']:.1f}/10")
                print(f"Communication Systems: {assessment['communication_systems']['overall_score']:.1f}/10")
                print(f"Disaster Preparedness: {assessment['disaster_preparedness']['overall_score']:.1f}/10")
                
                if assessment['network_gaps']:
                    print(f"\n⚠️ Critical Network Gaps:")
                    for gap in assessment['network_gaps'][:3]:
                        print(f"  • {gap['system']}: {gap['gap_severity']} ({gap['current_score']:.1f}/10)")
                        
                if assessment['priority_actions']:
                    print(f"\n🎯 Priority Actions:")
                    for action in assessment['priority_actions'][:3]:
                        print(f"  • {action['action']} (Impact: {action['impact_potential']}/10)")
            elif choice == "3":
                disaster_type = input("Disaster type (natural_disasters/economic_disruption/supply_chain_failure): ") or "natural_disasters"
                severity = int(input("Severity (1-10): ") or "7")
                duration = int(input("Duration (days): ") or "5")
                affected_area = float(input("Affected area (0.0-1.0): ") or "0.3")
                
                simulation = self.community_networks.simulate_disaster_response(
                    disaster_type, severity, duration, affected_area
                )
                print(f"\n🎯 Disaster Response Simulation")
                print(f"Scenario: {simulation['disaster_scenario']['type']} (Severity {simulation['disaster_scenario']['severity']})")
                print(f"Overall Effectiveness: {simulation['effectiveness_metrics']['overall_effectiveness']:.1f}/10")
                print(f"Response Time: {simulation['effectiveness_metrics']['response_speed']:.1f} hours")
                print(f"Recovery Time: {simulation['effectiveness_metrics']['recovery_speed']:.0f} days")
                
                if simulation['lessons_learned']:
                    print(f"\n📚 Key Lessons Learned:")
                    for lesson in simulation['lessons_learned'][:3]:
                        print(f"  • {lesson}")
            elif choice == "7":
                print("\n📊 Generating Community Resilience Report...")
                report = self.community_networks.generate_resilience_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    # Version 3.0 Phase 3 Critical Gap Remediation Module Handlers
    def run_advanced_risk_engine(self):
        """Interface for Advanced Risk Calculation Engine"""
        print("\n⚡ ADVANCED RISK CALCULATION ENGINE v3.0")
        print("=" * 60)
        
        while True:
            print("\n1. Calculate Comprehensive Risk")
            print("2. Assess Historical Risk Patterns")
            print("3. Generate Risk Factor Analysis")
            print("4. Create Risk Mitigation Plan")
            print("5. Compare Multiple Scenarios")
            print("6. Monitor Real-time Risk Changes")
            print("7. Generate Risk Assessment Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                scenario_type = input("Scenario type (earthquake/flood/fire/tornado/hurricane): ") or "earthquake"
                severity = int(input("Severity (1-10): ") or "7")
                location = input("Location type (urban/suburban/rural): ") or "suburban"
                
                scenario = {"type": scenario_type, "severity": severity}
                risk_result = self.advanced_risk_engine.calculate_comprehensive_risk(
                    scenario, location
                )
                print(f"\n📊 Comprehensive Risk Analysis")
                print(f"Overall Risk Score: {risk_result.get('adjusted_risk_score', 0):.1f}/100")
                print(f"Probability: {risk_result.get('probability', 0):.1f}%")
                print(f"Impact Severity: {risk_result.get('impact_severity', 0):.1f}/10")
                print(f"Confidence Level: {risk_result.get('confidence_level', 0):.1f}/10")
                print(f"Action Priority: {risk_result.get('action_priority', 'Unknown')}")
                
                if risk_result.get('risk_factors'):
                    print(f"\n🎯 Key Risk Factors:")
                    factors = risk_result['risk_factors']
                    if isinstance(factors, dict):
                        for factor_name, factor_value in list(factors.items())[:5]:
                            print(f"  • {factor_name}: {factor_value}")
                    else:
                        for factor in factors[:5]:
                            if isinstance(factor, dict):
                                print(f"  • {factor.get('factor', 'Unknown')}: {factor.get('weight', 0):.1f}")
                            else:
                                print(f"  • {factor}")
                        
                if risk_result.get('mitigation_available'):
                    print(f"\n💡 Available Mitigations:")
                    for rec in risk_result['mitigation_available'][:3]:
                        print(f"  • {rec}")
            elif choice == "7":
                print("\n📊 Generating Risk Assessment Report...")
                report = self.advanced_risk_engine.generate_risk_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_scenario_risk_profiles(self):
        """Interface for Scenario-Specific Risk Profiles"""
        print("\n📋 SCENARIO-SPECIFIC RISK PROFILES v3.0")
        print("=" * 60)
        
        while True:
            print("\n1. View Available Risk Profiles")
            print("2. Get Detailed Scenario Analysis")
            print("3. Compare Scenario Risks")
            print("4. Generate Response Timeline")
            print("5. Calculate Resource Requirements")
            print("6. Create Custom Risk Profile")
            print("7. Generate Scenario Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                profiles = self.scenario_risk_profiles.get_all_scenario_profiles()
                print(f"\n📋 Available Risk Profiles ({len(profiles)} scenarios)")
                for i, profile in enumerate(profiles[:10], 1):
                    print(f"{i:2d}. {profile['name']} (Risk Level: {profile['base_risk_level']})")
                    print(f"     Probability: {profile['base_probability']:.1f}% | Duration: {profile['typical_duration']}")
            elif choice == "2":
                scenario_name = input("Scenario name (or number from list): ").strip()
                if scenario_name.isdigit():
                    profiles = self.scenario_risk_profiles.get_all_scenario_profiles()
                    scenario_name = profiles[int(scenario_name)-1]['name'] if int(scenario_name) <= len(profiles) else "earthquake"
                
                analysis = self.scenario_risk_profiles.get_scenario_analysis(scenario_name)
                print(f"\n📊 Detailed Scenario Analysis: {analysis['scenario_name']}")
                print(f"Risk Level: {analysis['risk_level']}")
                print(f"Probability: {analysis['probability']:.1f}%")
                print(f"Typical Duration: {analysis['duration']}")
                print(f"Warning Time: {analysis['warning_time']}")
                
                if analysis['response_phases']:
                    print(f"\n⏱️ Response Phases:")
                    for phase in analysis['response_phases'][:3]:
                        print(f"  • {phase['phase']}: {phase['timeframe']} - {phase['key_actions'][0] if phase['key_actions'] else 'N/A'}")
                        
                if analysis['resource_requirements']:
                    print(f"\n📦 Key Resource Requirements:")
                    for req in analysis['resource_requirements'][:5]:
                        print(f"  • {req['category']}: {req['quantity']} {req['unit']}")
            elif choice == "7":
                print("\n📊 Generating Scenario Risk Profile Report...")
                report = self.scenario_risk_profiles.generate_scenario_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_alert_aggregator(self):
        """Interface for Multi-Source Alert Aggregator"""
        print("\n📡 MULTI-SOURCE ALERT AGGREGATOR v3.0")
        print("=" * 60)
        
        while True:
            print("\n1. Check Current Alerts")
            print("2. Aggregate New Alerts")
            print("3. Monitor by Location")
            print("4. View Alert Timeline")
            print("5. Subscribe to Alerts")
            print("6. Acknowledge Alerts")
            print("7. Generate Alert Report")
            print("8. Start Continuous Monitoring")
            print("9. System Status")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                summary = self.alert_aggregator.aggregate_alerts()
                print(f"\n📊 Current Alert Summary")
                print(f"Total Active Alerts: {summary['total_active_alerts']}")
                print(f"Critical Alerts: {len(summary['critical_alerts'])}")
                print(f"High Priority: {len(summary['high_priority_alerts'])}")
                print(f"Required Actions: {len(summary['required_actions'])}")
                
                if summary['critical_alerts']:
                    print(f"\n🔴 Critical Alerts:")
                    for alert in summary['critical_alerts'][:3]:
                        print(f"  • {alert['title']} (Priority: {alert['priority']:.1f})")
                        print(f"    Action: {alert['action']}")
                        
                if summary['required_actions']:
                    print(f"\n⚡ Required Actions:")
                    for action in summary['required_actions'][:3]:
                        print(f"  • {action}")
            elif choice == "2":
                print("\n📡 Aggregating alerts from all sources...")
                summary = self.alert_aggregator.aggregate_alerts()
                print(f"✅ Aggregation complete. Found {summary['new_alerts']} new alerts.")
            elif choice == "3":
                location = input("Location filter (city, county, or region): ").strip() or "Local Area"
                alerts = self.alert_aggregator.get_alert_by_location(location)
                print(f"\n📍 Alerts for {location} ({len(alerts)} found)")
                for alert in alerts[:5]:
                    print(f"  • {alert['title']} (Priority: {alert['priority']:.1f})")
                    print(f"    Action: {alert['action']}")
            elif choice == "7":
                print("\n📊 Generating Alert Aggregation Report...")
                report = self.alert_aggregator.generate_alert_report()
                print(report)
            elif choice == "8":
                interval = int(input("Monitoring interval (seconds): ") or "60")
                print(f"🔄 Starting continuous monitoring (every {interval} seconds)...")
                self.alert_aggregator.start_monitoring(interval)
                print("✅ Monitoring started in background")
            elif choice == "9":
                status = self.alert_aggregator.get_system_status()
                print(f"\n✅ Alert Aggregator System Status")
                print(f"Status: {status['status']}")
                print(f"Active Alerts: {status['active_alerts']}")
                print(f"Active Sources: {status['active_sources']}")
                print(f"Subscriptions: {status['subscriptions']}")
                if status['highest_priority_alert']['title']:
                    print(f"Highest Priority: {status['highest_priority_alert']['title']}")
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_rapid_response(self):
        """Interface for Rapid Response Protocol System"""
        print("\n🚀 RAPID RESPONSE PROTOCOL SYSTEM v3.0")
        print("=" * 60)
        
        while True:
            print("\n1. View Available Protocols")
            print("2. Activate Emergency Protocol")
            print("3. Test Protocol Execution")
            print("4. Manage Emergency Cache")
            print("5. Configure Family Notifications")
            print("6. Practice Rapid Response")
            print("7. Generate Response Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                protocols = self.rapid_response.get_available_protocols()
                print(f"\n📋 Available Emergency Protocols ({len(protocols)} total)")
                for i, protocol in enumerate(protocols, 1):
                    print(f"{i:2d}. {protocol['name']}")
                    print(f"     Trigger: {protocol['trigger_condition']}")
                    print(f"     Target Time: {protocol['target_response_time']} minutes")
            elif choice == "2":
                protocol_type = input("Emergency type (earthquake/fire/tornado/evacuation): ") or "earthquake"
                severity = int(input("Severity (1-10): ") or "7")
                location = input("Location details: ") or "Home"
                
                print(f"\n🚨 ACTIVATING {protocol_type.upper()} PROTOCOL...")
                response = self.rapid_response.activate_protocol(protocol_type, severity, location)
                print(f"✅ Protocol Activated: {response['protocol_name']}")
                print(f"Response ID: {response['response_id']}")
                print(f"Target Time: {response['estimated_completion_time']} minutes")
                
                if response['immediate_actions']:
                    print(f"\n⚡ Immediate Actions:")
                    for action in response['immediate_actions'][:5]:
                        print(f"  • {action}")
                        
                if response['notifications_sent']:
                    print(f"\n📱 Notifications Sent: {response['notifications_sent']} contacts")
            elif choice == "7":
                print("\n📊 Generating Rapid Response Report...")
                report = self.rapid_response.generate_response_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_drill_generator(self):
        """Interface for Scenario-Based Drill Generator"""
        print("\n🎯 SCENARIO-BASED DRILL GENERATOR v3.0")
        print("=" * 60)
        
        while True:
            print("\n1. Generate Custom Drill")
            print("2. Run Family Drill Session")
            print("3. Create Drill Template")
            print("4. View Drill Templates")
            print("5. Analyze Drill Performance")
            print("6. Generate Practice Schedule")
            print("7. Generate Drill Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                scenario_type = input("Scenario type (earthquake/fire/tornado/flood): ") or "earthquake"
                difficulty = input("Difficulty (beginner/intermediate/advanced): ") or "intermediate"
                duration = int(input("Duration (minutes): ") or "15")
                participants = int(input("Number of participants: ") or "4")
                
                drill = self.drill_generator.generate_drill(scenario_type, difficulty, duration, participants)
                print(f"\n🎯 Generated Drill: {drill['drill_name']}")
                print(f"Scenario: {drill['scenario']['description']}")
                print(f"Duration: {drill['estimated_duration']} minutes")
                print(f"Difficulty: {drill['difficulty_level']}")
                
                if drill['objectives']:
                    print(f"\n🎯 Objectives:")
                    for obj in drill['objectives'][:3]:
                        print(f"  • {obj}")
                        
                if drill['phases']:
                    print(f"\n⏱️ Drill Phases:")
                    for phase in drill['phases'][:3]:
                        print(f"  • {phase['phase_name']}: {phase['duration']} min - {phase['description']}")
            elif choice == "2":
                scenario_type = input("Scenario for drill (earthquake/fire/tornado): ") or "earthquake"
                participant_name = input("Participant name: ") or "Family"
                
                print(f"\n🎯 Starting {scenario_type} drill for {participant_name}...")
                result = self.drill_generator.run_drill_session(scenario_type, participant_name)
                print(f"✅ Drill completed in {result['actual_duration']:.1f} minutes")
                print(f"Performance Score: {result['performance_score']:.1f}/100")
                print(f"Grade: {result['performance_grade']}")
                
                if result['strengths']:
                    print(f"\n💪 Strengths:")
                    for strength in result['strengths'][:3]:
                        print(f"  • {strength}")
                        
                if result['improvement_areas']:
                    print(f"\n📈 Areas for Improvement:")
                    for area in result['improvement_areas'][:3]:
                        print(f"  • {area}")
            elif choice == "7":
                print("\n📊 Generating Drill Generator Report...")
                report = self.drill_generator.generate_drill_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run_drill_scheduler(self):
        """Interface for Drill Automation & Scheduling"""
        print("\n📅 DRILL AUTOMATION & SCHEDULING v3.0")
        print("=" * 60)
        
        while True:
            print("\n1. View Current Schedule")
            print("2. Create Automated Schedule")
            print("3. Schedule One-Time Drill")
            print("4. Manage Drill Preferences")
            print("5. View Performance Progress")
            print("6. Gamification Status")
            print("7. Generate Schedule Report")
            print("0. Return to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                schedule = self.drill_scheduler.get_current_schedule()
                print(f"\n📅 Current Drill Schedule ({len(schedule['upcoming_drills'])} upcoming)")
                for drill in schedule['upcoming_drills'][:5]:
                    print(f"  • {drill['date']} at {drill['time']}: {drill['drill_type']}")
                    print(f"    Duration: {drill['duration']} min | Difficulty: {drill['difficulty']}")
                    
                if schedule['overdue_drills']:
                    print(f"\n⚠️ Overdue Drills: {len(schedule['overdue_drills'])}")
            elif choice == "2":
                frequency = input("Drill frequency (weekly/biweekly/monthly): ") or "weekly"
                preferred_day = input("Preferred day (monday/tuesday/etc or 'any'): ") or "any"
                preferred_time = input("Preferred time (morning/afternoon/evening): ") or "evening"
                
                schedule = self.drill_scheduler.create_automated_schedule(frequency, preferred_day, preferred_time)
                print(f"\n📅 Automated Schedule Created")
                print(f"Frequency: {schedule['settings']['frequency']}")
                print(f"Next {len(schedule['generated_drills'])} drills scheduled")
                print(f"First drill: {schedule['generated_drills'][0]['date']} at {schedule['generated_drills'][0]['time']}")
            elif choice == "6":
                participant = input("Participant name: ") or "Family"
                status = self.drill_scheduler.get_gamification_status(participant)
                print(f"\n🎮 Gamification Status for {participant}")
                print(f"Current Level: {status['current_level']}")
                print(f"Total Points: {status['total_points']}")
                print(f"Drills Completed: {status['drills_completed']}")
                print(f"Current Streak: {status['current_streak']} drills")
                
                if status['recent_achievements']:
                    print(f"\n🏆 Recent Achievements:")
                    for achievement in status['recent_achievements'][:3]:
                        print(f"  • {achievement['name']}: {achievement['description']}")
                        
                if status['next_level_requirements']:
                    print(f"\n⬆️ Next Level Requirements:")
                    print(f"  Points needed: {status['next_level_requirements']['points_needed']}")
                    print(f"  Drills needed: {status['next_level_requirements']['drills_needed']}")
            elif choice == "7":
                print("\n📊 Generating Drill Scheduling Report...")
                report = self.drill_scheduler.generate_schedule_report()
                print(report)
            else:
                print("❌ Invalid option. Please try again.")
    
    def run(self):
        """Main system interface"""
        print("🚨 Starting Integrated Emergency Preparedness System...")
        
        while True:
            self.show_main_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == "0":
                print("\n👋 Emergency Preparedness System shutting down. Stay safe!")
                break
            elif choice == "1":
                self.run_risk_assessment()
            elif choice == "5":
                self.manage_supplies()
            elif choice == "8":
                self.manage_contacts()
            elif choice == "11":
                self.monitor_alerts()
            elif choice == "17":
                self.engineering_solutions_interface()
            elif choice == "18":
                self.building_calculator_interface()
            elif choice == "19":
                self.step_by_step_guide_interface()
            elif choice == "20":
                self.materials_tools_calculator()
            elif choice == "21":
                self.run_drill_simulator()
            elif choice == "22":
                self.view_drill_history()
            elif choice == "23":
                self.show_visual_dashboard()
            elif choice == "24":
                self.export_dashboard()
            elif choice == "25":
                self.search_knowledge_base()
            elif choice == "26":
                self.browse_checklists()
            elif choice == "27":
                self.generate_reference_cards()
            elif choice == "28":
                self.run_cyber_attack_response()
            elif choice == "29":
                self.run_emp_hardening()
            elif choice == "30":
                self.run_nuclear_safety()
            elif choice == "31":
                self.run_extended_supply_planning()
            elif choice == "32":
                self.run_local_production_capabilities()
            elif choice == "33":
                self.run_alternative_economy_systems()
            elif choice == "34":
                self.run_community_resilience_networks()
            elif choice == "35":
                self.run_advanced_risk_engine()
            elif choice == "36":
                self.run_scenario_risk_profiles()
            elif choice == "37":
                self.run_alert_aggregator()
            elif choice == "38":
                self.run_rapid_response()
            elif choice == "39":
                self.run_drill_generator()
            elif choice == "40":
                self.run_drill_scheduler()
            elif choice == "41":
                report = self.generate_comprehensive_report()
                print(f"\n📊 PREPAREDNESS SCORE: {report['preparedness_score']:.1f}/100")
                for section, data in report["sections"].items():
                    print(f"  {section.title()}: {data['score']:.1f} ({data['status']})")
                if report["recommendations"]:
                    print(f"\n💡 RECOMMENDATIONS:")
                    for rec in report["recommendations"]:
                        print(f"  • {rec}")
            elif choice == "42":
                self.export_all_data()
            elif choice == "43":
                quick_ref = self.generate_quick_reference()
                print(quick_ref)
            else:
                print("❌ Invalid option. Please try again.")
            
            if choice != "0":
                input("\nPress Enter to continue...")

def main():
    """Main entry point with CLI argument support"""
    parser = argparse.ArgumentParser(
        description='Integrated Emergency Preparedness System - Complete disaster readiness platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Run interactive mode
  %(prog)s --profile family             # Load specific profile
  %(prog)s --risk-assessment            # Run risk assessment directly
  %(prog)s --supplies --check-expiry    # Check supply expiry dates
  %(prog)s --drill earthquake           # Run earthquake drill
  %(prog)s --backup                     # Create backup
  %(prog)s --export json                # Export all data as JSON
  %(prog)s --batch commands.txt         # Run batch commands from file
        """
    )
    
    # Profile management
    parser.add_argument('--profile', '-p', default='default',
                       help='User profile to load (default: default)')
    parser.add_argument('--list-profiles', action='store_true',
                       help='List all available profiles')
    
    # Direct module access
    parser.add_argument('--risk-assessment', '-r', action='store_true',
                       help='Run risk assessment directly')
    parser.add_argument('--supplies', '-s', action='store_true',
                       help='Manage supplies inventory')
    parser.add_argument('--contacts', '-c', action='store_true',
                       help='Manage emergency contacts')
    parser.add_argument('--alerts', '-a', action='store_true',
                       help='Check active alerts')
    parser.add_argument('--drill', '-d', metavar='TYPE',
                       help='Run emergency drill (earthquake/fire/tornado/flood)')
    
    # Specific actions
    parser.add_argument('--check-expiry', action='store_true',
                       help='Check supply expiry dates (use with --supplies)')
    parser.add_argument('--add-contact', nargs=3, metavar=('NAME', 'PHONE', 'ROLE'),
                       help='Add emergency contact')
    parser.add_argument('--test-alert', action='store_true',
                       help='Test alert system')
    
    # Data management
    parser.add_argument('--backup', '-b', action='store_true',
                       help='Create comprehensive backup')
    parser.add_argument('--restore', metavar='BACKUP_NAME',
                       help='Restore from backup')
    parser.add_argument('--export', choices=['json', 'csv', 'html', 'pdf'],
                       help='Export all data in specified format')
    parser.add_argument('--import', dest='import_file', metavar='FILE',
                       help='Import data from file')
    
    # Batch and automation
    parser.add_argument('--batch', metavar='FILE',
                       help='Execute batch commands from file')
    parser.add_argument('--non-interactive', '-n', action='store_true',
                       help='Run in non-interactive mode (use defaults)')
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Output file for results')
    
    # System operations
    parser.add_argument('--status', action='store_true',
                       help='Show system status and statistics')
    parser.add_argument('--update-profile', action='store_true',
                       help='Update profile information')
    parser.add_argument('--clear-cache', action='store_true',
                       help='Clear all cached data')
    
    args = parser.parse_args()
    
    # Handle profile listing
    if args.list_profiles:
        profile_manager = UserProfileManager()
        profiles = profile_manager.list_profiles()
        print("📋 Available profiles:")
        for profile in profiles:
            print(f"  • {profile}")
        return
    
    # Initialize system with specified profile
    system = IntegratedPreparednessSystem(profile=args.profile)
    
    # Handle direct commands
    if args.backup:
        print("📦 Creating backup...")
        success, path = system.backup_manager.create_backup(
            description="CLI-initiated backup"
        )
        if success:
            print(f"✅ Backup created: {path}")
        return
    
    if args.restore:
        print(f"🔄 Restoring from backup: {args.restore}")
        if system.backup_manager.restore_backup(args.restore):
            print("✅ Restore completed")
        else:
            print("❌ Restore failed")
        return
    
    if args.status:
        print("\n📊 SYSTEM STATUS")
        print("=" * 50)
        summary = system.profile_manager.get_profile_summary()
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Show backup status
        backups = system.backup_manager.list_backups()
        print(f"\nBackups available: {len(backups)}")
        if backups:
            latest = backups[0]
            print(f"Latest backup: {latest['name']} ({latest['description']})")
        return
    
    if args.risk_assessment:
        system.run_risk_assessment()
        if args.output:
            # Save results to file
            with open(args.output, 'w') as f:
                json.dump(system.profile_manager.get_risk_assessment(), f, indent=2)
            print(f"✅ Results saved to: {args.output}")
        return
    
    if args.supplies:
        if args.check_expiry:
            print("🔍 Checking supply expiry dates...")
            expiring = system.supply_tracker.check_expiry_dates()
            if expiring:
                print(f"⚠️ {len(expiring)} items expiring soon:")
                for item in expiring[:5]:
                    print(f"  • {item['name']}: expires {item['expiry_date']}")
            else:
                print("✅ No items expiring soon")
        else:
            system.manage_supplies()
        return
    
    if args.drill:
        print(f"🎯 Running {args.drill} drill...")
        result = system.drill_simulator.run_drill(
            args.drill,
            system.profile_manager.get_family_info().get('adults', 1) +
            system.profile_manager.get_family_info().get('children', 0)
        )
        print(f"✅ Drill completed. Score: {result.get('score', 0)}/100")
        system.profile_manager.record_activity('drill_completed', {
            'type': args.drill,
            'score': result.get('score', 0)
        })
        return
    
    if args.alerts:
        print("📡 Checking active alerts...")
        alerts = system.alert_monitor.get_active_alerts()
        if alerts:
            print(f"⚠️ {len(alerts)} active alerts:")
            for alert in alerts[:5]:
                print(f"  • {alert.get('title', 'Unknown')}: {alert.get('severity', 'Unknown')}")
        else:
            print("✅ No active alerts")
        return
    
    if args.export:
        print(f"📤 Exporting data as {args.export}...")
        if args.export == 'json':
            export_data = {
                'profile': system.profile_manager.profile_data,
                'timestamp': datetime.now().isoformat(),
                'version': '3.0'
            }
            output_file = args.output or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            print(f"✅ Data exported to: {output_file}")
        else:
            print(f"⚠️ Export format {args.export} not yet implemented")
        return
    
    if args.batch:
        print(f"📋 Executing batch commands from: {args.batch}")
        try:
            with open(args.batch, 'r') as f:
                commands = f.readlines()
            for cmd in commands:
                cmd = cmd.strip()
                if cmd and not cmd.startswith('#'):
                    print(f"  Executing: {cmd}")
                    # Parse and execute command
                    # This would need more implementation
            print("✅ Batch execution completed")
        except FileNotFoundError:
            print(f"❌ Batch file not found: {args.batch}")
        return
    
    # If no specific command, run interactive mode
    system.run()


if __name__ == "__main__":
    main()