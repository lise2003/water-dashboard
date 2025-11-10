import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import os

# Set page configuration
st.set_page_config(
    page_title="HydroTransparent Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0f62fe;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #393939;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0f62fe;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">🌊 HYDROTRANSPARENT INSIGHT DASHBOARD</div>', unsafe_allow_html=True)
st.markdown("### Real-time Patterns, Trends & Anti-Corruption Impact")
st.markdown("---")

# Initialize session state for data persistence
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Data loading function
@st.cache_data
def load_data():
    """Load and cache all datasets"""
    try:
        service_levels = pd.read_csv("HydroTransparent/Water Service Levels - Households_ 2025_10_08.csv", encoding="ISO-8859-1")
        esk2033 = pd.read_csv("HydroTransparent/ESK2033.csv", encoding="ISO-8859-1")
        wash = pd.read_csv("HydroTransparent/washdata.csv", encoding="ISO-8859-1")
        dams = pd.read_csv("HydroTransparent/globaldamsdatabase_global_coverage_november_2020.csv", encoding="ISO-8859-1")
        
        # Clean service levels data
        service_levels = service_levels.drop(columns=[c for c in service_levels.columns if "Unnamed" in c], errors="ignore")
        service_levels.columns = service_levels.columns.str.replace('\xa0', ' ', regex=False).str.strip()
        
        # Process water sources columns
        water_sources = [
            'Piped water inside dwelling Households',
            'Piped water inside yard Households',
            'Distance Below 200m Households',
            'Distance greater than 200m Households',
            'Borehole Households',
            'Spring Households',
            'Rain-water tank Households',
            'Dam/pool/stagnant water Households',
            'River/stream Households',
            'Water vendor Households',
            'Other Water Households'
        ]
        
        for col in water_sources + ['Total Households']:
            if col in service_levels.columns:
                service_levels[col] = pd.to_numeric(service_levels[col], errors="coerce").fillna(0)
        
        # Compute water access percentage
        service_levels['Piped_Access_Percent'] = (
            (service_levels['Piped water inside dwelling Households'] +
             service_levels['Piped water inside yard Households']) /
            service_levels['Total Households'] * 100
        ).fillna(0)
        
        return service_levels, esk2033, wash, dams, True
        
    except Exception as e:
        st.error(f"Error loading datasets: {e}")
        return None, None, None, None, False

# Load data
with st.spinner("📊 Loading and processing datasets..."):
    service_levels, esk2033, wash, dams, success = load_data()
    
    if success:
        st.session_state.data_loaded = True
        st.success("✅ All datasets loaded successfully")
    else:
        st.error("❌ Failed to load datasets")

# Mock service classes (converted from original classes)
class AnalyticsService:
    @staticmethod
    def get_water_stress_prediction(province, rural_area):
        predictions = {
            "water_stress_level": float(max(0.6, min(0.95, 0.7 + np.random.normal(0, 0.1)))),
            "infrastructure_risk": float(max(0.3, min(0.9, 0.5 + np.random.normal(0, 0.1)))),
            "conservation_potential": float(max(0.4, min(0.95, 0.65 + np.random.normal(0, 0.1)))),
            "rainfall_variability": float(max(0.2, min(0.9, 0.45 + np.random.normal(0, 0.1)))),
            "drought_probability": float(max(0.05, min(0.85, 0.35 + np.random.normal(0, 0.1))))
        }
        insights = [
            f"Predicted water stress in {rural_area}: {predictions['water_stress_level']:.1%}",
            f"Suggested resilience investment ~ ZAR {75 + np.random.randint(10,40)}M",
            f"Conservation potential: {predictions['conservation_potential']:.1%}",
            f"Drought probability (36m): {predictions['drought_probability']:.1%}"
        ]
        return predictions, insights

class ImpactTargets:
    @staticmethod
    def get_impact_targets(province, rural_area, project_scale):
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
        
        scale_multipliers = {"Small": 0.6, "Medium": 0.8, "Large": 1.0, "Enterprise": 1.2}
        province_targets = base_targets.get(province, {"jobs_target": 400, "economic_impact_target": 80, "water_access_target": 80})
        multiplier = scale_multipliers.get(project_scale, 1.0)
        
        targets = {
            "jobs_target": int(province_targets["jobs_target"] * multiplier),
            "economic_impact_target": int(province_targets["economic_impact_target"] * multiplier),
            "water_access_target": province_targets["water_access_target"]
        }
        
        current_progress = {
            "jobs_current": int(targets["jobs_target"] * (0.3 + np.random.random() * 0.4)),
            "economic_current": int(targets["economic_impact_target"] * (0.25 + np.random.random() * 0.5)),
            "water_access_current": 42 + np.random.randint(5, 25)
        }
        
        return targets, current_progress

class HydrologicalModel:
    @staticmethod
    def simulate_water_flow(catchment_area, rainfall, evaporation, soil_type):
        runoff_coefficients = {"clay": 0.75, "sandy": 0.35, "loamy": 0.55, "rocky": 0.85}
        runoff_coeff = runoff_coefficients.get(soil_type.lower(), 0.6)
        effective_rainfall = max(0, rainfall - evaporation)
        peak_flow = (runoff_coeff * effective_rainfall * catchment_area) / 3.6
        
        time_steps = 24
        base_flow = peak_flow * 0.1
        rows = []
        
        for hour in range(time_steps):
            if 6 <= hour <= 18:
                flow = base_flow + (peak_flow - base_flow) * np.sin((hour - 6) * np.pi / 12)
            else:
                flow = base_flow
            flow = max(0, flow + np.random.normal(0, flow * 0.08))
            rows.append({"hour": hour, "flow_rate": flow, "stage": "Day" if 6 <= hour <= 18 else "Night"})
        
        return pd.DataFrame(rows), peak_flow

class IoTDataService:
    @staticmethod
    def get_sensor_data(province, rural_area):
        now = datetime.now()
        sensor = {
            "water_level": float(64.5 + np.random.normal(0, 2)),
            "water_quality": float(7.2 + np.random.normal(0, 0.1)),
            "turbidity": float(4.1 + np.random.normal(0, 0.5)),
            "temperature": float(18.5 + np.random.normal(0, 1)),
            "flow_rate": float(12.3 + np.random.normal(0, 0.5)),
            "last_updated": now,
            "sensor_status": "Online",
            "battery_level": int(87 + np.random.randint(-5, 5))
        }
        
        hours = [(now - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M") for i in range(24, 0, -1)]
        hist = pd.DataFrame({
            "timestamp": hours,
            "water_level": [sensor["water_level"] + np.random.normal(0, 1) for _ in range(24)],
            "flow_rate": [sensor["flow_rate"] + np.random.normal(0, 0.3) for _ in range(24)]
        })
        
        return sensor, hist

# Sidebar for controls
st.sidebar.markdown("## 🎛️ Enterprise Controls")

# Province selection
PROVINCES = [
    "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo",
    "Mpumalanga", "North West", "Northern Cape", "Western Cape"
]

rural_map = {
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

province = st.sidebar.selectbox("Province:", PROVINCES, index=2)  # Default to Gauteng
rural_area = st.sidebar.selectbox("Rural area:", rural_map.get(province, []))
project_scale = st.sidebar.selectbox("Project scale:", ["Small", "Medium", "Large", "Enterprise"], index=1)

st.sidebar.markdown("### 🏞️ Hydrology Controls")
soil_type = st.sidebar.selectbox("Soil type:", ["Clay", "Sandy", "Loamy", "Rocky"], index=2)
catchment_area = st.sidebar.slider("Catchment km²", 50, 300, 150)
rainfall = st.sidebar.slider("Rainfall mm/day", 10, 100, 45)
evaporation = st.sidebar.slider("Evaporation mm/day", 0, 20, 6)

# Main dashboard
if st.session_state.data_loaded:
    # Executive Summary
    st.markdown(f"## 📍 Enterprise Executive Summary — **{rural_area}, {province}**")
    
    # Get predictions and targets
    targets, current_progress = ImpactTargets.get_impact_targets(province, rural_area, project_scale)
    predictions, insights = AnalyticsService.get_water_stress_prediction(province, rural_area)
    sensor, hist = IoTDataService.get_sensor_data(province, rural_area)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Jobs Target", f"{targets['jobs_target']}", f"{current_progress['jobs_current']} Current")
    
    with col2:
        st.metric("Economic Impact Target", f"ZAR {targets['economic_impact_target']}M", 
                 f"ZAR {current_progress['economic_current']}M Current")
    
    with col3:
        st.metric("Water Access Target", f"{targets['water_access_target']}%", 
                 f"{current_progress['water_access_current']}% Current")
    
    # Strategic Insights
    st.markdown("### 🎯 Strategic Insights")
    for insight in insights:
        st.info(insight)
    
    # Real-time Monitoring
    st.markdown("### 📡 Real-time Monitoring (Simulated IoT)")
    iot_col1, iot_col2, iot_col3, iot_col4 = st.columns(4)
    
    with iot_col1:
        st.metric("Water Level", f"{sensor['water_level']:.1f}%")
    
    with iot_col2:
        st.metric("Water Quality (pH)", f"{sensor['water_quality']:.1f}")
    
    with iot_col3:
        st.metric("Flow Rate", f"{sensor['flow_rate']:.1f} m³/s")
    
    with iot_col4:
        st.metric("Sensor Status", sensor['sensor_status'], f"Battery: {sensor['battery_level']}%")
    
    # Hydrological Simulation
    st.markdown("### 🌊 Hydrological Simulation")
    flow_df, peak_flow = HydrologicalModel.simulate_water_flow(catchment_area, rainfall, evaporation, soil_type)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_flow = px.line(flow_df, x='hour', y='flow_rate', color='stage', 
                          title=f'Simulated Daily Flow - Peak: {peak_flow:.2f} m³/s')
        st.plotly_chart(fig_flow, use_container_width=True)
    
    with col2:
        st.metric("Peak Flow", f"{peak_flow:.2f} m³/s")
        st.dataframe(flow_df.head(10), use_container_width=True)
    
    # Impact Visualization
    st.markdown("### 📊 Impact: Target vs Current")
    impact_df = pd.DataFrame({
        "Metric": ["Jobs", "Economic (ZAR M)", "Water Access (%)"],
        "Target": [targets['jobs_target'], targets['economic_impact_target'], targets['water_access_target']],
        "Current": [current_progress['jobs_current'], current_progress['economic_current'], current_progress['water_access_current']]
    })
    
    fig_impact = px.bar(impact_df, x='Metric', y=['Target', 'Current'], 
                       barmode='group', title="Target vs Current Impact")
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # Water Access Trends
    if service_levels is not None:
        st.markdown("### 💧 Water Access Trends by Province")
        
        # Sort by piped access
        service_levels_sorted = service_levels.sort_values('Piped_Access_Percent', ascending=True)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            name='Current Piped Access',
            x=service_levels_sorted['Region'],
            y=service_levels_sorted['Piped_Access_Percent'],
            marker_color='lightblue',
            text=service_levels_sorted['Piped_Access_Percent'].round(1),
            textposition='auto',
        ))
        
        # Add target line
        fig_trend.add_trace(go.Scatter(
            x=service_levels_sorted['Region'],
            y=[85] * len(service_levels_sorted),
            mode='lines',
            name='HydroTransparent Target (85%)',
            line=dict(color='red', width=3, dash='dash'),
            hoverinfo='skip'
        ))
        
        fig_trend.update_layout(
            title='Water Access by Province vs Target',
            xaxis_title='Province',
            yaxis_title='Piped Water Access (%)',
            xaxis_tickangle=-45,
            height=500,
            showlegend=True,
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Performance Trends
    st.markdown("### 📈 Performance Improvement Trends")
    
    # Create performance data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    performance_data = pd.DataFrame({
        'Month': months * 3,
        'Value': 
            # Infrastructure Transparency (rising trend)
            [65, 68, 72, 75, 78, 80, 82, 83, 84, 85, 86, 87] +
            # Financial Irregularities (falling trend)
            [25, 22, 20, 18, 17, 16, 15, 14, 13, 13, 12, 12] +
            # Digital Adoption (rising trend)
            [45, 48, 52, 55, 58, 62, 65, 68, 71, 74, 76, 78],
        'Metric': ['Infrastructure Transparency ↗️'] * 12 + ['Financial Irregularities ↘️'] * 12 + ['Digital Adoption ↗️'] * 12
    })
    
    fig_performance = px.line(
        performance_data,
        x='Month',
        y='Value',
        color='Metric',
        title='Monthly Improvement Tracking',
        markers=True,
        line_shape='spline'
    )
    
    # Make lines thicker
    for trace in fig_performance.data:
        trace.update(line=dict(width=4))
    
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Impact Dashboard
    st.markdown("### 🛡️ HydroTransparent Impact Dashboard")
    
    metrics_data = {
        "Metric": [
            "💧 Audited Water Projects",
            "⚙️ Infrastructure Transparency",
            "🧾 Financial Irregularities",
            "🌍 Provincial Coverage",
            "🔐 Citizen Access",
            "🛰️ Digital Tracking"
        ],
        "Current": [92, 87, 12, 100, 95, 78],
        "Previous": [85, 79, 18, 85, 88, 65],
        "Trend_Icon": ["📈", "📈", "📉", "📈", "📈", "📈"],
        "Trend_Description": ["Steady Rise", "Strong Growth", "Significant Drop", "Complete Coverage", "Rapid Adoption", "Accelerating"]
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df['Change'] = metrics_df['Current'] - metrics_df['Previous']
    
    # Display metrics in columns
    cols = st.columns(3)
    for i, (_, row) in enumerate(metrics_df.iterrows()):
        with cols[i % 3]:
            delta = f"{row['Change']:+.0f}" if row['Metric'] != '🧾 Financial Irregularities' else f"{row['Change']:+.0f}"
            st.metric(
                label=f"{row['Metric']} {row['Trend_Icon']}",
                value=f"{row['Current']}%",
                delta=delta
            )
    
    # Export functionality
    st.markdown("### 💾 Export Report")
    if st.button("Save Project Report"):
        report = {
            "province": province,
            "rural_area": rural_area,
            "targets": targets,
            "current_progress": current_progress,
            "iot_snapshot": sensor,
            "peak_flow": float(peak_flow),
            "generated_at": datetime.now().isoformat()
        }
        
        fname = f"project_report_{province}_{rural_area}.json".replace(" ", "_")
        with open(fname, "w") as fh:
            json.dump(report, fh, indent=2, default=str)
        
        st.success(f"Project report saved to **{fname}**")
    
else:
    st.warning("Please ensure all data files are available in the HydroTransparent folder and restart the application.")

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Dashboard** - Built with Streamlit")
