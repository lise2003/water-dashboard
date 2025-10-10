# ENTERPRISE WATER INFRASTRUCTURE PLATFORM

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json
import io
import base64
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# =============================================
# DEPENDENCY HANDLING
# =============================================

try:
    import folium
    from streamlit_folium import folium_static
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# =============================================
# ENTERPRISE CONFIGURATION
# =============================================

st.set_page_config(
    page_title="Water Infrastructure Enterprise Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #054ADA 0%, #0062FF 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(5, 74, 218, 0.3);
    }
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #054ADA;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .section-header {
        border-bottom: 3px solid #054ADA;
        padding-bottom: 0.8rem;
        margin: 2.5rem 0 1rem 0;
        color: #054ADA;
        font-weight: 600;
        font-size: 1.4rem;
    }
    .engineering-diagram {
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        background: #f8f9fa;
        margin: 1rem 0;
    }
    .status-positive { color: #28a745; font-weight: 600; }
    .status-warning { color: #ffc107; font-weight: 600; }
    .status-critical { color: #dc3545; font-weight: 600; }
    .ibm-blue { color: #054ADA; }
    .job-breakdown { background: #f8f9fa; padding: 1rem; border-radius: 6px; margin: 0.5rem 0; }
    .compliance-status { padding: 0.5rem; border-radius: 4px; margin: 0.2rem 0; }
    .compliant { background: #d4edda; color: #155724; }
    .pending { background: #fff3cd; color: #856404; }
    .non-compliant { background: #f8d7da; color: #721c24; }
    .map-placeholder {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    .target-metric {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .current-metric {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 4px solid #054ADA;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# ENTERPRISE DATA SERVICES
# =============================================

class AnalyticsService:
    """Enterprise Analytics Integration"""
    
    @staticmethod
    def get_water_stress_prediction(province, rural_area):
        """Get water stress predictions from Enterprise Analytics"""
        try:
            # Simulated API call
            predictions = {
                "water_stress_level": max(0.6, min(0.9, 0.7 + np.random.normal(0, 0.1))),
                "infrastructure_risk": max(0.3, min(0.8, 0.5 + np.random.normal(0, 0.1))),
                "conservation_potential": max(0.4, min(0.9, 0.65 + np.random.normal(0, 0.1))),
                "rainfall_variability": max(0.2, min(0.8, 0.45 + np.random.normal(0, 0.1))),
                "drought_probability": max(0.1, min(0.7, 0.35 + np.random.normal(0, 0.1)))
            }
            
            insights = [
                f"Analysis predicts 78% probability of water stress in {rural_area} within 24 months",
                f"Infrastructure investment of ZAR {75 + np.random.randint(10, 40)}M recommended for resilience",
                f"Identified conservation potential: {predictions['conservation_potential']:.1%} through smart systems",
                f"Drought probability analysis: {predictions['drought_probability']:.1%} in next 36 months",
                f"Rainfall variability index: {predictions['rainfall_variability']:.1%} - Higher than regional average"
            ]
            
            return predictions, insights
        except Exception as e:
            st.error(f"Analytics Service temporarily unavailable: {e}")
            return {}, ["Service updating - check back in 5 minutes"]

class ImpactTargets:
    """Impact Targets and Current Progress Tracking"""
    
    @staticmethod
    def get_impact_targets(province, rural_area, project_scale):
        """Get target impacts and current progress"""
        
        # Base targets that vary by province and project scale
        base_targets = {
            "Eastern Cape": {"jobs_target": 420, "economic_impact_target": 85, "water_access_target": 85},
            "Free State": {"jobs_target": 380, "economic_impact_target": 75, "water_access_target": 80},
            "Gauteng": {"jobs_target": 500, "economic_impact_target": 100, "water_access_target": 90},
            "KwaZulu-Natal": {"jobs_target": 450, "economic_impact_target": 90, "water_access_target": 85},
            "Limpopo": {"jobs_target": 400, "economic_impact_target": 80, "water_access_target": 80},
            "Mpumalanga": {"jobs_target": 420, "economic_impact_target": 85, "water_access_target": 82},
            "North West": {"jobs_target": 380, "economic_impact_target": 75, "water_access_target": 78},
            "Northern Cape": {"jobs_target": 350, "economic_impact_target": 70, "water_access_target": 75},
            "Western Cape": {"jobs_target": 480, "economic_impact_target": 95, "water_access_target": 88}
        }
        
        # Scale multipliers
        scale_multipliers = {
            "Small": 0.6,
            "Medium": 0.8,
            "Large": 1.0,
            "Enterprise": 1.2
        }
        
        province_targets = base_targets.get(province, {"jobs_target": 400, "economic_impact_target": 80, "water_access_target": 80})
        multiplier = scale_multipliers.get(project_scale, 1.0)
        
        # Calculate adjusted targets
        targets = {
            "jobs_target": int(province_targets["jobs_target"] * multiplier),
            "economic_impact_target": int(province_targets["economic_impact_target"] * multiplier),
            "water_access_target": province_targets["water_access_target"]
        }
        
        # Calculate current progress (simulated - would come from real data)
        current_progress = {
            "jobs_current": int(targets["jobs_target"] * (0.3 + np.random.random() * 0.4)),  # 30-70% progress
            "economic_current": int(targets["economic_impact_target"] * (0.25 + np.random.random() * 0.5)),  # 25-75% progress
            "water_access_current": 42 + np.random.randint(5, 25)  # Current water access
        }
        
        return targets, current_progress

class SatelliteImageryService:
    """Live Satellite Imagery Integration"""
    
    @staticmethod
    def get_satellite_map(province, rural_area, lat=None, lng=None):
        """Generate interactive satellite map with terrain analysis"""
        try:
            if not FOLIUM_AVAILABLE:
                return None
                
            # Default coordinates for South African provinces
            province_coords = {
                "Eastern Cape": (-32.0833, 26.8833),
                "Free State": (-28.4556, 26.7683),
                "Gauteng": (-26.2044, 28.0456),
                "KwaZulu-Natal": (-29.8587, 31.0218),
                "Limpopo": (-23.4013, 29.4179),
                "Mpumalanga": (-25.5653, 30.5279),
                "North West": (-26.6639, 25.2838),
                "Northern Cape": (-29.0467, 21.8569),
                "Western Cape": (-33.9253, 18.4239)
            }
            
            center_lat, center_lng = province_coords.get(province, (-28.4793, 24.6727))
            
            # Create interactive map
            m = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=10,
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri World Imagery'
            )
            
            # Add dam construction site marker
            site_lat = center_lat + np.random.uniform(-0.5, 0.5)
            site_lng = center_lng + np.random.uniform(-0.5, 0.5)
            
            folium.Marker(
                [site_lat, site_lng],
                popup=f"Proposed Dam Site - {rural_area}",
                tooltip="Click for details",
                icon=folium.Icon(color='blue', icon='tint', prefix='fa')
            ).add_to(m)
            
            # Add catchment area
            folium.Circle(
                location=[site_lat, site_lng],
                radius=5000,  # 5km radius
                popup="Primary Catchment Area",
                color="#054ADA",
                fill=True,
                fillColor="#054ADA",
                fillOpacity=0.2
            ).add_to(m)
            
            return m
            
        except Exception as e:
            st.error(f"Satellite service unavailable: {e}")
            return None

class HydrologicalModel:
    """Advanced Hydrological Modeling System"""
    
    @staticmethod
    def simulate_water_flow(catchment_area, rainfall, evaporation, soil_type):
        """Advanced hydrological simulation using modified Rational Method"""
        try:
            # Complex hydrological parameters
            runoff_coefficients = {
                "clay": 0.75,
                "sandy": 0.35,
                "loamy": 0.55,
                "rocky": 0.85
            }
            
            runoff_coeff = runoff_coefficients.get(soil_type.lower(), 0.6)
            effective_rainfall = rainfall - evaporation
            
            if effective_rainfall < 0:
                effective_rainfall = 0
                
            # Peak flow calculation (m³/s)
            peak_flow = (runoff_coeff * effective_rainfall * catchment_area) / 3.6
            
            # Generate time series data
            time_steps = 24
            base_flow = peak_flow * 0.1
            time_series = []
            
            for hour in range(time_steps):
                if 6 <= hour <= 18:  # Daytime peak
                    flow = base_flow + (peak_flow - base_flow) * np.sin((hour - 6) * np.pi / 12)
                else:
                    flow = base_flow
                
                time_series.append({
                    "hour": hour,
                    "flow_rate": max(0, flow + np.random.normal(0, flow * 0.1)),
                    "stage": "Day" if 6 <= hour <= 18 else "Night"
                })
            
            return pd.DataFrame(time_series), peak_flow
            
        except Exception as e:
            st.error(f"Hydrological model error: {e}")
            return pd.DataFrame(), 0

class IoTDataService:
    """Real-time IoT Sensor Data Integration"""
    
    @staticmethod
    def get_sensor_data(province, rural_area):
        """Simulate real-time IoT sensor data from water monitoring systems"""
        try:
            current_time = datetime.now()
            sensor_data = {
                "water_level": 64.5 + np.random.normal(0, 2),
                "water_quality": 7.2 + np.random.normal(0, 0.1),
                "turbidity": 4.1 + np.random.normal(0, 0.5),
                "temperature": 18.5 + np.random.normal(0, 1),
                "flow_rate": 12.3 + np.random.normal(0, 0.5),
                "last_updated": current_time,
                "sensor_status": "Online",
                "battery_level": 87 + np.random.randint(-5, 5)
            }
            
            # Generate 24-hour historical data
            hours = [(current_time - timedelta(hours=i)).strftime("%H:%M") for i in range(24, 0, -1)]
            historical_levels = [sensor_data["water_level"] + np.random.normal(0, 1) for _ in range(24)]
            
            historical_df = pd.DataFrame({
                "timestamp": hours,
                "water_level": historical_levels,
                "flow_rate": [sensor_data["flow_rate"] + np.random.normal(0, 0.3) for _ in range(24)]
            })
            
            return sensor_data, historical_df
            
        except Exception as e:
            st.error(f"IoT data service unavailable: {e}")
            return {}, pd.DataFrame()

class RegulatoryCompliance:
    """Regulatory Compliance Tracking System"""
    
    @staticmethod
    def get_compliance_status(province, project_phase):
        """Track regulatory compliance across multiple agencies"""
        compliance_matrix = {
            "Environmental": [
                {"requirement": "NEMA Environmental Impact Assessment", "status": "Compliant", "deadline": "2024-03-15", "agency": "DEFF"},
                {"requirement": "Water Use License Application", "status": "Pending", "deadline": "2024-04-30", "agency": "DWS"},
                {"requirement": "Air Quality Emissions License", "status": "Compliant", "deadline": "2024-02-28", "agency": "DEFF"}
            ],
            "Construction": [
                {"requirement": "Construction Permit - Local Municipality", "status": "Compliant", "deadline": "2024-01-31", "agency": "Local Govt"},
                {"requirement": "Occupational Health & Safety Plan", "status": "Pending", "deadline": "2024-03-31", "agency": "DOL"},
                {"requirement": "Heritage Impact Assessment", "status": "Compliant", "deadline": "2024-02-15", "agency": "SAHRA"}
            ],
            "Operational": [
                {"requirement": "Operating License - DWS", "status": "Not Started", "deadline": "2025-12-31", "agency": "DWS"},
                {"requirement": "Water Quality Monitoring Protocol", "status": "Pending", "deadline": "2024-06-30", "agency": "DWS"},
                {"requirement": "Emergency Response Plan", "status": "Compliant", "deadline": "2024-03-31", "agency": "NDMC"}
            ]
        }
        
        return compliance_matrix

class StakeholderManagement:
    """Enterprise Stakeholder Management System"""
    
    def __init__(self):
        if 'stakeholders' not in st.session_state:
            st.session_state.stakeholders = self._get_default_stakeholders()
    
    def _get_default_stakeholders(self):
        return [
            {"name": "Local Community Representatives", "type": "Community", "engagement": "High", "last_contact": "2024-01-15", "status": "Active"},
            {"name": "Department of Water and Sanitation", "type": "Government", "engagement": "Critical", "last_contact": "2024-01-20", "status": "Active"},
            {"name": "Environmental Affairs Department", "type": "Government", "engagement": "High", "last_contact": "2024-01-18", "status": "Active"},
            {"name": "Agricultural Associations", "type": "Business", "engagement": "Medium", "last_contact": "2024-01-10", "status": "Active"},
            {"name": "Local Municipality Council", "type": "Government", "engagement": "High", "last_contact": "2024-01-22", "status": "Active"}
        ]
    
    def get_stakeholders(self):
        return st.session_state.stakeholders
    
    def add_stakeholder(self, name, stakeholder_type, engagement):
        new_stakeholder = {
            "name": name,
            "type": stakeholder_type,
            "engagement": engagement,
            "last_contact": datetime.now().strftime("%Y-%m-%d"),
            "status": "Active"
        }
        st.session_state.stakeholders.append(new_stakeholder)

class JobsAnalysis:
    """Comprehensive Jobs Creation Analysis"""
    
    @staticmethod
    def get_jobs_breakdown(province, rural_area, project_scale, targets):
        """Detailed jobs creation analysis with economic impact"""
        
        # Calculate jobs based on targets and progress
        target_jobs = targets["jobs_target"]
        current_jobs = int(target_jobs * (0.3 + np.random.random() * 0.4))  # Simulated progress
        
        # Jobs by phase and category (scaled to targets)
        scale_factor = target_jobs / 450  # Base scaling factor
        
        jobs_data = {
            "Construction Phase": {
                "Skilled Labor": {
                    "Civil Engineers": max(1, int(15 * scale_factor)),
                    "Structural Engineers": max(1, int(8 * scale_factor)),
                    "Construction Managers": max(1, int(6 * scale_factor)),
                    "Heavy Equipment Operators": max(1, int(25 * scale_factor)),
                    "Electricians": max(1, int(12 * scale_factor)),
                    "Plumbers": max(1, int(10 * scale_factor)),
                    "Welders": max(1, int(18 * scale_factor)),
                    "Surveyors": max(1, int(5 * scale_factor))
                },
                "Unskilled Labor": {
                    "General Laborers": max(1, int(120 * scale_factor)),
                    "Assistant Workers": max(1, int(80 * scale_factor)),
                    "Site Cleaners": max(1, int(15 * scale_factor)),
                    "Material Handlers": max(1, int(25 * scale_factor))
                },
                "Professional Services": {
                    "Project Managers": max(1, int(4 * scale_factor)),
                    "Safety Officers": max(1, int(6 * scale_factor)),
                    "Quality Inspectors": max(1, int(8 * scale_factor)),
                    "Administrative Staff": max(1, int(10 * scale_factor))
                }
            },
            "Operational Phase": {
                "Technical Operations": {
                    "Dam Operators": max(1, int(8 * scale_factor)),
                    "Maintenance Technicians": max(1, int(12 * scale_factor)),
                    "Water Quality Analysts": max(1, int(6 * scale_factor)),
                    "Electrical Technicians": max(1, int(4 * scale_factor))
                },
                "Administrative": {
                    "Facility Managers": max(1, int(2 * scale_factor)),
                    "Administrative Staff": max(1, int(6 * scale_factor)),
                    "Security Personnel": max(1, int(8 * scale_factor)),
                    "Grounds Maintenance": max(1, int(4 * scale_factor))
                }
            },
            "Indirect Employment": {
                "Local Economy": {
                    "Agriculture Support": max(1, int(45 * scale_factor)),
                    "Small Businesses": max(1, int(30 * scale_factor)),
                    "Transport Services": max(1, int(15 * scale_factor)),
                    "Hospitality Services": max(1, int(20 * scale_factor))
                }
            }
        }
        
        # Economic impact analysis
        wage_analysis = {
            "Skilled Labor": {"average_salary": 350000, "annual_income": 0},
            "Unskilled Labor": {"average_salary": 120000, "annual_income": 0},
            "Professional Services": {"average_salary": 450000, "annual_income": 0},
            "Technical Operations": {"average_salary": 280000, "annual_income": 0},
            "Administrative": {"average_salary": 180000, "annual_income": 0},
            "Local Economy": {"average_salary": 90000, "annual_income": 0}
        }
        
        # Calculate total jobs and economic impact
        total_jobs = 0
        total_annual_income = 0
        
        for phase, categories in jobs_data.items():
            for category, positions in categories.items():
                category_jobs = sum(positions.values())
                total_jobs += category_jobs
                
                if category in wage_analysis:
                    category_income = category_jobs * wage_analysis[category]["average_salary"]
                    wage_analysis[category]["annual_income"] = category_income
                    total_annual_income += category_income
        
        return jobs_data, wage_analysis, total_jobs, total_annual_income, current_jobs

# =============================================
# ENTERPRISE USER INTERFACE
# =============================================

# Initialize enterprise services
analytics_service = AnalyticsService()
impact_targets = ImpactTargets()
satellite_service = SatelliteImageryService()
hydrological_model = HydrologicalModel()
iot_service = IoTDataService()
regulatory_service = RegulatoryCompliance()
stakeholder_manager = StakeholderManagement()
jobs_analyzer = JobsAnalysis()

# Professional Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">Water Infrastructure Enterprise Platform</h1>
    <p style="color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0;">
    Enterprise-Grade Water Infrastructure Intelligence • Advanced Analytics • Real-Time Monitoring
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================
# ENTERPRISE DASHBOARD
# =============================================

if 'user_area_selected' not in st.session_state:
    st.session_state.user_area_selected = False

def show_enterprise_dashboard(province, rural_area):
    """Enterprise-grade dashboard with all integrated services"""
    
    # Add back button at the top
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Change Location", type="secondary", use_container_width=True):
            st.session_state.user_area_selected = False
            st.rerun()
    
    # Project scale selection
    project_scale = st.selectbox(
        "Project Scale:",
        ["Small", "Medium", "Large", "Enterprise"],
        key="project_scale"
    )
    
    # Get impact targets and current progress
    targets, current_progress = impact_targets.get_impact_targets(province, rural_area, project_scale)
    
    # Get all enterprise data
    predictions, insights = analytics_service.get_water_stress_prediction(province, rural_area)
    satellite_map = satellite_service.get_satellite_map(province, rural_area)
    iot_data, historical_data = iot_service.get_sensor_data(province, rural_area)
    compliance_data = regulatory_service.get_compliance_status(province, "Design")
    stakeholders = stakeholder_manager.get_stakeholders()
    jobs_data, wage_analysis, total_jobs, total_income, current_jobs = jobs_analyzer.get_jobs_breakdown(province, rural_area, project_scale, targets)
    
    # Show dependency warning only once at the top if folium is not available
    if not FOLIUM_AVAILABLE:
        st.warning("Mapping Features Limited: Folium package not installed. Some satellite mapping features will be limited.")
        st.info("To enable full mapping capabilities: Run the following command in your terminal:\n\n```bash\npip install folium streamlit-folium\n```")
    
    # =============================================
    # EXECUTIVE SUMMARY - TARGETS VS CURRENT PROGRESS
    # =============================================
    
    st.markdown(f'<div class="section-header">Enterprise Executive Summary: {rural_area}, {province}</div>', unsafe_allow_html=True)
    
    # Targets vs Current Progress
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="target-metric">
            <h3>Water Access Target</h3>
            <h2>{targets['water_access_target']}%</h2>
            <p>Post-Project Target</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="current-metric">
            <h3>Current Water Access</h3>
            <h2>{current_progress['water_access_current']}%</h2>
            <p>Pre-Project Baseline</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="target-metric">
            <h3>Jobs Creation Target</h3>
            <h2>{targets['jobs_target']}</h2>
            <p>Total Employment Target</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="current-metric">
            <h3>Current Jobs Created</h3>
            <h2>{current_jobs}</h2>
            <p>Progress to Date</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="target-metric">
            <h3>Economic Impact Target</h3>
            <h2>ZAR {targets['economic_impact_target']}M</h2>
            <p>Annual Target</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="current-metric">
            <h3>Current Economic Impact</h3>
            <h2>ZAR {current_progress['economic_current']}M</h2>
            <p>Annual Impact to Date</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        progress_percentage = min(100, int((current_jobs / targets['jobs_target']) * 100)) if targets['jobs_target'] > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>Overall Progress</h3>
            <h2>{progress_percentage}%</h2>
            <p>Towards Project Targets</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(progress_percentage / 100)
        st.caption(f"Project Completion: {progress_percentage}%")
    
    # =============================================
    # ENTERPRISE ANALYTICS
    # =============================================
    
    st.markdown('<div class="section-header">Enterprise Analytics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Strategic Insights")
        for insight in insights:
            st.write(f"• {insight}")
        
        # Risk Dashboard
        st.subheader("Enterprise Risk Assessment")
        risk_metrics = [
            ("Water Stress Level", predictions.get('water_stress_level', 0), 0.7),
            ("Infrastructure Risk", predictions.get('infrastructure_risk', 0), 0.5),
            ("Drought Probability", predictions.get('drought_probability', 0), 0.4)
        ]
        
        for metric, value, threshold in risk_metrics:
            col_a, col_b, col_c = st.columns([2, 1, 3])
            with col_a:
                st.write(metric)
            with col_b:
                st.write(f"{value:.1%}")
            with col_c:
                st.progress(value)
                if value > threshold:
                    st.caption("High Risk - Immediate Action Recommended")
    
    with col2:
        st.subheader("Real-Time Monitoring")
        if iot_data:
            st.metric("Water Level", f"{iot_data['water_level']:.1f}%", "-2.3%")
            st.metric("Water Quality pH", f"{iot_data['water_quality']:.1f}", "Optimal")
            st.metric("Flow Rate", f"{iot_data['flow_rate']:.1f} m³/s", "+0.5")
            st.metric("Sensor Status", iot_data['sensor_status'], f"{iot_data['battery_level']}%")
    
    # =============================================
    # ENGINEERING & CONSTRUCTION INTELLIGENCE
    # =============================================
    
    st.markdown('<div class="section-header">Engineering Intelligence & Construction Planning</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Satellite Analysis", 
        "Hydrological Modeling", 
        "Design Integration",
        "Construction Timeline"
    ])
    
    with tab1:
        st.subheader("Satellite Imagery & Geospatial Analysis")
        
        if satellite_map and FOLIUM_AVAILABLE:
            folium_static(satellite_map, width=800, height=500)
        else:
            st.markdown(f"""
            <div class="map-placeholder">
                <h3>Satellite Mapping Service</h3>
                <p>Interactive satellite mapping requires additional dependencies</p>
                <p style="margin-top: 1rem;">Proposed Dam Site Location: {rural_area}, {province}</p>
                <p>Catchment Area: 150 km² with favorable geology</p>
                <p>Site Status: Optimal dam location identified</p>
                <p>Topography: Gentle slopes with stable bedrock foundation</p>
                <p>Water Yield: Estimated 12.5 million m³ annual capacity</p>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Site Analysis")
            st.write("Topographical Assessment:")
            st.write("- Optimal dam location identified through terrain modeling")
            st.write("- Catchment area: 150 km² with favorable geology")
            st.write("- Minimal environmental disruption anticipated")
            st.write("- Existing infrastructure integration points mapped")
        
        with col2:
            st.subheader("Geotechnical Data")
            soil_data = {
                "Parameter": ["Soil Bearing Capacity", "Rock Depth", "Slope Stability", "Seismic Risk"],
                "Value": ["450 kPa", "8-12 meters", "Stable", "Low"],
                "Rating": ["Excellent", "Good", "Good", "Excellent"]
            }
            st.dataframe(pd.DataFrame(soil_data), use_container_width=True)
    
    with tab2:
        st.subheader("Hydrological Modeling")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Interactive hydrological simulation
            st.subheader("Water Flow Simulation")
            catchment_area = st.slider("Catchment Area (km²)", 50, 300, 150)
            rainfall = st.slider("Design Rainfall (mm/day)", 10, 100, 45)
            evaporation = st.slider("Evaporation Rate (mm/day)", 2, 15, 6)
            soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loamy", "Rocky"])
            
            flow_data, peak_flow = hydrological_model.simulate_water_flow(
                catchment_area, rainfall, evaporation, soil_type
            )
            
            if not flow_data.empty:
                fig = px.line(flow_data, x='hour', y='flow_rate', color='stage',
                             title='Simulated Daily Water Flow Pattern')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Model Output")
            st.metric("Peak Flow Rate", f"{peak_flow:.1f} m³/s")
            st.metric("Runoff Coefficient", "0.65")
            st.metric("Design Capacity", "125% of peak flow")
            
            st.download_button(
                "Download Hydrological Report",
                data=json.dumps({
                    "peak_flow": peak_flow,
                    "catchment_area": catchment_area,
                    "rainfall": rainfall,
                    "soil_type": soil_type
                }, indent=2),
                file_name=f"hydrological_analysis_{rural_area}.json",
                use_container_width=True
            )
    
    with tab3:
        st.subheader("Professional Design Integration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="engineering-diagram">', unsafe_allow_html=True)
            st.subheader("Structural Design - Cross Section")
            st.write("Professional CAD Integration")
            st.write("Enterprise CAD system would display detailed engineering drawings here.")
            st.write("Features:")
            st.write("- Structural cross-sections")
            st.write("- Reinforcement detailing")
            st.write("- Foundation design")
            st.write("- Hydraulic calculations")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button(
                "Download Design Specifications",
                data=json.dumps({
                    "project": f"Dam Construction - {rural_area}",
                    "structural_type": "Concrete Gravity Dam",
                    "height": "45 meters",
                    "capacity": "12,500,000 m³",
                    "design_standard": "SANS 10100"
                }, indent=2),
                file_name=f"dam_design_{rural_area}.json",
                use_container_width=True
            )
        
        with col2:
            st.markdown('<div class="engineering-diagram">', unsafe_allow_html=True)
            st.subheader("3D Engineering Model")
            # Create interactive 3D dam visualization
            x = np.linspace(-100, 100, 50)
            y = np.linspace(-50, 50, 50)
            X, Y = np.meshgrid(x, y)
            Z = 0.01 * (X**2) + 10
            
            fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Blues')])
            fig_3d.update_layout(
                title='3D Structural Analysis Model',
                scene=dict(
                    xaxis_title='Length (m)',
                    yaxis_title='Width (m)',
                    zaxis_title='Height (m)'
                ),
                height=400
            )
            st.plotly_chart(fig_3d, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Construction Management")
        
        # Gantt chart for construction timeline
        phases = [
            {"Task": "Site Preparation", "Start": "2024-01", "Finish": "2024-03", "Progress": 100},
            {"Task": "Foundation Work", "Start": "2024-04", "Finish": "2024-08", "Progress": 75},
            {"Task": "Dam Construction", "Start": "2024-09", "Finish": "2025-06", "Progress": 25},
            {"Task": "Mechanical Installation", "Start": "2025-03", "Finish": "2025-08", "Progress": 10},
            {"Task": "Testing & Commissioning", "Start": "2025-09", "Finish": "2025-12", "Progress": 0}
        ]
        
        fig_timeline = px.timeline(
            phases, 
            x_start="Start", 
            x_end="Finish", 
            y="Task",
            color="Progress",
            color_continuous_scale=["#dc3545", "#ffc107", "#28a745"]
        )
        fig_timeline.update_layout(height=300)
        fig_timeline.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # =============================================
    # COMPREHENSIVE IMPACT ANALYSIS
    # =============================================
    
    st.markdown('<div class="section-header">Comprehensive Impact Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Target vs Current Impact")
        
        # Create comparison chart
        impact_data = {
            "Metric": ["Jobs Creation", "Economic Impact (ZAR M)", "Water Access (%)"],
            "Target": [targets['jobs_target'], targets['economic_impact_target'], targets['water_access_target']],
            "Current": [current_jobs, current_progress['economic_current'], current_progress['water_access_current']]
        }
        
        df_impact = pd.DataFrame(impact_data)
        fig_impact = px.bar(df_impact, x='Metric', y=['Target', 'Current'], 
                           barmode='group', title="Target vs Current Impact Metrics")
        st.plotly_chart(fig_impact, use_container_width=True)
    
    with col2:
        st.subheader("Impact Summary")
        
        st.metric("Total Jobs Target", f"{targets['jobs_target']}")
        st.metric("Current Jobs Created", f"{current_jobs}")
        st.metric("Remaining Jobs", f"{targets['jobs_target'] - current_jobs}")
        
        st.metric("Economic Target", f"ZAR {targets['economic_impact_target']}M")
        st.metric("Current Economic Impact", f"ZAR {current_progress['economic_current']}M")
        st.metric("Water Access Target", f"{targets['water_access_target']}%")
        
        st.download_button(
            "Download Impact Report",
            data=json.dumps({
                "targets": targets,
                "current_progress": current_progress,
                "jobs_data": jobs_data
            }, indent=2),
            file_name=f"impact_analysis_{rural_area}.json",
            use_container_width=True
        )
    
    # Detailed jobs breakdown
    st.subheader("Detailed Employment Analysis")
    
    for phase, categories in jobs_data.items():
        with st.expander(f"{phase} - {sum(sum(subcat.values()) for subcat in categories.values())} Jobs"):
            for category, positions in categories.items():
                st.write(f"{category}:")
                cols = st.columns(4)
                for i, (position, count) in enumerate(positions.items()):
                    with cols[i % 4]:
                        st.metric(position, count)
    
    # =============================================
    # COMPLIANCE & STAKEHOLDER MANAGEMENT
    # =============================================
    
    st.markdown('<div class="section-header">Regulatory Compliance & Stakeholder Management</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Regulatory Compliance Tracking")
        
        for category, requirements in compliance_data.items():
            with st.expander(f"{category} Compliance"):
                for req in requirements:
                    status_class = req['status'].lower().replace(' ', '-')
                    st.markdown(f"""
                    <div class="compliance-status {status_class}">
                        <strong>{req['requirement']}</strong><br>
                        Status: {req['status']} | Agency: {req['agency']} | Deadline: {req['deadline']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Stakeholder Engagement Management")
        
        # Stakeholder table
        stakeholder_df = pd.DataFrame(stakeholders)
        st.dataframe(stakeholder_df, use_container_width=True)
        
        # Add new stakeholder
        with st.expander("Add New Stakeholder"):
            new_name = st.text_input("Stakeholder Name")
            new_type = st.selectbox("Type", ["Community", "Government", "Business", "NGO"])
            new_engagement = st.selectbox("Engagement Level", ["Critical", "High", "Medium", "Low"])
            
            if st.button("Add Stakeholder") and new_name:
                stakeholder_manager.add_stakeholder(new_name, new_type, new_engagement)
                st.success("Stakeholder added successfully")
                st.rerun()

# =============================================
# ENTERPRISE LANDING PAGE
# =============================================

def show_enterprise_landing():
    st.markdown('<div class="section-header">Enterprise Platform Access</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Project Location Selection")
        province = st.selectbox(
            "Select Province:",
            ["Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", 
             "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"],
            key="province_select"
        )
        
        rural_areas = {
            "Eastern Cape": ["Alice", "Butterworth", "Cradock", "Graaff-Reinet", "Lady Frere"],
            "Free State": ["Bethlehem", "Bothaville", "Frankfort", "Harrismith", "Philippolis"],
            "Gauteng": ["Bronkhorstspruit", "Cullinan", "Heidelberg", "Randfontein", "Soshanguve"],
            "KwaZulu-Natal": ["Eshowe", "Hluhluwe", "Ixopo", "Mtubatuba", "Nkandla"],
            "Limpopo": ["Alldays", "Giyani", "Lebowakgomo", "Makhado", "Tzaneen"],
            "Mpumalanga": ["Barberton", "Carolina", "Ermelo", "Hazyview", "Pilgrim's Rest"],
            "North West": ["Coligny", "Ganyesa", "Koster", "Madikwe", "Sannieshof"],
            "Northern Cape": ["Barkly West", "Calvinia", "Kenhardt", "Pofadder", "Upington"],
            "Western Cape": ["Barrydale", "Caledon", "Grabouw", "Prince Albert", "Tulbagh"]
        }
        
        rural_area = st.selectbox(
            "Select Rural Area:",
            rural_areas.get(province, ["Select province first"]),
            key="rural_select"
        )
        
        if st.button("Access Enterprise Dashboard", type="primary", use_container_width=True):
            if province and rural_area:
                st.session_state.user_area_selected = True
                st.session_state.selected_province = province
                st.session_state.selected_rural_area = rural_area
                st.rerun()
    
    with col2:
        st.subheader("Platform Features")
        st.markdown("""
        <div class="metric-card">
        <h4>Advanced Analytics Integration</h4>
        <p>Enterprise analytics for predictive analytics and risk assessment</p>
        
        <h4>Satellite Imagery</h4>
        <p>Real-time geospatial analysis and terrain modeling</p>
        
        <h4>Hydrological Modeling</h4>
        <p>Professional water flow simulation and analysis</p>
        
        <h4>Real-Time Monitoring</h4>
        <p>Live sensor data integration and alert systems</p>
        
        <h4>Impact Analysis</h4>
        <p>Detailed employment impact and economic modeling</p>
        
        <h4>Regulatory Compliance</h4>
        <p>Automated compliance monitoring across multiple agencies</p>
        
        <h4>Stakeholder Management</h4>
        <p>Enterprise-grade stakeholder engagement tracking</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# ENTERPRISE APPLICATION FLOW
# =============================================

if not st.session_state.user_area_selected:
    show_enterprise_landing()
else:
    show_enterprise_dashboard(st.session_state.selected_province, st.session_state.selected_rural_area)

# =============================================
# ENTERPRISE FOOTER
# =============================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <h4>Water Infrastructure Enterprise Platform</h4>
    <p>Enterprise-Grade Water Infrastructure Intelligence • Advanced Analytics • Professional Engineering</p>
    <p style="font-size: 0.9rem;">Integrated Satellite Imagery • Advanced Hydrological Modeling • Real-Time Monitoring</p>
</div>
""", unsafe_allow_html=True)
