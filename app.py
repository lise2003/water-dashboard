import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import os
import glob

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

# Province-specific base data
PROVINCE_BASE_DATA = {
    "Eastern Cape": {
        "water_stress": 0.75,
        "jobs_base": 420,
        "economic_base": 85,
        "water_access_base": 85,
        "coordinates": (-32.0833, 26.8833),
        "rainfall_factor": 1.2,
        "flow_factor": 0.9
    },
    "Free State": {
        "water_stress": 0.65,
        "jobs_base": 380,
        "economic_base": 75,
        "water_access_base": 80,
        "coordinates": (-28.4556, 26.7683),
        "rainfall_factor": 0.8,
        "flow_factor": 0.7
    },
    "Gauteng": {
        "water_stress": 0.85,
        "jobs_base": 500,
        "economic_base": 100,
        "water_access_base": 90,
        "coordinates": (-26.2044, 28.0456),
        "rainfall_factor": 0.9,
        "flow_factor": 0.6
    },
    "KwaZulu-Natal": {
        "water_stress": 0.70,
        "jobs_base": 450,
        "economic_base": 90,
        "water_access_base": 85,
        "coordinates": (-29.8587, 31.0218),
        "rainfall_factor": 1.4,
        "flow_factor": 1.2
    },
    "Limpopo": {
        "water_stress": 0.80,
        "jobs_base": 400,
        "economic_base": 80,
        "water_access_base": 80,
        "coordinates": (-23.4013, 29.4179),
        "rainfall_factor": 0.7,
        "flow_factor": 0.5
    },
    "Mpumalanga": {
        "water_stress": 0.72,
        "jobs_base": 420,
        "economic_base": 85,
        "water_access_base": 82,
        "coordinates": (-25.5653, 30.5279),
        "rainfall_factor": 1.1,
        "flow_factor": 1.0
    },
    "North West": {
        "water_stress": 0.68,
        "jobs_base": 380,
        "economic_base": 75,
        "water_access_base": 78,
        "coordinates": (-26.6639, 25.2838),
        "rainfall_factor": 0.6,
        "flow_factor": 0.4
    },
    "Northern Cape": {
        "water_stress": 0.90,
        "jobs_base": 350,
        "economic_base": 70,
        "water_access_base": 75,
        "coordinates": (-29.0467, 21.8569),
        "rainfall_factor": 0.4,
        "flow_factor": 0.3
    },
    "Western Cape": {
        "water_stress": 0.78,
        "jobs_base": 480,
        "economic_base": 95,
        "water_access_base": 88,
        "coordinates": (-33.9253, 18.4239),
        "rainfall_factor": 1.0,
        "flow_factor": 0.8
    }
}

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Data loading function
@st.cache_data
def load_data():
    """Load and cache all datasets"""
    try:
        csv_files = glob.glob("*.csv")
        
        file_mapping = {}
        for file in csv_files:
            file_lower = file.lower()
            if "service level" in file_lower or "household" in file_lower:
                file_mapping['service_levels'] = file
            elif "esk2033" in file_lower:
                file_mapping['esk2033'] = file
            elif "wash" in file_lower:
                file_mapping['wash'] = file
            elif "dam" in file_lower or "global_coverage" in file_lower:
                file_mapping['dams'] = file
        
        def safe_read_csv(filepath):
            encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
            for encoding in encodings:
                try:
                    return pd.read_csv(filepath, encoding=encoding, low_memory=False)
                except UnicodeDecodeError:
                    continue
            return pd.read_csv(filepath, low_memory=False)
        
        datasets = {}
        for key, filename in file_mapping.items():
            datasets[key] = safe_read_csv(filename)
        
        if 'service_levels' in datasets:
            service_levels = datasets['service_levels']
            service_levels = service_levels.drop(columns=[c for c in service_levels.columns if "Unnamed" in c], errors="ignore")
            service_levels.columns = service_levels.columns.str.replace('\xa0', ' ', regex=False).str.strip()
            
            water_sources = [
                'Piped water inside dwelling Households', 'Piped water inside yard Households',
                'Distance Below 200m Households', 'Distance greater than 200m Households',
                'Borehole Households', 'Spring Households', 'Rain-water tank Households',
                'Dam/pool/stagnant water Households', 'River/stream Households',
                'Water vendor Households', 'Other Water Households'
            ]
            
            for col in water_sources + ['Total Households']:
                if col in service_levels.columns:
                    service_levels[col] = pd.to_numeric(service_levels[col], errors="coerce").fillna(0)
            
            if all(col in service_levels.columns for col in ['Piped water inside dwelling Households', 
                                                           'Piped water inside yard Households', 
                                                           'Total Households']):
                service_levels['Piped_Access_Percent'] = (
                    (service_levels['Piped water inside dwelling Households'] +
                     service_levels['Piped water inside yard Households']) /
                    service_levels['Total Households'] * 100
                ).fillna(0)
            else:
                service_levels['Piped_Access_Percent'] = 0
            
            datasets['service_levels'] = service_levels
        
        return (datasets.get('service_levels'), 
                datasets.get('esk2033'), 
                datasets.get('wash'), 
                datasets.get('dams'), 
                True)
        
    except Exception as e:
        st.error(f"Error loading datasets: {str(e)}")
        return None, None, None, None, False

