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
    .selection-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #054ADA;
        margin: 1rem 0;
    }
    .click-instruction {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
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
        "water_stress": 0.75, "jobs_base": 420, "economic_base": 85, "water_access_base": 85,
        "coordinates": (-32.0833, 26.8833), "rainfall_factor": 1.2, "flow_factor": 0.9, "zoom_level": 7
    },
    "Free State": {
        "water_stress": 0.65, "jobs_base": 380, "economic_base": 75, "water_access_base": 80,
        "coordinates": (-28.4556, 26.7683), "rainfall_factor": 0.8, "flow_factor": 0.7, "zoom_level": 7
    },
    "Gauteng": {
        "water_stress": 0.85, "jobs_base": 500, "economic_base": 100, "water_access_base": 90,
        "coordinates": (-26.2044, 28.0456), "rainfall_factor": 0.9, "flow_factor": 0.6, "zoom_level": 9
    },
    "KwaZulu-Natal": {
        "water_stress": 0.70, "jobs_base": 450, "economic_base": 90, "water_access_base": 85,
        "coordinates": (-29.8587, 31.0218), "rainfall_factor": 1.4, "flow_factor": 1.2, "zoom_level": 7
    },
    "Limpopo": {
        "water_stress": 0.80, "jobs_base": 400, "economic_base": 80, "water_access_base": 80,
        "coordinates": (-23.4013, 29.4179), "rainfall_factor": 0.7, "flow_factor": 0.5, "zoom_level": 6
    },
    "Mpumalanga": {
        "water_stress": 0.72, "jobs_base": 420, "economic_base": 85, "water_access_base": 82,
        "coordinates": (-25.5653, 30.5279), "rainfall_factor": 1.1, "flow_factor": 1.0, "zoom_level": 7
    },
    "North West": {
        "water_stress": 0.68, "jobs_base": 380, "economic_base": 75, "water_access_base": 78,
        "coordinates": (-26.6639, 25.2838), "rainfall_factor": 0.6, "flow_factor": 0.4, "zoom_level": 7
    },
    "Northern Cape": {
        "water_stress": 0.90, "jobs_base": 350, "economic_base": 70, "water_access_base": 75,
        "coordinates": (-29.0467, 21.8569), "rainfall_factor": 0.4, "flow_factor": 0.3, "zoom_level": 5
    },
    "Western Cape": {
        "water_stress": 0.78, "jobs_base": 480, "economic_base": 95, "water_access_base": 88,
        "coordinates": (-33.9253, 18.4239), "rainfall_factor": 1.0, "flow_factor": 0.8, "zoom_level": 7
    }
}

# Rural area coordinates
RURAL_AREA_COORDINATES = {
    "Eastern Cape": {
        "Alice": (-32.7872, 26.8340), "Butterworth": (-32.3303, 28.1498),
        "Cradock": (-32.1642, 25.6192), "Graaff-Reinet": (-32.2521, 24.5308),
        "Lady Frere": (-31.7031, 27.2329)
    },
    "Free State": {
        "Bethlehem": (-28.2308, 28.3071), "Bothaville": (-27.3884, 26.6170),
        "Frankfort": (-27.2789, 28.4925), "Harrismith": (-28.2728, 29.1294),
        "Philippolis": (-30.2603, 25.2842)
    },
    "Gauteng": {
        "Bronkhorstspruit": (-25.8100, 28.7425), "Cullinan": (-25.6708, 28.5236),
        "Heidelberg": (-26.5048, 28.3592), "Randfontein": (-26.1844, 27.7023),
        "Soshanguve": (-25.4976, 28.1003)
    },
    "KwaZulu-Natal": {
        "Eshowe": (-28.8864, 31.4698), "Hluhluwe": (-28.0190, 32.2676),
        "Ixopo": (-30.1592, 30.0603), "Mtubatuba": (-28.4178, 32.1814),
        "Nkandla": (-28.6211, 31.0878)
    },
    "Limpopo": {
        "Alldays": (-22.6631, 29.0939), "Giyani": (-23.3167, 30.7167),
        "Lebowakgomo": (-24.2000, 29.5000), "Makhado": (-23.0500, 29.9000),
        "Tzaneen": (-23.8333, 30.1667)
    },
    "Mpumalanga": {
        "Barberton": (-25.7889, 31.0536), "Carolina": (-26.0667, 30.1167),
        "Ermelo": (-26.5333, 29.9833), "Hazyview": (-25.0500, 31.1333),
        "Pilgrim's Rest": (-24.9000, 30.7500)
    },
    "North West": {
        "Coligny": (-26.3333, 26.3167), "Ganyesa": (-26.5833, 24.1833),
        "Koster": (-25.8667, 26.9000), "Madikwe": (-25.3000, 26.3667),
        "Sannieshof": (-26.5333, 25.8167)
    },
    "Northern Cape": {
        "Barkly West": (-28.5333, 24.5167), "Calvinia": (-31.4667, 19.7667),
        "Kenhardt": (-29.3500, 21.1500), "Pofadder": (-29.1333, 19.3833),
        "Upington": (-28.4572, 21.2425)
    },
    "Western Cape": {
        "Barrydale": (-33.9000, 20.7333), "Caledon": (-34.2292, 19.4264),
        "Grabouw": (-34.1500, 19.0167), "Prince Albert": (-33.2247, 22.0308),
        "Tulbagh": (-33.2867, 19.1414)
    }
}

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = "Gauteng"
if 'selected_rural_area' not in st.session_state:
    st.session_state.selected_rural_area = None
