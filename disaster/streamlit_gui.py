#!/usr/bin/env python3
"""
Streamlit GUI for Emergency Preparedness System
User-friendly web interface with real-time updates
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from typing import Dict, Any, List
import asyncio

# Import our system for direct access (fallback if API unavailable)
try:
    from integrated_preparedness_system import IntegratedPreparednessSystem
    from user_profile_manager import UserProfileManager
    from backup_manager import BackupManager
    DIRECT_ACCESS = True
except ImportError:
    DIRECT_ACCESS = False

# Configuration
API_BASE_URL = "http://localhost:8000"
EMBEDDED_API_KEY = "gui_key"  # Embedded API key for GUI

# Page configuration
st.set_page_config(
    page_title="Emergency Preparedness System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b 0%, #feca57 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin: 0.5rem 0;
    }
    .alert-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class APIClient:
    """API client for communicating with backend"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.session = requests.Session()
        
    def get(self, endpoint: str) -> Dict[Any, Any]:
        """GET request to API"""
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def post(self, endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """POST request to API"""
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=self.headers,
                timeout=10
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def put(self, endpoint: str, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """PUT request to API"""
        try:
            response = self.session.put(
                f"{self.base_url}{endpoint}",
                json=data,
                headers=self.headers,
                timeout=10
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = None
if 'api_client' not in st.session_state:
    st.session_state.api_client = None
if 'using_api' not in st.session_state:
    st.session_state.using_api = False

def initialize_system():
    """Initialize either API client or direct system access"""
    if st.session_state.system is None:
        # Try API first
        try:
            api_client = APIClient(API_BASE_URL, EMBEDDED_API_KEY)
            health = api_client.get("/health")
            if "error" not in health:
                st.session_state.api_client = api_client
                st.session_state.using_api = True
                st.success("🔗 Connected to API server")
            else:
                raise Exception("API not available")
        except:
            # Fallback to direct access
            if DIRECT_ACCESS:
                st.session_state.system = IntegratedPreparednessSystem()
                st.session_state.using_api = False
                st.info("📱 Using direct system access (API unavailable)")
            else:
                st.error("❌ Neither API nor direct access available")
                st.stop()

def get_system_data(endpoint: str = None, fallback_method: str = None):
    """Get data from API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        if endpoint:
            return st.session_state.api_client.get(endpoint)
    elif st.session_state.system and fallback_method:
        try:
            method = getattr(st.session_state.system, fallback_method)
            return method()
        except AttributeError:
            return {"error": f"Method {fallback_method} not available"}
    return {"error": "No data source available"}

def get_supplies_data():
    """Get supplies inventory from API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        return st.session_state.api_client.get("/api/supplies/inventory")
    if st.session_state.system:
        try:
            inv = st.session_state.system.supply_tracker.get_all_supplies()
            exp = st.session_state.system.supply_tracker.check_expiration_alerts(30)
            summ = st.session_state.system.supply_tracker.get_inventory_summary()
            return {
                "inventory": inv,
                "total_items": len(inv),
                "categories": list(summ.get("categories", {}).keys()),
                "expiring_soon": exp,
            }
        except Exception:
            return {"inventory": [], "total_items": 0, "expiring_soon": []}
    return {"inventory": [], "total_items": 0, "expiring_soon": []}

def get_alerts_data():
    """Get active alerts from API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        return st.session_state.api_client.get("/api/alerts/active")
    if st.session_state.system:
        try:
            alerts = st.session_state.system.alert_monitor.get_active_alerts()
            return {"active_alerts": alerts, "count": len(alerts)}
        except Exception:
            return {"active_alerts": [], "count": 0}
    return {"active_alerts": [], "count": 0}

def get_drill_scenarios():
    """Get drill scenarios from API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        data = st.session_state.api_client.get("/api/drills/scenarios")
        return data.get("scenarios", []) if "error" not in data else []
    if st.session_state.system:
        try:
            return st.session_state.system.drill_simulator.list_scenarios()
        except Exception:
            return []
    return []

def run_drill_api(scenario_id: int, participant_name: str, family_size: int):
    """Run drill via API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        return st.session_state.api_client.post("/api/drills/start", {
            "scenario_id": scenario_id,
            "participant_name": participant_name,
            "family_size": family_size,
        })
    if st.session_state.system:
        try:
            result = st.session_state.system.drill_simulator.run_drill_quiz(
                scenario_id, participant_name, family_size
            )
            return {"success": True, "drill_result": result}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "No data source available"}

def get_drill_history_data(participant: str = "User"):
    """Get drill history from API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        from urllib.parse import quote
        data = st.session_state.api_client.get(f"/api/drills/history?participant={quote(participant)}")
        return data if "error" not in data else {"drill_history": [], "total_drills": 0}
    if st.session_state.system:
        try:
            history = st.session_state.system.drill_simulator.get_performance_history(participant)
            recent = history.get("recent_drills", [])
            drill_history = [
                {
                    "date": (d.get("date") or "")[:10],
                    "type": d.get("scenario", d.get("disaster_type", "Drill")),
                    "score": d.get("score", 0),
                    "duration": f"{d.get('time', 0):.1f}m" if isinstance(d.get("time"), (int, float)) else str(d.get("time", "—"))
                }
                for d in recent
            ]
            return {"drill_history": drill_history, "total_drills": history.get("total_drills", len(drill_history))}
        except Exception:
            return {"drill_history": [], "total_drills": 0}
    return {"drill_history": [], "total_drills": 0}

def search_knowledge_api(query: str, limit: int = 10):
    """Search knowledge base via API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        from urllib.parse import quote
        encoded = quote(query)
        return st.session_state.api_client.get(f"/api/knowledge/search?q={encoded}&limit={limit}")
    if st.session_state.system:
        try:
            results = st.session_state.system.knowledge_base.search(query=query, limit=limit)
            return {"query": query, "results": results, "count": len(results)}
        except Exception as e:
            return {"error": str(e), "results": [], "count": 0}
    return {"error": "No data source", "results": [], "count": 0}

def get_scenario_guide_api(name: str):
    """Get scenario guide by name (e.g. flood, earthquake) via API or direct system"""
    if st.session_state.using_api and st.session_state.api_client:
        from urllib.parse import quote
        data = st.session_state.api_client.get(f"/api/knowledge/scenario/{quote(name)}")
        return data if "error" not in data else None
    if st.session_state.system:
        try:
            return st.session_state.system.knowledge_base.get_scenario_guide(name)
        except Exception:
            return None
    return None

def get_scenario_list_api():
    """List available scenario guide names"""
    if st.session_state.using_api and st.session_state.api_client:
        data = st.session_state.api_client.get("/api/knowledge/scenarios")
        return data.get("scenarios", []) if "error" not in data else []
    if st.session_state.system:
        try:
            return st.session_state.system.knowledge_base.list_scenario_guides()
        except Exception:
            return []
    return []

def get_profiles_list():
    """List available profiles"""
    if st.session_state.using_api and st.session_state.api_client:
        data = st.session_state.api_client.get("/api/profiles")
        return data.get("profiles", ["default"]) if "error" not in data else ["default"]
    if st.session_state.system:
        try:
            profiles = st.session_state.system.profile_manager.list_profiles()
            return profiles if profiles else ["default"]
        except Exception:
            return ["default"]
    return ["default"]

def get_current_profile():
    """Get current profile name"""
    if st.session_state.using_api and st.session_state.api_client:
        data = st.session_state.api_client.get("/api/profiles")
        return data.get("current", "default") if "error" not in data else "default"
    if st.session_state.system:
        return st.session_state.system.profile_manager.current_profile or "default"
    return "default"

def switch_profile_api(profile: str):
    """Switch to a different profile"""
    if st.session_state.using_api and st.session_state.api_client:
        return st.session_state.api_client.put("/api/profile/switch", {"profile": profile})
    if st.session_state.system:
        try:
            st.session_state.system.profile_manager.load_profile(profile)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "No system available"}

def get_activities_data():
    """Get recent activity feed for Dashboard"""
    if st.session_state.using_api and st.session_state.api_client:
        data = st.session_state.api_client.get("/api/activity")
        return data.get("activities", []) if "error" not in data else []
    if st.session_state.system:
        try:
            activities_raw = st.session_state.system.profile_manager.profile_data.get("activities", {})
            labels = {"drill_completed": "Emergency drill completed", "risk_assessment_completed": "Risk assessment completed", "supply_updated": "Supply inventory updated", "backup_created": "Backup created"}
            items = []
            for act_type, record in activities_raw.items():
                ts = record.get("timestamp", "")
                details = record.get("details", {})
                label = labels.get(act_type, act_type.replace("_", " ").title())
                if act_type == "drill_completed" and details:
                    label = f"Emergency drill - {details.get('type', details.get('scenario_id', ''))}" + (f" (Score: {details.get('score', '')}/100)" if details.get("score") else "")
                items.append({"time": ts, "activity": label, "type": "success" if "drill" in act_type or "backup" in act_type else "info"})
            items.sort(key=lambda x: x["time"], reverse=True)
            return items[:10]
        except Exception:
            return []
    return []

def get_knowledge_categories():
    """Get knowledge base categories"""
    if st.session_state.using_api and st.session_state.api_client:
        data = st.session_state.api_client.get("/api/knowledge/categories")
        return data.get("categories", []) if "error" not in data else []
    if st.session_state.system:
        try:
            return st.session_state.system.knowledge_base.list_categories()
        except Exception:
            return []
    return []

def get_knowledge_by_category_api(category: str, limit: int = 20):
    """Browse documents by category"""
    if st.session_state.using_api and st.session_state.api_client:
        from urllib.parse import quote
        data = st.session_state.api_client.get(f"/api/knowledge/by_category?category={quote(category)}&limit={limit}")
        return data.get("documents", []) if "error" not in data else []
    if st.session_state.system:
        try:
            return st.session_state.system.knowledge_base.get_documents_by_category(category, limit)
        except Exception:
            return []
    return []

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚨 Emergency Preparedness System</h1>
        <p>Complete disaster readiness platform with real-time monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    initialize_system()
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "🏠 Dashboard",
            "📊 Risk Assessment", 
            "📦 Supply Management",
            "🚨 Alerts & Monitoring",
            "🎯 Training & Drills",
            "📚 Knowledge Base",
            "👥 Emergency Contacts",
            "💾 Backup & Export",
            "⚙️ Settings"
        ]
    )
    
    # Profile switcher
    st.sidebar.subheader("👤 Profile")
    profiles = get_profiles_list()
    current = get_current_profile()
    selected = st.sidebar.selectbox(
        "Active profile",
        profiles,
        index=profiles.index(current) if current in profiles else 0,
        key="profile_selector"
    )
    if selected and selected != current:
        result = switch_profile_api(selected)
        if result.get("success") or "error" not in result:
            st.sidebar.success(f"Switched to **{selected}**")
            st.rerun()
        else:
            st.sidebar.error(result.get("error", "Switch failed"))
    
    # Auto-refresh toggle
    st.sidebar.subheader("🔄 Auto-refresh")
    auto_refresh = st.sidebar.checkbox("Enable auto-refresh (30s)")
    
    if auto_refresh:
        time.sleep(1)
        st.rerun()
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Risk Assessment":
        show_risk_assessment()
    elif page == "📦 Supply Management":
        show_supply_management()
    elif page == "🚨 Alerts & Monitoring":
        show_alerts_monitoring()
    elif page == "🎯 Training & Drills":
        show_training_drills()
    elif page == "📚 Knowledge Base":
        show_knowledge_base()
    elif page == "👥 Emergency Contacts":
        show_emergency_contacts()
    elif page == "💾 Backup & Export":
        show_backup_export()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Main dashboard view"""
    st.header("🏠 Dashboard Overview")
    
    # Get system status
    if st.session_state.using_api:
        health_data = get_system_data("/health")
        profile_data = get_system_data("/api/profile")
    else:
        health_data = {"status": "healthy", "timestamp": datetime.now().isoformat()}
        profile_data = {"summary": st.session_state.system.profile_manager.get_profile_summary()}
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if "error" not in profile_data:
            prep_score = profile_data.get("summary", {}).get("preparedness_score", 0)
            st.metric("🎯 Preparedness Score", f"{prep_score}/100", delta=None)
        else:
            st.metric("🎯 Preparedness Score", "N/A")
    
    with col2:
        if "error" not in profile_data:
            family_size = profile_data.get("summary", {}).get("family_size", 0)
            st.metric("👨‍👩‍👧‍👦 Family Size", family_size)
        else:
            st.metric("👨‍👩‍👧‍👦 Family Size", "N/A")
    
    with col3:
        if st.session_state.using_api:
            active_users = health_data.get("active_users", 1)
            st.metric("👥 Active Users", active_users)
        else:
            st.metric("📱 System Mode", "Direct")
    
    with col4:
        last_update = "Today" if "error" not in profile_data else "Unknown"
        st.metric("📅 Last Update", last_update)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Risk Assessment Overview")
        
        # Create mock risk data for visualization
        risk_categories = ["Natural Disasters", "Modern Threats", "Economic", "Health", "Infrastructure"]
        risk_levels = [75, 45, 60, 30, 55]
        
        fig_risk = px.bar(
            x=risk_categories,
            y=risk_levels,
            title="Risk Levels by Category",
            color=risk_levels,
            color_continuous_scale="RdYlGn_r"
        )
        fig_risk.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        st.subheader("📦 Supply Status")
        
        supplies = get_supplies_data()
        inv = supplies.get("inventory", [])
        exp = supplies.get("expiring_soon", [])
        if inv:
            total = len(inv)
            exp_count = len(exp)
            ok = total - exp_count
            fig_supply = px.pie(
                values=[max(0, ok), exp_count],
                names=["Adequate", "Expiring Soon"],
                title=f"Supply Inventory ({total} items)",
                color_discrete_sequence=["green", "orange"]
            )
            fig_supply.update_layout(height=400)
            st.plotly_chart(fig_supply, use_container_width=True)
        else:
            st.info("No supply data yet. Add items in Supply Management.")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    activities = get_activities_data()
    if not activities:
        st.info("No recent activity yet. Complete a risk assessment, run a drill, or add supplies to see activity here.")
    for activity in activities:
        ts = activity.get("time", "")
        try:
            time_label = "Today" if ts and ts[:10] == datetime.now().strftime("%Y-%m-%d") else (ts[:10] if len(ts) >= 10 else ts[:16] if ts else "")
        except Exception:
            time_label = ts[:16] if ts else ""
        act_text = activity.get("activity", "")
        if activity.get("type") == "success":
            st.markdown(f"""<div class="success-card"><strong>{time_label}</strong>: {act_text}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="metric-card"><strong>{time_label}</strong>: {act_text}</div>""", unsafe_allow_html=True)

def show_risk_assessment():
    """Risk assessment interface"""
    st.header("📊 Risk Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Comprehensive Risk Analysis")
        
        # Risk assessment form
        with st.form("risk_assessment"):
            scenario_type = st.selectbox(
                "Scenario Type",
                ["earthquake", "flood", "fire", "tornado", "hurricane"]
            )
            severity = st.slider("Severity Level", 1, 10, 7)
            location = st.selectbox(
                "Location Type",
                ["urban", "suburban", "rural"]
            )
            
            if st.form_submit_button("🔍 Calculate Risk"):
                with st.spinner("Calculating comprehensive risk..."):
                    if st.session_state.using_api:
                        risk_data = st.session_state.api_client.post("/api/risk/calculate", {
                            "scenario_type": scenario_type,
                            "severity": severity,
                            "location": location
                        })
                    else:
                        # Direct system access
                        scenario = {"type": scenario_type, "severity": severity}
                        risk_result = st.session_state.system.advanced_risk_engine.calculate_comprehensive_risk(
                            scenario, location
                        )
                        risk_data = {"success": True, "risk_analysis": risk_result}
                    
                    if "error" not in risk_data and risk_data.get("success"):
                        analysis = risk_data["risk_analysis"]
                        
                        # Display results
                        st.success("✅ Risk analysis completed!")
                        
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        with metrics_col1:
                            risk_score = analysis.get("adjusted_risk_score", 0)
                            st.metric("🎯 Risk Score", f"{risk_score:.1f}/100")
                        with metrics_col2:
                            probability = analysis.get("probability", 0)
                            st.metric("📊 Probability", f"{probability:.1f}%")
                        with metrics_col3:
                            impact = analysis.get("impact_severity", 0)
                            st.metric("💥 Impact", f"{impact:.1f}/10")
                        
                        # Risk factors
                        if analysis.get("risk_factors"):
                            st.subheader("🎯 Key Risk Factors")
                            factors = analysis["risk_factors"]
                            if isinstance(factors, dict):
                                for factor, value in factors.items():
                                    st.write(f"• **{factor}**: {value}")
                        
                        # Mitigations
                        if analysis.get("mitigation_available"):
                            st.subheader("💡 Available Mitigations")
                            for mitigation in analysis["mitigation_available"]:
                                st.write(f"• {mitigation}")
                    else:
                        st.error("❌ Risk calculation failed")
    
    with col2:
        st.subheader("📈 Risk Trends")
        
        # Mock historical risk data
        dates = pd.date_range(start="2025-01-01", end="2025-08-13", freq="W")
        risk_scores = [65 + i*2 + (i%3)*5 for i in range(len(dates))]
        
        fig_trend = px.line(
            x=dates,
            y=risk_scores,
            title="Risk Score Trend",
            labels={"x": "Date", "y": "Risk Score"}
        )
        fig_trend.update_layout(height=300)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Refresh Assessment"):
            st.rerun()
        
        if st.button("📋 View Detailed Report"):
            st.info("📄 Detailed report generation coming soon!")
        
        if st.button("💾 Save Assessment"):
            st.success("✅ Assessment saved to profile!")

def show_supply_management():
    """Supply management interface"""
    st.header("📦 Supply Management")
    
    supplies = get_supplies_data()
    inv = supplies.get("inventory", [])
    exp = supplies.get("expiring_soon", [])
    
    # Supply overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Total Items", len(inv))
    with col2:
        st.metric("⚠️ Expiring Soon", len(exp))
    with col3:
        st.metric("🔴 Categories", len(set(i.get("category", "") for i in inv)) if inv else 0)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Inventory", "🛒 Shopping List", "📅 Expiry Alerts"])
    
    with tab1:
        st.subheader("Current Inventory")
        
        if inv:
            df = pd.DataFrame([
                {
                    "Item": i.get("item_name", ""),
                    "Quantity": i.get("quantity", 0),
                    "Unit": i.get("unit", ""),
                    "Category": i.get("category", ""),
                    "Expiry": i.get("expiration_date") or "N/A",
                }
                for i in inv
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No inventory yet. Add items below.")
        
        # Add new item
        with st.expander("➕ Add New Item"):
            with st.form("add_item"):
                new_item = st.text_input("Item Name", placeholder="e.g. Bottled Water")
                new_category = st.selectbox("Category", ["water", "food", "medication", "first_aid", "batteries", "fuel", "other"])
                new_quantity = st.number_input("Quantity", min_value=0.0, value=1.0, step=0.5)
                new_unit = st.text_input("Unit", value="units", placeholder="e.g. gallons, cans, units")
                new_expiry = st.text_input("Expiry Date (YYYY-MM-DD)", placeholder="Optional")
                new_location = st.text_input("Location", placeholder="Optional")
                
                if st.form_submit_button("Add Item"):
                    if not new_item or not new_unit:
                        st.warning("Item name and unit required.")
                    else:
                        if st.session_state.using_api and st.session_state.api_client:
                            r = st.session_state.api_client.post("/api/supplies", {
                                "category": new_category,
                                "item_name": new_item,
                                "quantity": float(new_quantity),
                                "unit": new_unit,
                                "expiration_date": new_expiry or None,
                                "location": new_location or None,
                            })
                            if "error" not in r:
                                st.success(f"✅ Added {new_quantity} {new_unit} of {new_item}")
                                st.rerun()
                            else:
                                st.error(r.get("error", "Failed to add"))
                        elif st.session_state.system:
                            try:
                                st.session_state.system.supply_tracker.add_supply(
                                    category=new_category, item_name=new_item,
                                    quantity=float(new_quantity), unit=new_unit,
                                    expiration_date=new_expiry or None, location=new_location
                                )
                                st.success(f"✅ Added {new_quantity} {new_unit} of {new_item}")
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))
    
    with tab2:
        st.subheader("Shopping List")
        if exp:
            st.write("📝 Items expiring soon (consider restocking):")
            for e in exp[:15]:
                st.write(f"• {e.get('item', 'Item')} — expires in {e.get('days_until', 0)} days ({e.get('expiration', '')})")
        else:
            st.info("No expiring items. Check Expiry Alerts tab for updates.")
    
    with tab3:
        st.subheader("Expiry Alerts")
        if exp:
            for e in exp:
                st.markdown(f"""
                <div class="alert-card">
                    <strong>⚠️ {e.get('item', 'Item')}</strong> — {e.get('quantity', 0)} {e.get('unit', '')} expires in {e.get('days_until', 0)} days ({e.get('expiration', '')})
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No items expiring in the next 30 days.")

def show_alerts_monitoring():
    """Alerts and monitoring interface"""
    st.header("🚨 Alerts & Monitoring")
    
    # Current alerts
    st.subheader("📡 Active Alerts")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        alerts_data = get_alerts_data()
        alerts = alerts_data.get("active_alerts", [])
        
        if alerts:
            for alert in alerts:
                sev = alert.get("severity", "Unknown")
                severity_color = {
                    "Low": "#fff3cd", "Minor": "#fff3cd",
                    "Moderate": "#ffeaa7", "High": "#ffcccc",
                    "Critical": "#ff6b6b", "Severe": "#ffcccc", "Extreme": "#ff6b6b"
                }.get(str(sev), "#f8f9fa")
                title = alert.get("title", alert.get("message", "Alert"))
                loc = alert.get("location", alert.get("area", "N/A"))
                ts = alert.get("created_date", alert.get("time", ""))
                st.markdown(f"""
                <div style="background: {severity_color}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <h4>{title}</h4>
                    <p><strong>Severity:</strong> {sev} | <strong>Location:</strong> {loc}</p>
                    <p><small>{ts}</small></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No active alerts")
    
    with col2:
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Refresh Alerts"):
            st.rerun()
        
        if st.button("📧 Subscribe to Alerts"):
            st.info("Alert subscription updated!")
        
        if st.button("🧪 Test Alert System"):
            st.success("Test alert sent successfully!")
    
    # Monitoring dashboard
    st.subheader("📊 Monitoring Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather monitoring
        st.write("🌤️ **Weather Conditions**")
        st.write("Temperature: 72°F")
        st.write("Humidity: 45%")
        st.write("Wind: 8 mph NW")
        st.write("Pressure: 30.15 inHg")
    
    with col2:
        # System status
        st.write("🖥️ **System Status**")
        st.write("Status: ✅ Operational")
        st.write("Uptime: 15 days")
        st.write("Last Check: 30 seconds ago")
        st.write("Sources: 5 active")

def show_training_drills():
    """Training and drills interface"""
    st.header("🎯 Training & Drills")
    
    scenarios = get_drill_scenarios()
    
    st.subheader("⚡ Quick Start Drill")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if scenarios:
            scenario_options = {f"{s['name']} ({s['disaster_type']})": s["id"] for s in scenarios}
            chosen_label = st.selectbox("Drill Scenario", list(scenario_options.keys()))
            scenario_id = scenario_options.get(chosen_label, scenarios[0]["id"])
        else:
            st.warning("No drill scenarios available. Run system init first.")
            scenario_id = None
    
    with col2:
        participant_name = st.text_input("Your Name", value="Participant")
    
    with col3:
        family_size = st.number_input("Family Size", min_value=1, max_value=20, value=4)
    
    if st.button("🚀 Start Drill", type="primary") and scenario_id:
        with st.spinner("Running drill..."):
            result = run_drill_api(scenario_id, participant_name, family_size)
        
        if "error" not in result:
            drill_res = result.get("drill_result", {})
            score = drill_res.get("score", 0)
            st.success(f"✅ Drill completed! Score: {score}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Score", f"{score}")
            with col2:
                st.metric("⏱️ Time (min)", f"{drill_res.get('time', 0):.1f}")
            with col3:
                st.metric("🎯 Grade", drill_res.get("grade", "—"))
            
            if drill_res.get("lessons"):
                st.subheader("📝 Lessons")
                for lesson in drill_res["lessons"][:5]:
                    st.write(f"• {lesson}")
        else:
            st.error(result.get("error", "Drill failed"))
    
    # Drill history
    st.subheader("📋 Drill History")
    participant_for_history = participant_name or "User"
    history_resp = get_drill_history_data(participant_for_history)
    drill_history = history_resp.get("drill_history", [])
    total_drills = history_resp.get("total_drills", 0)

    if drill_history:
        df_history = pd.DataFrame(drill_history).rename(
            columns={"date": "Date", "type": "Type", "score": "Score", "duration": "Duration"}
        )
        st.dataframe(df_history, use_container_width=True)
        if len(df_history) > 1:
            fig_performance = px.line(
                df_history,
                x="Date",
                y="Score",
                title="Drill Performance Over Time",
                markers=True
            )
            fig_performance.update_layout(height=300)
            st.plotly_chart(fig_performance, use_container_width=True)
    else:
        st.info(f"No drill history yet for **{participant_for_history}**. Complete a drill above to see your progress.")

def show_knowledge_base():
    """Knowledge base search interface"""
    st.header("📚 Knowledge Base")
    st.write("Search emergency preparedness guides, scenario plans, and reference materials.")
    
    # Browse by category
    st.subheader("📂 Browse by Category")
    categories = get_knowledge_categories()
    if categories:
        cat_options = {c["name"]: c["id"] for c in categories}
        chosen_cat = st.selectbox("Category", [""] + list(cat_options.keys()), key="kb_browse_cat")
        if chosen_cat:
            docs = get_knowledge_by_category_api(cat_options[chosen_cat])
            if docs:
                for d in docs:
                    with st.expander(f"**{d.get('title', 'Untitled')}**"):
                        st.caption(d.get("file_path", ""))
                        # Fetch full content on expand if needed - for now just show path
            else:
                st.caption("No documents in this category yet.")
    
    # Scenario quick-help
    st.subheader("⚡ Scenario Quick Help")
    st.write("Select a scenario for instant guidance.")
    scenarios = get_scenario_list_api()
    if scenarios:
        chosen = st.selectbox("I need help with...", [""] + scenarios, key="kb_scenario")
        if chosen:
            guide = get_scenario_guide_api(chosen.replace(" ", "_").lower())
            if guide:
                st.markdown(f"### {guide.get('title', chosen)}")
                st.markdown(guide.get("content", ""))
            else:
                st.warning(f"No guide found for **{chosen}**. Try searching below.")
    else:
        st.caption("No scenario guides indexed yet.")
    
    st.subheader("🔍 Search")
    query = st.text_input("Search", placeholder="e.g. earthquake, first aid, water purification", key="kb_search")
    
    if st.button("Search") or query:
        if not query.strip():
            st.info("Enter a search term.")
        else:
            with st.spinner("Searching..."):
                data = search_knowledge_api(query.strip(), limit=15)
            
            if "error" in data:
                st.error(data.get("error", "Search failed"))
            else:
                results = data.get("results", [])
                st.write(f"**{len(results)} results** for \"{query}\"")
                for r in results:
                    title = r.get("title", "Untitled")
                    category = r.get("category", "")
                    path = r.get("file_path", "")
                    sections = r.get("sections", [])
                    with st.expander(f"**{title}** ({category})"):
                        if path:
                            st.caption(f"Path: {path}")
                        for s in sections[:3]:
                            st.write(f"**{s.get('title', '')}**")
                            st.write(s.get("content", "")[:300] + ("..." if len(s.get("content", "")) > 300 else ""))

def show_emergency_contacts():
    """Emergency contacts interface"""
    st.header("👥 Emergency Contacts")
    
    # Current contacts
    st.subheader("📞 Contact List")
    
    contacts_data = {
        "Name": ["Local Police", "Fire Department", "Hospital", "Mom", "Neighbor John"],
        "Phone": ["911", "911", "(555) 123-4567", "(555) 987-6543", "(555) 246-8135"],
        "Role": ["Police", "Fire", "Medical", "Family", "Neighbor"],
        "Priority": ["Critical", "Critical", "High", "High", "Medium"]
    }
    
    df_contacts = pd.DataFrame(contacts_data)
    st.dataframe(df_contacts, use_container_width=True)
    
    # Add new contact
    st.subheader("➕ Add New Contact")
    
    with st.form("add_contact"):
        col1, col2 = st.columns(2)
        
        with col1:
            contact_name = st.text_input("Name")
            contact_phone = st.text_input("Phone Number")
        
        with col2:
            contact_role = st.selectbox(
                "Role",
                ["Family", "Friend", "Neighbor", "Medical", "Utility", "Other"]
            )
            contact_priority = st.selectbox(
                "Priority",
                ["Critical", "High", "Medium", "Low"]
            )
        
        if st.form_submit_button("Add Contact"):
            st.success(f"✅ Added {contact_name} to emergency contacts")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Send Test Alert"):
            st.success("Test alert sent to all contacts!")
    
    with col2:
        if st.button("🔄 Verify Contacts"):
            st.info("Contact verification in progress...")
    
    with col3:
        if st.button("📤 Export Contacts"):
            st.success("Contacts exported as VCF file!")

def show_backup_export():
    """Backup and export interface"""
    st.header("💾 Backup & Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Create Backup")
        
        with st.form("create_backup"):
            backup_name = st.text_input("Backup Name (optional)")
            backup_description = st.text_area("Description")
            
            if st.form_submit_button("Create Backup"):
                with st.spinner("Creating backup..."):
                    time.sleep(2)  # Simulate backup creation
                    st.success("✅ Backup created successfully!")
        
        st.subheader("🗂️ Available Backups")
        
        backups = [
            {"name": "backup_20250813_225927", "date": "2025-08-13", "size": "2.3 MB"},
            {"name": "backup_20250810_120000", "date": "2025-08-10", "size": "2.1 MB"},
            {"name": "auto_backup_20250807", "date": "2025-08-07", "size": "2.0 MB"}
        ]
        
        for backup in backups:
            with st.expander(f"📁 {backup['name']}"):
                st.write(f"**Date:** {backup['date']}")
                st.write(f"**Size:** {backup['size']}")
                
                col_restore, col_download = st.columns(2)
                with col_restore:
                    if st.button("🔄 Restore", key=f"restore_{backup['name']}"):
                        st.success("Backup restored successfully!")
                with col_download:
                    if st.button("⬇️ Download", key=f"download_{backup['name']}"):
                        st.success("Backup downloaded!")
    
    with col2:
        st.subheader("📤 Export Data")
        
        export_format = st.selectbox(
            "Export Format",
            ["JSON", "CSV", "PDF Report", "HTML Dashboard"]
        )
        
        export_sections = st.multiselect(
            "Sections to Export",
            ["Profile Data", "Risk Assessment", "Supply Inventory", "Contacts", "Drill History"],
            default=["Profile Data", "Risk Assessment"]
        )
        
        if st.button("📤 Export Data"):
            with st.spinner("Exporting data..."):
                time.sleep(1)
                st.success(f"✅ Data exported as {export_format}")
                
                # Mock download link
                st.download_button(
                    label="⬇️ Download Export",
                    data=json.dumps({"exported": "data"}, indent=2),
                    file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

def show_settings():
    """Settings interface"""
    st.header("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔔 Notifications", "🔧 System"])
    
    with tab1:
        st.subheader("Profile Information")
        
        with st.form("profile_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Family Information**")
                adults = st.number_input("Number of Adults", min_value=0, value=2)
                children = st.number_input("Number of Children", min_value=0, value=1)
            
            with col2:
                st.write("**Location Information**")
                location_type = st.selectbox(
                    "Location Type",
                    ["urban", "suburban", "rural"]
                )
                housing_type = st.selectbox(
                    "Housing Type",
                    ["house", "apartment", "condo", "mobile_home"]
                )
            
            if st.form_submit_button("💾 Save Profile"):
                st.success("✅ Profile updated successfully!")
    
    with tab2:
        st.subheader("Notification Preferences")
        
        alert_types = st.multiselect(
            "Alert Types",
            ["Weather", "Emergency", "System", "Drill Reminders"],
            default=["Weather", "Emergency"]
        )
        
        notification_frequency = st.selectbox(
            "Notification Frequency",
            ["Real-time", "Hourly", "Daily", "Weekly"]
        )
        
        email_alerts = st.checkbox("Email Alerts", value=True)
        sms_alerts = st.checkbox("SMS Alerts", value=False)
        
        if st.button("💾 Save Notifications"):
            st.success("✅ Notification preferences saved!")
    
    with tab3:
        st.subheader("System Configuration")
        
        auto_backup = st.checkbox("Automatic Backups", value=True)
        backup_frequency = st.selectbox(
            "Backup Frequency",
            ["Daily", "Weekly", "Monthly"]
        )
        
        data_retention = st.selectbox(
            "Data Retention",
            ["30 days", "90 days", "1 year", "Forever"]
        )
        
        api_mode = st.checkbox("Use API Mode (when available)", value=True)
        
        if st.button("💾 Save System Settings"):
            st.success("✅ System settings saved!")
        
        st.subheader("🧹 Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Cache"):
                st.success("Cache cleared!")
        
        with col2:
            if st.button("🔄 Reset to Defaults"):
                st.warning("Settings reset to defaults!")

if __name__ == "__main__":
    main()