def create_demo_data():
    """Create demo data for testing"""
    provinces = list(PROVINCE_BASE_DATA.keys())
    
    demo_service_levels = pd.DataFrame({
        'Region': provinces,
        'Piped water inside dwelling Households': [int(PROVINCE_BASE_DATA[p]['water_access_base'] * 5000) for p in provinces],
        'Piped water inside yard Households': [int(PROVINCE_BASE_DATA[p]['water_access_base'] * 3000) for p in provinces],
        'Total Households': [100000] * len(provinces)
    })
    
    demo_service_levels['Piped_Access_Percent'] = (
        (demo_service_levels['Piped water inside dwelling Households'] +
         demo_service_levels['Piped water inside yard Households']) /
        demo_service_levels['Total Households'] * 100
    ).fillna(0)
    
    return demo_service_levels, None, None, None, True

# Load data
with st.spinner("📊 Loading and processing datasets..."):
    try:
        service_levels, esk2033, wash, dams, success = load_data()
        
        if not success:
            service_levels, esk2033, wash, dams, success = create_demo_data()
            
        if success:
            st.session_state.data_loaded = True
            st.success("✅ Datasets loaded successfully")
    except Exception as e:
        service_levels, esk2033, wash, dams, success = create_demo_data()
        if success:
            st.session_state.data_loaded = True
            st.success("✅ Using demo data for demonstration")

# Updated service classes with province-specific data
class AnalyticsService:
    @staticmethod
    def get_water_stress_prediction(province, rural_area):
        base_data = PROVINCE_BASE_DATA.get(province, PROVINCE_BASE_DATA["Gauteng"])
        
        # Use province-specific base values with some variation
        base_stress = base_data["water_stress"]
        predictions = {
            "water_stress_level": float(max(0.3, min(0.95, base_stress + np.random.normal(0, 0.05)))),
            "infrastructure_risk": float(max(0.2, min(0.9, 0.5 + np.random.normal(0, 0.1)))),
            "conservation_potential": float(max(0.4, min(0.95, 0.7 - base_stress * 0.3 + np.random.normal(0, 0.1)))),
            "rainfall_variability": float(max(0.1, min(0.8, (1 - base_data["rainfall_factor"]) + np.random.normal(0, 0.1)))),
            "drought_probability": float(max(0.05, min(0.85, base_stress * 0.8 + np.random.normal(0, 0.1))))
        }
        
        insights = [
            f"Predicted water stress in {rural_area}, {province}: {predictions['water_stress_level']:.1%}",
            f"Suggested resilience investment ~ ZAR {int(50 + base_stress * 100)}M",
            f"Conservation potential: {predictions['conservation_potential']:.1%}",
            f"Drought probability (36m): {predictions['drought_probability']:.1%}",
            f"Regional rainfall factor: {base_data['rainfall_factor']:.1f}x national average"
        ]
        
        return predictions, insights

class ImpactTargets:
    @staticmethod
    def get_impact_targets(province, rural_area, project_scale):
        base_data = PROVINCE_BASE_DATA.get(province, PROVINCE_BASE_DATA["Gauteng"])
        
        scale_multipliers = {"Small": 0.6, "Medium": 0.8, "Large": 1.0, "Enterprise": 1.2}
        multiplier = scale_multipliers.get(project_scale, 1.0)
        
        targets = {
            "jobs_target": int(base_data["jobs_base"] * multiplier),
            "economic_impact_target": int(base_data["economic_base"] * multiplier),
            "water_access_target": base_data["water_access_base"]
        }
        
        # Province-specific progress based on base characteristics
        progress_factor = 0.3 + (base_data["water_access_base"] / 100) * 0.4
        
        current_progress = {
            "jobs_current": int(targets["jobs_target"] * progress_factor),
            "economic_current": int(targets["economic_impact_target"] * (progress_factor - 0.1)),
            "water_access_current": int(base_data["water_access_base"] * (0.4 + np.random.random() * 0.3))
        }
        
        return targets, current_progress

