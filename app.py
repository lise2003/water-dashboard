import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration FIRST
st.set_page_config(
    page_title="HydroTransparent Water Management Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = "Gauteng"
if 'selected_rural_area' not in st.session_state:
    st.session_state.selected_rural_area = None

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

# Title and description - ALWAYS SHOW
st.markdown('<div class="main-header">HYDROTRANSPARENT WATER MANAGEMENT PLATFORM</div>', unsafe_allow_html=True)
st.markdown("### Comprehensive Water Resource Management, Employment Analytics, and Financial Transparency")
st.markdown("---")

# Enhanced Province-specific base data
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

# Enhanced Rural area data
RURAL_AREA_DATA = {
    "Eastern Cape": {
        "Alice": {"employment_rate": 45.2, "water_quality": "Moderate Risk", "leakage_detected": True, "current_projects": 3},
        "Butterworth": {"employment_rate": 42.8, "water_quality": "High Risk", "leakage_detected": True, "current_projects": 2},
        "Cradock": {"employment_rate": 48.9, "water_quality": "Moderate Risk", "leakage_detected": False, "current_projects": 1},
    },
    "Gauteng": {
        "Bronkhorstspruit": {"employment_rate": 55.3, "water_quality": "Low Risk", "leakage_detected": False, "current_projects": 3},
        "Cullinan": {"employment_rate": 52.1, "water_quality": "Moderate Risk", "leakage_detected": True, "current_projects": 2},
        "Heidelberg": {"employment_rate": 57.8, "water_quality": "Low Risk", "leakage_detected": False, "current_projects": 1},
    }
}

# Financial transparency data
FINANCIAL_DATA = {
    "Eastern Cape": [
        {"company": "AquaTech Solutions", "service": "Pipe Replacement", "amount": 4500000, "status": "Completed"},
        {"company": "WaterWorks Engineering", "service": "Water Treatment Chemicals", "amount": 1200000, "status": "In Progress"},
    ],
    "Gauteng": [
        {"company": "Metro Water Systems", "service": "Leak Detection System", "amount": 3200000, "status": "Completed"},
        {"company": "PureFlow Technologies", "service": "Water Quality Monitoring", "amount": 1850000, "status": "In Progress"},
    ]
}

# Employment opportunity projections
EMPLOYMENT_PROJECTIONS = {
    "Small": {"engineers": 2, "technicians": 5, "administrative": 3, "general_labor": 15},
    "Medium": {"engineers": 5, "technicians": 12, "administrative": 8, "general_labor": 35},
    "Large": {"engineers": 12, "technicians": 25, "administrative": 15, "general_labor": 80},
    "Enterprise": {"engineers": 25, "technicians": 50, "administrative": 30, "general_labor": 200}
}

# DEBUG: Show current state
st.sidebar.markdown("### Debug Info")
st.sidebar.write(f"Current Step: {st.session_state.current_step}")
st.sidebar.write(f"Selected Province: {st.session_state.selected_province}")

# MAIN APPLICATION LOGIC
try:
    if st.session_state.current_step == 1:
        st.markdown('<div class="section-header">PROVINCE SELECTION AND OVERVIEW</div>', unsafe_allow_html=True)
        
        # Province selection dropdown
        selected_province = st.selectbox(
            "Select Province for Analysis:",
            options=list(PROVINCE_BASE_DATA.keys()),
            index=list(PROVINCE_BASE_DATA.keys()).index(st.session_state.selected_province),
            key="province_selector"
        )
        
        st.success(f"Currently analyzing: {selected_province}")
        
        # Display province metrics
        province_data = PROVINCE_BASE_DATA[selected_province]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Key Performance Indicators**")
            st.metric("Water Stress Level", f"{province_data['water_stress']*100:.1f}%")
            st.metric("Water Access Rate", f"{province_data['water_access_base']}%")
            st.metric("Employment Rate", f"{province_data['employment_rate']}%")
            st.metric("Water Quality Score", f"{province_data['water_quality_score']}/100")
        
        with col2:
            st.markdown("**Infrastructure Status**")
            st.metric("Current Water Supply", f"{province_data['current_supply_megalitres']} ML")
            st.metric("Water Demand", f"{province_data['demand_megalitres']} ML")
            st.metric("System Leakage Rate", f"{province_data['leakage_rate']*100:.1f}%")
            st.metric("Contamination Incidents", province_data['contamination_incidents'])
        
        # Water safety status
        water_quality = province_data['water_quality_score']
        if water_quality >= 80:
            st.markdown('<div class="success-card">', unsafe_allow_html=True)
            st.markdown("**WATER SAFETY STATUS: EXCELLENT** - Water meets all safety standards for consumption")
            st.markdown('</div>', unsafe_allow_html=True)
        elif water_quality >= 60:
            st.markdown('<div class="warning-card">', unsafe_allow_html=True)
            st.markdown("**WATER SAFETY STATUS: MODERATE** - Regular monitoring required")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="danger-card">', unsafe_allow_html=True)
            st.markdown("**WATER SAFETY STATUS: POOR** - Immediate intervention required")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Employment opportunities
        st.markdown('<div class="section-header">EMPLOYMENT OPPORTUNITIES</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Available Engineers", province_data['engineers_available'])
        with col2:
            st.metric("Technical Staff", province_data['technical_staff'])
        with col3:
            st.metric("General Workers", f"{province_data['general_workers']:,}")
        with col4:
            st.metric("Unemployment Rate", f"{province_data['unemployment_rate']}%")
        
        # Interactive Map
        st.markdown('<div class="section-header">INTERACTIVE PROVINCE MAP</div>', unsafe_allow_html=True)
        
        map_data = []
        for province_name, data in PROVINCE_BASE_DATA.items():
            color = 'green'
            if data['water_stress'] > 0.8:
                color = 'red'
            elif data['water_stress'] > 0.6:
                color = 'orange'
            
            map_data.append({
                'Province': province_name,
                'Latitude': data['coordinates'][0],
                'Longitude': data['coordinates'][1],
                'Water_Stress': data['water_stress'],
                'Color': color,
                'Size': 25
            })
        
        map_df = pd.DataFrame(map_data)
        
        fig = px.scatter_mapbox(
            map_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Province",
            hover_data={"Water_Stress": ":.2f"},
            color="Color",
            color_discrete_map={'red': 'red', 'orange': 'orange', 'green': 'green'},
            size="Size",
            size_max=20,
            zoom=5,
            height=400,
            title="South Africa Provincial Water Stress Levels"
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig, use_container_width=True)
        
        # Navigation button
        if st.button("View Detailed Provincial Analysis", type="primary"):
            st.session_state.selected_province = selected_province
            st.session_state.current_step = 2
            st.rerun()

    elif st.session_state.current_step == 2:
        province = st.session_state.selected_province
        st.markdown(f'<div class="section-header">DETAILED ANALYSIS: {province}</div>', unsafe_allow_html=True)
        
        if st.button("← Back to Province Selection"):
            st.session_state.current_step = 1
            st.rerun()
        
        # Financial Transparency Section
        st.markdown("**FINANCIAL TRANSPARENCY: EXPENDITURE TRACKING**")
        if province in FINANCIAL_DATA:
            for payment in FINANCIAL_DATA[province]:
                st.write(f"**{payment['company']}** - {payment['service']} - R {payment['amount']:,} - {payment['status']}")
        else:
            st.info("Financial data being updated for this province")
        
        # Rural Area Analysis
        st.markdown("**RURAL AREA ANALYSIS**")
        if province in RURAL_AREA_DATA:
            rural_areas = list(RURAL_AREA_DATA[province].keys())
            selected_rural = st.selectbox("Select Rural Area:", options=rural_areas)
            
            rural_data = RURAL_AREA_DATA[province][selected_rural]
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Employment Rate", f"{rural_data['employment_rate']}%")
                st.metric("Water Quality", rural_data['water_quality'])
            with col2:
                st.metric("Leakage Detected", "Yes" if rural_data['leakage_detected'] else "No")
                st.metric("Active Projects", rural_data['current_projects'])
        
        # Employment Projections
        st.markdown("**EMPLOYMENT PROJECTIONS BY PROJECT SCALE**")
        project_scale = st.selectbox("Select Project Scale:", options=list(EMPLOYMENT_PROJECTIONS.keys()))
        projections = EMPLOYMENT_PROJECTIONS[project_scale]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Engineers", projections['engineers'])
        with col2:
            st.metric("Technicians", projections['technicians'])
        with col3:
            st.metric("Administrative", projections['administrative'])
        with col4:
            st.metric("General Labor", projections['general_labor'])
        
        st.info(f"Total projected jobs: {sum(projections.values())} positions")

except Exception as e:
    st.error(f"Application error: {str(e)}")
    st.info("Please refresh the page to restart the application")

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Platform** - Department of Water and Sanitation | Real-time Water Management Analytics")
st.markdown("*Transparent. Accountable. Data-Driven.*")
