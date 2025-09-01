#!/usr/bin/env python3
"""
Community Resilience Networks Module - Version 2.0 Phase 2B
Final module for long-term sustainability - builds interconnected community networks
for disaster preparedness, resource sharing, and collective resilience.
"""

import sqlite3
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional

class CommunityResilienceNetworks:
    """
    Manages assessment and development of community resilience networks
    for comprehensive disaster preparedness and sustainable community building.
    """
    
    def __init__(self, db_path: str = "community_resilience.db"):
        """Initialize the Community Resilience Networks system."""
        self.db_path = db_path
        self.initialize_database()
        
        # Network types and their characteristics
        self.network_types = {
            'neighborhood_groups': {
                'optimal_size': 25, 'max_size': 50, 'min_trust': 7,
                'coordination_complexity': 3, 'response_speed': 9
            },
            'skill_circles': {
                'optimal_size': 15, 'max_size': 30, 'min_trust': 6,
                'coordination_complexity': 4, 'response_speed': 7
            },
            'resource_hubs': {
                'optimal_size': 100, 'max_size': 500, 'min_trust': 5,
                'coordination_complexity': 6, 'response_speed': 6
            },
            'mutual_aid_networks': {
                'optimal_size': 75, 'max_size': 200, 'min_trust': 8,
                'coordination_complexity': 5, 'response_speed': 8
            },
            'communication_webs': {
                'optimal_size': 1000, 'max_size': 10000, 'min_trust': 4,
                'coordination_complexity': 7, 'response_speed': 10
            },
            'economic_cooperatives': {
                'optimal_size': 40, 'max_size': 150, 'min_trust': 8,
                'coordination_complexity': 8, 'response_speed': 4
            }
        }
        
        # Resilience factors for different disaster types
        self.disaster_resilience_factors = {
            'natural_disasters': {
                'early_warning': 0.3, 'resource_pooling': 0.25, 'evacuation_coordination': 0.2,
                'recovery_cooperation': 0.15, 'information_sharing': 0.1
            },
            'economic_disruption': {
                'alternative_economy': 0.4, 'resource_sharing': 0.3, 'skill_exchange': 0.2, 
                'mutual_support': 0.1
            },
            'supply_chain_failure': {
                'local_production': 0.35, 'resource_stockpiling': 0.25, 'distribution_networks': 0.25,
                'alternative_suppliers': 0.15
            },
            'infrastructure_failure': {
                'backup_systems': 0.3, 'repair_capability': 0.25, 'alternative_services': 0.25,
                'coordination_resilience': 0.2
            },
            'social_unrest': {
                'community_cohesion': 0.4, 'conflict_resolution': 0.25, 'mutual_protection': 0.2,
                'information_accuracy': 0.15
            }
        }
    
    def initialize_database(self):
        """Create necessary database tables for network tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Network assessments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_date TEXT NOT NULL,
                community_size INTEGER NOT NULL,
                geographic_area REAL,
                assessment_data TEXT,
                overall_score REAL,
                resilience_rating TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Network nodes (individuals, households, organizations)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT UNIQUE NOT NULL,
                node_type TEXT NOT NULL,
                node_name TEXT,
                location_lat REAL,
                location_lon REAL,
                capabilities TEXT,
                resources TEXT,
                trust_score REAL,
                participation_level INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Network connections and relationships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_a_id TEXT NOT NULL,
                node_b_id TEXT NOT NULL,
                connection_type TEXT NOT NULL,
                connection_strength REAL,
                communication_frequency INTEGER,
                resource_exchange REAL,
                trust_level REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(node_a_id, node_b_id, connection_type)
            )
        ''')
        
        # Network activities and events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_date TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                participants TEXT,
                resources_involved TEXT,
                outcomes TEXT,
                effectiveness_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Resilience scenarios and responses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resilience_scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_name TEXT NOT NULL,
                scenario_type TEXT NOT NULL,
                severity_level INTEGER,
                duration_days INTEGER,
                affected_area REAL,
                network_response TEXT,
                effectiveness_score REAL,
                lessons_learned TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Community assets and infrastructure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                location_lat REAL,
                location_lon REAL,
                capacity INTEGER,
                condition_score INTEGER,
                access_level TEXT,
                backup_systems TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def assess_network_resilience(self, community_size: int, geographic_area: float, 
                                existing_networks: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive assessment of community network resilience across all dimensions.
        """
        
        assessment = {
            'timestamp': datetime.now().isoformat(),
            'community_size': community_size,
            'geographic_area': geographic_area,
            'network_topology': self._assess_network_topology(community_size, geographic_area),
            'social_capital': self._assess_social_capital(community_size, existing_networks),
            'communication_systems': self._assess_communication_systems(community_size),
            'resource_distribution': self._assess_resource_distribution(community_size, geographic_area),
            'leadership_structures': self._assess_leadership_structures(community_size),
            'collective_efficacy': self._assess_collective_efficacy(community_size),
            'disaster_preparedness': self._assess_disaster_preparedness_networks(community_size),
            'adaptive_capacity': self._assess_adaptive_capacity(community_size),
            'overall_score': 0,
            'resilience_rating': '',
            'network_gaps': [],
            'priority_actions': []
        }
        
        # Calculate overall network resilience score
        subsystem_scores = [
            assessment['network_topology']['overall_score'],
            assessment['social_capital']['overall_score'],
            assessment['communication_systems']['overall_score'],
            assessment['resource_distribution']['overall_score'],
            assessment['leadership_structures']['overall_score'],
            assessment['collective_efficacy']['overall_score'],
            assessment['disaster_preparedness']['overall_score'],
            assessment['adaptive_capacity']['overall_score']
        ]
        
        assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        # Assign resilience rating
        assessment['resilience_rating'] = self._assign_resilience_rating(assessment['overall_score'])
        
        # Identify network gaps
        assessment['network_gaps'] = self._identify_network_gaps(assessment)
        
        # Generate priority actions
        assessment['priority_actions'] = self._generate_priority_actions(assessment)
        
        # Store assessment in database
        self._store_assessment(assessment)
        
        return assessment
    
    def _assess_network_topology(self, community_size: int, geographic_area: float) -> Dict[str, Any]:
        """Assess the structure and connectivity of community networks."""
        
        topology_assessment = {
            'network_density': {},
            'connectivity_patterns': {},
            'redundancy_levels': {},
            'geographic_distribution': {},
            'network_efficiency': {},
            'scalability': {},
            'overall_score': 0
        }
        
        # Calculate theoretical optimal network parameters
        population_density = community_size / geographic_area if geographic_area > 0 else community_size
        optimal_cluster_size = min(150, max(25, community_size ** 0.5))  # Dunbar's number consideration
        
        # Network density assessment
        max_connections = community_size * (community_size - 1) / 2
        estimated_actual_connections = community_size * min(optimal_cluster_size * 0.3, 50)
        network_density = estimated_actual_connections / max_connections if max_connections > 0 else 0
        
        topology_assessment['network_density'] = {
            'theoretical_max_connections': max_connections,
            'estimated_actual_connections': estimated_actual_connections,
            'density_ratio': network_density,
            'optimal_density_range': [0.05, 0.15],  # 5-15% connectivity optimal
            'current_adequacy': 8 if 0.05 <= network_density <= 0.15 else 5,
            'score': min(network_density * 100, 10)
        }
        
        # Connectivity patterns (small-world vs random vs scale-free)
        clustering_coefficient = min(0.7, max(0.1, 1.0 - (community_size / 1000)))  # Smaller communities cluster more
        path_length = max(2, min(6, math.log2(community_size)))  # Average path length
        
        topology_assessment['connectivity_patterns'] = {
            'clustering_coefficient': clustering_coefficient,
            'average_path_length': path_length,
            'small_world_index': clustering_coefficient / path_length,  # Higher is better
            'network_diameter': path_length * 2,
            'centralization_level': 0.3,  # Moderate centralization
            'score': min(clustering_coefficient * 15, 10)
        }
        
        # Redundancy and resilience to node failures
        critical_nodes = max(1, community_size * 0.05)  # 5% are critical nodes
        redundancy_ratio = 1 - (critical_nodes / community_size)
        
        topology_assessment['redundancy_levels'] = {
            'critical_nodes': critical_nodes,
            'redundant_paths': community_size * 0.4,  # 40% have redundant paths
            'single_point_failures': critical_nodes,
            'redundancy_ratio': redundancy_ratio,
            'failure_tolerance': min(redundancy_ratio * 15, 10),
            'score': min(redundancy_ratio * 12, 10)
        }
        
        # Geographic distribution and spatial clustering
        geographic_efficiency = min(1.0, max(0.3, 1.0 - (geographic_area / 100)))  # Efficiency decreases with area
        spatial_clustering = 0.7  # Assumption of moderate spatial clustering
        
        topology_assessment['geographic_distribution'] = {
            'area_coverage_sq_miles': geographic_area,
            'population_density': population_density,
            'geographic_efficiency': geographic_efficiency,
            'spatial_clustering': spatial_clustering,
            'transportation_accessibility': 0.6,  # 60% easily accessible
            'communication_range': min(geographic_area, 50),  # Communication range in miles
            'score': geographic_efficiency * 10
        }
        
        # Network efficiency metrics
        information_flow_rate = min(10, max(3, 10 - path_length))
        resource_flow_efficiency = min(10, max(2, geographic_efficiency * clustering_coefficient * 15))
        
        topology_assessment['network_efficiency'] = {
            'information_flow_rate': information_flow_rate,
            'resource_flow_efficiency': resource_flow_efficiency,
            'coordination_efficiency': (information_flow_rate + resource_flow_efficiency) / 2,
            'bottleneck_nodes': max(1, community_size * 0.02),  # 2% are bottlenecks
            'load_distribution': 0.7,  # 70% even load distribution
            'score': (information_flow_rate + resource_flow_efficiency) / 2
        }
        
        # Scalability assessment
        growth_accommodation = min(10, max(3, 10 - (community_size / 200)))  # Harder to scale larger networks
        structure_flexibility = 7  # Moderate flexibility
        
        topology_assessment['scalability'] = {
            'growth_accommodation': growth_accommodation,
            'structure_flexibility': structure_flexibility,
            'expansion_potential': (growth_accommodation + structure_flexibility) / 2,
            'integration_ease': 6,  # Moderate ease of integrating new members
            'modularity': 8,  # High modularity for scalability
            'score': (growth_accommodation + structure_flexibility + 6 + 8) / 4
        }
        
        # Calculate overall network topology score
        subsystem_scores = [
            topology_assessment['network_density']['score'],
            topology_assessment['connectivity_patterns']['score'],
            topology_assessment['redundancy_levels']['score'],
            topology_assessment['geographic_distribution']['score'],
            topology_assessment['network_efficiency']['score'],
            topology_assessment['scalability']['score']
        ]
        
        topology_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return topology_assessment
    
    def _assess_social_capital(self, community_size: int, existing_networks: Dict[str, Any] = None) -> Dict[str, Any]:
        """Assess social capital and trust within community networks."""
        
        social_assessment = {
            'trust_levels': {},
            'social_cohesion': {},
            'civic_engagement': {},
            'shared_norms': {},
            'reciprocity_networks': {},
            'bridging_capital': {},
            'overall_score': 0
        }
        
        # Trust levels across different relationship types
        community_scale_factor = min(1.0, max(0.3, 1.0 - (community_size / 1500)))  # Trust decreases with size
        base_trust = 6.5 * community_scale_factor  # Base trust level
        
        social_assessment['trust_levels'] = {
            'interpersonal_trust': base_trust + 1,  # Higher for close relationships
            'institutional_trust': base_trust - 0.5,  # Lower for institutions
            'generalized_trust': base_trust,  # Trust in community generally
            'trust_in_leadership': base_trust - 0.2,  # Slightly lower than generalized
            'trust_variance': 2.0,  # Standard deviation in trust levels
            'trust_building_rate': 0.1,  # Annual improvement in trust
            'score': base_trust
        }
        
        # Social cohesion indicators
        cohesion_factors = {
            'shared_identity': 0.7,  # 70% feel shared community identity
            'collective_goals': 0.6,  # 60% agree on community goals  
            'social_participation': 0.5,  # 50% actively participate in community
            'conflict_resolution': 0.4,  # 40% effective at resolving conflicts
            'inclusion_level': 0.8,  # 80% feel included in community
            'diversity_integration': 0.6   # 60% well-integrated diversity
        }
        
        cohesion_score = sum(cohesion_factors.values()) / len(cohesion_factors)
        
        social_assessment['social_cohesion'] = {
            **cohesion_factors,
            'overall_cohesion': cohesion_score,
            'fragmentation_risk': 1 - cohesion_score,
            'bonding_strength': cohesion_score * 1.2,  # Strong bonding
            'score': cohesion_score * 10
        }
        
        # Civic engagement and participation
        participation_rate = min(0.8, max(0.2, 0.6 - (community_size / 2000)))  # Participation decreases with size
        
        social_assessment['civic_engagement'] = {
            'voter_participation': participation_rate + 0.1,
            'volunteer_participation': participation_rate,
            'meeting_attendance': participation_rate - 0.1,
            'leadership_participation': participation_rate * 0.2,  # 20% of participants become leaders
            'issue_advocacy': participation_rate * 0.3,  # 30% advocate on issues
            'civic_knowledge': 0.6,  # 60% have adequate civic knowledge
            'score': participation_rate * 10
        }
        
        # Shared norms and values
        social_assessment['shared_norms'] = {
            'cooperation_norm': 0.75,  # 75% value cooperation
            'reciprocity_norm': 0.80,  # 80% practice reciprocity
            'collective_responsibility': 0.65,  # 65% feel collective responsibility
            'rule_compliance': 0.70,  # 70% comply with community rules
            'conflict_avoidance': 0.60,  # 60% prefer avoiding conflict
            'mutual_aid_norm': 0.85,  # 85% support mutual aid concept
            'score': 7.2  # Average of above * 10
        }
        
        # Reciprocity networks and exchange
        reciprocity_strength = min(1.0, max(0.4, 1.0 - (community_size / 1000)))  # Stronger in smaller communities
        
        social_assessment['reciprocity_networks'] = {
            'informal_exchanges': reciprocity_strength * 0.8,  # 80% engage in informal exchanges
            'favor_networks': reciprocity_strength * 0.7,  # 70% have favor networks
            'resource_sharing': reciprocity_strength * 0.6,  # 60% share resources
            'skill_exchange': reciprocity_strength * 0.5,  # 50% exchange skills
            'childcare_networks': reciprocity_strength * 0.4,  # 40% have childcare networks
            'elder_care_networks': reciprocity_strength * 0.3,  # 30% have elder care networks
            'score': reciprocity_strength * 10
        }
        
        # Bridging capital (connections across groups)
        diversity_factor = min(1.0, max(0.5, community_size / 500))  # More diversity in larger communities
        
        social_assessment['bridging_capital'] = {
            'cross_group_connections': diversity_factor * 0.4,  # 40% have cross-group connections
            'intergroup_cooperation': diversity_factor * 0.5,  # 50% cooperate across groups
            'cultural_exchange': diversity_factor * 0.6,  # 60% engage in cultural exchange
            'economic_bridging': diversity_factor * 0.3,  # 30% economic connections across groups
            'leadership_diversity': diversity_factor * 0.7,  # 70% diverse leadership
            'conflict_mediation': diversity_factor * 0.4,  # 40% can mediate intergroup conflicts
            'score': diversity_factor * 6  # Slightly lower due to challenges
        }
        
        # Calculate overall social capital score
        subsystem_scores = [
            social_assessment['trust_levels']['score'],
            social_assessment['social_cohesion']['score'],
            social_assessment['civic_engagement']['score'],
            social_assessment['shared_norms']['score'],
            social_assessment['reciprocity_networks']['score'],
            social_assessment['bridging_capital']['score']
        ]
        
        social_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return social_assessment
    
    def _assess_communication_systems(self, community_size: int) -> Dict[str, Any]:
        """Assess communication infrastructure and information flow."""
        
        comm_assessment = {
            'infrastructure': {},
            'information_flow': {},
            'emergency_communication': {},
            'digital_systems': {},
            'informal_networks': {},
            'redundancy': {},
            'overall_score': 0
        }
        
        # Communication infrastructure
        infrastructure_quality = min(10, max(4, 4 + (community_size / 200)))  # Better infrastructure in larger communities
        
        comm_assessment['infrastructure'] = {
            'cellular_coverage': min(0.95, max(0.6, 0.6 + (community_size / 1000))),
            'internet_penetration': min(0.90, max(0.5, 0.5 + (community_size / 800))),
            'landline_availability': min(0.8, max(0.3, 0.8 - (community_size / 2000))),  # Decreases in larger communities
            'radio_systems': 0.4,  # 40% have radio systems
            'public_address_systems': min(0.8, max(0.2, community_size / 500)),
            'bulletin_boards': 0.7,  # 70% have physical bulletin systems
            'score': infrastructure_quality
        }
        
        # Information flow efficiency
        flow_efficiency = min(10, max(3, 10 - math.log2(max(1, community_size / 50))))  # Decreases with size
        
        comm_assessment['information_flow'] = {
            'message_reach_percent': min(95, max(60, 95 - (community_size / 100))),
            'transmission_speed_hours': max(0.5, min(24, community_size / 100)),  # Slower in larger communities
            'accuracy_rate': min(0.95, max(0.7, 0.95 - (community_size / 2000))),
            'feedback_loops': 0.6,  # 60% have feedback mechanisms
            'information_verification': 0.5,  # 50% verify information
            'rumor_control': 0.4,  # 40% effective at controlling rumors
            'score': flow_efficiency
        }
        
        # Emergency communication capabilities
        emergency_readiness = min(10, max(2, 2 + (community_size / 300)))  # Improves with resources
        
        comm_assessment['emergency_communication'] = {
            'alert_systems': min(1.0, max(0.3, community_size / 400)),  # Alert system coverage
            'backup_power': 0.4,  # 40% have backup power for communications
            'ham_radio_operators': max(0, min(20, community_size * 0.02)),  # 2% are ham operators
            'emergency_contacts': 0.8,  # 80% have emergency contact lists
            'evacuation_communication': 0.5,  # 50% have evacuation communication plans
            'coordination_protocols': 0.6,  # 60% have coordination protocols
            'score': emergency_readiness
        }
        
        # Digital communication systems
        digital_adoption = min(0.9, max(0.4, 0.4 + (community_size / 1500)))  # Higher in larger communities
        
        comm_assessment['digital_systems'] = {
            'social_media_use': digital_adoption,
            'community_apps': min(1.0, max(0.1, community_size / 800)),  # More apps in larger communities
            'email_lists': 0.7,  # 70% use email lists
            'text_messaging': 0.85,  # 85% use text messaging
            'video_conferencing': digital_adoption * 0.8,
            'digital_literacy': min(0.8, max(0.5, 0.5 + (community_size / 2000))),
            'score': digital_adoption * 10
        }
        
        # Informal communication networks
        informal_strength = min(1.0, max(0.6, 1.0 - (community_size / 1000)))  # Stronger in smaller communities
        
        comm_assessment['informal_networks'] = {
            'word_of_mouth': informal_strength,
            'social_gatherings': informal_strength * 0.8,
            'community_spaces': informal_strength * 0.7,
            'informal_leaders': informal_strength * 0.3,  # 30% are informal communication leaders
            'gossip_networks': informal_strength * 0.9,  # High gossip network strength
            'personal_relationships': informal_strength,
            'score': informal_strength * 8
        }
        
        # Communication redundancy
        redundancy_score = min(10, max(3, 3 + (len([k for k in comm_assessment['infrastructure'] 
                                               if k != 'score' and comm_assessment['infrastructure'][k] > 0.5]))))
        
        comm_assessment['redundancy'] = {
            'multiple_channels': redundancy_score / 10,
            'backup_systems': 0.4,  # 40% have backup systems
            'alternative_routes': 0.6,  # 60% have alternative communication routes
            'offline_capabilities': 0.5,  # 50% maintain offline communication
            'cross_platform_integration': 0.3,  # 30% integrate across platforms
            'resilience_rating': redundancy_score,
            'score': redundancy_score
        }
        
        # Calculate overall communication score
        subsystem_scores = [
            comm_assessment['infrastructure']['score'],
            comm_assessment['information_flow']['score'],
            comm_assessment['emergency_communication']['score'],
            comm_assessment['digital_systems']['score'],
            comm_assessment['informal_networks']['score'],
            comm_assessment['redundancy']['score']
        ]
        
        comm_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return comm_assessment
    
    def _assess_resource_distribution(self, community_size: int, geographic_area: float) -> Dict[str, Any]:
        """Assess resource distribution networks and logistics."""
        
        resource_assessment = {
            'distribution_networks': {},
            'storage_systems': {},
            'logistics_coordination': {},
            'equity_mechanisms': {},
            'efficiency_metrics': {},
            'resilience_factors': {},
            'overall_score': 0
        }
        
        # Distribution network infrastructure
        network_reach = min(1.0, max(0.4, 1.0 - (geographic_area / 100)))  # Harder to reach larger areas
        
        resource_assessment['distribution_networks'] = {
            'distribution_points': max(1, community_size / 100),  # 1 per 100 people
            'coverage_area_percent': network_reach * 100,
            'transportation_capacity': community_size * 2,  # 2 lbs per person capacity
            'delivery_frequency_per_week': min(7, max(1, 7 - (geographic_area / 20))),
            'last_mile_capability': network_reach * 0.8,  # 80% of network reach
            'accessibility_score': network_reach * 10,
            'score': network_reach * 10
        }
        
        # Storage and warehousing systems
        storage_per_capita = min(50, max(10, 50 - (community_size / 100)))  # Less per capita in larger communities
        
        resource_assessment['storage_systems'] = {
            'total_storage_capacity': community_size * storage_per_capita,
            'distributed_storage_sites': max(3, community_size / 150),
            'specialized_storage': 0.6,  # 60% have specialized storage (cold, dry, etc.)
            'climate_controlled': 0.4,  # 40% climate controlled
            'security_level': 7,  # Security rating 1-10
            'inventory_management': 0.5,  # 50% have inventory management systems
            'score': min(storage_per_capita / 5, 10)
        }
        
        # Logistics coordination capabilities
        coordination_efficiency = min(10, max(4, 10 - (community_size / 300)))  # Harder to coordinate larger groups
        
        resource_assessment['logistics_coordination'] = {
            'demand_forecasting': 0.4,  # 40% can forecast demand
            'supply_planning': 0.5,  # 50% plan supply effectively
            'route_optimization': 0.3,  # 30% optimize delivery routes
            'real_time_tracking': 0.2,  # 20% have real-time tracking
            'volunteer_coordination': 0.7,  # 70% coordinate volunteers
            'professional_logistics': 0.1,  # 10% have professional logistics staff
            'score': coordination_efficiency
        }
        
        # Equity and fairness mechanisms
        resource_assessment['equity_mechanisms'] = {
            'needs_based_allocation': 0.6,  # 60% use needs-based allocation
            'fair_distribution_protocols': 0.5,  # 50% have fair distribution protocols
            'vulnerable_population_priority': 0.7,  # 70% prioritize vulnerable populations
            'contribution_requirements': 0.4,  # 40% require contributions
            'dispute_resolution': 0.3,  # 30% have dispute resolution for distribution
            'transparency_measures': 0.5,  # 50% have transparent distribution
            'score': 5.5
        }
        
        # Distribution efficiency metrics
        efficiency_score = min(10, max(3, 10 - (geographic_area / 25) - (community_size / 500)))
        
        resource_assessment['efficiency_metrics'] = {
            'delivery_time_hours': max(1, min(72, geographic_area + (community_size / 100))),
            'resource_wastage_percent': max(5, min(25, 5 + (community_size / 200))),
            'fulfillment_rate_percent': min(95, max(70, 95 - (community_size / 200))),
            'cost_per_delivery': max(5, min(50, 5 + geographic_area)),
            'volunteer_hours_required': community_size * 2,  # 2 hours per person annually
            'automation_level': 0.2,  # 20% automated
            'score': efficiency_score
        }
        
        # Resilience and backup systems
        resource_assessment['resilience_factors'] = {
            'backup_suppliers': max(1, min(10, community_size / 200)),
            'alternative_distribution_methods': 0.6,  # 60% have alternatives
            'emergency_stockpiles': 0.4,  # 40% maintain emergency stockpiles
            'local_production_integration': 0.5,  # 50% integrate local production
            'failure_recovery_time_days': max(1, min(14, 14 - (community_size / 200))),
            'redundancy_level': 0.4,  # 40% redundancy in critical systems
            'score': 6
        }
        
        # Calculate overall resource distribution score
        subsystem_scores = [
            resource_assessment['distribution_networks']['score'],
            resource_assessment['storage_systems']['score'],
            resource_assessment['logistics_coordination']['score'],
            resource_assessment['equity_mechanisms']['score'],
            resource_assessment['efficiency_metrics']['score'],
            resource_assessment['resilience_factors']['score']
        ]
        
        resource_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return resource_assessment
    
    def _assess_leadership_structures(self, community_size: int) -> Dict[str, Any]:
        """Assess leadership and governance structures within networks."""
        
        leadership_assessment = {
            'formal_leadership': {},
            'informal_leadership': {},
            'distributed_leadership': {},
            'decision_making': {},
            'accountability': {},
            'leadership_development': {},
            'overall_score': 0
        }
        
        # Formal leadership structures
        formal_leaders = max(1, community_size / 50)  # 1 formal leader per 50 people
        
        leadership_assessment['formal_leadership'] = {
            'elected_leaders': formal_leaders * 0.6,  # 60% elected
            'appointed_leaders': formal_leaders * 0.4,  # 40% appointed
            'leadership_effectiveness': 6.5,  # Effectiveness rating 1-10
            'representative_diversity': 0.6,  # 60% diverse representation
            'term_limits': 0.7,  # 70% have term limits
            'leadership_training': 0.3,  # 30% have formal leadership training
            'score': 6.5
        }
        
        # Informal leadership networks
        informal_influence = min(1.0, max(0.6, 1.0 - (community_size / 1000)))  # Stronger in smaller communities
        
        leadership_assessment['informal_leadership'] = {
            'opinion_leaders': community_size * 0.05,  # 5% are opinion leaders
            'connector_nodes': community_size * 0.03,  # 3% are connectors
            'expertise_leaders': community_size * 0.08,  # 8% lead through expertise
            'influence_networks': informal_influence,
            'leadership_recognition': 0.7,  # 70% recognize informal leaders
            'integration_with_formal': 0.5,  # 50% integration with formal leadership
            'score': informal_influence * 8
        }
        
        # Distributed leadership model
        distribution_level = min(1.0, max(0.3, 0.3 + (community_size / 2000)))  # More distributed in larger communities
        
        leadership_assessment['distributed_leadership'] = {
            'task_based_leadership': distribution_level,
            'rotating_responsibilities': 0.4,  # 40% rotate responsibilities
            'skill_based_assignments': 0.6,  # 60% assign based on skills
            'collective_leadership': 0.3,  # 30% use collective leadership models
            'shared_decision_making': 0.5,  # 50% share decision making
            'leadership_pipeline': 0.4,  # 40% develop leadership pipeline
            'score': distribution_level * 8
        }
        
        # Decision making processes
        decision_efficiency = min(10, max(4, 10 - (community_size / 200)))  # Harder in larger communities
        
        leadership_assessment['decision_making'] = {
            'consensus_building': 0.4,  # 40% use consensus building
            'majority_voting': 0.7,  # 70% use majority voting
            'expert_consultation': 0.5,  # 50% consult experts
            'community_input': 0.6,  # 60% seek community input
            'decision_speed': decision_efficiency / 2,  # Speed of decision making
            'implementation_rate': 0.6,  # 60% of decisions implemented
            'score': decision_efficiency
        }
        
        # Accountability mechanisms
        leadership_assessment['accountability'] = {
            'performance_monitoring': 0.4,  # 40% monitor leader performance
            'feedback_systems': 0.5,  # 50% have feedback systems
            'removal_mechanisms': 0.6,  # 60% can remove ineffective leaders
            'transparency_requirements': 0.5,  # 50% require transparency
            'conflict_of_interest_policies': 0.3,  # 30% have conflict policies
            'regular_evaluations': 0.3,  # 30% conduct regular evaluations
            'score': 4.6
        }
        
        # Leadership development and succession
        development_capacity = min(10, max(3, 3 + (community_size / 300)))  # Better in larger communities
        
        leadership_assessment['leadership_development'] = {
            'mentorship_programs': 0.3,  # 30% have mentorship programs
            'leadership_training_opportunities': 0.4,  # 40% provide training
            'succession_planning': 0.2,  # 20% have succession plans
            'youth_leadership_development': 0.3,  # 30% develop youth leaders
            'cross_training': 0.2,  # 20% cross-train leaders
            'external_development_resources': 0.4,  # 40% access external resources
            'score': development_capacity
        }
        
        # Calculate overall leadership score
        subsystem_scores = [
            leadership_assessment['formal_leadership']['score'],
            leadership_assessment['informal_leadership']['score'],
            leadership_assessment['distributed_leadership']['score'],
            leadership_assessment['decision_making']['score'],
            leadership_assessment['accountability']['score'],
            leadership_assessment['leadership_development']['score']
        ]
        
        leadership_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return leadership_assessment
    
    def _assess_collective_efficacy(self, community_size: int) -> Dict[str, Any]:
        """Assess community's collective ability to solve problems and achieve goals."""
        
        efficacy_assessment = {
            'problem_solving_capacity': {},
            'collective_action': {},
            'goal_achievement': {},
            'innovation_adaptation': {},
            'learning_systems': {},
            'empowerment': {},
            'overall_score': 0
        }
        
        # Problem-solving capacity
        problem_solving_scale = min(10, max(4, 4 + (community_size / 500)))  # Improves with resources
        
        efficacy_assessment['problem_solving_capacity'] = {
            'problem_identification': 0.7,  # 70% can identify problems
            'root_cause_analysis': 0.4,  # 40% can analyze root causes
            'solution_generation': 0.6,  # 60% can generate solutions
            'resource_mobilization': 0.5,  # 50% can mobilize resources
            'implementation_capability': 0.5,  # 50% can implement solutions
            'success_rate': 0.6,  # 60% success rate in problem solving
            'score': problem_solving_scale
        }
        
        # Collective action capabilities
        action_capacity = min(1.0, max(0.4, 1.0 - (community_size / 1500)))  # Harder to coordinate larger groups
        
        efficacy_assessment['collective_action'] = {
            'mobilization_speed_days': max(1, min(30, 30 - (action_capacity * 25))),
            'participation_rate': action_capacity * 0.8,  # 80% of capacity
            'sustained_effort_capability': action_capacity * 0.7,  # 70% can sustain effort
            'coordination_effectiveness': action_capacity,
            'resource_contribution': action_capacity * 0.6,  # 60% contribute resources
            'volunteer_hours_annual': community_size * action_capacity * 50,  # 50 hours per person
            'score': action_capacity * 10
        }
        
        # Goal achievement track record
        efficacy_assessment['goal_achievement'] = {
            'goal_setting_ability': 0.6,  # 60% can set clear goals
            'goal_alignment': 0.5,  # 50% align on shared goals
            'milestone_tracking': 0.4,  # 40% track progress
            'completion_rate': 0.5,  # 50% complete projects
            'quality_of_outcomes': 0.6,  # 60% achieve quality outcomes
            'impact_measurement': 0.3,  # 30% measure impact
            'score': 5.4
        }
        
        # Innovation and adaptation capacity
        innovation_score = min(10, max(3, 3 + (community_size / 400)))  # Innovation improves with size
        
        efficacy_assessment['innovation_adaptation'] = {
            'creative_problem_solving': innovation_score / 10 * 0.7,
            'technology_adoption': min(0.8, max(0.3, 0.3 + (community_size / 1000))),
            'process_improvement': 0.5,  # 50% continuously improve
            'experimentation_willingness': 0.4,  # 40% willing to experiment
            'adaptation_speed': min(1.0, max(0.3, 1.0 - (community_size / 2000))),
            'knowledge_integration': 0.5,  # 50% integrate new knowledge
            'score': innovation_score
        }
        
        # Learning systems and knowledge management
        efficacy_assessment['learning_systems'] = {
            'lesson_capture': 0.4,  # 40% capture lessons learned
            'knowledge_sharing': 0.6,  # 60% share knowledge
            'best_practice_adoption': 0.3,  # 30% adopt best practices
            'failure_analysis': 0.3,  # 30% analyze failures
            'continuous_improvement': 0.4,  # 40% practice continuous improvement
            'institutional_memory': 0.5,  # 50% maintain institutional memory
            'score': 4.2
        }
        
        # Community empowerment levels
        empowerment_level = min(10, max(4, 10 - (community_size / 400)))  # Empowerment harder in larger groups
        
        efficacy_assessment['empowerment'] = {
            'self_determination': empowerment_level / 10 * 0.8,
            'control_over_outcomes': empowerment_level / 10 * 0.7,
            'influence_on_decisions': empowerment_level / 10 * 0.6,
            'resource_control': empowerment_level / 10 * 0.5,
            'skill_development': 0.5,  # 50% actively develop skills
            'confidence_in_abilities': empowerment_level / 10 * 0.8,
            'score': empowerment_level
        }
        
        # Calculate overall collective efficacy score
        subsystem_scores = [
            efficacy_assessment['problem_solving_capacity']['score'],
            efficacy_assessment['collective_action']['score'],
            efficacy_assessment['goal_achievement']['score'],
            efficacy_assessment['innovation_adaptation']['score'],
            efficacy_assessment['learning_systems']['score'],
            efficacy_assessment['empowerment']['score']
        ]
        
        efficacy_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return efficacy_assessment
    
    def _assess_disaster_preparedness_networks(self, community_size: int) -> Dict[str, Any]:
        """Assess disaster-specific network preparedness and response capabilities."""
        
        disaster_assessment = {
            'early_warning_networks': {},
            'emergency_response_coordination': {},
            'evacuation_networks': {},
            'resource_sharing_protocols': {},
            'recovery_networks': {},
            'preparedness_education': {},
            'overall_score': 0
        }
        
        # Early warning and information networks
        warning_reach = min(1.0, max(0.6, 1.0 - (community_size / 2000)))  # Better reach in smaller communities
        
        disaster_assessment['early_warning_networks'] = {
            'weather_monitoring': 0.7,  # 70% monitor weather
            'alert_dissemination': warning_reach * 0.9,  # 90% of reach capability
            'warning_verification': 0.5,  # 50% verify warnings
            'multi_channel_alerts': 0.6,  # 60% use multiple channels
            'response_time_minutes': max(5, min(120, 120 - (warning_reach * 100))),
            'coverage_population_percent': warning_reach * 100,
            'score': warning_reach * 10
        }
        
        # Emergency response coordination
        response_coordination = min(10, max(3, 3 + (community_size / 300)))  # Better coordination with more resources
        
        disaster_assessment['emergency_response_coordination'] = {
            'incident_command_system': 0.4,  # 40% use incident command system
            'response_team_organization': 0.6,  # 60% have organized response teams
            'inter_agency_coordination': 0.3,  # 30% coordinate with external agencies
            'volunteer_coordination': 0.7,  # 70% coordinate volunteers
            'resource_deployment': 0.5,  # 50% can deploy resources effectively
            'communication_redundancy': 0.4,  # 40% have redundant communication
            'score': response_coordination
        }
        
        # Evacuation and shelter networks
        evacuation_capacity = min(1.0, max(0.4, 1.0 - (community_size / 1000)))  # Harder to evacuate larger communities
        
        disaster_assessment['evacuation_networks'] = {
            'evacuation_route_planning': 0.5,  # 50% have evacuation routes planned
            'transportation_coordination': evacuation_capacity * 0.6,
            'shelter_capacity': community_size * 0.8,  # 80% shelter capacity
            'special_needs_support': 0.4,  # 40% support special needs evacuation
            'pet_accommodation': 0.3,  # 30% accommodate pets
            'evacuation_drill_frequency': 1,  # 1 drill per year
            'score': evacuation_capacity * 8
        }
        
        # Resource sharing protocols during disasters
        disaster_assessment['resource_sharing_protocols'] = {
            'emergency_stockpile_sharing': 0.6,  # 60% share emergency stockpiles
            'equipment_sharing': 0.7,  # 70% share equipment
            'skill_sharing': 0.8,  # 80% share skills during emergencies
            'space_sharing': 0.5,  # 50% share space (shelter, storage)
            'information_sharing': 0.9,  # 90% share information
            'coordination_protocols': 0.4,  # 40% have formal protocols
            'score': 6.5
        }
        
        # Recovery and rebuilding networks
        disaster_assessment['recovery_networks'] = {
            'damage_assessment_capability': 0.4,  # 40% can assess damage
            'cleanup_coordination': 0.7,  # 70% coordinate cleanup
            'rebuilding_cooperation': 0.6,  # 60% cooperate in rebuilding
            'mutual_aid_activation': 0.8,  # 80% activate mutual aid
            'resource_replacement': 0.5,  # 50% help replace resources
            'psychological_support': 0.3,  # 30% provide psychological support
            'score': 5.5
        }
        
        # Preparedness education and training networks
        education_reach = min(1.0, max(0.4, 0.4 + (community_size / 1500)))  # Better reach with more resources
        
        disaster_assessment['preparedness_education'] = {
            'preparedness_training_participation': education_reach * 0.5,
            'skill_training_programs': education_reach * 0.4,
            'drill_participation': education_reach * 0.6,
            'educational_material_distribution': education_reach * 0.8,
            'peer_to_peer_education': education_reach * 0.7,
            'knowledge_retention': 0.6,  # 60% retain preparedness knowledge
            'score': education_reach * 7
        }
        
        # Calculate overall disaster preparedness score
        subsystem_scores = [
            disaster_assessment['early_warning_networks']['score'],
            disaster_assessment['emergency_response_coordination']['score'],
            disaster_assessment['evacuation_networks']['score'],
            disaster_assessment['resource_sharing_protocols']['score'],
            disaster_assessment['recovery_networks']['score'],
            disaster_assessment['preparedness_education']['score']
        ]
        
        disaster_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return disaster_assessment
    
    def _assess_adaptive_capacity(self, community_size: int) -> Dict[str, Any]:
        """Assess community's ability to adapt and evolve networks over time."""
        
        adaptive_assessment = {
            'flexibility': {},
            'learning_capability': {},
            'evolution_mechanisms': {},
            'resilience_building': {},
            'external_connectivity': {},
            'future_orientation': {},
            'overall_score': 0
        }
        
        # Network flexibility and adaptability
        flexibility_score = min(10, max(4, 10 - (community_size / 500)))  # Smaller communities more flexible
        
        adaptive_assessment['flexibility'] = {
            'structure_modification': flexibility_score / 10 * 0.7,
            'role_reassignment': flexibility_score / 10 * 0.8,
            'process_adaptation': flexibility_score / 10 * 0.6,
            'technology_integration': min(0.8, max(0.3, 0.3 + (community_size / 1000))),
            'cultural_adaptation': 0.5,  # 50% can adapt culturally
            'change_acceptance': flexibility_score / 10 * 0.8,
            'score': flexibility_score
        }
        
        # Learning and knowledge evolution
        adaptive_assessment['learning_capability'] = {
            'experience_integration': 0.6,  # 60% integrate experiences
            'external_learning': 0.4,  # 40% learn from external sources
            'knowledge_updating': 0.5,  # 50% update knowledge regularly
            'skill_development': 0.6,  # 60% develop new skills
            'practice_evolution': 0.4,  # 40% evolve practices
            'wisdom_accumulation': 0.7,  # 70% accumulate collective wisdom
            'score': 5.4
        }
        
        # Evolution and growth mechanisms
        evolution_capacity = min(10, max(3, 3 + (community_size / 400)))  # Larger communities have more evolution capacity
        
        adaptive_assessment['evolution_mechanisms'] = {
            'network_expansion': evolution_capacity / 10 * 0.6,
            'new_connection_formation': evolution_capacity / 10 * 0.7,
            'obsolete_connection_pruning': 0.3,  # 30% prune obsolete connections
            'emergent_structure_recognition': 0.4,  # 40% recognize emergent structures
            'intentional_restructuring': 0.3,  # 30% intentionally restructure
            'organic_growth': 0.8,  # 80% grow organically
            'score': evolution_capacity
        }
        
        # Resilience building over time
        adaptive_assessment['resilience_building'] = {
            'redundancy_development': 0.5,  # 50% build redundancy over time
            'diversity_cultivation': 0.6,  # 60% cultivate diversity
            'strength_reinforcement': 0.7,  # 70% reinforce strengths
            'weakness_addressing': 0.4,  # 40% address weaknesses
            'capacity_building': 0.6,  # 60% build capacity systematically
            'vulnerability_reduction': 0.5,  # 50% reduce vulnerabilities
            'score': 5.6
        }
        
        # External connectivity and resources
        external_reach = min(1.0, max(0.3, 0.3 + (community_size / 800)))  # Larger communities have better external reach
        
        adaptive_assessment['external_connectivity'] = {
            'regional_networks': external_reach * 0.6,
            'professional_networks': external_reach * 0.5,
            'government_connections': external_reach * 0.4,
            'ngo_partnerships': external_reach * 0.3,
            'academic_connections': external_reach * 0.2,
            'resource_access': external_reach * 0.7,
            'score': external_reach * 8
        }
        
        # Future orientation and planning
        adaptive_assessment['future_orientation'] = {
            'long_term_planning': 0.4,  # 40% engage in long-term planning
            'scenario_planning': 0.2,  # 20% do scenario planning
            'trend_monitoring': 0.3,  # 30% monitor trends
            'strategic_thinking': 0.4,  # 40% think strategically
            'vision_development': 0.3,  # 30% develop shared vision
            'intergenerational_planning': 0.5,  # 50% plan for next generation
            'score': 3.5
        }
        
        # Calculate overall adaptive capacity score
        subsystem_scores = [
            adaptive_assessment['flexibility']['score'],
            adaptive_assessment['learning_capability']['score'],
            adaptive_assessment['evolution_mechanisms']['score'],
            adaptive_assessment['resilience_building']['score'],
            adaptive_assessment['external_connectivity']['score'],
            adaptive_assessment['future_orientation']['score']
        ]
        
        adaptive_assessment['overall_score'] = sum(subsystem_scores) / len(subsystem_scores)
        
        return adaptive_assessment
    
    def _assign_resilience_rating(self, overall_score: float) -> str:
        """Assign qualitative resilience rating based on overall score."""
        
        if overall_score >= 8.5:
            return "EXCEPTIONAL"
        elif overall_score >= 7.5:
            return "HIGH"
        elif overall_score >= 6.5:
            return "GOOD"
        elif overall_score >= 5.5:
            return "MODERATE"
        elif overall_score >= 4.5:
            return "FAIR"
        elif overall_score >= 3.5:
            return "LIMITED"
        else:
            return "POOR"
    
    def _identify_network_gaps(self, assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify critical gaps in network resilience."""
        
        gaps = []
        
        # Check each subsystem for gaps (scores below 6)
        subsystems = [
            ('Network Topology', assessment['network_topology']['overall_score']),
            ('Social Capital', assessment['social_capital']['overall_score']),
            ('Communication Systems', assessment['communication_systems']['overall_score']),
            ('Resource Distribution', assessment['resource_distribution']['overall_score']),
            ('Leadership Structures', assessment['leadership_structures']['overall_score']),
            ('Collective Efficacy', assessment['collective_efficacy']['overall_score']),
            ('Disaster Preparedness', assessment['disaster_preparedness']['overall_score']),
            ('Adaptive Capacity', assessment['adaptive_capacity']['overall_score'])
        ]
        
        for system_name, score in subsystems:
            if score < 6:
                severity = "CRITICAL" if score < 4 else "MODERATE" if score < 5 else "MINOR"
                gaps.append({
                    'system': system_name,
                    'current_score': score,
                    'gap_severity': severity,
                    'improvement_needed': 6 - score,
                    'priority_level': 10 - score  # Higher score = higher priority
                })
        
        # Sort gaps by priority level
        gaps.sort(key=lambda x: x['priority_level'], reverse=True)
        
        return gaps
    
    def _generate_priority_actions(self, assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate priority actions for improving network resilience."""
        
        actions = []
        community_size = assessment['community_size']
        
        # Actions based on identified gaps
        for gap in assessment['network_gaps'][:5]:  # Top 5 gaps
            system_name = gap['system']
            
            if system_name == 'Network Topology':
                actions.append({
                    'category': 'Network Building',
                    'action': 'Create Neighborhood Connection Groups',
                    'description': 'Form groups of 15-25 neighbors for regular interaction and mutual support',
                    'impact_potential': 8,
                    'implementation_difficulty': 4,
                    'timeline_weeks': 8,
                    'participants_needed': max(50, community_size * 0.1),
                    'resources_required': 'Meeting spaces, basic coordination tools'
                })
            
            elif system_name == 'Social Capital':
                actions.append({
                    'category': 'Social Cohesion',
                    'action': 'Launch Community Trust Building Initiative',
                    'description': 'Regular social events, shared projects, and conflict resolution training',
                    'impact_potential': 9,
                    'implementation_difficulty': 6,
                    'timeline_weeks': 16,
                    'participants_needed': max(30, community_size * 0.15),
                    'resources_required': 'Event coordination, trained facilitators'
                })
            
            elif system_name == 'Communication Systems':
                actions.append({
                    'category': 'Communication',
                    'action': 'Establish Multi-Channel Communication Network',
                    'description': 'Create redundant communication systems using digital and analog methods',
                    'impact_potential': 8,
                    'implementation_difficulty': 5,
                    'timeline_weeks': 12,
                    'participants_needed': max(15, community_size * 0.05),
                    'resources_required': 'Communication equipment, technical expertise'
                })
            
            elif system_name == 'Resource Distribution':
                actions.append({
                    'category': 'Resource Networks',
                    'action': 'Create Community Resource Sharing System',
                    'description': 'Establish tool libraries, bulk buying groups, and resource exchange',
                    'impact_potential': 7,
                    'implementation_difficulty': 5,
                    'timeline_weeks': 10,
                    'participants_needed': max(25, community_size * 0.08),
                    'resources_required': 'Storage space, inventory systems'
                })
            
            elif system_name == 'Leadership Structures':
                actions.append({
                    'category': 'Leadership Development',
                    'action': 'Implement Distributed Leadership Training',
                    'description': 'Train multiple community members in leadership and coordination skills',
                    'impact_potential': 8,
                    'implementation_difficulty': 6,
                    'timeline_weeks': 20,
                    'participants_needed': max(20, community_size * 0.04),
                    'resources_required': 'Training materials, experienced trainers'
                })
            
            elif system_name == 'Collective Efficacy':
                actions.append({
                    'category': 'Empowerment',
                    'action': 'Start Community Problem-Solving Projects',
                    'description': 'Practice collective action on small projects to build confidence and skills',
                    'impact_potential': 7,
                    'implementation_difficulty': 4,
                    'timeline_weeks': 6,
                    'participants_needed': max(40, community_size * 0.12),
                    'resources_required': 'Project coordination, basic resources'
                })
            
            elif system_name == 'Disaster Preparedness':
                actions.append({
                    'category': 'Emergency Preparedness',
                    'action': 'Create Neighborhood Emergency Response Teams',
                    'description': 'Train and organize local emergency response capabilities',
                    'impact_potential': 9,
                    'implementation_difficulty': 7,
                    'timeline_weeks': 24,
                    'participants_needed': max(30, community_size * 0.06),
                    'resources_required': 'Emergency equipment, professional training'
                })
            
            elif system_name == 'Adaptive Capacity':
                actions.append({
                    'category': 'Adaptive Learning',
                    'action': 'Establish Community Learning Network',
                    'description': 'Create systems for continuous learning and adaptation',
                    'impact_potential': 6,
                    'implementation_difficulty': 6,
                    'timeline_weeks': 16,
                    'participants_needed': max(20, community_size * 0.04),
                    'resources_required': 'Learning resources, facilitation skills'
                })
        
        # Add universal high-impact actions
        actions.append({
            'category': 'Foundation Building',
            'action': 'Map Community Assets and Connections',
            'description': 'Create comprehensive map of community resources, skills, and relationships',
            'impact_potential': 8,
            'implementation_difficulty': 3,
            'timeline_weeks': 4,
            'participants_needed': max(10, community_size * 0.02),
            'resources_required': 'Survey tools, data compilation'
        })
        
        actions.append({
            'category': 'Network Integration',
            'action': 'Launch Monthly Community Gatherings',
            'description': 'Regular gatherings to strengthen relationships and coordinate activities',
            'impact_potential': 7,
            'implementation_difficulty': 3,
            'timeline_weeks': 2,
            'participants_needed': max(5, community_size * 0.01),
            'resources_required': 'Meeting venue, basic refreshments'
        })
        
        # Sort actions by impact potential and feasibility
        for action in actions:
            action['feasibility_score'] = 10 - action['implementation_difficulty']
            action['priority_score'] = (action['impact_potential'] + action['feasibility_score']) / 2
        
        actions.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return actions[:10]  # Return top 10 actions
    
    def _store_assessment(self, assessment: Dict[str, Any]):
        """Store the network assessment in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO network_assessments 
            (assessment_date, community_size, geographic_area, assessment_data, 
             overall_score, resilience_rating)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            assessment['timestamp'],
            assessment['community_size'],
            assessment['geographic_area'],
            json.dumps(assessment),
            assessment['overall_score'],
            assessment['resilience_rating']
        ))
        
        conn.commit()
        conn.close()
    
    def create_network_map(self, nodes: List[Dict[str, Any]], 
                         connections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a network map from nodes and connections data."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        network_map = {
            'nodes_added': 0,
            'connections_added': 0,
            'network_stats': {},
            'topology_analysis': {}
        }
        
        # Add nodes to database
        for node in nodes:
            cursor.execute('''
                INSERT OR REPLACE INTO network_nodes 
                (node_id, node_type, node_name, location_lat, location_lon, 
                 capabilities, resources, trust_score, participation_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                node['id'], node['type'], node['name'],
                node.get('lat'), node.get('lon'),
                json.dumps(node.get('capabilities', [])),
                json.dumps(node.get('resources', [])),
                node.get('trust_score', 5.0),
                node.get('participation_level', 5)
            ))
            network_map['nodes_added'] += 1
        
        # Add connections to database
        for connection in connections:
            cursor.execute('''
                INSERT OR REPLACE INTO network_connections 
                (node_a_id, node_b_id, connection_type, connection_strength,
                 communication_frequency, resource_exchange, trust_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                connection['node_a'], connection['node_b'], connection['type'],
                connection.get('strength', 0.5),
                connection.get('communication_frequency', 1),
                connection.get('resource_exchange', 0.0),
                connection.get('trust_level', 5.0)
            ))
            network_map['connections_added'] += 1
        
        conn.commit()
        
        # Calculate network statistics
        cursor.execute('SELECT COUNT(*) FROM network_nodes')
        total_nodes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM network_connections')
        total_connections = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(trust_score) FROM network_nodes')
        avg_trust = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(participation_level) FROM network_nodes')
        avg_participation = cursor.fetchone()[0] or 0
        
        network_map['network_stats'] = {
            'total_nodes': total_nodes,
            'total_connections': total_connections,
            'density': total_connections / max((total_nodes * (total_nodes - 1) / 2), 1),
            'average_trust': avg_trust,
            'average_participation': avg_participation,
            'connections_per_node': total_connections / max(total_nodes, 1)
        }
        
        # Basic topology analysis
        network_map['topology_analysis'] = {
            'network_type': 'small_world' if network_map['network_stats']['density'] < 0.1 else 'dense',
            'connectivity_assessment': 'good' if network_map['network_stats']['connections_per_node'] > 3 else 'sparse',
            'trust_level': 'high' if avg_trust > 7 else 'moderate' if avg_trust > 5 else 'low',
            'participation_level': 'high' if avg_participation > 7 else 'moderate' if avg_participation > 5 else 'low'
        }
        
        conn.close()
        
        return network_map
    
    def simulate_disaster_response(self, disaster_type: str, severity: int, 
                                 duration_days: int, affected_area_percent: float) -> Dict[str, Any]:
        """Simulate how the community network would respond to a disaster."""
        
        simulation = {
            'disaster_scenario': {
                'type': disaster_type,
                'severity': severity,  # 1-10 scale
                'duration_days': duration_days,
                'affected_area_percent': affected_area_percent
            },
            'network_response': {},
            'effectiveness_metrics': {},
            'lessons_learned': [],
            'improvement_recommendations': []
        }
        
        # Get resilience factors for this disaster type
        if disaster_type in self.disaster_resilience_factors:
            resilience_factors = self.disaster_resilience_factors[disaster_type]
        else:
            # Use natural disasters as default
            resilience_factors = self.disaster_resilience_factors['natural_disasters']
        
        # Simulate network response phases
        simulation['network_response'] = {
            'immediate_response': self._simulate_immediate_response(severity, affected_area_percent, resilience_factors),
            'coordination_phase': self._simulate_coordination_phase(severity, duration_days, resilience_factors),
            'resource_mobilization': self._simulate_resource_mobilization(severity, affected_area_percent, resilience_factors),
            'recovery_phase': self._simulate_recovery_phase(severity, duration_days, resilience_factors)
        }
        
        # Calculate effectiveness metrics
        response_scores = [
            simulation['network_response']['immediate_response']['effectiveness'],
            simulation['network_response']['coordination_phase']['effectiveness'],
            simulation['network_response']['resource_mobilization']['effectiveness'],
            simulation['network_response']['recovery_phase']['effectiveness']
        ]
        
        simulation['effectiveness_metrics'] = {
            'overall_effectiveness': sum(response_scores) / len(response_scores),
            'response_speed': simulation['network_response']['immediate_response']['response_time_hours'],
            'coordination_quality': simulation['network_response']['coordination_phase']['effectiveness'],
            'resource_adequacy': simulation['network_response']['resource_mobilization']['resource_sufficiency'],
            'recovery_speed': simulation['network_response']['recovery_phase']['recovery_time_days'],
            'network_resilience': max(0, 10 - (severity * affected_area_percent * 0.5))
        }
        
        # Generate lessons learned
        simulation['lessons_learned'] = self._generate_disaster_lessons(simulation)
        
        # Generate improvement recommendations
        simulation['improvement_recommendations'] = self._generate_disaster_improvements(simulation)
        
        # Store simulation results
        self._store_disaster_simulation(simulation)
        
        return simulation
    
    def _simulate_immediate_response(self, severity: int, affected_area: float, 
                                   factors: Dict[str, float]) -> Dict[str, Any]:
        """Simulate immediate disaster response (first 24 hours)."""
        
        # Response time decreases with severity and affected area
        base_response_time = min(24, max(0.5, severity * affected_area * 2))
        
        # Early warning effectiveness
        early_warning_score = factors.get('early_warning', 0.3) * 10
        warning_effectiveness = min(1.0, max(0.2, early_warning_score / 10))
        
        response_time = base_response_time * (1 - warning_effectiveness * 0.5)
        
        return {
            'response_time_hours': response_time,
            'warning_effectiveness': warning_effectiveness,
            'initial_mobilization': min(1.0, max(0.3, 1.0 - (severity * 0.1))),
            'information_sharing': factors.get('information_sharing', 0.1) * 10,
            'immediate_aid_provided': min(1.0, max(0.2, 1.0 - (affected_area * 0.8))),
            'effectiveness': min(10, max(2, 10 - severity * affected_area))
        }
    
    def _simulate_coordination_phase(self, severity: int, duration: int, 
                                   factors: Dict[str, float]) -> Dict[str, Any]:
        """Simulate coordination phase (days 1-7)."""
        
        coordination_effectiveness = factors.get('evacuation_coordination', 0.2) * 10
        
        return {
            'leadership_emergence': min(1.0, max(0.4, 1.0 - (severity * 0.08))),
            'communication_maintenance': min(1.0, max(0.3, 1.0 - (severity * 0.1))),
            'resource_coordination': min(1.0, max(0.3, coordination_effectiveness / 10)),
            'volunteer_organization': min(1.0, max(0.5, 1.0 - (severity * 0.05))),
            'decision_making_speed': min(10, max(2, 10 - severity * 0.5)),
            'effectiveness': coordination_effectiveness
        }
    
    def _simulate_resource_mobilization(self, severity: int, affected_area: float, 
                                      factors: Dict[str, float]) -> Dict[str, Any]:
        """Simulate resource mobilization phase."""
        
        resource_pooling_score = factors.get('resource_pooling', 0.25) * 10
        resource_need = severity * affected_area * 10  # Total resource need
        resource_available = resource_pooling_score * 5  # Available resources
        
        return {
            'resource_need': resource_need,
            'resource_available': resource_available,
            'resource_sufficiency': min(1.0, resource_available / max(resource_need, 1)),
            'distribution_efficiency': min(1.0, max(0.3, 1.0 - affected_area * 0.6)),
            'external_resource_access': min(1.0, max(0.2, 1.0 - severity * 0.1)),
            'stockpile_utilization': 0.8,  # 80% of stockpiles utilized
            'effectiveness': resource_pooling_score
        }
    
    def _simulate_recovery_phase(self, severity: int, duration: int, 
                               factors: Dict[str, float]) -> Dict[str, Any]:
        """Simulate recovery and rebuilding phase."""
        
        recovery_cooperation = factors.get('recovery_cooperation', 0.15) * 10
        recovery_time = max(7, min(365, severity * duration * 2))  # Recovery time in days
        
        return {
            'recovery_time_days': recovery_time,
            'community_cooperation': min(1.0, max(0.4, recovery_cooperation / 10)),
            'rebuilding_coordination': min(1.0, max(0.3, 1.0 - severity * 0.08)),
            'lesson_integration': 0.6,  # 60% integrate lessons learned
            'network_strengthening': min(1.0, max(0.2, 1.0 - severity * 0.06)),
            'resilience_improvement': min(1.0, max(0.0, 0.5 - severity * 0.05)),
            'effectiveness': recovery_cooperation
        }
    
    def _generate_disaster_lessons(self, simulation: Dict[str, Any]) -> List[str]:
        """Generate lessons learned from disaster simulation."""
        
        lessons = []
        effectiveness = simulation['effectiveness_metrics']['overall_effectiveness']
        disaster_type = simulation['disaster_scenario']['type']
        severity = simulation['disaster_scenario']['severity']
        
        if effectiveness < 6:
            lessons.append("Communication systems need significant improvement for effective disaster response")
            lessons.append("Community coordination mechanisms require strengthening")
        
        if simulation['network_response']['immediate_response']['response_time_hours'] > 6:
            lessons.append("Early warning systems need faster activation and broader reach")
        
        if simulation['network_response']['resource_mobilization']['resource_sufficiency'] < 0.7:
            lessons.append("Community resource stockpiles and sharing systems need expansion")
        
        if simulation['network_response']['recovery_phase']['recovery_time_days'] > 30:
            lessons.append("Recovery coordination and mutual aid systems need development")
        
        if severity > 7:
            lessons.append("High-severity disasters reveal need for external support networks")
        
        # Disaster-specific lessons
        if disaster_type == 'natural_disasters':
            lessons.append("Physical infrastructure backup and redundancy critical for natural disasters")
        elif disaster_type == 'economic_disruption':
            lessons.append("Alternative economic systems become essential during economic disruption")
        elif disaster_type == 'supply_chain_failure':
            lessons.append("Local production and distribution networks need strengthening")
        
        return lessons[:6]  # Return top 6 lessons
    
    def _generate_disaster_improvements(self, simulation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement recommendations from disaster simulation."""
        
        improvements = []
        effectiveness = simulation['effectiveness_metrics']['overall_effectiveness']
        
        if effectiveness < 7:
            improvements.append({
                'area': 'Emergency Communication',
                'action': 'Establish redundant communication systems with backup power',
                'priority': 'HIGH',
                'timeline_months': 6,
                'expected_improvement': 2.0
            })
        
        if simulation['network_response']['immediate_response']['response_time_hours'] > 8:
            improvements.append({
                'area': 'Early Warning',
                'action': 'Create multi-channel alert system with community wardens',
                'priority': 'HIGH',
                'timeline_months': 4,
                'expected_improvement': 1.5
            })
        
        if simulation['network_response']['resource_mobilization']['resource_sufficiency'] < 0.6:
            improvements.append({
                'area': 'Resource Networks',
                'action': 'Develop community stockpiles and resource sharing protocols',
                'priority': 'MEDIUM',
                'timeline_months': 8,
                'expected_improvement': 1.8
            })
        
        improvements.append({
            'area': 'Network Resilience',
            'action': 'Regular disaster simulation exercises and network testing',
            'priority': 'MEDIUM',
            'timeline_months': 3,
            'expected_improvement': 1.0
        })
        
        return improvements
    
    def _store_disaster_simulation(self, simulation: Dict[str, Any]):
        """Store disaster simulation results in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        scenario = simulation['disaster_scenario']
        effectiveness = simulation['effectiveness_metrics']['overall_effectiveness']
        
        cursor.execute('''
            INSERT INTO resilience_scenarios 
            (scenario_name, scenario_type, severity_level, duration_days, 
             affected_area, network_response, effectiveness_score, lessons_learned)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f"{scenario['type']} - Severity {scenario['severity']}",
            scenario['type'],
            scenario['severity'],
            scenario['duration_days'],
            scenario['affected_area_percent'],
            json.dumps(simulation['network_response']),
            effectiveness,
            json.dumps(simulation['lessons_learned'])
        ))
        
        conn.commit()
        conn.close()
    
    def generate_resilience_report(self, assessment_data: Dict[str, Any] = None) -> str:
        """Generate comprehensive ASCII report of community network resilience."""
        
        if not assessment_data:
            # Get most recent assessment from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT assessment_data FROM network_assessments ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return "No assessment data available. Run assess_network_resilience() first."
            
            assessment_data = json.loads(result[0])
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                    COMMUNITY RESILIENCE NETWORKS REPORT                     ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        report.append("")
        
        # Assessment overview
        report.append("🌐 NETWORK RESILIENCE OVERVIEW")
        report.append("=" * 80)
        report.append(f"Assessment Date: {assessment_data['timestamp'][:10]}")
        report.append(f"Community Size: {assessment_data['community_size']} people")
        report.append(f"Geographic Area: {assessment_data['geographic_area']} square miles")
        report.append(f"Overall Resilience Score: {assessment_data['overall_score']:.1f}/10")
        report.append(f"Resilience Rating: {assessment_data['resilience_rating']}")
        report.append("")
        
        # Create score visualization
        score = assessment_data['overall_score']
        filled_bars = int(score)
        empty_bars = 10 - filled_bars
        score_bar = "█" * filled_bars + "░" * empty_bars
        report.append(f"Network Resilience: [{score_bar}] {score:.1f}/10")
        report.append("")
        
        # Subsystem performance matrix
        subsystems = [
            ("🔗 Network Topology", assessment_data['network_topology']['overall_score']),
            ("🤝 Social Capital", assessment_data['social_capital']['overall_score']),
            ("📡 Communication Systems", assessment_data['communication_systems']['overall_score']),
            ("📦 Resource Distribution", assessment_data['resource_distribution']['overall_score']),
            ("👥 Leadership Structures", assessment_data['leadership_structures']['overall_score']),
            ("💪 Collective Efficacy", assessment_data['collective_efficacy']['overall_score']),
            ("🚨 Disaster Preparedness", assessment_data['disaster_preparedness']['overall_score']),
            ("🔄 Adaptive Capacity", assessment_data['adaptive_capacity']['overall_score'])
        ]
        
        report.append("🎯 NETWORK SYSTEM PERFORMANCE")
        report.append("=" * 80)
        for name, score in subsystems:
            filled = int(score)
            empty = 10 - filled
            bar = "█" * filled + "░" * empty
            status = "STRONG" if score >= 7 else "ADEQUATE" if score >= 5.5 else "NEEDS WORK"
            report.append(f"{name:<24} [{bar}] {score:.1f}/10 {status}")
        report.append("")
        
        # Network topology details
        topology_data = assessment_data['network_topology']
        report.append("🔗 NETWORK TOPOLOGY ANALYSIS")
        report.append("=" * 80)
        
        if 'network_density' in topology_data:
            density = topology_data['network_density']
            report.append(f"Network Density: {density['density_ratio']:.3f} ({density['current_adequacy']}/10 adequacy)")
        
        if 'connectivity_patterns' in topology_data:
            patterns = topology_data['connectivity_patterns']
            report.append(f"Network Structure: Clustering={patterns['clustering_coefficient']:.2f}, Path Length={patterns['average_path_length']:.1f}")
        
        if 'redundancy_levels' in topology_data:
            redundancy = topology_data['redundancy_levels']
            report.append(f"Redundancy: {redundancy['redundant_paths']:.0f} redundant paths, {redundancy['single_point_failures']:.0f} critical nodes")
        report.append("")
        
        # Social capital breakdown
        social_data = assessment_data['social_capital']
        report.append("🤝 SOCIAL CAPITAL ANALYSIS")
        report.append("=" * 80)
        
        if 'trust_levels' in social_data:
            trust = social_data['trust_levels']
            report.append(f"Community Trust: {trust['generalized_trust']:.1f}/10 (Interpersonal: {trust['interpersonal_trust']:.1f}/10)")
        
        if 'social_cohesion' in social_data:
            cohesion = social_data['social_cohesion']
            report.append(f"Social Cohesion: {cohesion['overall_cohesion']:.1f} (Identity: {cohesion['shared_identity']*100:.0f}%, Goals: {cohesion['collective_goals']*100:.0f}%)")
        
        if 'civic_engagement' in social_data:
            civic = social_data['civic_engagement']
            report.append(f"Civic Participation: {civic['volunteer_participation']*100:.0f}% volunteer, {civic['meeting_attendance']*100:.0f}% meeting attendance")
        report.append("")
        
        # Communication systems
        comm_data = assessment_data['communication_systems']
        report.append("📡 COMMUNICATION SYSTEMS ANALYSIS")
        report.append("=" * 80)
        
        if 'information_flow' in comm_data:
            flow = comm_data['information_flow']
            report.append(f"Information Flow: {flow['message_reach_percent']:.0f}% reach in {flow['transmission_speed_hours']:.1f} hours")
            report.append(f"Accuracy Rate: {flow['accuracy_rate']*100:.0f}% (Verification: {flow['information_verification']*100:.0f}%)")
        
        if 'emergency_communication' in comm_data:
            emergency = comm_data['emergency_communication']
            report.append(f"Emergency Systems: {emergency['alert_systems']*100:.0f}% alert coverage, {emergency['ham_radio_operators']:.0f} ham operators")
        
        if 'redundancy' in comm_data:
            redundancy = comm_data['redundancy']
            report.append(f"Communication Redundancy: {redundancy['resilience_rating']:.0f}/10 (Backup: {redundancy['backup_systems']*100:.0f}%)")
        report.append("")
        
        # Leadership and governance
        leadership_data = assessment_data['leadership_structures']
        report.append("👥 LEADERSHIP STRUCTURES ANALYSIS")
        report.append("=" * 80)
        
        if 'formal_leadership' in leadership_data:
            formal = leadership_data['formal_leadership']
            report.append(f"Formal Leadership: {formal['elected_leaders']:.0f} elected, {formal['appointed_leaders']:.0f} appointed")
            report.append(f"Leadership Effectiveness: {formal['leadership_effectiveness']:.1f}/10")
        
        if 'decision_making' in leadership_data:
            decision = leadership_data['decision_making']
            report.append(f"Decision Making: {decision['consensus_building']*100:.0f}% consensus, {decision['community_input']*100:.0f}% community input")
        
        if 'distributed_leadership' in leadership_data:
            distributed = leadership_data['distributed_leadership']
            report.append(f"Distributed Leadership: {distributed['shared_decision_making']*100:.0f}% shared decisions")
        report.append("")
        
        # Disaster preparedness capabilities
        disaster_data = assessment_data['disaster_preparedness']
        report.append("🚨 DISASTER PREPAREDNESS ANALYSIS")
        report.append("=" * 80)
        
        if 'early_warning_networks' in disaster_data:
            warning = disaster_data['early_warning_networks']
            report.append(f"Early Warning: {warning['coverage_population_percent']:.0f}% coverage, {warning['response_time_minutes']:.0f} min response")
        
        if 'emergency_response_coordination' in disaster_data:
            response = disaster_data['emergency_response_coordination']
            report.append(f"Emergency Response: {response['incident_command_system']*100:.0f}% ICS, {response['volunteer_coordination']*100:.0f}% volunteer coord")
        
        if 'evacuation_networks' in disaster_data:
            evacuation = disaster_data['evacuation_networks']
            report.append(f"Evacuation Capacity: {evacuation['shelter_capacity']:.0f} people, {evacuation['evacuation_route_planning']*100:.0f}% route planning")
        report.append("")
        
        # Network gaps analysis
        if 'network_gaps' in assessment_data and assessment_data['network_gaps']:
            report.append("⚠️  CRITICAL NETWORK GAPS")
            report.append("=" * 80)
            
            for gap in assessment_data['network_gaps'][:5]:
                severity_icon = "🔴" if gap['gap_severity'] == "CRITICAL" else "🟡" if gap['gap_severity'] == "MODERATE" else "🟢"
                report.append(f"{severity_icon} {gap['system']}: {gap['current_score']:.1f}/10 - {gap['gap_severity']} GAP")
                report.append(f"   Improvement Needed: +{gap['improvement_needed']:.1f} points")
            report.append("")
        
        # Priority actions
        if 'priority_actions' in assessment_data and assessment_data['priority_actions']:
            report.append("🎯 PRIORITY ACTIONS")
            report.append("=" * 80)
            
            for i, action in enumerate(assessment_data['priority_actions'][:6], 1):
                impact_bar = "█" * int(action['impact_potential']) + "░" * (10 - int(action['impact_potential']))
                report.append(f"{i}. {action['action']}")
                report.append(f"   {action['description']}")
                report.append(f"   Impact: [{impact_bar[:10]}] {action['impact_potential']}/10")
                report.append(f"   Timeline: {action['timeline_weeks']} weeks | Participants: {action['participants_needed']:.0f}")
                report.append("")
        
        # Resilience rating interpretation
        report.append("📊 RESILIENCE RATING INTERPRETATION")
        report.append("=" * 80)
        rating = assessment_data['resilience_rating']
        
        if rating == "EXCEPTIONAL":
            interpretation = "Community has exceptional network resilience with redundant systems and strong adaptive capacity"
        elif rating == "HIGH":
            interpretation = "Community has high resilience with effective networks and good disaster preparedness"
        elif rating == "GOOD":
            interpretation = "Community has good basic resilience but could strengthen some network areas"
        elif rating == "MODERATE":
            interpretation = "Community has moderate resilience with several areas needing improvement"
        elif rating == "FAIR":
            interpretation = "Community has fair resilience but significant gaps in network capabilities"
        elif rating == "LIMITED":
            interpretation = "Community has limited resilience with major network weaknesses"
        else:
            interpretation = "Community has poor resilience requiring comprehensive network development"
        
        report.append(f"Rating: {rating}")
        report.append(f"Assessment: {interpretation}")
        report.append("")
        
        # Recommendations summary
        report.append("📋 IMPLEMENTATION ROADMAP")
        report.append("=" * 80)
        
        if assessment_data['overall_score'] < 5:
            report.append("🚨 IMMEDIATE PRIORITY: Focus on basic network building and trust development")
            report.append("   → Start with neighborhood groups and communication systems")
        elif assessment_data['overall_score'] < 7:
            report.append("⚡ DEVELOPMENT FOCUS: Strengthen existing networks and fill critical gaps")
            report.append("   → Enhance coordination systems and disaster preparedness")
        else:
            report.append("🎯 OPTIMIZATION FOCUS: Fine-tune systems and build advanced capabilities")
            report.append("   → Develop adaptive capacity and external connections")
        
        report.append("")
        report.append("🔄 CONTINUOUS IMPROVEMENT:")
        report.append("   • Conduct quarterly network assessments")
        report.append("   • Run annual disaster response simulations")
        report.append("   • Maintain network mapping and relationship tracking")
        report.append("   • Regular community feedback and adjustment cycles")
        report.append("")
        
        report.append("━" * 80)
        report.append("🎯 NEXT STEPS: Begin with highest-priority actions and build network systematically")
        report.append("━" * 80)
        
        return "\n".join(report)

# Example usage and testing
if __name__ == "__main__":
    print("Community Resilience Networks Module - Test Suite")
    print("=" * 60)
    
    # Initialize the system
    resilience_system = CommunityResilienceNetworks("test_community_resilience.db")
    
    # Test assessments for different community configurations
    test_scenarios = [
        {"community_size": 150, "geographic_area": 5.0, "description": "Small Rural Community"},
        {"community_size": 800, "geographic_area": 15.0, "description": "Medium Suburban Community"},
        {"community_size": 2500, "geographic_area": 50.0, "description": "Large Urban Community"}
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 TEST SCENARIO {i}: {scenario['description']}")
        print(f"Population: {scenario['community_size']}, Area: {scenario['geographic_area']} sq mi")
        print("-" * 60)
        
        assessment = resilience_system.assess_network_resilience(
            scenario['community_size'],
            scenario['geographic_area']
        )
        
        print(f"Overall Resilience Score: {assessment['overall_score']:.1f}/10")
        print(f"Resilience Rating: {assessment['resilience_rating']}")
        print("")
        
        # Show subsystem scores
        subsystem_scores = {
            "Network Topology": assessment['network_topology']['overall_score'],
            "Social Capital": assessment['social_capital']['overall_score'],
            "Communication": assessment['communication_systems']['overall_score'],
            "Resource Distribution": assessment['resource_distribution']['overall_score'],
            "Leadership": assessment['leadership_structures']['overall_score'],
            "Collective Efficacy": assessment['collective_efficacy']['overall_score'],
            "Disaster Preparedness": assessment['disaster_preparedness']['overall_score'],
            "Adaptive Capacity": assessment['adaptive_capacity']['overall_score']
        }
        
        for system, score in subsystem_scores.items():
            status = "✅" if score >= 7 else "⚠️" if score >= 5.5 else "❌"
            print(f"  {status} {system}: {score:.1f}/10")
        
        print(f"\nTop Network Gaps:")
        for gap in assessment['network_gaps'][:3]:
            print(f"  • {gap['system']}: {gap['gap_severity']} gap ({gap['current_score']:.1f}/10)")
        
        print(f"\nTop Priority Actions:")
        for j, action in enumerate(assessment['priority_actions'][:3], 1):
            print(f"  {j}. {action['action']} (Impact: {action['impact_potential']}/10)")
        
        if i == 2:  # Generate full report for second scenario
            print(f"\n📊 FULL RESILIENCE ASSESSMENT REPORT")
            print("=" * 80)
            report = resilience_system.generate_resilience_report(assessment)
            print(report)
    
    # Test network mapping
    print(f"\n🧪 TESTING NETWORK MAPPING")
    print("-" * 50)
    
    # Create sample network nodes
    sample_nodes = [
        {'id': 'node_001', 'type': 'household', 'name': 'Smith Family', 'capabilities': ['medical', 'mechanical']},
        {'id': 'node_002', 'type': 'household', 'name': 'Jones Family', 'capabilities': ['food_production', 'education']},
        {'id': 'node_003', 'type': 'organization', 'name': 'Community Center', 'capabilities': ['coordination', 'shelter']},
        {'id': 'node_004', 'type': 'business', 'name': 'Local Market', 'capabilities': ['food_supply', 'communications']}
    ]
    
    # Create sample connections
    sample_connections = [
        {'node_a': 'node_001', 'node_b': 'node_002', 'type': 'neighbor', 'strength': 0.8},
        {'node_a': 'node_001', 'node_b': 'node_003', 'type': 'volunteer', 'strength': 0.6},
        {'node_a': 'node_002', 'node_b': 'node_003', 'type': 'volunteer', 'strength': 0.7},
        {'node_a': 'node_003', 'node_b': 'node_004', 'type': 'partner', 'strength': 0.9}
    ]
    
    network_map = resilience_system.create_network_map(sample_nodes, sample_connections)
    print(f"Network Nodes Added: {network_map['nodes_added']}")
    print(f"Network Connections Added: {network_map['connections_added']}")
    print(f"Network Density: {network_map['network_stats']['density']:.3f}")
    print(f"Average Trust Level: {network_map['network_stats']['average_trust']:.1f}")
    print(f"Network Type: {network_map['topology_analysis']['network_type']}")
    
    # Test disaster simulation
    print(f"\n🧪 TESTING DISASTER RESPONSE SIMULATION")
    print("-" * 50)
    
    simulation = resilience_system.simulate_disaster_response(
        disaster_type='natural_disasters',
        severity=7,
        duration_days=5,
        affected_area_percent=0.3
    )
    
    print(f"Disaster Scenario: {simulation['disaster_scenario']['type']} (Severity {simulation['disaster_scenario']['severity']})")
    print(f"Overall Response Effectiveness: {simulation['effectiveness_metrics']['overall_effectiveness']:.1f}/10")
    print(f"Response Time: {simulation['effectiveness_metrics']['response_speed']:.1f} hours")
    print(f"Recovery Time: {simulation['effectiveness_metrics']['recovery_speed']:.0f} days")
    
    print(f"\nTop Lessons Learned:")
    for lesson in simulation['lessons_learned'][:3]:
        print(f"  • {lesson}")
    
    print(f"\nTop Improvement Recommendations:")
    for improvement in simulation['improvement_recommendations'][:3]:
        print(f"  • {improvement['action']} ({improvement['priority']} priority)")
    
    print(f"\n✅ Community Resilience Networks Module test completed successfully!")
    print("🎯 Phase 2B: Long-term Sustainability System - All modules complete!")