class HydrologicalModel:
    @staticmethod
    def simulate_water_flow(catchment_area, rainfall, evaporation, soil_type, province):
        base_data = PROVINCE_BASE_DATA.get(province, PROVINCE_BASE_DATA["Gauteng"])
        
        runoff_coefficients = {"clay": 0.75, "sandy": 0.35, "loamy": 0.55, "rocky": 0.85}
        runoff_coeff = runoff_coefficients.get(soil_type.lower(), 0.6)
        
        # Adjust rainfall by province factor
        adjusted_rainfall = rainfall * base_data["rainfall_factor"]
        effective_rainfall = max(0, adjusted_rainfall - evaporation)
        peak_flow = (runoff_coeff * effective_rainfall * catchment_area * base_data["flow_factor"]) / 3.6
        
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
        base_data = PROVINCE_BASE_DATA.get(province, PROVINCE_BASE_DATA["Gauteng"])
        
        now = datetime.now()
        
        # Province-specific sensor readings
        base_water_level = 50 + (base_data["water_stress"] * 30)  # Higher stress = higher levels needed
        base_flow = 8 + (base_data["flow_factor"] * 8)  # Higher flow factor = higher flow rates
        
        sensor = {
            "water_level": float(base_water_level + np.random.normal(0, 2)),
            "water_quality": float(7.0 + (1 - base_data["water_stress"]) * 0.5 + np.random.normal(0, 0.1)),
            "turbidity": float(3.0 + base_data["water_stress"] * 2 + np.random.normal(0, 0.5)),
            "temperature": float(18.5 + np.random.normal(0, 1)),
            "flow_rate": float(base_flow + np.random.normal(0, 0.5)),
            "last_updated": now,
            "sensor_status": "Online",
            "battery_level": int(80 + np.random.randint(-10, 10))
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

PROVINCES = list(PROVINCE_BASE_DATA.keys())

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

province = st.sidebar.selectbox("Province:", PROVINCES, index=2)
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
    
    # Get province-specific predictions and targets
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
    
    # Hydrological Simulation - Now province-specific
    st.markdown("### 🌊 Hydrological Simulation")
    flow_df, peak_flow = HydrologicalModel.simulate_water_flow(catchment_area, rainfall, evaporation, soil_type, province)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_flow = px.line(flow_df, x='hour', y='flow_rate', color='stage', 
                          title=f'Simulated Daily Flow - {province} - Peak: {peak_flow:.2f} m³/s')
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
                       barmode='group', title=f"Target vs Current Impact - {province}")
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # Geospatial Map
    st.markdown("### 🗺️ Geospatial Analysis")
    
    # Create province coordinates dataframe
    province_coords = []
    for prov, data in PROVINCE_BASE_DATA.items():
        province_coords.append({
            'Province': prov,
            'Latitude': data['coordinates'][0],
            'Longitude': data['coordinates'][1],
            'Water_Stress': data['water_stress'],
            'Water_Access': data['water_access_base'],
            'Current_Selection': prov == province
        })
    
    map_df = pd.DataFrame(province_coords)
    
    # Create the map
    fig_map = px.scatter_mapbox(
        map_df,
        lat="Latitude",
        lon="Longitude",
        color="Water_Stress",
        size="Water_Access",
        hover_name="Province",
        hover_data={"Water_Stress": ":.2f", "Water_Access": True},
        color_continuous_scale="Viridis",
        size_max=15,
        zoom=5,
        height=400,
        title=f"Water Stress and Access by Province - Selected: {province}"
    )
    
    # Highlight selected province
    selected_province = map_df[map_df['Province'] == province]
    if not selected_province.empty:
        fig_map.add_trace(px.scatter_mapbox(
            selected_province,
            lat="Latitude",
            lon="Longitude",
            color_discrete_sequence=["red"]
        ).data[0])
    
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Water Access Trends
    if service_levels is not None and 'Region' in service_levels.columns:
        st.markdown("### 💧 Water Access Trends by Province")
        
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
        
        # Highlight current province
        if province in service_levels_sorted['Region'].values:
            province_value = service_levels_sorted[service_levels_sorted['Region'] == province]['Piped_Access_Percent'].iloc[0]
            fig_trend.add_trace(go.Scatter(
                x=[province],
                y=[province_value],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star'),
                name=f'Selected: {province}'
            ))
        
        fig_trend.add_trace(go.Scatter(
            x=service_levels_sorted['Region'],
            y=[85] * len(service_levels_sorted),
            mode='lines',
            name='HydroTransparent Target (85%)',
            line=dict(color='red', width=3, dash='dash'),
            hoverinfo='skip'
        ))
        
        fig_trend.update_layout(
            title=f'Water Access by Province - Selected: {province}',
            xaxis_title='Province',
            yaxis_title='Piped Water Access (%)',
            xaxis_tickangle=-45,
            height=500,
            showlegend=True,
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Province Comparison
    st.markdown("### 📈 Province Comparison")
    
    comparison_data = []
    for prov, data in PROVINCE_BASE_DATA.items():
        comparison_data.append({
            'Province': prov,
            'Water Stress': data['water_stress'] * 100,
            'Base Water Access': data['water_access_base'],
            'Rainfall Factor': data['rainfall_factor'],
            'Flow Factor': data['flow_factor'],
            'Is Selected': prov == province
        })
    
    comp_df = pd.DataFrame(comparison_data)
    
    fig_comp = px.bar(
        comp_df,
        x='Province',
        y=['Water Stress', 'Base Water Access'],
        barmode='group',
        title='Province Comparison: Water Stress vs Access',
        color_discrete_map={'Water Stress': 'red', 'Base Water Access': 'blue'}
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)
    
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
            "water_stress": predictions['water_stress_level'],
            "generated_at": datetime.now().isoformat()
        }
        
        fname = f"project_report_{province}_{rural_area}.json".replace(" ", "_")
        with open(fname, "w") as fh:
            json.dump(report, fh, indent=2, default=str)
        
        st.success(f"Project report saved to **{fname}**")
    
else:
    st.warning("Please ensure all data files are available and restart the application.")

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Dashboard** - Built with Streamlit")
