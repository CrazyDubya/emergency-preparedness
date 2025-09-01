#!/usr/bin/env python3
"""
Alternative Economy Systems Module - Version 2.0 Phase 2B
Enables economic resilience through barter systems, local currencies, 
skill sharing networks, and resource exchange platforms for disaster preparedness.
"""

import sqlite3
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional

class AlternativeEconomySystems:
    """
    Manages assessment and implementation of alternative economic systems
    for long-term disaster preparedness and community economic resilience.
    """
    
    def __init__(self, db_path: str = "alternative_economy.db"):
        """Initialize the Alternative Economy Systems module."""
        self.db_path = db_path
        self.initialize_database()
        
        # Standard skill categories and their economic values
        self.skill_categories = {
            'medical': {'base_value': 100, 'demand_multiplier': 3.0},
            'mechanical': {'base_value': 50, 'demand_multiplier': 2.5},
            'electrical': {'base_value': 60, 'demand_multiplier': 2.3},
            'construction': {'base_value': 45, 'demand_multiplier': 2.2},
            'food_production': {'base_value': 40, 'demand_multiplier': 2.8},
            'food_preservation': {'base_value': 35, 'demand_multiplier': 2.0},
            'textile_craft': {'base_value': 30, 'demand_multiplier': 1.8},
            'education': {'base_value': 40, 'demand_multiplier': 1.5},
            'childcare': {'base_value': 25, 'demand_multiplier': 2.0},
            'security': {'base_value': 55, 'demand_multiplier': 2.7},
            'communications': {'base_value': 45, 'demand_multiplier': 2.1},
            'transportation': {'base_value': 40, 'demand_multiplier': 1.9}
        }
        
        # Resource categories for barter systems
        self.resource_categories = {
            'food_staples': {'durability_months': 6, 'value_per_lb': 3},
            'preserved_food': {'durability_months': 24, 'value_per_lb': 8},
            'fuel': {'durability_months': 12, 'value_per_gallon': 4},
            'medical_supplies': {'durability_months': 36, 'value_per_unit': 15},
            'tools': {'durability_months': 120, 'value_per_unit': 25},
            'electronics': {'durability_months': 60, 'value_per_unit': 50},
            'clothing': {'durability_months': 24, 'value_per_item': 20},
            'seeds': {'durability_months': 18, 'value_per_packet': 5},
            'raw_materials': {'durability_months': 240, 'value_per_lb': 2}
        }
    
    def initialize_database(self):
        """Create necessary database tables for alternative economy tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Economic systems assessments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS economy_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_date TEXT NOT NULL,
                household_size INTEGER NOT NULL,
                community_size INTEGER,
                assessment_data TEXT,
                overall_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Skill inventories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_inventories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                skill_category TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                proficiency_level INTEGER,
                teaching_ability INTEGER,
                time_availability INTEGER,
                trade_value REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Resource inventories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resource_inventories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                resource_category TEXT NOT NULL,
                resource_name TEXT NOT NULL,
                quantity REAL,
                unit TEXT,
                condition_score INTEGER,
                trade_value REAL,
                expiration_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Barter transactions log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS barter_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                party_a_user_id TEXT,
                party_b_user_id TEXT,
                items_offered TEXT,
                items_received TEXT,
                transaction_value REAL,
                satisfaction_rating INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Local currency systems
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS local_currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_name TEXT NOT NULL,
                currency_type TEXT,
                initial_supply INTEGER,
                backing_assets TEXT,
                exchange_rate REAL,
                circulation_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Community networks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_name TEXT NOT NULL,
                network_type TEXT,
                member_count INTEGER,
                activity_level INTEGER,
                network_data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def assess_economic_resilience(self, household_size: int, 
                                 community_size: int = 500) -> Dict[str, Any]:
        """
        Comprehensive assessment of alternative economic system potential
        and current preparedness level.
        """
        
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'household_size': household_size,
            'community_size': community_size,
            'barter_systems': self._assess_barter_potential(household_size, community_size),
            'skill_sharing': self._assess_skill_sharing_potential(household_size, community_size),
            'local_currency': self._assess_local_currency_potential(community_size),
            'resource_networks': self._assess_resource_networks(household_size, community_size),
            'mutual_aid': self._assess_mutual_aid_systems(community_size),
            'alternative_markets': self._assess_alternative_markets(community_size),
            'overall_score': 0,
            'economic_resilience_months': 0,
            'recommendations': []
        }
        
        # Calculate overall economic resilience score
        subsystem_scores = [
            assessment['barter_systems']['overall_score'],
            assessment['skill_sharing']['overall_score'],
            assessment['local_currency']['overall_score'],
            assessment['resource_networks']['overall_score'],
            assessment['mutual_aid']['overall_score'],
            assessment['alternative_markets']['overall_score']
        ]
        
        assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        # Calculate economic resilience duration
        assessment['economic_resilience_months'] = self._calculate_economic_resilience_duration(assessment)
        
        # Generate specific recommendations
        assessment['recommendations'] = self._generate_economic_recommendations(assessment)
        
        # Store assessment in database
        self._store_assessment(assessment)
        
        return assessment
    
    def _assess_barter_potential(self, household_size: int, community_size: int) -> Dict[str, Any]:
        """Assess potential for barter trade systems."""
        
        barter_assessment = {
            'tradeable_resources': {},
            'skill_offerings': {},
            'trading_networks': {},
            'valuation_systems': {},
            'storage_capacity': {},
            'market_dynamics': {},
            'overall_score': 0
        }
        
        # Assess tradeable resources potential
        barter_assessment['tradeable_resources'] = {
            'food_surplus': {
                'production_capacity': household_size * 50,  # lbs per person surplus potential
                'preservation_capability': 0.7,  # 70% can be preserved for trade
                'seasonal_availability': 8,  # months per year
                'trade_value_annual': household_size * 50 * 0.7 * 3,  # $3/lb preserved food
                'score': 7
            },
            'manufactured_goods': {
                'craft_capability': household_size * 10,  # items per person annually  
                'skill_diversity': 0.6,  # 60% skill coverage
                'quality_rating': 7,
                'trade_value_annual': household_size * 10 * 20,  # $20 per item
                'score': 6
            },
            'services': {
                'labor_hours_available': household_size * 500,  # hours per person annually
                'skill_premium': 1.5,  # 50% premium for specialized skills
                'availability_consistency': 0.8,
                'trade_value_annual': household_size * 500 * 25,  # $25/hour average
                'score': 8
            },
            'raw_materials': {
                'collection_capability': household_size * 200,  # lbs per person
                'processing_ability': 0.4,  # 40% can be processed to higher value
                'storage_capacity': household_size * 100,  # lbs storage per person
                'trade_value_annual': household_size * 200 * 2,  # $2/lb raw materials
                'score': 5
            }
        }
        
        # Assess skill offerings
        skill_value_total = 0
        for skill, data in self.skill_categories.items():
            skill_hours = household_size * 100  # 100 hours per skill per person
            skill_value = skill_hours * data['base_value'] * data['demand_multiplier'] / 100
            skill_value_total += skill_value
        
        barter_assessment['skill_offerings'] = {
            'total_skills': len(self.skill_categories),
            'skill_coverage': 0.6,  # 60% of skills available
            'skill_depth': 6.5,  # Average proficiency level 1-10
            'teaching_capability': 0.4,  # 40% can teach skills
            'annual_trade_value': skill_value_total * 0.6,
            'score': 7
        }
        
        # Trading networks assessment
        network_reach = min(community_size, 2000)  # Effective network size capped at 2000
        barter_assessment['trading_networks'] = {
            'local_network_size': network_reach,
            'network_density': min(network_reach / 100, 10),  # Connections per person
            'trust_level': 6.5,  # Trust score 1-10
            'communication_systems': 7,  # Effectiveness of communication
            'geographic_reach_miles': min(network_reach / 10, 50),
            'transaction_frequency': 12,  # Transactions per year
            'score': network_reach / 200  # Higher community size = better networks
        }
        
        # Valuation systems
        barter_assessment['valuation_systems'] = {
            'standardized_pricing': 0.3,  # 30% standardization
            'quality_assessment': 0.6,  # Quality grading systems
            'dispute_resolution': 0.4,  # Dispute resolution mechanisms
            'record_keeping': 0.5,  # Transaction record systems
            'trust_mechanisms': 0.7,  # Reputation and trust systems
            'score': 5
        }
        
        # Storage and preservation capacity
        storage_multiplier = 1.5 if household_size >= 4 else 1.0
        barter_assessment['storage_capacity'] = {
            'dry_goods_capacity_lbs': household_size * 500 * storage_multiplier,
            'refrigeration_capacity': household_size * 20,  # cubic feet
            'tool_storage_items': household_size * 50,
            'raw_materials_capacity': household_size * 200,
            'preservation_systems': 6,  # Effectiveness score
            'inventory_management': 5,  # Organization score
            'score': 6
        }
        
        # Market dynamics and efficiency
        market_efficiency = min((community_size / 1000) * 8, 8)  # Efficiency improves with size
        barter_assessment['market_dynamics'] = {
            'market_liquidity': market_efficiency,
            'price_discovery': market_efficiency * 0.8,
            'transaction_costs': 10 - (market_efficiency * 0.5),  # Lower is better
            'market_access': market_efficiency * 1.1,
            'seasonal_stability': 6,
            'economic_diversity': min(community_size / 100, 10),
            'score': market_efficiency
        }
        
        # Calculate overall barter system score
        subsystem_scores = []
        for category in ['tradeable_resources', 'skill_offerings', 'trading_networks', 
                        'valuation_systems', 'storage_capacity', 'market_dynamics']:
            if category == 'tradeable_resources':
                # Average the resource subcategory scores
                resource_scores = [barter_assessment[category][k]['score'] 
                                 for k in barter_assessment[category]]
                subsystem_scores.append(sum(resource_scores) / len(resource_scores))
            else:
                subsystem_scores.append(barter_assessment[category]['score'])
        
        barter_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return barter_assessment
    
    def _assess_skill_sharing_potential(self, household_size: int, community_size: int) -> Dict[str, Any]:
        """Assess potential for skill sharing networks."""
        
        skill_assessment = {
            'available_skills': {},
            'skill_gaps': {},
            'teaching_capacity': {},
            'learning_systems': {},
            'skill_exchange': {},
            'knowledge_preservation': {},
            'overall_score': 0
        }
        
        # Assess available skills across categories
        total_skill_value = 0
        skills_available = 0
        
        for skill_category, skill_data in self.skill_categories.items():
            # Estimate skill availability based on household size and community size
            household_has_skill = min(household_size * 0.3, 1.0)  # 30% chance per person
            community_availability = min(community_size * 0.1, 50)  # 10% have each skill, max 50
            
            skill_level = 5 + (community_size / 200)  # Skill level improves with community size
            skill_level = min(skill_level, 9)
            
            annual_value = skill_data['base_value'] * skill_data['demand_multiplier'] * skill_level
            
            skill_assessment['available_skills'][skill_category] = {
                'household_availability': household_has_skill,
                'community_practitioners': community_availability,
                'average_skill_level': skill_level,
                'demand_level': skill_data['demand_multiplier'],
                'annual_economic_value': annual_value,
                'teaching_potential': community_availability * 0.3,  # 30% can teach
                'score': min(community_availability / 10, 10)
            }
            
            total_skill_value += annual_value
            if community_availability > 5:  # At least 5 practitioners
                skills_available += 1
        
        # Assess skill gaps - what's missing
        critical_skills = ['medical', 'mechanical', 'electrical', 'food_production', 'security']
        skill_assessment['skill_gaps'] = {
            'critical_gaps': [skill for skill in critical_skills 
                            if skill_assessment['available_skills'][skill]['community_practitioners'] < 10],
            'gap_severity': 10 - skills_available,  # How many skills are missing
            'gap_impact': sum([self.skill_categories[skill]['demand_multiplier'] 
                             for skill in critical_skills 
                             if skill_assessment['available_skills'][skill]['community_practitioners'] < 10]),
            'training_priority': critical_skills,
            'score': min(skills_available, 10)
        }
        
        # Teaching and mentorship capacity
        total_teachers = sum([skill_assessment['available_skills'][skill]['teaching_potential'] 
                            for skill in skill_assessment['available_skills']])
        
        skill_assessment['teaching_capacity'] = {
            'total_teachers': total_teachers,
            'student_teacher_ratio': community_size / max(total_teachers, 1),
            'teaching_effectiveness': 7,  # Average teaching quality
            'knowledge_transfer_rate': min(total_teachers / community_size * 100, 10),
            'mentorship_programs': 0.4,  # 40% formal mentorship
            'skill_certification': 0.3,  # 30% have certification systems
            'score': min(total_teachers / (community_size * 0.05), 10)  # 5% should be teachers
        }
        
        # Learning systems and infrastructure
        skill_assessment['learning_systems'] = {
            'formal_training': 0.3,  # 30% have formal training programs
            'apprenticeship_systems': 0.4,  # 40% have apprenticeships
            'knowledge_repositories': 0.5,  # 50% have organized knowledge systems
            'practical_workshops': 0.6,  # 60% have workshop spaces
            'learning_materials': 0.4,  # 40% have adequate learning materials
            'assessment_systems': 0.3,  # 30% have skill assessment
            'score': 4.5  # Average of above percentages * 10
        }
        
        # Skill exchange mechanisms
        skill_assessment['skill_exchange'] = {
            'time_banking': 0.2,  # 20% participate in time banking
            'skill_swaps': 0.4,  # 40% participate in skill swapping
            'community_workshops': 0.5,  # 50% have community workshops
            'online_platforms': 0.3,  # 30% use online skill sharing
            'skill_currencies': 0.1,  # 10% use skill-based currencies
            'exchange_efficiency': 6,  # How well skill exchanges work
            'score': 3.5  # Average participation * 10
        }
        
        # Knowledge preservation and continuity
        skill_assessment['knowledge_preservation'] = {
            'documentation_systems': 0.4,  # 40% document knowledge
            'video_libraries': 0.3,  # 30% have video documentation
            'written_manuals': 0.6,  # 60% have written guides
            'master_craftsman_programs': 0.2,  # 20% have master programs
            'knowledge_redundancy': 0.5,  # 50% have multiple knowledge sources
            'intergenerational_transfer': 0.7,  # 70% transfer to next generation
            'score': 5.1  # Average preservation * 10
        }
        
        # Calculate overall skill sharing score
        subsystem_scores = [
            min(skills_available, 10),  # Available skills score
            skill_assessment['skill_gaps']['score'],
            skill_assessment['teaching_capacity']['score'],
            skill_assessment['learning_systems']['score'],
            skill_assessment['skill_exchange']['score'],
            skill_assessment['knowledge_preservation']['score']
        ]
        
        skill_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return skill_assessment
    
    def _assess_local_currency_potential(self, community_size: int) -> Dict[str, Any]:
        """Assess potential for local currency systems."""
        
        currency_assessment = {
            'currency_types': {},
            'implementation_readiness': {},
            'economic_backing': {},
            'circulation_systems': {},
            'acceptance_potential': {},
            'regulatory_environment': {},
            'overall_score': 0
        }
        
        # Different types of local currencies and their suitability
        currency_types = {
            'time_banking': {
                'complexity': 3,
                'trust_required': 6,
                'economic_impact': 7,
                'implementation_cost': 2,
                'community_size_min': 50,
                'suitability_score': 8 if community_size >= 50 else 3
            },
            'local_exchange_trading': {
                'complexity': 5,
                'trust_required': 7,
                'economic_impact': 8,
                'implementation_cost': 4,
                'community_size_min': 200,
                'suitability_score': 8 if community_size >= 200 else 4
            },
            'mutual_credit': {
                'complexity': 7,
                'trust_required': 8,
                'economic_impact': 9,
                'implementation_cost': 3,
                'community_size_min': 100,
                'suitability_score': 9 if community_size >= 100 else 3
            },
            'commodity_backed': {
                'complexity': 6,
                'trust_required': 5,
                'economic_impact': 8,
                'implementation_cost': 7,
                'community_size_min': 300,
                'suitability_score': 7 if community_size >= 300 else 2
            },
            'gift_economy': {
                'complexity': 2,
                'trust_required': 9,
                'economic_impact': 6,
                'implementation_cost': 1,
                'community_size_min': 20,
                'suitability_score': 7 if community_size >= 20 else 5
            }
        }
        
        currency_assessment['currency_types'] = currency_types
        
        # Implementation readiness factors
        currency_assessment['implementation_readiness'] = {
            'community_cohesion': min(community_size / 100, 10),  # Larger communities may be less cohesive
            'leadership_capability': min(community_size / 200, 8),
            'technical_expertise': min(community_size / 150, 7),
            'financial_literacy': 6,  # Average financial understanding
            'organizational_capacity': min(community_size / 100, 9),
            'startup_resources': community_size / 100,  # Resources available for startup
            'score': min(community_size / 100, 8)
        }
        
        # Economic backing and stability
        local_economy_strength = min(community_size / 200, 10)
        currency_assessment['economic_backing'] = {
            'local_business_participation': local_economy_strength * 0.4,
            'resource_diversity': local_economy_strength * 0.8,
            'production_capacity': local_economy_strength * 0.7,
            'service_sector_strength': local_economy_strength * 0.6,
            'agricultural_base': local_economy_strength * 0.9,
            'external_dependency': 10 - local_economy_strength,  # Lower is better
            'score': local_economy_strength
        }
        
        # Circulation and transaction systems
        currency_assessment['circulation_systems'] = {
            'digital_infrastructure': 0.6,  # 60% have adequate digital systems
            'physical_exchange_points': min(community_size / 200, 5),
            'transaction_recording': 0.4,  # 40% have transaction recording
            'account_management': 0.3,  # 30% have account management systems
            'mobile_payment_capability': 0.5,  # 50% can use mobile payments
            'offline_resilience': 0.7,  # 70% can operate offline
            'score': 5
        }
        
        # Community acceptance potential
        currency_assessment['acceptance_potential'] = {
            'cultural_openness': 6,  # Openness to new economic systems
            'cooperative_history': 5,  # History of cooperation
            'trust_in_institutions': 4,  # Lower trust may increase acceptance
            'economic_stress': 7,  # Higher stress increases acceptance
            'age_demographics': 6,  # Younger populations more accepting
            'education_level': 6,  # Higher education increases acceptance
            'score': 6
        }
        
        # Regulatory environment
        currency_assessment['regulatory_environment'] = {
            'legal_clarity': 4,  # Low clarity on local currency laws
            'tax_implications': 3,  # Unclear tax treatment
            'banking_regulations': 5,  # Some regulatory constraints
            'local_government_support': 6,  # Moderate local government support
            'federal_restrictions': 4,  # Some federal restrictions
            'compliance_costs': 6,  # Moderate compliance costs
            'score': 5
        }
        
        # Calculate overall local currency score
        subsystem_scores = [
            max([currency_types[ct]['suitability_score'] for ct in currency_types]),  # Best currency type
            currency_assessment['implementation_readiness']['score'],
            currency_assessment['economic_backing']['score'],
            currency_assessment['circulation_systems']['score'],
            currency_assessment['acceptance_potential']['score'],
            currency_assessment['regulatory_environment']['score']
        ]
        
        currency_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return currency_assessment
    
    def _assess_resource_networks(self, household_size: int, community_size: int) -> Dict[str, Any]:
        """Assess resource sharing and pooling networks."""
        
        resource_assessment = {
            'resource_pools': {},
            'sharing_systems': {},
            'distribution_networks': {},
            'inventory_management': {},
            'access_equity': {},
            'sustainability': {},
            'overall_score': 0
        }
        
        # Resource pooling potential by category
        for resource_cat, resource_data in self.resource_categories.items():
            pool_capacity = community_size * household_size * 10  # Base capacity
            sharing_efficiency = min(community_size / 200, 1.0)  # Efficiency improves with size
            
            resource_assessment['resource_pools'][resource_cat] = {
                'total_pool_capacity': pool_capacity,
                'sharing_efficiency': sharing_efficiency,
                'durability_months': resource_data['durability_months'],
                'economic_value': pool_capacity * resource_data.get('value_per_lb', 
                                                                  resource_data.get('value_per_gallon',
                                                                                  resource_data.get('value_per_unit', 
                                                                                                  resource_data.get('value_per_item', 1)))),
                'access_fairness': 7,  # Fairness of access
                'replenishment_rate': 0.8,  # How well pool is replenished
                'score': 6 + sharing_efficiency * 2  # Higher efficiency = higher score
            }
        
        # Sharing systems and mechanisms
        resource_assessment['sharing_systems'] = {
            'tool_libraries': {
                'participation_rate': 0.4,  # 40% participate
                'tool_variety': community_size / 20,  # More people = more tools
                'usage_efficiency': 0.7,  # 70% utilization rate
                'maintenance_quality': 6,
                'score': min(community_size / 50, 8)
            },
            'seed_libraries': {
                'participation_rate': 0.3,
                'seed_variety': community_size / 10,
                'success_rate': 0.8,  # 80% germination success
                'genetic_diversity': 7,
                'score': min(community_size / 100, 7)
            },
            'equipment_sharing': {
                'participation_rate': 0.5,
                'equipment_value': community_size * 1000,  # $1000 per person in shared equipment
                'coordination_effectiveness': 6,
                'conflict_resolution': 5,
                'score': min(community_size / 100, 8)
            },
            'bulk_purchasing': {
                'participation_rate': 0.6,
                'cost_savings_percent': 25,
                'coordination_quality': 7,
                'distribution_efficiency': 6,
                'score': min(community_size / 75, 9)
            }
        }
        
        # Distribution networks
        network_efficiency = min(community_size / 300, 1.0)
        resource_assessment['distribution_networks'] = {
            'physical_distribution': {
                'distribution_points': community_size / 100,
                'coverage_area_sq_miles': community_size / 50,
                'delivery_capability': network_efficiency * 8,
                'storage_capacity': community_size * 50,  # lbs per person
                'score': network_efficiency * 8
            },
            'information_systems': {
                'inventory_tracking': 0.4,  # 40% have inventory tracking
                'needs_communication': 0.6,  # 60% can communicate needs
                'allocation_algorithms': 0.2,  # 20% use allocation algorithms
                'real_time_updates': 0.3,  # 30% have real-time updates
                'score': 4
            },
            'transportation': {
                'vehicle_availability': community_size / 200,  # Vehicles per person
                'fuel_independence': 0.3,  # 30% fuel independent
                'route_optimization': 0.4,  # 40% optimize routes
                'backup_systems': 0.5,  # 50% have backup transportation
                'score': 5
            }
        }
        
        # Inventory management systems
        resource_assessment['inventory_management'] = {
            'tracking_systems': {
                'digital_tracking': 0.3,  # 30% use digital tracking
                'manual_systems': 0.7,  # 70% use manual tracking
                'accuracy_rate': 0.6,  # 60% accuracy
                'update_frequency': 0.5,  # 50% update regularly
                'score': 5
            },
            'quality_control': {
                'inspection_systems': 0.4,  # 40% have quality inspection
                'condition_standards': 0.5,  # 50% have condition standards
                'rejection_rate': 0.1,  # 10% rejection rate
                'improvement_tracking': 0.3,  # 30% track quality improvements
                'score': 6
            },
            'rotation_systems': {
                'first_in_first_out': 0.6,  # 60% use FIFO
                'expiration_tracking': 0.4,  # 40% track expiration dates
                'waste_prevention': 0.7,  # 70% prevent waste
                'usage_optimization': 0.5,  # 50% optimize usage
                'score': 6
            }
        }
        
        # Access equity and fairness
        resource_assessment['access_equity'] = {
            'needs_based_allocation': 0.6,  # 60% use needs-based allocation
            'contribution_requirements': 0.7,  # 70% require contributions
            'emergency_access': 0.8,  # 80% provide emergency access
            'vulnerable_population_support': 0.5,  # 50% support vulnerable populations
            'dispute_resolution': 0.4,  # 40% have dispute resolution
            'transparency': 0.5,  # 50% transparent operations
            'score': 6
        }
        
        # Long-term sustainability
        resource_assessment['sustainability'] = {
            'replenishment_systems': 0.6,  # 60% have replenishment systems
            'local_production': 0.4,  # 40% local production
            'waste_reduction': 0.7,  # 70% focus on waste reduction
            'circular_economy': 0.3,  # 30% practice circular economy
            'resource_efficiency': 0.6,  # 60% efficiency
            'environmental_impact': 7,  # Environmental sustainability score
            'score': 6
        }
        
        # Calculate overall resource networks score
        subsystem_scores = []
        
        # Resource pools average
        pool_scores = [resource_assessment['resource_pools'][rp]['score'] 
                      for rp in resource_assessment['resource_pools']]
        subsystem_scores.append(sum(pool_scores) / len(pool_scores))
        
        # Sharing systems average
        sharing_scores = [resource_assessment['sharing_systems'][ss]['score'] 
                         for ss in resource_assessment['sharing_systems']]
        subsystem_scores.append(sum(sharing_scores) / len(sharing_scores))
        
        # Distribution networks average
        dist_scores = [resource_assessment['distribution_networks'][dn]['score'] 
                      for dn in resource_assessment['distribution_networks']]
        subsystem_scores.append(sum(dist_scores) / len(dist_scores))
        
        # Add other subsystem scores
        for subsystem in ['inventory_management', 'access_equity', 'sustainability']:
            subsystem_scores.append(resource_assessment[subsystem]['score'])
        
        resource_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return resource_assessment
    
    def _assess_mutual_aid_systems(self, community_size: int) -> Dict[str, Any]:
        """Assess mutual aid and cooperative support systems."""
        
        mutual_aid_assessment = {
            'support_networks': {},
            'crisis_response': {},
            'cooperative_structures': {},
            'decision_making': {},
            'resource_mobilization': {},
            'social_cohesion': {},
            'overall_score': 0
        }
        
        # Support networks assessment
        network_strength = min(community_size / 200, 10)
        mutual_aid_assessment['support_networks'] = {
            'neighborhood_groups': {
                'coverage_percent': 0.6,  # 60% neighborhood coverage
                'active_participation': 0.4,  # 40% active participation
                'meeting_frequency': 12,  # Monthly meetings
                'support_types': 8,  # Different types of support offered
                'response_time_hours': 4,  # 4-hour average response time
                'score': 7
            },
            'skill_networks': {
                'professional_volunteers': community_size * 0.1,
                'skill_diversity': min(community_size / 50, 10),
                'availability_rate': 0.6,  # 60% available when needed
                'expertise_level': 7,  # Average expertise level
                'knowledge_sharing': 0.5,  # 50% share knowledge regularly
                'score': network_strength
            },
            'care_networks': {
                'childcare_support': 0.7,  # 70% have childcare support
                'elder_care': 0.5,  # 50% have elder care support
                'disability_support': 0.4,  # 40% have disability support
                'mental_health': 0.3,  # 30% have mental health support
                'crisis_intervention': 0.6,  # 60% have crisis intervention
                'score': 6
            }
        }
        
        # Crisis response capabilities
        mutual_aid_assessment['crisis_response'] = {
            'emergency_coordination': {
                'response_teams': community_size / 50,
                'coordination_systems': 0.5,  # 50% have coordination systems
                'communication_redundancy': 0.6,  # 60% have backup communication
                'resource_stockpiles': 0.4,  # 40% have emergency stockpiles
                'evacuation_plans': 0.3,  # 30% have evacuation plans
                'score': 6
            },
            'immediate_aid': {
                'food_distribution': 0.7,  # 70% can distribute food
                'shelter_provision': 0.4,  # 40% can provide shelter
                'medical_response': 0.5,  # 50% have medical response
                'transportation': 0.6,  # 60% can provide transportation
                'communication_support': 0.8,  # 80% provide communication support
                'score': 6
            },
            'recovery_support': {
                'cleanup_crews': 0.6,  # 60% can organize cleanup
                'repair_teams': 0.4,  # 40% have repair teams
                'psychological_support': 0.3,  # 30% provide psychological support
                'resource_replacement': 0.5,  # 50% help replace resources
                'rebuilding_coordination': 0.4,  # 40% coordinate rebuilding
                'score': 5
            }
        }
        
        # Cooperative structures and organizations
        mutual_aid_assessment['cooperative_structures'] = {
            'formal_cooperatives': {
                'number_of_coops': community_size / 200,
                'membership_penetration': 0.3,  # 30% belong to cooperatives
                'economic_impact': community_size * 500,  # $500 per person economic impact
                'success_rate': 0.7,  # 70% success rate
                'diversity_of_sectors': 5,  # Different sectors represented
                'score': min(community_size / 100, 8)
            },
            'informal_groups': {
                'mutual_aid_groups': community_size / 30,
                'activity_level': 0.6,  # 60% actively meeting
                'project_completion': 0.7,  # 70% complete projects
                'member_satisfaction': 0.8,  # 80% member satisfaction
                'growth_rate': 0.1,  # 10% annual growth
                'score': 7
            },
            'support_organizations': {
                'ngo_presence': community_size / 500,
                'government_programs': 0.4,  # 40% have relevant government programs
                'funding_availability': 0.3,  # 30% adequate funding
                'volunteer_coordination': 0.5,  # 50% coordinate volunteers well
                'program_effectiveness': 0.6,  # 60% program effectiveness
                'score': 5
            }
        }
        
        # Decision making and governance
        mutual_aid_assessment['decision_making'] = {
            'consensus_systems': {
                'consensus_experience': 0.4,  # 40% have consensus experience
                'facilitation_skills': 0.3,  # 30% have facilitation skills
                'conflict_resolution': 0.5,  # 50% can resolve conflicts
                'inclusive_participation': 0.6,  # 60% inclusive participation
                'decision_speed': 0.4,  # 40% make decisions quickly
                'score': 5
            },
            'democratic_participation': {
                'voting_systems': 0.7,  # 70% use voting systems
                'representation': 0.6,  # 60% feel represented
                'transparency': 0.5,  # 50% transparent processes
                'accountability': 0.4,  # 40% hold leaders accountable
                'civic_engagement': 0.6,  # 60% civic engagement
                'score': 6
            },
            'leadership_development': {
                'leadership_training': 0.3,  # 30% have leadership training
                'succession_planning': 0.2,  # 20% have succession plans
                'distributed_leadership': 0.5,  # 50% practice distributed leadership
                'mentor_programs': 0.4,  # 40% have mentor programs
                'leadership_diversity': 0.6,  # 60% diverse leadership
                'score': 4
            }
        }
        
        # Resource mobilization capabilities
        mutual_aid_assessment['resource_mobilization'] = {
            'fundraising': {
                'fundraising_capacity': community_size * 10,  # $10 per person capacity
                'grant_writing_skills': 0.2,  # 20% have grant writing skills
                'donor_networks': 0.3,  # 30% have donor networks
                'crowdfunding_success': 0.4,  # 40% crowdfunding success
                'sustainable_funding': 0.3,  # 30% sustainable funding
                'score': 4
            },
            'volunteer_mobilization': {
                'volunteer_pool': community_size * 0.4,  # 40% potential volunteers
                'skill_matching': 0.3,  # 30% effective skill matching
                'volunteer_retention': 0.6,  # 60% retention rate
                'training_programs': 0.4,  # 40% have training programs
                'recognition_systems': 0.5,  # 50% recognize volunteers
                'score': 6
            },
            'resource_acquisition': {
                'donation_systems': 0.6,  # 60% have donation systems
                'resource_identification': 0.5,  # 50% identify needed resources
                'procurement_efficiency': 0.4,  # 40% procurement efficiency
                'inventory_management': 0.3,  # 30% manage inventory well
                'distribution_systems': 0.5,  # 50% distribute effectively
                'score': 5
            }
        }
        
        # Social cohesion and trust
        mutual_aid_assessment['social_cohesion'] = {
            'community_trust': 6,  # Trust level 1-10
            'social_capital': min(community_size / 200, 8),  # Social connections
            'shared_values': 7,  # Alignment on values
            'cultural_diversity_integration': 5,  # How well diversity is integrated
            'intergenerational_connections': 6,  # Connections across age groups
            'newcomer_integration': 5,  # How well newcomers are integrated
            'score': 6
        }
        
        # Calculate overall mutual aid score
        subsystem_scores = []
        
        # Support networks average
        support_scores = [mutual_aid_assessment['support_networks'][sn]['score'] 
                         for sn in mutual_aid_assessment['support_networks']]
        subsystem_scores.append(sum(support_scores) / len(support_scores))
        
        # Crisis response average
        crisis_scores = [mutual_aid_assessment['crisis_response'][cr]['score'] 
                        for cr in mutual_aid_assessment['crisis_response']]
        subsystem_scores.append(sum(crisis_scores) / len(crisis_scores))
        
        # Cooperative structures average
        coop_scores = [mutual_aid_assessment['cooperative_structures'][cs]['score'] 
                      for cs in mutual_aid_assessment['cooperative_structures']]
        subsystem_scores.append(sum(coop_scores) / len(coop_scores))
        
        # Decision making average
        decision_scores = [mutual_aid_assessment['decision_making'][dm]['score'] 
                          for dm in mutual_aid_assessment['decision_making']]
        subsystem_scores.append(sum(decision_scores) / len(decision_scores))
        
        # Resource mobilization average
        resource_scores = [mutual_aid_assessment['resource_mobilization'][rm]['score'] 
                          for rm in mutual_aid_assessment['resource_mobilization']]
        subsystem_scores.append(sum(resource_scores) / len(resource_scores))
        
        # Social cohesion score
        subsystem_scores.append(mutual_aid_assessment['social_cohesion']['score'])
        
        mutual_aid_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return mutual_aid_assessment
    
    def _assess_alternative_markets(self, community_size: int) -> Dict[str, Any]:
        """Assess alternative marketplace and exchange systems."""
        
        market_assessment = {
            'marketplace_infrastructure': {},
            'alternative_exchanges': {},
            'value_creation': {},
            'market_regulation': {},
            'economic_diversity': {},
            'resilience_factors': {},
            'overall_score': 0
        }
        
        # Physical and digital marketplace infrastructure
        market_scale = min(community_size / 100, 10)
        market_assessment['marketplace_infrastructure'] = {
            'physical_markets': {
                'farmers_markets': community_size / 500,  # Markets per capita
                'flea_markets': community_size / 800,
                'artisan_markets': community_size / 1000,
                'swap_meets': community_size / 600,
                'market_frequency': 20,  # Days per year with markets
                'vendor_participation': community_size * 0.05,  # 5% are vendors
                'customer_reach': community_size * 0.8,  # 80% participate as customers
                'score': market_scale
            },
            'digital_platforms': {
                'online_marketplaces': 0.3,  # 30% use online platforms
                'social_media_commerce': 0.6,  # 60% use social media for commerce
                'community_apps': 0.2,  # 20% have community commerce apps
                'payment_systems': 0.4,  # 40% have alternative payment systems
                'mobile_adoption': 0.7,  # 70% mobile adoption
                'digital_literacy': 0.6,  # 60% adequate digital literacy
                'score': 5
            },
            'meeting_spaces': {
                'community_centers': community_size / 300,
                'shared_workspaces': community_size / 400,
                'public_spaces': community_size / 200,
                'accessibility_rating': 7,  # How accessible spaces are
                'usage_optimization': 0.6,  # 60% optimal usage
                'maintenance_quality': 6,  # Maintenance quality
                'score': 7
            }
        }
        
        # Alternative exchange mechanisms
        market_assessment['alternative_exchanges'] = {
            'gift_economy': {
                'participation_rate': 0.4,  # 40% participate in gift economy
                'gift_volume': community_size * 100,  # $100 per person in gifts
                'reciprocity_strength': 0.7,  # 70% reciprocity rate
                'cultural_acceptance': 0.6,  # 60% cultural acceptance
                'sustainability': 0.5,  # 50% sustainable practices
                'score': 6
            },
            'sharing_economy': {
                'asset_sharing': 0.5,  # 50% share assets
                'ride_sharing': 0.3,  # 30% ride sharing participation
                'tool_sharing': 0.4,  # 40% tool sharing
                'space_sharing': 0.2,  # 20% space sharing
                'skill_sharing': 0.4,  # 40% skill sharing
                'coordination_systems': 0.3,  # 30% have coordination systems
                'score': 5
            },
            'cooperative_purchasing': {
                'buying_clubs': community_size / 200,
                'bulk_purchasing': 0.6,  # 60% participate in bulk purchasing
                'cost_savings': 0.25,  # 25% cost savings achieved
                'coordination_quality': 0.6,  # 60% coordination quality
                'supplier_relationships': 0.5,  # 50% good supplier relationships
                'score': 6
            }
        }
        
        # Value creation and economic multipliers
        market_assessment['value_creation'] = {
            'local_production': {
                'manufacturing_capacity': community_size * 200,  # $200 per person production
                'artisan_production': community_size * 100,  # $100 per person artisan goods
                'agricultural_production': community_size * 300,  # $300 per person agriculture
                'service_provision': community_size * 400,  # $400 per person services
                'value_retention': 0.6,  # 60% value stays local
                'score': 7
            },
            'import_substitution': {
                'food_localization': 0.4,  # 40% food produced locally
                'goods_localization': 0.2,  # 20% goods produced locally
                'services_localization': 0.7,  # 70% services provided locally
                'energy_localization': 0.3,  # 30% energy produced locally
                'economic_leakage_reduction': 0.35,  # 35% reduction in economic leakage
                'score': 6
            },
            'value_added_processing': {
                'raw_material_processing': 0.3,  # 30% process raw materials locally
                'product_finishing': 0.4,  # 40% finishing done locally
                'packaging_branding': 0.5,  # 50% packaging/branding local
                'quality_improvement': 0.6,  # 60% focus on quality improvement
                'price_premiums': 0.2,  # 20% price premium for local goods
                'score': 5
            }
        }
        
        # Market regulation and fairness
        market_assessment['market_regulation'] = {
            'fair_trade_practices': {
                'price_fairness': 0.7,  # 70% fair pricing
                'labor_standards': 0.6,  # 60% good labor standards
                'environmental_standards': 0.5,  # 50% environmental standards
                'transparency': 0.4,  # 40% transparent practices
                'dispute_resolution': 0.5,  # 50% effective dispute resolution
                'score': 6
            },
            'market_access': {
                'barrier_reduction': 0.5,  # 50% reduced barriers to entry
                'vendor_support': 0.4,  # 40% support for new vendors
                'customer_education': 0.3,  # 30% customer education
                'financing_access': 0.3,  # 30% access to financing
                'regulatory_simplification': 0.4,  # 40% simplified regulations
                'score': 4
            },
            'quality_assurance': {
                'product_standards': 0.5,  # 50% have product standards
                'certification_systems': 0.3,  # 30% certification systems
                'consumer_protection': 0.6,  # 60% consumer protection
                'feedback_systems': 0.4,  # 40% feedback systems
                'improvement_tracking': 0.3,  # 30% track improvements
                'score': 5
            }
        }
        
        # Economic diversity and resilience
        market_assessment['economic_diversity'] = {
            'sector_diversity': min(community_size / 100, 8),  # More people = more sectors
            'business_size_distribution': 0.7,  # 70% good distribution of business sizes
            'innovation_rate': 0.4,  # 40% innovation rate
            'adaptation_capability': 0.6,  # 60% can adapt to changes
            'competitive_balance': 0.5,  # 50% competitive balance
            'score': 6
        }
        
        # Resilience factors for alternative markets
        market_assessment['resilience_factors'] = {
            'supply_chain_independence': 0.4,  # 40% supply chain independence
            'energy_independence': 0.3,  # 30% energy independence
            'financial_independence': 0.3,  # 30% financial independence
            'knowledge_retention': 0.6,  # 60% knowledge retained locally
            'social_infrastructure': 0.7,  # 70% strong social infrastructure
            'adaptive_capacity': 0.6,  # 60% adaptive capacity
            'score': 5
        }
        
        # Calculate overall alternative markets score
        subsystem_scores = []
        
        # Infrastructure average
        infra_scores = [market_assessment['marketplace_infrastructure'][mi]['score'] 
                       for mi in market_assessment['marketplace_infrastructure']]
        subsystem_scores.append(sum(infra_scores) / len(infra_scores))
        
        # Alternative exchanges average
        exchange_scores = [market_assessment['alternative_exchanges'][ae]['score'] 
                          for ae in market_assessment['alternative_exchanges']]
        subsystem_scores.append(sum(exchange_scores) / len(exchange_scores))
        
        # Value creation average
        value_scores = [market_assessment['value_creation'][vc]['score'] 
                       for vc in market_assessment['value_creation']]
        subsystem_scores.append(sum(value_scores) / len(value_scores))
        
        # Market regulation average
        regulation_scores = [market_assessment['market_regulation'][mr]['score'] 
                           for mr in market_assessment['market_regulation']]
        subsystem_scores.append(sum(regulation_scores) / len(regulation_scores))
        
        # Add other subsystem scores
        subsystem_scores.append(market_assessment['economic_diversity']['score'])
        subsystem_scores.append(market_assessment['resilience_factors']['score'])
        
        market_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return market_assessment
    
    def _calculate_economic_resilience_duration(self, assessment: Dict[str, Any]) -> float:
        """Calculate how long alternative economic systems could sustain community."""
        
        # Base resilience from different systems
        barter_resilience = assessment['barter_systems']['overall_score'] * 2  # months
        skill_resilience = assessment['skill_sharing']['overall_score'] * 3  # months
        currency_resilience = assessment['local_currency']['overall_score'] * 4  # months
        resource_resilience = assessment['resource_networks']['overall_score'] * 3  # months
        mutual_aid_resilience = assessment['mutual_aid']['overall_score'] * 5  # months
        market_resilience = assessment['alternative_markets']['overall_score'] * 2  # months
        
        # Calculate weighted average - some systems more important for duration
        weights = {
            'barter': 0.15,
            'skill': 0.20,
            'currency': 0.15,
            'resource': 0.25,
            'mutual_aid': 0.15,
            'market': 0.10
        }
        
        weighted_resilience = (
            barter_resilience * weights['barter'] +
            skill_resilience * weights['skill'] +
            currency_resilience * weights['currency'] +
            resource_resilience * weights['resource'] +
            mutual_aid_resilience * weights['mutual_aid'] +
            market_resilience * weights['market']
        )
        
        # Apply community size multiplier
        community_size = assessment['community_size']
        if community_size > 1000:
            size_multiplier = 1.3  # Larger communities more resilient
        elif community_size > 500:
            size_multiplier = 1.1
        elif community_size > 200:
            size_multiplier = 1.0
        elif community_size > 100:
            size_multiplier = 0.9
        else:
            size_multiplier = 0.7  # Smaller communities less resilient
        
        return weighted_resilience * size_multiplier
    
    def _generate_economic_recommendations(self, assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate priority recommendations for improving economic resilience."""
        
        recommendations = []
        
        # Analyze each subsystem for improvement opportunities
        subsystems = {
            'Barter Systems': assessment['barter_systems'],
            'Skill Sharing': assessment['skill_sharing'],
            'Local Currency': assessment['local_currency'],
            'Resource Networks': assessment['resource_networks'],
            'Mutual Aid': assessment['mutual_aid'],
            'Alternative Markets': assessment['alternative_markets']
        }
        
        # Get recommendations based on lowest scores
        for system_name, system_data in subsystems.items():
            if system_data['overall_score'] < 6:  # Systems needing improvement
                recommendations.extend(self._get_economic_system_recommendations(system_name, system_data, assessment))
        
        # Sort by impact and feasibility
        recommendations.sort(key=lambda x: (x['impact'] * x['feasibility'] / x['cost_score']), reverse=True)
        
        return recommendations[:12]  # Top 12 recommendations
    
    def _get_economic_system_recommendations(self, system_name: str, system_data: Dict[str, Any], 
                                          assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get specific recommendations for an economic system."""
        
        recommendations = []
        community_size = assessment['community_size']
        
        if system_name == "Barter Systems":
            recommendations.append({
                'category': 'Barter Systems',
                'title': 'Establish Community Barter Network',
                'description': 'Create organized system for trading goods and services',
                'impact': 8,
                'feasibility': 7,
                'cost_score': 3,  # Lower cost = higher score
                'timeline_weeks': 8,
                'participants_needed': max(20, community_size * 0.1)
            })
            
            recommendations.append({
                'category': 'Barter Systems',
                'title': 'Create Skill Exchange Platform',
                'description': 'Digital or physical board for advertising available skills',
                'impact': 7,
                'feasibility': 8,
                'cost_score': 9,
                'timeline_weeks': 4,
                'participants_needed': max(10, community_size * 0.05)
            })
        
        elif system_name == "Skill Sharing":
            recommendations.append({
                'category': 'Skill Sharing',
                'title': 'Launch Community Skill Assessment',
                'description': 'Survey and catalog all available skills in the community',
                'impact': 8,
                'feasibility': 9,
                'cost_score': 8,
                'timeline_weeks': 6,
                'participants_needed': max(5, community_size * 0.02)
            })
            
            recommendations.append({
                'category': 'Skill Sharing',
                'title': 'Start Monthly Skill Share Workshops',
                'description': 'Regular workshops where community members teach each other',
                'impact': 7,
                'feasibility': 8,
                'cost_score': 7,
                'timeline_weeks': 2,
                'participants_needed': max(15, community_size * 0.1)
            })
        
        elif system_name == "Local Currency":
            if community_size >= 100:
                recommendations.append({
                    'category': 'Local Currency',
                    'title': 'Implement Time Banking System',
                    'description': 'Hour-based currency where 1 hour = 1 credit regardless of skill',
                    'impact': 8,
                    'feasibility': 6,
                    'cost_score': 5,
                    'timeline_weeks': 12,
                    'participants_needed': max(30, community_size * 0.15)
                })
            
            recommendations.append({
                'category': 'Local Currency',
                'title': 'Create Local Business Directory',
                'description': 'Directory of businesses willing to accept alternative currencies',
                'impact': 6,
                'feasibility': 9,
                'cost_score': 9,
                'timeline_weeks': 4,
                'participants_needed': max(10, community_size * 0.05)
            })
        
        elif system_name == "Resource Networks":
            recommendations.append({
                'category': 'Resource Networks',
                'title': 'Start Tool Library',
                'description': 'Community-owned collection of tools available for borrowing',
                'impact': 8,
                'feasibility': 8,
                'cost_score': 4,
                'timeline_weeks': 8,
                'participants_needed': max(20, community_size * 0.08)
            })
            
            recommendations.append({
                'category': 'Resource Networks',
                'title': 'Organize Bulk Buying Groups',
                'description': 'Coordinate group purchases for better prices on essentials',
                'impact': 7,
                'feasibility': 9,
                'cost_score': 8,
                'timeline_weeks': 3,
                'participants_needed': max(8, community_size * 0.04)
            })
        
        elif system_name == "Mutual Aid":
            recommendations.append({
                'category': 'Mutual Aid',
                'title': 'Form Neighborhood Response Teams',
                'description': 'Organize teams for emergency response and mutual support',
                'impact': 9,
                'feasibility': 7,
                'cost_score': 7,
                'timeline_weeks': 6,
                'participants_needed': max(15, community_size * 0.06)
            })
            
            recommendations.append({
                'category': 'Mutual Aid',
                'title': 'Create Community Support Fund',
                'description': 'Pooled financial resource for community member emergencies',
                'impact': 8,
                'feasibility': 6,
                'cost_score': 3,
                'timeline_weeks': 10,
                'participants_needed': max(25, community_size * 0.12)
            })
        
        elif system_name == "Alternative Markets":
            recommendations.append({
                'category': 'Alternative Markets',
                'title': 'Start Farmers/Makers Market',
                'description': 'Regular market for local producers to sell directly to community',
                'impact': 8,
                'feasibility': 7,
                'cost_score': 5,
                'timeline_weeks': 10,
                'participants_needed': max(15, community_size * 0.07)
            })
            
            recommendations.append({
                'category': 'Alternative Markets',
                'title': 'Launch Community Supported Agriculture',
                'description': 'Direct relationship between producers and consumers with shared risk/benefit',
                'impact': 7,
                'feasibility': 6,
                'cost_score': 4,
                'timeline_weeks': 16,
                'participants_needed': max(20, community_size * 0.10)
            })
        
        return recommendations
    
    def _store_assessment(self, assessment: Dict[str, Any]):
        """Store the economic assessment in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO economy_assessments 
            (assessment_date, household_size, community_size, assessment_data, overall_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            assessment['timestamp'],
            assessment['household_size'],
            assessment['community_size'],
            json.dumps(assessment),
            assessment['overall_score']
        ))
        
        conn.commit()
        conn.close()
    
    def create_skill_inventory(self, user_id: str, skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a skill inventory for a community member."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inventory_summary = {
            'user_id': user_id,
            'skills_added': 0,
            'total_trade_value': 0,
            'skill_categories': set(),
            'teaching_skills': 0
        }
        
        for skill in skills:
            # Calculate trade value based on skill category and proficiency
            skill_category = skill['category']
            proficiency = skill['proficiency_level']  # 1-10
            time_available = skill['time_availability']  # hours per month
            teaching_ability = skill.get('teaching_ability', 0)  # 1-10
            
            if skill_category in self.skill_categories:
                base_value = self.skill_categories[skill_category]['base_value']
                demand_multiplier = self.skill_categories[skill_category]['demand_multiplier']
                
                # Calculate monthly trade value
                trade_value = (base_value * demand_multiplier * proficiency * time_available) / 100
            else:
                trade_value = proficiency * time_available * 2  # Generic calculation
            
            cursor.execute('''
                INSERT INTO skill_inventories 
                (user_id, skill_category, skill_name, proficiency_level, 
                 teaching_ability, time_availability, trade_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, skill_category, skill['name'], proficiency,
                teaching_ability, time_available, trade_value
            ))
            
            inventory_summary['skills_added'] += 1
            inventory_summary['total_trade_value'] += trade_value
            inventory_summary['skill_categories'].add(skill_category)
            
            if teaching_ability >= 6:  # Can teach others
                inventory_summary['teaching_skills'] += 1
        
        conn.commit()
        conn.close()
        
        inventory_summary['skill_categories'] = list(inventory_summary['skill_categories'])
        inventory_summary['average_trade_value'] = (inventory_summary['total_trade_value'] / 
                                                   max(inventory_summary['skills_added'], 1))
        
        return inventory_summary
    
    def create_resource_inventory(self, user_id: str, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a resource inventory for trading and sharing."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inventory_summary = {
            'user_id': user_id,
            'resources_added': 0,
            'total_trade_value': 0,
            'resource_categories': set(),
            'expiring_soon': 0
        }
        
        for resource in resources:
            resource_category = resource['category']
            quantity = resource['quantity']
            unit = resource['unit']
            condition_score = resource.get('condition_score', 8)  # 1-10
            expiration_date = resource.get('expiration_date')
            
            # Calculate trade value
            if resource_category in self.resource_categories:
                category_data = self.resource_categories[resource_category]
                
                # Get appropriate value key
                if 'value_per_lb' in category_data:
                    base_value = category_data['value_per_lb']
                elif 'value_per_gallon' in category_data:
                    base_value = category_data['value_per_gallon']
                elif 'value_per_unit' in category_data:
                    base_value = category_data['value_per_unit']
                elif 'value_per_item' in category_data:
                    base_value = category_data['value_per_item']
                else:
                    base_value = 5  # Default
                
                # Adjust for condition
                condition_multiplier = condition_score / 10
                
                # Adjust for approaching expiration
                expiration_multiplier = 1.0
                if expiration_date:
                    try:
                        exp_date = datetime.fromisoformat(expiration_date)
                        days_until_expiration = (exp_date - datetime.now()).days
                        
                        if days_until_expiration < 30:
                            expiration_multiplier = 0.5
                            inventory_summary['expiring_soon'] += 1
                        elif days_until_expiration < 90:
                            expiration_multiplier = 0.8
                    except:
                        pass  # Invalid date format
                
                trade_value = base_value * quantity * condition_multiplier * expiration_multiplier
            else:
                trade_value = quantity * 2 * (condition_score / 10)  # Generic calculation
            
            cursor.execute('''
                INSERT INTO resource_inventories 
                (user_id, resource_category, resource_name, quantity, unit, 
                 condition_score, trade_value, expiration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, resource_category, resource['name'], quantity, unit,
                condition_score, trade_value, expiration_date
            ))
            
            inventory_summary['resources_added'] += 1
            inventory_summary['total_trade_value'] += trade_value
            inventory_summary['resource_categories'].add(resource_category)
        
        conn.commit()
        conn.close()
        
        inventory_summary['resource_categories'] = list(inventory_summary['resource_categories'])
        inventory_summary['average_resource_value'] = (inventory_summary['total_trade_value'] / 
                                                      max(inventory_summary['resources_added'], 1))
        
        return inventory_summary
    
    def find_trading_matches(self, user_id: str, seeking: List[str], offering: List[str]) -> Dict[str, Any]:
        """Find potential trading matches based on what user seeks and offers."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        matches = {
            'skill_matches': [],
            'resource_matches': [],
            'potential_trades': [],
            'match_score': 0
        }
        
        # Find skill matches
        for sought_skill in seeking:
            if sought_skill in [skill for skill in self.skill_categories.keys()]:
                cursor.execute('''
                    SELECT user_id, skill_name, proficiency_level, teaching_ability, 
                           time_availability, trade_value
                    FROM skill_inventories 
                    WHERE skill_category = ? AND user_id != ? AND teaching_ability >= 6
                    ORDER BY proficiency_level DESC, teaching_ability DESC
                ''', (sought_skill, user_id))
                
                skill_providers = cursor.fetchall()
                for provider in skill_providers[:5]:  # Top 5 matches
                    matches['skill_matches'].append({
                        'provider_id': provider[0],
                        'skill_name': provider[1],
                        'proficiency': provider[2],
                        'teaching_ability': provider[3],
                        'time_available': provider[4],
                        'trade_value': provider[5],
                        'match_type': 'skill_teaching'
                    })
        
        # Find resource matches
        for sought_resource in seeking:
            if sought_resource in [resource for resource in self.resource_categories.keys()]:
                cursor.execute('''
                    SELECT user_id, resource_name, quantity, unit, condition_score, trade_value
                    FROM resource_inventories 
                    WHERE resource_category = ? AND user_id != ? AND condition_score >= 7
                    ORDER BY condition_score DESC, trade_value DESC
                ''', (sought_resource, user_id))
                
                resource_providers = cursor.fetchall()
                for provider in resource_providers[:5]:  # Top 5 matches
                    matches['resource_matches'].append({
                        'provider_id': provider[0],
                        'resource_name': provider[1],
                        'quantity': provider[2],
                        'unit': provider[3],
                        'condition': provider[4],
                        'trade_value': provider[5],
                        'match_type': 'resource_trade'
                    })
        
        # Create potential trade combinations
        user_offerings = []
        
        # Get user's offerings
        for offered_item in offering:
            # Check if it's a skill
            cursor.execute('''
                SELECT skill_name, proficiency_level, time_availability, trade_value
                FROM skill_inventories 
                WHERE user_id = ? AND (skill_category = ? OR skill_name = ?)
            ''', (user_id, offered_item, offered_item))
            
            skill_offerings = cursor.fetchall()
            for skill in skill_offerings:
                user_offerings.append({
                    'type': 'skill',
                    'name': skill[0],
                    'value': skill[3],
                    'details': f"Proficiency: {skill[1]}/10, Available: {skill[2]} hrs/month"
                })
            
            # Check if it's a resource
            cursor.execute('''
                SELECT resource_name, quantity, unit, trade_value
                FROM resource_inventories 
                WHERE user_id = ? AND (resource_category = ? OR resource_name = ?)
            ''', (user_id, offered_item, offered_item))
            
            resource_offerings = cursor.fetchall()
            for resource in resource_offerings:
                user_offerings.append({
                    'type': 'resource',
                    'name': resource[0],
                    'value': resource[3],
                    'details': f"Quantity: {resource[1]} {resource[2]}"
                })
        
        # Match offerings with seekers
        for offering in user_offerings:
            for skill_match in matches['skill_matches']:
                value_ratio = offering['value'] / max(skill_match['trade_value'], 1)
                if 0.5 <= value_ratio <= 2.0:  # Fair trade ratio
                    matches['potential_trades'].append({
                        'partner_id': skill_match['provider_id'],
                        'user_offers': offering,
                        'partner_offers': skill_match,
                        'trade_ratio': value_ratio,
                        'fairness_score': 1.0 - abs(1.0 - value_ratio)
                    })
            
            for resource_match in matches['resource_matches']:
                value_ratio = offering['value'] / max(resource_match['trade_value'], 1)
                if 0.5 <= value_ratio <= 2.0:  # Fair trade ratio
                    matches['potential_trades'].append({
                        'partner_id': resource_match['provider_id'],
                        'user_offers': offering,
                        'partner_offers': resource_match,
                        'trade_ratio': value_ratio,
                        'fairness_score': 1.0 - abs(1.0 - value_ratio)
                    })
        
        # Calculate overall match score
        skill_match_score = min(len(matches['skill_matches']) * 2, 10)
        resource_match_score = min(len(matches['resource_matches']) * 2, 10)
        trade_match_score = min(len(matches['potential_trades']), 10)
        
        matches['match_score'] = (skill_match_score + resource_match_score + trade_match_score) / 3
        
        # Sort potential trades by fairness score
        matches['potential_trades'].sort(key=lambda x: x['fairness_score'], reverse=True)
        
        conn.close()
        
        return matches
    
    def generate_economy_report(self, assessment_data: Dict[str, Any] = None) -> str:
        """Generate comprehensive ASCII report of alternative economy assessment."""
        
        if not assessment_data:
            # Get most recent assessment from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT assessment_data FROM economy_assessments ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return "No assessment data available. Run assess_economic_resilience() first."
            
            assessment_data = json.loads(result[0])
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                    ALTERNATIVE ECONOMY SYSTEMS REPORT                       ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        report.append("")
        
        # Assessment overview
        report.append("📊 ECONOMIC RESILIENCE OVERVIEW")
        report.append("=" * 80)
        report.append(f"Assessment Date: {assessment_data['timestamp'][:10]}")
        report.append(f"Household Size: {assessment_data['household_size']} people")
        report.append(f"Community Size: {assessment_data['community_size']} people")
        report.append(f"Overall Resilience Score: {assessment_data['overall_score']:.1f}/10")
        report.append(f"Economic Resilience Duration: {assessment_data['economic_resilience_months']:.1f} months")
        report.append("")
        
        # Create score visualization
        score = assessment_data['overall_score']
        filled_bars = int(score)
        empty_bars = 10 - filled_bars
        score_bar = "█" * filled_bars + "░" * empty_bars
        report.append(f"Economic Preparedness: [{score_bar}] {score:.1f}/10")
        report.append("")
        
        # Subsystem performance
        subsystems = [
            ("🔄 Barter Systems", assessment_data['barter_systems']['overall_score']),
            ("🎓 Skill Sharing", assessment_data['skill_sharing']['overall_score']),
            ("💰 Local Currency", assessment_data['local_currency']['overall_score']),
            ("📦 Resource Networks", assessment_data['resource_networks']['overall_score']),
            ("🤝 Mutual Aid", assessment_data['mutual_aid']['overall_score']),
            ("🏪 Alternative Markets", assessment_data['alternative_markets']['overall_score'])
        ]
        
        report.append("🎯 ECONOMIC SYSTEM PERFORMANCE")
        report.append("=" * 80)
        for name, score in subsystems:
            filled = int(score)
            empty = 10 - filled
            bar = "█" * filled + "░" * empty
            report.append(f"{name:<22} [{bar}] {score:.1f}/10")
        report.append("")
        
        # Barter systems details
        barter_data = assessment_data['barter_systems']
        report.append("🔄 BARTER SYSTEMS ANALYSIS")
        report.append("=" * 80)
        
        # Resource trading potential
        if 'tradeable_resources' in barter_data:
            resources = barter_data['tradeable_resources']
            report.append("Trading Potential:")
            
            if 'food_surplus' in resources:
                food = resources['food_surplus']
                report.append(f"  Food Surplus: {food['trade_value_annual']:.0f} value/year")
            
            if 'services' in resources:
                services = resources['services']
                report.append(f"  Service Hours: {services['labor_hours_available']} hrs/year @ ${services['trade_value_annual']/services['labor_hours_available']:.0f}/hr")
        
        # Trading network size
        if 'trading_networks' in barter_data:
            network = barter_data['trading_networks']
            report.append(f"Trading Network: {network['local_network_size']} people, {network['geographic_reach_miles']} mile radius")
        report.append("")
        
        # Skill sharing details
        skill_data = assessment_data['skill_sharing']
        report.append("🎓 SKILL SHARING ANALYSIS")
        report.append("=" * 80)
        
        if 'available_skills' in skill_data:
            skills = skill_data['available_skills']
            high_value_skills = [skill for skill, data in skills.items() 
                               if data['demand_level'] >= 2.5]
            report.append(f"High-Demand Skills Available: {len(high_value_skills)}")
            for skill in high_value_skills[:5]:  # Show top 5
                skill_info = skills[skill]
                report.append(f"  {skill.replace('_', ' ').title()}: {skill_info['community_practitioners']:.0f} practitioners")
        
        if 'teaching_capacity' in skill_data:
            teaching = skill_data['teaching_capacity']
            report.append(f"Teaching Capacity: {teaching['total_teachers']:.0f} teachers for {teaching['student_teacher_ratio']:.0f}:1 ratio")
        
        if 'skill_gaps' in skill_data:
            gaps = skill_data['skill_gaps']
            if gaps['critical_gaps']:
                report.append(f"Critical Skill Gaps: {', '.join([gap.replace('_', ' ').title() for gap in gaps['critical_gaps']])}")
        report.append("")
        
        # Local currency potential
        currency_data = assessment_data['local_currency']
        report.append("💰 LOCAL CURRENCY ANALYSIS")
        report.append("=" * 80)
        
        if 'currency_types' in currency_data:
            # Find best currency type for this community
            best_currency = max(currency_data['currency_types'].items(), 
                               key=lambda x: x[1]['suitability_score'])
            report.append(f"Best Currency Type: {best_currency[0].replace('_', ' ').title()}")
            report.append(f"  Suitability Score: {best_currency[1]['suitability_score']}/10")
            report.append(f"  Implementation Complexity: {best_currency[1]['complexity']}/10")
            report.append(f"  Economic Impact Potential: {best_currency[1]['economic_impact']}/10")
        
        if 'implementation_readiness' in currency_data:
            readiness = currency_data['implementation_readiness']
            report.append(f"Implementation Readiness: {readiness['score']:.1f}/10")
            report.append(f"Community Cohesion: {readiness['community_cohesion']:.1f}/10")
        report.append("")
        
        # Resource networks
        resource_data = assessment_data['resource_networks']
        report.append("📦 RESOURCE NETWORKS ANALYSIS")
        report.append("=" * 80)
        
        if 'sharing_systems' in resource_data:
            sharing = resource_data['sharing_systems']
            
            # Tool library potential
            if 'tool_libraries' in sharing:
                tools = sharing['tool_libraries']
                report.append(f"Tool Library Potential: {tools['participation_rate']*100:.0f}% participation")
                report.append(f"  Tool Variety: {tools['tool_variety']:.0f} different tools")
                report.append(f"  Utilization Rate: {tools['usage_efficiency']*100:.0f}%")
            
            # Bulk purchasing
            if 'bulk_purchasing' in sharing:
                bulk = sharing['bulk_purchasing']
                report.append(f"Bulk Purchasing: {bulk['participation_rate']*100:.0f}% participation")
                report.append(f"  Cost Savings: {bulk['cost_savings_percent']}% average savings")
        report.append("")
        
        # Mutual aid systems
        mutual_data = assessment_data['mutual_aid']
        report.append("🤝 MUTUAL AID ANALYSIS")
        report.append("=" * 80)
        
        if 'support_networks' in mutual_data:
            support = mutual_data['support_networks']
            
            if 'neighborhood_groups' in support:
                groups = support['neighborhood_groups']
                report.append(f"Neighborhood Coverage: {groups['coverage_percent']*100:.0f}%")
                report.append(f"Response Time: {groups['response_time_hours']} hours average")
            
            if 'skill_networks' in support:
                skill_net = support['skill_networks']
                report.append(f"Professional Volunteers: {skill_net['professional_volunteers']:.0f}")
                report.append(f"Skill Diversity: {skill_net['skill_diversity']:.0f}/10")
        
        if 'crisis_response' in mutual_data:
            crisis = mutual_data['crisis_response']
            if 'emergency_coordination' in crisis:
                coord = crisis['emergency_coordination']
                report.append(f"Emergency Response Teams: {coord['response_teams']:.0f}")
        report.append("")
        
        # Alternative markets
        market_data = assessment_data['alternative_markets']
        report.append("🏪 ALTERNATIVE MARKETS ANALYSIS")
        report.append("=" * 80)
        
        if 'marketplace_infrastructure' in market_data:
            infra = market_data['marketplace_infrastructure']
            
            if 'physical_markets' in infra:
                markets = infra['physical_markets']
                report.append(f"Market Infrastructure:")
                report.append(f"  Farmers Markets: {markets['farmers_markets']:.1f}")
                report.append(f"  Vendor Participation: {markets['vendor_participation']:.0f} vendors")
                report.append(f"  Customer Reach: {markets['customer_reach']:.0f} customers")
        
        if 'value_creation' in market_data:
            value = market_data['value_creation']
            if 'local_production' in value:
                production = value['local_production']
                total_local_value = (production['manufacturing_capacity'] + 
                                   production['artisan_production'] + 
                                   production['agricultural_production'] + 
                                   production['service_provision'])
                report.append(f"Local Production Value: ${total_local_value:,.0f} annually")
                report.append(f"Value Retention: {production['value_retention']*100:.0f}% stays local")
        report.append("")
        
        # Priority recommendations
        if 'recommendations' in assessment_data and assessment_data['recommendations']:
            report.append("🎯 PRIORITY RECOMMENDATIONS")
            report.append("=" * 80)
            
            for i, rec in enumerate(assessment_data['recommendations'][:6], 1):
                report.append(f"{i}. {rec['title']}")
                report.append(f"   Category: {rec['category']}")
                report.append(f"   {rec['description']}")
                report.append(f"   Impact: {rec['impact']}/10 | Feasibility: {rec['feasibility']}/10 | Timeline: {rec['timeline_weeks']} weeks")
                report.append(f"   Participants Needed: {rec['participants_needed']:.0f}")
                report.append("")
        
        # Economic resilience summary
        report.append("💪 ECONOMIC RESILIENCE SUMMARY")
        report.append("=" * 80)
        resilience_months = assessment_data['economic_resilience_months']
        
        if resilience_months < 3:
            resilience_level = "LOW"
            resilience_desc = "Limited economic alternatives, high dependency on external systems"
        elif resilience_months < 6:
            resilience_level = "MODERATE"
            resilience_desc = "Some economic alternatives, moderate resilience during disruptions"
        elif resilience_months < 12:
            resilience_level = "GOOD" 
            resilience_desc = "Strong economic alternatives, good resilience for most disruptions"
        else:
            resilience_level = "EXCELLENT"
            resilience_desc = "Highly diverse economy, excellent long-term resilience"
        
        report.append(f"Resilience Level: {resilience_level}")
        report.append(f"Duration Estimate: {resilience_months:.1f} months")
        report.append(f"Assessment: {resilience_desc}")
        report.append("")
        
        report.append("━" * 80)
        report.append("🎯 NEXT STEPS: Begin with highest-priority recommendations and build economic networks")
        report.append("━" * 80)
        
        return "\n".join(report)

# Example usage and testing
if __name__ == "__main__":
    print("Alternative Economy Systems Module - Test Suite")
    print("=" * 60)
    
    # Initialize the system
    economy_system = AlternativeEconomySystems("test_alternative_economy.db")
    
    # Test assessments for different community sizes
    test_scenarios = [
        {"household_size": 4, "community_size": 150},
        {"household_size": 2, "community_size": 800},
        {"household_size": 6, "community_size": 2500}
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 TEST SCENARIO {i}: Community of {scenario['community_size']} people")
        print("-" * 50)
        
        assessment = economy_system.assess_economic_resilience(
            scenario['household_size'],
            scenario['community_size']
        )
        
        print(f"Overall Score: {assessment['overall_score']:.1f}/10")
        print(f"Economic Resilience: {assessment['economic_resilience_months']:.1f} months")
        print(f"Barter Systems: {assessment['barter_systems']['overall_score']:.1f}/10")
        print(f"Skill Sharing: {assessment['skill_sharing']['overall_score']:.1f}/10")
        print(f"Local Currency: {assessment['local_currency']['overall_score']:.1f}/10")
        print(f"Resource Networks: {assessment['resource_networks']['overall_score']:.1f}/10")
        print(f"Mutual Aid: {assessment['mutual_aid']['overall_score']:.1f}/10")
        print(f"Alternative Markets: {assessment['alternative_markets']['overall_score']:.1f}/10")
        
        print(f"\nTop Recommendations:")
        for j, rec in enumerate(assessment['recommendations'][:3], 1):
            print(f"  {j}. {rec['title']} ({rec['category']})")
        
        if i == 1:  # Generate full report for first scenario
            print(f"\n📊 FULL ECONOMIC ASSESSMENT REPORT")
            print("=" * 80)
            report = economy_system.generate_economy_report(assessment)
            print(report)
    
    # Test skill and resource inventory management
    print(f"\n🧪 TESTING INVENTORY MANAGEMENT")
    print("-" * 50)
    
    # Create sample skill inventory
    test_skills = [
        {'category': 'medical', 'name': 'First Aid', 'proficiency_level': 7, 'teaching_ability': 6, 'time_availability': 10},
        {'category': 'mechanical', 'name': 'Auto Repair', 'proficiency_level': 8, 'teaching_ability': 8, 'time_availability': 15},
        {'category': 'food_production', 'name': 'Gardening', 'proficiency_level': 6, 'teaching_ability': 7, 'time_availability': 20}
    ]
    
    skill_inventory = economy_system.create_skill_inventory('user_001', test_skills)
    print(f"Skills Added: {skill_inventory['skills_added']}")
    print(f"Total Trade Value: ${skill_inventory['total_trade_value']:.2f}/month")
    print(f"Teaching Skills: {skill_inventory['teaching_skills']}")
    
    # Create sample resource inventory
    test_resources = [
        {'category': 'food_staples', 'name': 'Rice', 'quantity': 50, 'unit': 'lbs', 'condition_score': 9},
        {'category': 'tools', 'name': 'Hand Drill', 'quantity': 1, 'unit': 'each', 'condition_score': 8},
        {'category': 'seeds', 'name': 'Tomato Seeds', 'quantity': 10, 'unit': 'packets', 'condition_score': 10}
    ]
    
    resource_inventory = economy_system.create_resource_inventory('user_001', test_resources)
    print(f"Resources Added: {resource_inventory['resources_added']}")
    print(f"Total Trade Value: ${resource_inventory['total_trade_value']:.2f}")
    
    # Test trading matches
    seeking = ['electrical', 'preserved_food']
    offering = ['medical', 'food_staples']
    
    matches = economy_system.find_trading_matches('user_001', seeking, offering)
    print(f"Trading Matches Found:")
    print(f"  Skill Matches: {len(matches['skill_matches'])}")
    print(f"  Resource Matches: {len(matches['resource_matches'])}")
    print(f"  Potential Trades: {len(matches['potential_trades'])}")
    print(f"  Match Score: {matches['match_score']:.1f}/10")
    
    print(f"\n✅ Alternative Economy Systems Module test completed successfully!")
    print("🎯 Module ready for integration with main preparedness system")