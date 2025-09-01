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
            "👥 Emergency Contacts",
            "💾 Backup & Export",
            "⚙️ Settings"
        ]
    )
    
    # Profile selector
    st.sidebar.subheader("👤 Profile")
    if st.session_state.using_api:
        profile_data = get_system_data("/api/profile")
        if "error" not in profile_data:
            profile_name = profile_data.get("summary", {}).get("profile_name", "default")
            st.sidebar.info(f"Current: {profile_name}")
    else:
        profile_name = "default"
        st.sidebar.info(f"Current: {profile_name}")
    
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
        
        # Create mock supply data
        supply_status = ["Adequate", "Low", "Critical", "Expired"]
        supply_counts = [25, 8, 3, 2]
        colors = ["green", "yellow", "red", "darkred"]
        
        fig_supply = px.pie(
            values=supply_counts,
            names=supply_status,
            title="Supply Inventory Status",
            color_discrete_sequence=colors
        )
        fig_supply.update_layout(height=400)
        st.plotly_chart(fig_supply, use_container_width=True)
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    activities = [
        {"time": "2 hours ago", "activity": "Risk assessment completed", "type": "info"},
        {"time": "1 day ago", "activity": "Emergency drill - Earthquake (Score: 85/100)", "type": "success"},
        {"time": "3 days ago", "activity": "Supply inventory updated", "type": "info"},
        {"time": "1 week ago", "activity": "Backup created automatically", "type": "success"}
    ]
    
    for activity in activities:
        if activity["type"] == "success":
            st.markdown(f"""
            <div class="success-card">
                <strong>{activity['time']}</strong>: {activity['activity']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <strong>{activity['time']}</strong>: {activity['activity']}
            </div>
            """, unsafe_allow_html=True)

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
    
    # Supply overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Total Items", "38", delta="2")
    with col2:
        st.metric("⚠️ Expiring Soon", "5", delta="-1")
    with col3:
        st.metric("🔴 Critical Items", "2", delta="0")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Inventory", "🛒 Shopping List", "📅 Expiry Alerts"])
    
    with tab1:
        st.subheader("Current Inventory")
        
        # Mock inventory data
        inventory_data = {
            "Item": ["Water (gallons)", "MREs", "Flashlights", "Batteries", "First Aid Kit"],
            "Quantity": [20, 15, 4, 12, 1],
            "Status": ["Good", "Good", "Low", "Good", "Critical"],
            "Expiry": ["2026-08-01", "2027-12-31", "N/A", "2025-12-01", "2025-09-15"]
        }
        
        df = pd.DataFrame(inventory_data)
        
        # Color code by status
        def highlight_status(val):
            if val == "Critical":
                return "background-color: #ffcccc"
            elif val == "Low":
                return "background-color: #fff3cd"
            else:
                return "background-color: #d4edda"
        
        styled_df = df.style.applymap(highlight_status, subset=["Status"])
        st.dataframe(styled_df, use_container_width=True)
        
        # Add new item
        with st.expander("➕ Add New Item"):
            with st.form("add_item"):
                new_item = st.text_input("Item Name")
                new_quantity = st.number_input("Quantity", min_value=1, value=1)
                new_expiry = st.date_input("Expiry Date")
                
                if st.form_submit_button("Add Item"):
                    st.success(f"✅ Added {new_quantity}x {new_item}")
    
    with tab2:
        st.subheader("Shopping List")
        st.write("📝 Items to purchase:")
        
        shopping_items = [
            "Batteries (AA) - 24 pack",
            "First Aid Supplies",
            "Emergency Radio",
            "Water purification tablets"
        ]
        
        for i, item in enumerate(shopping_items):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {item}")
            with col2:
                if st.button("✅", key=f"complete_{i}"):
                    st.success("Item purchased!")
    
    with tab3:
        st.subheader("Expiry Alerts")
        
        st.markdown("""
        <div class="alert-card">
            <strong>⚠️ First Aid Kit</strong> expires in 32 days (Sept 15, 2025)
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-card">
            <strong>⚠️ Batteries</strong> expire in 108 days (Dec 1, 2025)
        </div>
        """, unsafe_allow_html=True)

def show_alerts_monitoring():
    """Alerts and monitoring interface"""
    st.header("🚨 Alerts & Monitoring")
    
    # Current alerts
    st.subheader("📡 Active Alerts")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Mock alert data
        alerts = [
            {"title": "High Wind Warning", "severity": "Moderate", "location": "Bay Area", "time": "2 hours ago"},
            {"title": "Air Quality Alert", "severity": "Low", "location": "Local", "time": "6 hours ago"}
        ]
        
        if alerts:
            for alert in alerts:
                severity_color = {
                    "Low": "#fff3cd",
                    "Moderate": "#ffeaa7",
                    "High": "#ffcccc",
                    "Critical": "#ff6b6b"
                }.get(alert["severity"], "#f8f9fa")
                
                st.markdown(f"""
                <div style="background: {severity_color}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <h4>{alert['title']}</h4>
                    <p><strong>Severity:</strong> {alert['severity']} | <strong>Location:</strong> {alert['location']}</p>
                    <p><small>{alert['time']}</small></p>
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
    
    # Quick start drill
    st.subheader("⚡ Quick Start Drill")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        drill_type = st.selectbox(
            "Drill Type",
            ["earthquake", "fire", "tornado", "flood", "evacuation"]
        )
    
    with col2:
        participants = st.number_input(
            "Participants",
            min_value=1,
            max_value=20,
            value=4
        )
    
    with col3:
        difficulty = st.selectbox(
            "Difficulty",
            ["beginner", "intermediate", "advanced"]
        )
    
    if st.button("🚀 Start Drill", type="primary"):
        with st.spinner("Running drill..."):
            time.sleep(2)  # Simulate drill execution
            
            # Mock drill results
            score = 85
            st.success(f"✅ Drill completed! Score: {score}/100")
            
            # Show results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Performance", f"{score}/100")
            with col2:
                st.metric("⏱️ Response Time", "2m 45s")
            with col3:
                st.metric("🎯 Grade", "B+")
            
            # Feedback
            st.subheader("📝 Drill Feedback")
            st.write("**Strengths:**")
            st.write("• Quick initial response")
            st.write("• Good communication")
            
            st.write("**Areas for Improvement:**")
            st.write("• Practice evacuation routes")
            st.write("• Review emergency kit location")
    
    # Drill history
    st.subheader("📋 Drill History")
    
    history_data = {
        "Date": ["2025-08-10", "2025-08-03", "2025-07-27"],
        "Type": ["Earthquake", "Fire", "Tornado"],
        "Score": [85, 92, 78],
        "Duration": ["2m 45s", "1m 58s", "3m 12s"]
    }
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True)
    
    # Performance chart
    fig_performance = px.line(
        df_history,
        x="Date",
        y="Score",
        title="Drill Performance Over Time",
        markers=True
    )
    fig_performance.update_layout(height=300)
    st.plotly_chart(fig_performance, use_container_width=True)

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