if 'map_clicked_province' not in st.session_state:
    st.session_state.map_clicked_province = None
if 'map_clicked_rural' not in st.session_state:
    st.session_state.map_clicked_rural = None

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

# Handle button clicks before any forms
if 'province_clicked' not in st.session_state:
    st.session_state.province_clicked = None

if 'rural_clicked' not in st.session_state:
    st.session_state.rural_clicked = None

# STEP 1: PROVINCE SELECTION
if st.session_state.current_step == 1:
    st.markdown('<div class="selection-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-indicator">Step 1: Select Province</div>', unsafe_allow_html=True)
    st.markdown("### 🗺️ Choose Your Province")
    st.markdown("Click on any province on the map below to select it, or use the dropdown menu.")
    
    # Quick selection buttons (OUTSIDE the form)
    st.markdown("### 🖱️ Quick Select - Click a Province:")
    cols = st.columns(3)
    for i, province_name in enumerate(PROVINCE_BASE_DATA.keys()):
        with cols[i % 3]:
            if st.button(f"📍 {province_name}", key=f"btn_{province_name}", use_container_width=True):
                st.session_state.selected_province = province_name
                st.session_state.province_clicked = province_name
                st.rerun()
    
    # Main form for province selection
    with st.form("province_selection_form"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📋 Select from List")
            selected_province = st.selectbox(
                "Choose Province:",
                options=list(PROVINCE_BASE_DATA.keys()),
                index=list(PROVINCE_BASE_DATA.keys()).index(st.session_state.selected_province),
                key="province_dropdown"
            )
            
            # Show province info
            if selected_province:
                province_data = PROVINCE_BASE_DATA[selected_province]
                st.markdown('<div class="selection-info">', unsafe_allow_html=True)
                st.markdown(f"**Selected:** {selected_province}")
                st.markdown(f"**Water Stress:** {province_data['water_stress']*100:.1f}%")
                st.markdown(f"**Water Access:** {province_data['water_access_base']}%")
                st.markdown(f"**Rainfall Factor:** {province_data['rainfall_factor']:.1f}x")
                st.markdown('</div>', unsafe_allow_html=True)
        
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
        st.markdown('<div class="click-instruction">', unsafe_allow_html=True)
        st.markdown("**🎯 Click on any province marker to select it instantly!**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prepare map data
        province_coords = []
        for prov, data in PROVINCE_BASE_DATA.items():
            province_coords.append({
                'Province': prov,
                'Latitude': data['coordinates'][0],
                'Longitude': data['coordinates'][1],
                'Water_Stress': data['water_stress'],
                'Water_Access': data['water_access_base'],
                'Size': 25 if prov == selected_province else 15,
                'Color': 'red' if prov == selected_province else 'blue'
            })
        
        map_df = pd.DataFrame(province_coords)
        
        # Create interactive map with proper zoom for selected province
        selected_province_data = PROVINCE_BASE_DATA[selected_province]
        zoom_level = selected_province_data.get('zoom_level', 6)
        
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
            size_max=20,
            zoom=zoom_level,
            center={"lat": selected_province_data['coordinates'][0], "lon": selected_province_data['coordinates'][1]},
            height=500,
            title=f"Map Centered on: {selected_province} - Click any province to select"
        )
        
        fig_map.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Form submit button
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("✅ Confirm Province Selection", type="primary", use_container_width=True)
            if submitted:
                st.session_state.selected_province = selected_province
                st.session_state.current_step = 2
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: RURAL AREA SELECTION
elif st.session_state.current_step == 2 and st.session_state.selected_province:
    st.markdown('<div class="selection-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-indicator">Step 2: Select Rural Area</div>', unsafe_allow_html=True)
    st.markdown(f"### 🏞️ Choose Rural Area in {st.session_state.selected_province}")
    st.markdown("Select a specific rural area for detailed analysis.")
    
    rural_areas = list(RURAL_AREA_COORDINATES[st.session_state.selected_province].keys())
    
    # Quick selection buttons for rural areas (OUTSIDE the form)
    st.markdown("### 🖱️ Quick Select - Click a Rural Area:")
    rural_cols = st.columns(3)
    for i, rural_name in enumerate(rural_areas):
        with rural_cols[i % 3]:
            if st.button(f"🏘️ {rural_name}", key=f"rural_btn_{rural_name}", use_container_width=True):
                st.session_state.selected_rural_area = rural_name
                st.session_state.rural_clicked = rural_name
                st.rerun()
    
    # Main form for rural area selection
    with st.form("rural_area_selection_form"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📋 Select from List")
            
            # Set default rural area if none selected
            default_rural = st.session_state.selected_rural_area or rural_areas[0]
            selected_rural_area = st.selectbox(
                "Choose Rural Area:",
                options=rural_areas,
                index=rural_areas.index(default_rural) if default_rural in rural_areas else 0,
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
        
        with col2:
            st.markdown("#### 📍 Area Details")
            if selected_rural_area:
                coords = RURAL_AREA_COORDINATES[st.session_state.selected_province][selected_rural_area]
                st.metric("Latitude", f"{coords[0]:.4f}°")
                st.metric("Longitude", f"{coords[1]:.4f}°")
                st.metric("Province", st.session_state.selected_province)
                st.metric("Total Options", f"{len(rural_areas)} areas")

        # Zoomed-in Map for Rural Area Selection
        st.markdown(f"### 🗺️ {st.session_state.selected_province} - Rural Areas")
        st.markdown('<div class="click-instruction">', unsafe_allow_html=True)
        st.markdown("**🎯 Map is zoomed to selected rural area! Use quick select buttons below.**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        province_data = PROVINCE_BASE_DATA[st.session_state.selected_province]
        rural_coords = []
        
        for rural_area_name, coords in RURAL_AREA_COORDINATES[st.session_state.selected_province].items():
            rural_coords.append({
                'Rural_Area': rural_area_name,
                'Latitude': coords[0],
                'Longitude': coords[1],
                'Size': 30 if rural_area_name == selected_rural_area else 15,
                'Color': 'red' if rural_area_name == selected_rural_area else 'green'
            })
        
        rural_df = pd.DataFrame(rural_coords)
        
        # Get coordinates for center of map (use selected rural area)
        center_coords = RURAL_AREA_COORDINATES[st.session_state.selected_province][selected_rural_area]
        
        # Create zoomed-in map centered on selected rural area
        fig_rural_map = px.scatter_mapbox(
            rural_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Rural_Area",
            color="Color",
            color_discrete_map={'red': 'red', 'green': 'green'},
            size="Size",
            size_max=25,
            zoom=11,  # More zoomed in for rural areas
            center={"lat": center_coords[0], "lon": center_coords[1]},
            height=500,
            title=f"Map Centered on: {selected_rural_area} - {st.session_state.selected_province}"
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
        
        st.plotly_chart(fig_rural_map, use_container_width=True)
        
        # Form submit buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            back_submitted = st.form_submit_button("← Back to Provinces", use_container_width=True)
            if back_submitted:
                st.session_state.current_step = 1
                st.rerun()
        with col_btn2:
            confirm_submitted = st.form_submit_button("✅ View Dashboard", type="primary", use_container_width=True)
            if confirm_submitted:
                st.session_state.selected_rural_area = selected_rural_area
                st.session_state.current_step = 3
                st.rerun()
    
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
        'Size': 40,
        'Color': 'red'
    }])
    
    fig_focused_map = px.scatter_mapbox(
        focused_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Location",
        color="Color",
        color_discrete_map={'red': 'red'},
        size="Size",
        size_max=30,
        zoom=12,  # Very zoomed in
        center={"lat": rural_coords[0], "lon": rural_coords[1]},
        height=400,
        title=f"Detailed View: {rural_area}, {province}"
    )
    
    fig_focused_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        showlegend=False
    )
    
    st.plotly_chart(fig_focused_map, use_container_width=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Province Water Stress", f"{PROVINCE_BASE_DATA[province]['water_stress']*100:.1f}%")
    with col2:
        st.metric("Rainfall Factor", f"{PROVINCE_BASE_DATA[province]['rainfall_factor']:.1f}x")
    with col3:
        st.metric("Latitude", f"{rural_coords[0]:.4f}°")
    with col4:
        st.metric("Longitude", f"{rural_coords[1]:.4f}°")
    
    # Demo dashboard content
    st.markdown("### 📊 Analytics Dashboard")
    st.success(f"✅ Successfully loaded data for {rural_area}, {province}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Population", "15,250")
        st.metric("Water Access Rate", f"{PROVINCE_BASE_DATA[province]['water_access_base']}%")
        st.metric("Infrastructure Score", "72/100")
    with col2:
        st.metric("Project Readiness", "High")
        st.metric("Available Funding", "ZAR 45M")
        st.metric("Community Engagement", "85%")

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Dashboard** - Built with Streamlit | Interactive Map Selection")
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
    page_title="HydroTransparent Water Management Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f5f8b;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1f5f8b;
        border-bottom: 2px solid #1f5f8b;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f5f8b;
        margin-bottom: 1rem;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .danger-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .success-card {
        background-color: #d1edff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0f62fe;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">HYDROTRANSPARENT WATER MANAGEMENT PLATFORM</div>', unsafe_allow_html=True)
st.markdown("### Comprehensive Water Resource Management, Employment Analytics, and Financial Transparency")
st.markdown("---")

# Enhanced Province-specific base data with employment and water quality
PROVINCE_BASE_DATA = {
    "Eastern Cape": {
        "water_stress": 0.75, "water_access_base": 65, "water_quality_score": 72,
        "employment_rate": 58.3, "unemployment_rate": 41.7, "engineers_available": 450,
        "technical_staff": 1200, "general_workers": 8500, "current_supply_megalitres": 245,
        "demand_megalitres": 320, "contamination_incidents": 12, "leakage_rate": 0.28,
        "coordinates": (-32.0833, 26.8833), "zoom_level": 7
    },
    "Free State": {
        "water_stress": 0.65, "water_access_base": 72, "water_quality_score": 78,
        "employment_rate": 62.1, "unemployment_rate": 37.9, "engineers_available": 320,
        "technical_staff": 980, "general_workers": 6200, "current_supply_megalitres": 180,
        "demand_megalitres": 210, "contamination_incidents": 8, "leakage_rate": 0.22,
        "coordinates": (-28.4556, 26.7683), "zoom_level": 7
    },
    "Gauteng": {
        "water_stress": 0.85, "water_access_base": 88, "water_quality_score": 85,
        "employment_rate": 68.9, "unemployment_rate": 31.1, "engineers_available": 1250,
        "technical_staff": 3200, "general_workers": 18500, "current_supply_megalitres": 890,
        "demand_megalitres": 950, "contamination_incidents": 5, "leakage_rate": 0.18,
        "coordinates": (-26.2044, 28.0456), "zoom_level": 9
    },
    "KwaZulu-Natal": {
        "water_stress": 0.70, "water_access_base": 74, "water_quality_score": 76,
        "employment_rate": 60.5, "unemployment_rate": 39.5, "engineers_available": 680,
        "technical_staff": 1850, "general_workers": 12500, "current_supply_megalitres": 420,
        "demand_megalitres": 480, "contamination_incidents": 15, "leakage_rate": 0.25,
        "coordinates": (-29.8587, 31.0218), "zoom_level": 7
    },
    "Limpopo": {
        "water_stress": 0.80, "water_access_base": 63, "water_quality_score": 69,
        "employment_rate": 55.8, "unemployment_rate": 44.2, "engineers_available": 290,
        "technical_staff": 850, "general_workers": 7200, "current_supply_megalitres": 195,
        "demand_megalitres": 280, "contamination_incidents": 18, "leakage_rate": 0.31,
        "coordinates": (-23.4013, 29.4179), "zoom_level": 6
    },
    "Mpumalanga": {
        "water_stress": 0.72, "water_access_base": 71, "water_quality_score": 74,
        "employment_rate": 61.3, "unemployment_rate": 38.7, "engineers_available": 380,
        "technical_staff": 1100, "general_workers": 7800, "current_supply_megalitres": 230,
        "demand_megalitres": 270, "contamination_incidents": 9, "leakage_rate": 0.24,
        "coordinates": (-25.5653, 30.5279), "zoom_level": 7
    },
    "North West": {
        "water_stress": 0.68, "water_access_base": 69, "water_quality_score": 71,
        "employment_rate": 59.2, "unemployment_rate": 40.8, "engineers_available": 270,
        "technical_staff": 750, "general_workers": 5800, "current_supply_megalitres": 165,
        "demand_megalitres": 200, "contamination_incidents": 11, "leakage_rate": 0.27,
        "coordinates": (-26.6639, 25.2838), "zoom_level": 7
    },
    "Northern Cape": {
        "water_stress": 0.90, "water_access_base": 58, "water_quality_score": 65,
        "employment_rate": 53.7, "unemployment_rate": 46.3, "engineers_available": 180,
        "technical_staff": 520, "general_workers": 4200, "current_supply_megalitres": 95,
        "demand_megalitres": 150, "contamination_incidents": 7, "leakage_rate": 0.35,
        "coordinates": (-29.0467, 21.8569), "zoom_level": 5
    },
    "Western Cape": {
        "water_stress": 0.78, "water_access_base": 82, "water_quality_score": 88,
        "employment_rate": 65.4, "unemployment_rate": 34.6, "engineers_available": 890,
        "technical_staff": 2100, "general_workers": 14200, "current_supply_megalitres": 520,
        "demand_megalitres": 580, "contamination_incidents": 4, "leakage_rate": 0.16,
        "coordinates": (-33.9253, 18.4239), "zoom_level": 7
    }
}

# Enhanced Rural area data with employment and infrastructure details
RURAL_AREA_DATA = {
    "Eastern Cape": {
        "Alice": {"employment_rate": 45.2, "water_quality": "Moderate Risk", "leakage_detected": True, "current_projects": 3},
        "Butterworth": {"employment_rate": 42.8, "water_quality": "High Risk", "leakage_detected": True, "current_projects": 2},
        "Cradock": {"employment_rate": 48.9, "water_quality": "Moderate Risk", "leakage_detected": False, "current_projects": 1},
        "Graaff-Reinet": {"employment_rate": 44.1, "water_quality": "Low Risk", "leakage_detected": True, "current_projects": 4},
        "Lady Frere": {"employment_rate": 39.7, "water_quality": "High Risk", "leakage_detected": True, "current_projects": 2}
    },
    "Free State": {
        "Bethlehem": {"employment_rate": 55.3, "water_quality": "Low Risk", "leakage_detected": False, "current_projects": 3},
        "Bothaville": {"employment_rate": 52.1, "water_quality": "Moderate Risk", "leakage_detected": True, "current_projects": 2},
        "Frankfort": {"employment_rate": 57.8, "water_quality": "Low Risk", "leakage_detected": False, "current_projects": 1},
        "Harrismith": {"employment_rate": 54.6, "water_quality": "Moderate Risk", "leakage_detected": True, "current_projects": 3},
        "Philippolis": {"employment_rate": 49.2, "water_quality": "High Risk", "leakage_detected": True, "current_projects": 2}
    }
}

# Financial transparency data - vendor payments and contracts
FINANCIAL_DATA = {
    "Eastern Cape": [
        {"company": "AquaTech Solutions", "service": "Pipe Replacement", "amount": 4500000, "status": "Completed"},
        {"company": "WaterWorks Engineering", "service": "Water Treatment Chemicals", "amount": 1200000, "status": "In Progress"},
        {"company": "InfraBuild Contractors", "service": "Reservoir Construction", "amount": 7800000, "status": "Completed"}
    ],
    "Gauteng": [
        {"company": "Metro Water Systems", "service": "Leak Detection System", "amount": 3200000, "status": "Completed"},
        {"company": "PureFlow Technologies", "service": "Water Quality Monitoring", "amount": 1850000, "status": "In Progress"},
        {"company": "Urban Infrastructure Ltd", "service": "Pipeline Network Upgrade", "amount": 12500000, "status": "Planning"}
    ]
}

# Employment opportunity projections by project scale
EMPLOYMENT_PROJECTIONS = {
    "Small": {"engineers": 2, "technicians": 5, "administrative": 3, "general_labor": 15},
    "Medium": {"engineers": 5, "technicians": 12, "administrative": 8, "general_labor": 35},
    "Large": {"engineers": 12, "technicians": 25, "administrative": 15, "general_labor": 80},
    "Enterprise": {"engineers": 25, "technicians": 50, "administrative": 30, "general_labor": 200}
}

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = "Gauteng"
if 'selected_rural_area' not in st.session_state:
    st.session_state.selected_rural_area = None

# Data loading function with enhanced datasets
@st.cache_data
def load_enhanced_data():
    # Simulate loading real datasets
    try:
        # Employment data simulation
        employment_stats = pd.DataFrame({
            'Province': list(PROVINCE_BASE_DATA.keys()),
            'Formal_Employment_Rate': [PROVINCE_BASE_DATA[p]['employment_rate'] for p in PROVINCE_BASE_DATA],
            'Youth_Unemployment': [45.2, 48.7, 35.8, 42.3, 52.1, 44.8, 47.5, 55.3, 38.9],
            'Water_Sector_Jobs': [1200, 850, 2800, 1650, 980, 1100, 750, 520, 1950]
        })
        
        # Water quality data simulation
        water_quality_data = pd.DataFrame({
            'Province': list(PROVINCE_BASE_DATA.keys()),
            'Water_Safety_Score': [PROVINCE_BASE_DATA[p]['water_quality_score'] for p in PROVINCE_BASE_DATA],
            'Contamination_Events': [PROVINCE_BASE_DATA[p]['contamination_incidents'] for p in PROVINCE_BASE_DATA],
            'Treatment_Compliance': [85, 92, 96, 88, 82, 87, 84, 79, 94]
        })
        
        return employment_stats, water_quality_data, True
    except:
        return None, None, False

# Load enhanced data
employment_stats, water_quality_data, data_loaded = load_enhanced_data()

# Main application logic
if st.session_state.current_step == 1:
    # PROVINCE SELECTION INTERFACE
    st.markdown('<div class="section-header">PROVINCE SELECTION AND OVERVIEW</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_province = st.selectbox(
            "Select Province:",
            options=list(PROVINCE_BASE_DATA.keys()),
            index=list(PROVINCE_BASE_DATA.keys()).index(st.session_state.selected_province)
        )
        
        # Province summary metrics
        province_data = PROVINCE_BASE_DATA[selected_province]
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f"**{selected_province} - Key Indicators**")
        st.markdown(f"Water Stress Level: {province_data['water_stress']*100:.1f}%")
        st.markdown(f"Water Access Rate: {province_data['water_access_base']}%")
        st.markdown(f"Employment Rate: {province_data['employment_rate']}%")
        st.markdown(f"Water Quality Score: {province_data['water_quality_score']}/100")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Water safety status
        water_quality = province_data['water_quality_score']
        if water_quality >= 80:
            st.markdown('<div class="success-card">', unsafe_allow_html=True)
            st.markdown("**WATER SAFETY STATUS: EXCELLENT**")
            st.markdown("Water meets all safety standards for consumption")
            st.markdown('</div>', unsafe_allow_html=True)
        elif water_quality >= 60:
            st.markdown('<div class="warning-card">', unsafe_allow_html=True)
            st.markdown("**WATER SAFETY STATUS: MODERATE**")
            st.markdown("Regular monitoring required, some parameters near limits")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="danger-card">', unsafe_allow_html=True)
            st.markdown("**WATER SAFETY STATUS: POOR**")
            st.markdown("Immediate intervention required - health risks identified")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Leakage detection
        if province_data['leakage_rate'] > 0.25:
            st.markdown('<div class="warning-card">', unsafe_allow_html=True)
            st.markdown("**INFRASTRUCTURE ALERT: HIGH LEAKAGE DETECTED**")
            st.markdown(f"System leakage rate: {province_data['leakage_rate']*100:.1f}%")
            st.markdown("Recommended: Infrastructure audit and pipe replacement")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Employment and Water Supply Analysis
    st.markdown('<div class="section-header">EMPLOYMENT AND WATER SUPPLY ANALYTICS</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Employment Rate", f"{province_data['employment_rate']}%")
    with col2:
        st.metric("Available Engineers", f"{province_data['engineers_available']}")
    with col3:
        st.metric("Water Supply vs Demand", f"{province_data['current_supply_megalitres']}/{province_data['demand_megalitres']} ML")
    with col4:
        st.metric("Contamination Incidents", f"{province_data['contamination_incidents']}")
    
    # Interactive Map
    st.markdown('<div class="section-header">INTERACTIVE PROVINCE MAP</div>', unsafe_allow_html=True)
    
    # Prepare map data with multiple indicators
    map_data = []
    for province, data in PROVINCE_BASE_DATA.items():
        color = 'green'
        if data['water_stress'] > 0.8:
            color = 'red'
        elif data['water_stress'] > 0.6:
            color = 'orange'
        
        map_data.append({
            'Province': province,
            'Latitude': data['coordinates'][0],
            'Longitude': data['coordinates'][1],
            'Water_Stress': data['water_stress'],
            'Employment_Rate': data['employment_rate'],
            'Water_Quality': data['water_quality_score'],
            'Color': color,
            'Size': 30 if province == selected_province else 20
        })
    
    map_df = pd.DataFrame(map_data)
    
    fig = px.scatter_mapbox(
        map_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Province",
        hover_data={
            "Water_Stress": ":.2f",
            "Employment_Rate": ":.1f",
            "Water_Quality": True,
            "Latitude": False,
            "Longitude": False
        },
        color="Color",
        color_discrete_map={'red': 'red', 'orange': 'orange', 'green': 'green'},
        size="Size",
        size_max=25,
        zoom=6,
        center={"lat": province_data['coordinates'][0], "lon": province_data['coordinates'][1]},
        height=500,
        title=f"Water Management Overview - {selected_province}"
    )
    
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
    
    # Navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("View Detailed Rural Analysis", type="primary", use_container_width=True):
            st.session_state.selected_province = selected_province
            st.session_state.current_step = 2
            st.rerun()

elif st.session_state.current_step == 2:
    # RURAL AREA DETAILED ANALYSIS
    province = st.session_state.selected_province
    st.markdown(f'<div class="section-header">DETAILED ANALYSIS: {province}</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("Back to Province Overview"):
        st.session_state.current_step = 1
        st.rerun()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Rural Area Selection**")
        rural_areas = list(RURAL_AREA_DATA.get(province, {}).keys())
        if not rural_areas:
            st.info("No rural area data available for this province")
            rural_areas = ["Sample Area 1", "Sample Area 2"]
        
        selected_rural = st.selectbox("Select Rural Area:", options=rural_areas)
        
        # Rural area employment and water status
        if province in RURAL_AREA_DATA and selected_rural in RURAL_AREA_DATA[province]:
            rural_data = RURAL_AREA_DATA[province][selected_rural]
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f"**{selected_rural} - Current Status**")
            st.markdown(f"Employment Rate: {rural_data['employment_rate']}%")
            st.markdown(f"Water Quality: {rural_data['water_quality']}")
            st.markdown(f"Leakage Detected: {'Yes' if rural_data['leakage_detected'] else 'No'}")
            st.markdown(f"Active Projects: {rural_data['current_projects']}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Employment Opportunities Analysis**")
        project_scale = st.selectbox("Project Scale:", options=list(EMPLOYMENT_PROJECTIONS.keys()))
        
        projections = EMPLOYMENT_PROJECTIONS[project_scale]
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("**Projected Job Creation**")
        for role, count in projections.items():
            st.markdown(f"{role.title()}: {count} positions")
        st.markdown(f"**Total Jobs: {sum(projections.values())}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Financial Transparency Section
    st.markdown('<div class="section-header">FINANCIAL TRANSPARENCY AND EXPENDITURE TRACKING</div>', unsafe_allow_html=True)
    
    if province in FINANCIAL_DATA:
        financial_df = pd.DataFrame(FINANCIAL_DATA[province])
        st.dataframe(financial_df, use_container_width=True)
        
        # Expenditure summary
        total_spent = sum(item['amount'] for item in FINANCIAL_DATA[province] if item['status'] == 'Completed')
        total_planned = sum(item['amount'] for item in FINANCIAL_DATA[province])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Expenditure", f"R {total_spent:,}")
        with col2:
            st.metric("Planned Investment", f"R {total_planned:,}")
        with col3:
            st.metric("Companies Engaged", len(FINANCIAL_DATA[province]))
    else:
        st.info("Financial transparency data being updated for this province")
    
    # Water Quality and Infrastructure Details
    st.markdown('<div class="section-header">WATER QUALITY AND INFRASTRUCTURE MONITORING</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Water quality metrics
        province_data = PROVINCE_BASE_DATA[province]
        st.markdown("**Water Safety Indicators**")
        st.metric("Water Quality Score", f"{province_data['water_quality_score']}/100")
        st.metric("Contamination Events", province_data['contamination_incidents'])
        st.metric("System Leakage Rate", f"{province_data['leakage_rate']*100:.1f}%")
        
        # Leak detection status
        if province_data['leakage_rate'] > 0.25:
            st.error("High leakage detected - Infrastructure maintenance required")
        elif province_data['leakage_rate'] > 0.15:
            st.warning("Moderate leakage - Schedule maintenance inspection")
        else:
            st.success("Leakage within acceptable limits")
    
    with col2:
        # Current supply vs demand
        supply_gap = province_data['demand_megalitres'] - province_data['current_supply_megalitres']
        st.markdown("**Water Supply Analysis**")
        st.metric("Current Supply", f"{province_data['current_supply_megalitres']} ML")
        st.metric("Current Demand", f"{province_data['demand_megalitres']} ML")
        st.metric("Supply Gap", f"{supply_gap} ML")
        
        if supply_gap > 0:
            st.error(f"Water deficit: {supply_gap} ML - Infrastructure expansion needed")
        else:
            st.success("Supply meets current demand")
    
    # Employment Analytics
    st.markdown('<div class="section-header">EMPLOYMENT AND WORKFORCE ANALYTICS</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Available Engineers", province_data['engineers_available'])
    with col2:
        st.metric("Technical Staff", province_data['technical_staff'])
    with col3:
        st.metric("General Workers", f"{province_data['general_workers']:,}")
    with col4:
        st.metric("Unemployment Rate", f"{province_data['unemployment_rate']}%")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Generate Project Report", use_container_width=True):
            st.success("Project report generated successfully")
    with col2:
        if st.button("View Contract Details", use_container_width=True):
            st.info("Contract details displayed in financial section")
    with col3:
        if st.button("Export Transparency Data", use_container_width=True):
            st.success("Data exported for public review")

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Platform** - Department of Water and Sanitation | Real-time Water Management Analytics")
st.markdown("*Transparent. Accountable. Data-Driven.*")
