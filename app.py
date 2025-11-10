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
    .selection-card {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0f62fe;
        margin-bottom: 2rem;
    }
    .step-indicator {
        background-color: #0f62fe;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin-bottom: 1rem;
        display: inline-block;
    }
    .map-container {
        border: 2px solid #0f62fe;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .selection-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #054ADA;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">🌊 HYDROTRANSPARENT INSIGHT DASHBOARD</div>', unsafe_allow_html=True)
st.markdown("### Real-time Patterns, Trends & Anti-Corruption Impact")
st.markdown("---")

# Province-specific base data with detailed coordinates for rural areas
PROVINCE_BASE_DATA = {
    "Eastern Cape": {
        "water_stress": 0.75,
        "jobs_base": 420,
        "economic_base": 85,
        "water_access_base": 85,
        "coordinates": (-32.0833, 26.8833),
        "rainfall_factor": 1.2,
        "flow_factor": 0.9,
        "zoom_level": 7
    },
    "Free State": {
        "water_stress": 0.65,
        "jobs_base": 380,
        "economic_base": 75,
        "water_access_base": 80,
        "coordinates": (-28.4556, 26.7683),
        "rainfall_factor": 0.8,
        "flow_factor": 0.7,
        "zoom_level": 7
    },
    "Gauteng": {
        "water_stress": 0.85,
        "jobs_base": 500,
        "economic_base": 100,
        "water_access_base": 90,
        "coordinates": (-26.2044, 28.0456),
        "rainfall_factor": 0.9,
        "flow_factor": 0.6,
        "zoom_level": 8
    },
    "KwaZulu-Natal": {
        "water_stress": 0.70,
        "jobs_base": 450,
        "economic_base": 90,
        "water_access_base": 85,
        "coordinates": (-29.8587, 31.0218),
        "rainfall_factor": 1.4,
        "flow_factor": 1.2,
        "zoom_level": 7
    },
    "Limpopo": {
        "water_stress": 0.80,
        "jobs_base": 400,
        "economic_base": 80,
        "water_access_base": 80,
        "coordinates": (-23.4013, 29.4179),
        "rainfall_factor": 0.7,
        "flow_factor": 0.5,
        "zoom_level": 6
    },
    "Mpumalanga": {
        "water_stress": 0.72,
        "jobs_base": 420,
        "economic_base": 85,
        "water_access_base": 82,
        "coordinates": (-25.5653, 30.5279),
        "rainfall_factor": 1.1,
        "flow_factor": 1.0,
        "zoom_level": 7
    },
    "North West": {
        "water_stress": 0.68,
        "jobs_base": 380,
        "economic_base": 75,
        "water_access_base": 78,
        "coordinates": (-26.6639, 25.2838),
        "rainfall_factor": 0.6,
        "flow_factor": 0.4,
        "zoom_level": 7
    },
    "Northern Cape": {
        "water_stress": 0.90,
        "jobs_base": 350,
        "economic_base": 70,
        "water_access_base": 75,
        "coordinates": (-29.0467, 21.8569),
        "rainfall_factor": 0.4,
        "flow_factor": 0.3,
        "zoom_level": 5
    },
    "Western Cape": {
        "water_stress": 0.78,
        "jobs_base": 480,
        "economic_base": 95,
        "water_access_base": 88,
        "coordinates": (-33.9253, 18.4239),
        "rainfall_factor": 1.0,
        "flow_factor": 0.8,
        "zoom_level": 7
    }
}

# Detailed rural area coordinates within each province
RURAL_AREA_COORDINATES = {
    "Eastern Cape": {
        "Alice": (-32.7872, 26.8340),
        "Butterworth": (-32.3303, 28.1498),
        "Cradock": (-32.1642, 25.6192),
        "Graaff-Reinet": (-32.2521, 24.5308),
        "Lady Frere": (-31.7031, 27.2329)
    },
    "Free State": {
        "Bethlehem": (-28.2308, 28.3071),
        "Bothaville": (-27.3884, 26.6170),
        "Frankfort": (-27.2789, 28.4925),
        "Harrismith": (-28.2728, 29.1294),
        "Philippolis": (-30.2603, 25.2842)
    },
    "Gauteng": {
        "Bronkhorstspruit": (-25.8100, 28.7425),
        "Cullinan": (-25.6708, 28.5236),
        "Heidelberg": (-26.5048, 28.3592),
        "Randfontein": (-26.1844, 27.7023),
        "Soshanguve": (-25.4976, 28.1003)
    },
    "KwaZulu-Natal": {
        "Eshowe": (-28.8864, 31.4698),
        "Hluhluwe": (-28.0190, 32.2676),
        "Ixopo": (-30.1592, 30.0603),
        "Mtubatuba": (-28.4178, 32.1814),
        "Nkandla": (-28.6211, 31.0878)
    },
    "Limpopo": {
        "Alldays": (-22.6631, 29.0939),
        "Giyani": (-23.3167, 30.7167),
        "Lebowakgomo": (-24.2000, 29.5000),
        "Makhado": (-23.0500, 29.9000),
        "Tzaneen": (-23.8333, 30.1667)
    },
    "Mpumalanga": {
        "Barberton": (-25.7889, 31.0536),
        "Carolina": (-26.0667, 30.1167),
        "Ermelo": (-26.5333, 29.9833),
        "Hazyview": (-25.0500, 31.1333),
        "Pilgrim's Rest": (-24.9000, 30.7500)
    },
    "North West": {
        "Coligny": (-26.3333, 26.3167),
        "Ganyesa": (-26.5833, 24.1833),
        "Koster": (-25.8667, 26.9000),
        "Madikwe": (-25.3000, 26.3667),
        "Sannieshof": (-26.5333, 25.8167)
    },
    "Northern Cape": {
        "Barkly West": (-28.5333, 24.5167),
        "Calvinia": (-31.4667, 19.7667),
        "Kenhardt": (-29.3500, 21.1500),
        "Pofadder": (-29.1333, 19.3833),
        "Upington": (-28.4572, 21.2425)
    },
    "Western Cape": {
        "Barrydale": (-33.9000, 20.7333),
        "Caledon": (-34.2292, 19.4264),
        "Grabouw": (-34.1500, 19.0167),
        "Prince Albert": (-33.2247, 22.0308),
        "Tulbagh": (-33.2867, 19.1414)
    }
}

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = None
if 'selected_rural_area' not in st.session_state:
    st.session_state.selected_rural_area = None

# Data loading function
@st.cache_data
def load_data():
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
            
            datasets['service_levels'] = service_levels
        
        return (datasets.get('service_levels'), 
                datasets.get('esk2033'), 
                datasets.get('wash'), 
                datasets.get('dams'), 
                True)
        
    except Exception as e:
        return None, None, None, None, False

# Load data
with st.spinner("📊 Loading and processing datasets..."):
    try:
        service_levels, esk2033, wash, dams, success = load_data()
        if not success:
            # Create demo data
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
            service_levels = demo_service_levels
            success = True
        
        if success:
            st.session_state.data_loaded = True
    except Exception as e:
        st.session_state.data_loaded = False

# STEP 1: PROVINCE SELECTION
if st.session_state.current_step == 1:
    st.markdown('<div class="selection-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-indicator">Step 1: Select Province</div>', unsafe_allow_html=True)
    st.markdown("### 🗺️ Choose Your Province")
    st.markdown("Click on any province on the map below to select it, or use the dropdown menu.")
    
    # Two-column layout for selection options
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Select from List")
        selected_province = st.selectbox(
            "Choose Province:",
            options=list(PROVINCE_BASE_DATA.keys()),
            index=2,
            key="province_dropdown"
        )
        
        # Show province info when selected
        if selected_province:
            province_data = PROVINCE_BASE_DATA[selected_province]
            st.markdown('<div class="selection-info">', unsafe_allow_html=True)
            st.markdown(f"**Selected:** {selected_province}")
            st.markdown(f"**Water Stress:** {province_data['water_stress']*100:.1f}%")
            st.markdown(f"**Water Access:** {province_data['water_access_base']}%")
            st.markdown(f"**Rainfall Factor:** {province_data['rainfall_factor']:.1f}x")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("✅ Confirm Province Selection", type="primary", use_container_width=True):
                st.session_state.selected_province = selected_province
                st.session_state.current_step = 2
                st.rerun()
    
    with col2:
        st.markdown("#### 📊 Quick Stats")
        if selected_province:
            province_data = PROVINCE_BASE_DATA[selected_province]
            st.metric("Water Stress Level", f"{province_data['water_stress']*100:.1f}%")
            st.metric("Base Water Access", f"{province_data['water_access_base']}%")
            st.metric("Rainfall Factor", f"{province_data['rainfall_factor']:.1f}x")
            st.metric("Available Rural Areas", f"{len(RURAL_AREA_COORDINATES[selected_province])}")

    # Interactive Map for Province Selection
    st.markdown("### 🗺️ Interactive Province Map")
    st.markdown("**Click on any province marker to select it**")
    
    # Prepare map data
    province_coords = []
    for prov, data in PROVINCE_BASE_DATA.items():
        province_coords.append({
            'Province': prov,
            'Latitude': data['coordinates'][0],
            'Longitude': data['coordinates'][1],
            'Water_Stress': data['water_stress'],
            'Water_Access': data['water_access_base'],
            'Size': 20,
            'Color': 'red' if prov == selected_province else 'blue'
        })
    
    map_df = pd.DataFrame(province_coords)
    
    # Create interactive map
    fig_map = px.scatter_mapbox(
        map_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Province",
        hover_data={
            "Water_Stress": ":.2f",
            "Water_Access": True,
            "Latitude": False,
            "Longitude": False,
            "Color": False
        },
        color="Color",
        color_discrete_map={'red': 'red', 'blue': 'blue'},
        size="Size",
        size_max=15,
        zoom=5,
        height=500,
        title="Click on any province to select it"
    )
    
    # Update layout for better interactivity
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        clickmode='event+select'
    )
    
    # Add custom data for click events
    fig_map.update_traces(
        customdata=map_df['Province']
    )
    
    # Display the map
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Instructions
    st.info("💡 **Tip:** Click directly on province markers on the map to select them, or use the dropdown menu above.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: RURAL AREA SELECTION
elif st.session_state.current_step == 2 and st.session_state.selected_province:
    st.markdown('<div class="selection-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-indicator">Step 2: Select Rural Area</div>', unsafe_allow_html=True)
    st.markdown(f"### 🏞️ Choose Rural Area in {st.session_state.selected_province}")
    st.markdown("Select a specific rural area for detailed analysis. Click on the map or use the dropdown.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Select from List")
        rural_areas = list(RURAL_AREA_COORDINATES[st.session_state.selected_province].keys())
        selected_rural_area = st.selectbox(
            "Choose Rural Area:",
            options=rural_areas,
            key="rural_dropdown"
        )
        
        # Show rural area info
        if selected_rural_area:
            coords = RURAL_AREA_COORDINATES[st.session_state.selected_province][selected_rural_area]
            st.markdown('<div class="selection-info">', unsafe_allow_html=True)
            st.markdown(f"**Selected:** {selected_rural_area}")
            st.markdown(f"**Coordinates:** {coords[0]:.4f}°, {coords[1]:.4f}°")
            st.markdown(f"**Area Type:** Rural Settlement")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("← Back to Provinces", use_container_width=True):
                    st.session_state.current_step = 1
                    st.rerun()
            with col_btn2:
                if st.button("✅ View Dashboard", type="primary", use_container_width=True):
                    st.session_state.selected_rural_area = selected_rural_area
                    st.session_state.current_step = 3
                    st.rerun()
    
    with col2:
        st.markdown("#### 📍 Area Details")
        if selected_rural_area:
            coords = RURAL_AREA_COORDINATES[st.session_state.selected_province][selected_rural_area]
            st.metric("Latitude", f"{coords[0]:.4f}°")
            st.metric("Longitude", f"{coords[1]:.4f}°")
            st.metric("Province", st.session_state.selected_province)
            st.metric("Selection Method", "Map Click" if st.session_state.get('map_click', False) else "Dropdown")

    # Zoomed-in Map for Rural Area Selection
    st.markdown(f"### 🗺️ {st.session_state.selected_province} - Rural Areas")
    st.markdown("**Click on any rural area marker to select it**")
    
    province_data = PROVINCE_BASE_DATA[st.session_state.selected_province]
    rural_coords = []
    
    for rural_area, coords in RURAL_AREA_COORDINATES[st.session_state.selected_province].items():
        rural_coords.append({
            'Rural_Area': rural_area,
            'Latitude': coords[0],
            'Longitude': coords[1],
            'Size': 25 if rural_area == selected_rural_area else 15,
            'Color': 'red' if rural_area == selected_rural_area else 'green'
        })
    
    rural_df = pd.DataFrame(rural_coords)
    
    # Create zoomed-in map
    fig_rural_map = px.scatter_mapbox(
        rural_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Rural_Area",
        color="Color",
        color_discrete_map={'red': 'red', 'green': 'green'},
        size="Size",
        size_max=20,
        zoom=province_data["zoom_level"],
        height=500,
        title=f"Rural Areas in {st.session_state.selected_province} - Click to select"
    )
    
    # Add province center for reference
    fig_rural_map.add_trace(go.Scattermapbox(
        lat=[province_data['coordinates'][0]],
        lon=[province_data['coordinates'][1]],
        mode='markers',
        marker=dict(size=12, color='orange'),
        name='Province Center',
        hovertext='Province Center',
        hoverinfo='text'
    ))
    
    fig_rural_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        showlegend=True
    )
    
    # Add custom data for click events
    fig_rural_map.update_traces(
        customdata=rural_df['Rural_Area']
    )
    
    st.plotly_chart(fig_rural_map, use_container_width=True)
    
    st.info(f"💡 **Exploring {st.session_state.selected_province}:** {len(rural_areas)} rural areas available for analysis.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3: MAIN DASHBOARD
elif st.session_state.current_step == 3 and st.session_state.selected_province and st.session_state.selected_rural_area:
    
    # Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("← Back to Area Selection"):
            st.session_state.current_step = 2
            st.rerun()
    
    with col_nav2:
        st.markdown(f"### 📍 Currently Viewing: {st.session_state.selected_rural_area}, {st.session_state.selected_province}")
    
    # Main dashboard content
    province = st.session_state.selected_province
    rural_area = st.session_state.selected_rural_area
    
    # Sidebar for project configuration
    st.sidebar.markdown("## 🎛️ Project Configuration")
    st.sidebar.markdown(f"**Selected Area:** {rural_area}, {province}")
    
    project_scale = st.sidebar.selectbox("Project scale:", ["Small", "Medium", "Large", "Enterprise"], index=1)
    soil_type = st.sidebar.selectbox("Soil type:", ["Clay", "Sandy", "Loamy", "Rocky"], index=2)
    catchment_area = st.sidebar.slider("Catchment km²", 50, 300, 150)
    rainfall = st.sidebar.slider("Rainfall mm/day", 10, 100, 45)
    evaporation = st.sidebar.slider("Evaporation mm/day", 0, 20, 6)
    
    # Executive Summary with focused map
    st.markdown("### 🗺️ Selected Area Overview")
    
    province_coords = PROVINCE_BASE_DATA[province]['coordinates']
    rural_coords = RURAL_AREA_COORDINATES[province][rural_area]
    
    # Create highly focused map
    focused_data = pd.DataFrame([{
        'Location': rural_area,
        'Latitude': rural_coords[0],
        'Longitude': rural_coords[1],
        'Type': 'Selected Rural Area',
        'Size': 30,
        'Color': 'red'
    }, {
        'Location': f'{province} Center',
        'Latitude': province_coords[0],
        'Longitude': province_coords[1],
        'Type': 'Province Center',
        'Size': 15,
        'Color': 'orange'
    }])
    
    fig_focused_map = px.scatter_mapbox(
        focused_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Location",
        color="Color",
        color_discrete_map={'red': 'red', 'orange': 'orange'},
        size="Size",
        size_max=25,
        zoom=10,  # Very zoomed in
        height=400,
        title=f"Detailed View: {rural_area}, {province}"
    )
    
    fig_focused_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        showlegend=True
    )
    
    st.plotly_chart(fig_focused_map, use_container_width=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Province Water Stress", f"{PROVINCE_BASE_DATA[province]['water_stress']*100:.1f}%")
    with col2:
        st.metric("Rainfall Factor", f"{PROVINCE_BASE_DATA[province]['rainfall_factor']:.1f}x")
    with col3:
        st.metric("Area Coordinates", f"{rural_coords[0]:.3f}°")
    with col4:
        st.metric("", f"{rural_coords[1]:.3f}°")
    
    # Placeholder for dashboard content
    st.markdown("### 📊 Analytics Dashboard")
    st.info("🚧 Full analytics and visualizations would load here based on the selected area...")
    
    # Demo content
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Population", "15,250")
        st.metric("Water Access Rate", f"{PROVINCE_BASE_DATA[province]['water_access_base']}%")
    with col2:
        st.metric("Infrastructure Score", "72/100")
        st.metric("Project Readiness", "High")

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Dashboard** - Built with Streamlit | Interactive Map Selection")
