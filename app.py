import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
        font-size: 3rem;
        color: #1f5f8b;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        padding: 1rem;
        background: linear-gradient(135deg, #1f5f8b 0%, #1891ac 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 2rem;
        color: #1f5f8b;
        border-bottom: 3px solid #1f5f8b;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
    }
    .subsection-header {
        font-size: 1.5rem;
        color: #1891ac;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f5f8b;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning-card {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .danger-card {
        background: linear-gradient(135deg, #f8d7da 0%, #f1aeb5 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-card {
        background: linear-gradient(135deg, #d1edff 0%, #a8d8ff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #0f62fe;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .selection-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #1f5f8b;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .nav-button {
        background: linear-gradient(135deg, #1f5f8b 0%, #1891ac 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        margin: 0.5rem;
    }
    .map-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">HYDROTRANSPARENT WATER MANAGEMENT PLATFORM</div>', unsafe_allow_html=True)
st.markdown("### Comprehensive Water Resource Management, Employment Analytics, and Financial Transparency")
st.markdown("---")

# Enhanced Province-specific base data with comprehensive metrics
PROVINCE_BASE_DATA = {
    "Eastern Cape": {
        "water_stress": 0.75, "water_access_base": 65, "water_quality_score": 72,
        "employment_rate": 58.3, "unemployment_rate": 41.7, 
        "engineers_available": 450, "technical_staff": 1200, "general_workers": 8500,
        "current_supply_megalitres": 245, "demand_megalitres": 320, 
        "contamination_incidents": 12, "leakage_rate": 0.28, "water_safety": "Moderate Risk",
        "coordinates": (-32.0833, 26.8833), "zoom_level": 7,
        "infrastructure_score": 68, "project_readiness": "Medium", "available_funding": 35000000
    },
    "Free State": {
        "water_stress": 0.65, "water_access_base": 72, "water_quality_score": 78,
        "employment_rate": 62.1, "unemployment_rate": 37.9, 
        "engineers_available": 320, "technical_staff": 980, "general_workers": 6200,
        "current_supply_megalitres": 180, "demand_megalitres": 210, 
        "contamination_incidents": 8, "leakage_rate": 0.22, "water_safety": "Low Risk",
        "coordinates": (-28.4556, 26.7683), "zoom_level": 7,
        "infrastructure_score": 75, "project_readiness": "High", "available_funding": 28000000
    },
    "Gauteng": {
        "water_stress": 0.85, "water_access_base": 88, "water_quality_score": 85,
        "employment_rate": 68.9, "unemployment_rate": 31.1, 
        "engineers_available": 1250, "technical_staff": 3200, "general_workers": 18500,
        "current_supply_megalitres": 890, "demand_megalitres": 950, 
        "contamination_incidents": 5, "leakage_rate": 0.18, "water_safety": "Excellent",
        "coordinates": (-26.2044, 28.0456), "zoom_level": 9,
        "infrastructure_score": 88, "project_readiness": "Very High", "available_funding": 85000000
    },
    "KwaZulu-Natal": {
        "water_stress": 0.70, "water_access_base": 74, "water_quality_score": 76,
        "employment_rate": 60.5, "unemployment_rate": 39.5, 
        "engineers_available": 680, "technical_staff": 1850, "general_workers": 12500,
        "current_supply_megalitres": 420, "demand_megalitres": 480, 
        "contamination_incidents": 15, "leakage_rate": 0.25, "water_safety": "Moderate Risk",
        "coordinates": (-29.8587, 31.0218), "zoom_level": 7,
        "infrastructure_score": 72, "project_readiness": "Medium", "available_funding": 45000000
    },
    "Limpopo": {
        "water_stress": 0.80, "water_access_base": 63, "water_quality_score": 69,
        "employment_rate": 55.8, "unemployment_rate": 44.2, 
        "engineers_available": 290, "technical_staff": 850, "general_workers": 7200,
        "current_supply_megalitres": 195, "demand_megalitres": 280, 
        "contamination_incidents": 18, "leakage_rate": 0.31, "water_safety": "High Risk",
        "coordinates": (-23.4013, 29.4179), "zoom_level": 6,
        "infrastructure_score": 62, "project_readiness": "Low", "available_funding": 25000000
    },
    "Mpumalanga": {
        "water_stress": 0.72, "water_access_base": 71, "water_quality_score": 74,
        "employment_rate": 61.3, "unemployment_rate": 38.7, 
        "engineers_available": 380, "technical_staff": 1100, "general_workers": 7800,
        "current_supply_megalitres": 230, "demand_megalitres": 270, 
        "contamination_incidents": 9, "leakage_rate": 0.24, "water_safety": "Moderate Risk",
        "coordinates": (-25.5653, 30.5279), "zoom_level": 7,
        "infrastructure_score": 70, "project_readiness": "Medium", "available_funding": 32000000
    },
    "North West": {
        "water_stress": 0.68, "water_access_base": 69, "water_quality_score": 71,
        "employment_rate": 59.2, "unemployment_rate": 40.8, 
        "engineers_available": 270, "technical_staff": 750, "general_workers": 5800,
        "current_supply_megalitres": 165, "demand_megalitres": 200, 
        "contamination_incidents": 11, "leakage_rate": 0.27, "water_safety": "Moderate Risk",
        "coordinates": (-26.6639, 25.2838), "zoom_level": 7,
        "infrastructure_score": 65, "project_readiness": "Medium", "available_funding": 28000000
    },
    "Northern Cape": {
        "water_stress": 0.90, "water_access_base": 58, "water_quality_score": 65,
        "employment_rate": 53.7, "unemployment_rate": 46.3, 
        "engineers_available": 180, "technical_staff": 520, "general_workers": 4200,
        "current_supply_megalitres": 95, "demand_megalitres": 150, 
        "contamination_incidents": 7, "leakage_rate": 0.35, "water_safety": "High Risk",
        "coordinates": (-29.0467, 21.8569), "zoom_level": 5,
        "infrastructure_score": 58, "project_readiness": "Low", "available_funding": 18000000
    },
    "Western Cape": {
        "water_stress": 0.78, "water_access_base": 82, "water_quality_score": 88,
        "employment_rate": 65.4, "unemployment_rate": 34.6, 
        "engineers_available": 890, "technical_staff": 2100, "general_workers": 14200,
        "current_supply_megalitres": 520, "demand_megalitres": 580, 
        "contamination_incidents": 4, "leakage_rate": 0.16, "water_safety": "Excellent",
        "coordinates": (-33.9253, 18.4239), "zoom_level": 7,
        "infrastructure_score": 85, "project_readiness": "High", "available_funding": 65000000
    }
}

# Comprehensive Rural area coordinates and data
RURAL_AREA_COORDINATES = {
    "Eastern Cape": {
        "Alice": (-32.7872, 26.8340), "Butterworth": (-32.3303, 28.1498),
        "Cradock": (-32.1642, 25.6192), "Graaff-Reinet": (-32.2521, 24.5308),
        "Lady Frere": (-31.7031, 27.2329), "Mount Fletcher": (-30.6769, 28.5008),
        "Queenstown": (-31.8976, 26.8753), "Umtata": (-31.5889, 28.7844)
    },
    "Free State": {
        "Bethlehem": (-28.2308, 28.3071), "Bothaville": (-27.3884, 26.6170),
        "Frankfort": (-27.2789, 28.4925), "Harrismith": (-28.2728, 29.1294),
        "Philippolis": (-30.2603, 25.2842), "Sasolburg": (-26.8136, 27.8169),
        "Vrede": (-27.4264, 29.1658), "Wepener": (-29.7333, 27.0333)
    },
    "Gauteng": {
        "Bronkhorstspruit": (-25.8100, 28.7425), "Cullinan": (-25.6708, 28.5236),
        "Heidelberg": (-26.5048, 28.3592), "Randfontein": (-26.1844, 27.7023),
        "Soshanguve": (-25.4976, 28.1003), "Carletonville": (-26.3608, 27.3975),
        "Krugersdorp": (-26.1000, 27.7667), "Springs": (-26.2547, 28.4433)
    },
    "KwaZulu-Natal": {
        "Eshowe": (-28.8864, 31.4698), "Hluhluwe": (-28.0190, 32.2676),
        "Ixopo": (-30.1592, 30.0603), "Mtubatuba": (-28.4178, 32.1814),
        "Nkandla": (-28.6211, 31.0878), "Pongola": (-27.3833, 31.6167),
        "Utrecht": (-27.6586, 30.3217), "Vryheid": (-27.7667, 30.8000)
    },
    "Limpopo": {
        "Alldays": (-22.6631, 29.0939), "Giyani": (-23.3167, 30.7167),
        "Lebowakgomo": (-24.2000, 29.5000), "Makhado": (-23.0500, 29.9000),
        "Tzaneen": (-23.8333, 30.1667), "Modimolle": (-24.7000, 28.4000),
        "Phalaborwa": (-23.9429, 31.1411), "Thohoyandou": (-22.9500, 30.4833)
    },
    "Mpumalanga": {
        "Barberton": (-25.7889, 31.0536), "Carolina": (-26.0667, 30.1167),
        "Ermelo": (-26.5333, 29.9833), "Hazyview": (-25.0500, 31.1333),
        "Pilgrim's Rest": (-24.9000, 30.7500), "Belfast": (-25.6897, 30.0353),
        "Middelburg": (-25.7750, 29.4653), "Standerton": (-26.9500, 29.2500)
    },
    "North West": {
        "Coligny": (-26.3333, 26.3167), "Ganyesa": (-26.5833, 24.1833),
        "Koster": (-25.8667, 26.9000), "Madikwe": (-25.3000, 26.3667),
        "Sannieshof": (-26.5333, 25.8167), "Bloemhof": (-27.6500, 25.5833),
        "Klerksdorp": (-26.8667, 26.6667), "Potchefstroom": (-26.7147, 27.1019)
    },
    "Northern Cape": {
        "Barkly West": (-28.5333, 24.5167), "Calvinia": (-31.4667, 19.7667),
        "Kenhardt": (-29.3500, 21.1500), "Pofadder": (-29.1333, 19.3833),
        "Upington": (-28.4572, 21.2425), "De Aar": (-30.6500, 24.0167),
        "Kuruman": (-27.4500, 23.4167), "Springbok": (-29.6667, 17.8833)
    },
    "Western Cape": {
        "Barrydale": (-33.9000, 20.7333), "Caledon": (-34.2292, 19.4264),
        "Grabouw": (-34.1500, 19.0167), "Prince Albert": (-33.2247, 22.0308),
        "Tulbagh": (-33.2867, 19.1414), "Ceres": (-33.3667, 19.3167),
        "Robertson": (-33.8000, 19.8833), "Worcester": (-33.6464, 19.4489)
    }
}

# Enhanced Rural area detailed data
RURAL_AREA_DETAILED_DATA = {
    "Eastern Cape": {
        "Alice": {"employment_rate": 45.2, "water_quality": "Moderate Risk", "leakage_detected": True, 
                 "current_projects": 3, "water_supply_gap": 25, "contamination_level": "Medium",
                 "available_workers": 1200, "skilled_labor": 180, "infrastructure_age": 25},
        "Butterworth": {"employment_rate": 42.8, "water_quality": "High Risk", "leakage_detected": True, 
                       "current_projects": 2, "water_supply_gap": 35, "contamination_level": "High",
                       "available_workers": 950, "skilled_labor": 120, "infrastructure_age": 30},
        "Cradock": {"employment_rate": 48.9, "water_quality": "Moderate Risk", "leakage_detected": False, 
                   "current_projects": 1, "water_supply_gap": 18, "contamination_level": "Low",
                   "available_workers": 850, "skilled_labor": 150, "infrastructure_age": 22}
    },
    "Gauteng": {
        "Bronkhorstspruit": {"employment_rate": 55.3, "water_quality": "Low Risk", "leakage_detected": False, 
                            "current_projects": 3, "water_supply_gap": 12, "contamination_level": "Low",
                            "available_workers": 1800, "skilled_labor": 320, "infrastructure_age": 15},
        "Cullinan": {"employment_rate": 52.1, "water_quality": "Moderate Risk", "leakage_detected": True, 
                    "current_projects": 2, "water_supply_gap": 20, "contamination_level": "Medium",
                    "available_workers": 1200, "skilled_labor": 210, "infrastructure_age": 18},
        "Heidelberg": {"employment_rate": 57.8, "water_quality": "Low Risk", "leakage_detected": False, 
                      "current_projects": 1, "water_supply_gap": 8, "contamination_level": "Low",
                      "available_workers": 1500, "skilled_labor": 280, "infrastructure_age": 12}
    }
}

# Comprehensive Financial transparency data
FINANCIAL_TRANSPARENCY_DATA = {
    "Eastern Cape": [
        {"company": "AquaTech Solutions", "service": "Pipe Network Replacement", "amount": 4500000, 
         "status": "Completed", "date": "2024-01-15", "contractor_type": "Infrastructure", "workers_employed": 45},
        {"company": "WaterWorks Engineering", "service": "Water Treatment Chemicals Supply", "amount": 1200000, 
         "status": "In Progress", "date": "2024-02-20", "contractor_type": "Supplies", "workers_employed": 12},
        {"company": "InfraBuild Contractors", "service": "Reservoir Construction", "amount": 7800000, 
         "status": "Completed", "date": "2024-01-05", "contractor_type": "Construction", "workers_employed": 85},
        {"company": "PureFlow Systems", "service": "Leak Detection Equipment", "amount": 850000, 
         "status": "Completed", "date": "2024-03-10", "contractor_type": "Equipment", "workers_employed": 8}
    ],
    "Gauteng": [
        {"company": "Metro Water Systems", "service": "Advanced Leak Detection System Installation", "amount": 3200000, 
         "status": "Completed", "date": "2024-02-28", "contractor_type": "Technology", "workers_employed": 28},
        {"company": "PureFlow Technologies", "service": "Water Quality Monitoring Network", "amount": 1850000, 
         "status": "In Progress", "date": "2024-03-15", "contractor_type": "Monitoring", "workers_employed": 15},
        {"company": "Urban Infrastructure Ltd", "service": "Pipeline Network Upgrade Phase 1", "amount": 12500000, 
         "status": "Planning", "date": "2024-04-01", "contractor_type": "Infrastructure", "workers_employed": 0},
        {"company": "HydroClean Services", "service": "Water Contamination Response", "amount": 650000, 
         "status": "Completed", "date": "2024-01-20", "contractor_type": "Emergency", "workers_employed": 18}
    ]
}

# Comprehensive Employment projections
EMPLOYMENT_PROJECTIONS = {
    "Small Community Project": {
        "civil_engineers": 2, "water_engineers": 1, "technicians": 5, 
        "administrative": 3, "general_labor": 15, "skilled_trades": 8,
        "total_jobs": 34, "duration_months": 6, "estimated_cost": 5000000
    },
    "Medium Regional Project": {
        "civil_engineers": 5, "water_engineers": 3, "technicians": 12, 
        "administrative": 8, "general_labor": 35, "skilled_trades": 18,
        "total_jobs": 81, "duration_months": 12, "estimated_cost": 15000000
    },
    "Large Provincial Project": {
        "civil_engineers": 12, "water_engineers": 8, "technicians": 25, 
        "administrative": 15, "general_labor": 80, "skilled_trades": 35,
        "total_jobs": 175, "duration_months": 24, "estimated_cost": 45000000
    },
    "Enterprise National Project": {
        "civil_engineers": 25, "water_engineers": 15, "technicians": 50, 
        "administrative": 30, "general_labor": 200, "skilled_trades": 80,
        "total_jobs": 400, "duration_months": 36, "estimated_cost": 120000000
    }
}

# Water contamination and safety data
WATER_SAFETY_DATA = {
    "Eastern Cape": {
        "bacterial_contamination": "Medium", "chemical_contamination": "High", 
        "heavy_metals": "Low", "turbidity": "Medium", "safety_status": "Moderate Risk",
        "last_test_date": "2024-03-15", "compliance_score": 72
    },
    "Gauteng": {
        "bacterial_contamination": "Low", "chemical_contamination": "Low", 
        "heavy_metals": "Low", "turbidity": "Low", "safety_status": "Excellent",
        "last_test_date": "2024-03-20", "compliance_score": 95
    },
    "Limpopo": {
        "bacterial_contamination": "High", "chemical_contamination": "Medium", 
        "heavy_metals": "Medium", "turbidity": "High", "safety_status": "High Risk",
        "last_test_date": "2024-03-10", "compliance_score": 58
    }
}

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = "Gauteng"
if 'selected_rural_area' not in st.session_state:
    st.session_state.selected_rural_area = None
if 'map_clicked' not in st.session_state:
    st.session_state.map_clicked = None

# STEP 1: INTERACTIVE PROVINCE SELECTION WITH MAP
if st.session_state.current_step == 1:
    st.markdown('<div class="section-header">INTERACTIVE PROVINCE SELECTION</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="selection-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Province Selection")
            selected_province = st.selectbox(
                "Choose Province for Detailed Analysis:",
                options=list(PROVINCE_BASE_DATA.keys()),
                index=list(PROVINCE_BASE_DATA.keys()).index(st.session_state.selected_province),
                key="province_selector_main"
            )
            
            # Quick province statistics
            province_data = PROVINCE_BASE_DATA[selected_province]
            st.markdown("#### Quick Statistics")
            col1a, col1b = st.columns(2)
            with col1a:
                st.metric("Water Stress", f"{province_data['water_stress']*100:.1f}%")
                st.metric("Employment Rate", f"{province_data['employment_rate']}%")
            with col1b:
                st.metric("Water Access", f"{province_data['water_access_base']}%")
                st.metric("Available Funding", f"R {province_data['available_funding']:,}")
        
        with col2:
            st.markdown("### Water Safety Status")
            water_quality = province_data['water_quality_score']
            if water_quality >= 80:
                st.markdown('<div class="success-card">', unsafe_allow_html=True)
                st.markdown("**SAFETY STATUS: EXCELLENT**")
                st.markdown(f"Water Quality Score: {water_quality}/100")
                st.markdown("All parameters within safe limits")
                st.markdown('</div>', unsafe_allow_html=True)
            elif water_quality >= 60:
                st.markdown('<div class="warning-card">', unsafe_allow_html=True)
                st.markdown("**SAFETY STATUS: MODERATE RISK**")
                st.markdown(f"Water Quality Score: {water_quality}/100")
                st.markdown("Enhanced monitoring recommended")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="danger-card">', unsafe_allow_html=True)
                st.markdown("**SAFETY STATUS: HIGH RISK**")
                st.markdown(f"Water Quality Score: {water_quality}/100")
                st.markdown("Immediate intervention required")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive Map for Province Selection
    st.markdown('<div class="subsection-header">Interactive Geographic Selection Map</div>', unsafe_allow_html=True)
    
    # Create comprehensive map data
    map_data = []
    for province_name, data in PROVINCE_BASE_DATA.items():
        # Determine color based on water stress
        if data['water_stress'] > 0.8:
            color = 'red'
            size = 30
        elif data['water_stress'] > 0.6:
            color = 'orange'
            size = 25
        else:
            color = 'green'
            size = 20
        
        # Adjust size for selected province
        if province_name == selected_province:
            size = 35
        
        map_data.append({
            'Province': province_name,
            'Latitude': data['coordinates'][0],
            'Longitude': data['coordinates'][1],
            'Water_Stress': data['water_stress'],
            'Employment_Rate': data['employment_rate'],
            'Water_Quality': data['water_quality_score'],
            'Color': color,
            'Size': size,
            'Selected': province_name == selected_province
        })
    
    map_df = pd.DataFrame(map_data)
    
    # Create interactive map
    fig = px.scatter_mapbox(
        map_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Province",
        hover_data={
            "Water_Stress": ":.2f",
            "Employment_Rate": ":.1f",
            "Water_Quality": True,
            "Color": False,
            "Size": False
        },
        color="Color",
        color_discrete_map={'red': '#dc3545', 'orange': '#fd7e14', 'green': '#28a745'},
        size="Size",
        size_max=35,
        zoom=5,
        center={"lat": -30.5, "lon": 25},
        height=600,
        title="South Africa Provincial Water Management Overview - Click on provinces for selection"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":40,"l":0,"b":0},
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick selection buttons
    st.markdown("### Quick Province Selection")
    cols = st.columns(3)
    for i, province in enumerate(PROVINCE_BASE_DATA.keys()):
        with cols[i % 3]:
            if st.button(f"Select {province}", key=f"btn_{province}"):
                st.session_state.selected_province = province
                st.rerun()
    
    # Navigation to next step
    if st.button("Proceed to Detailed Provincial Analysis", type="primary", use_container_width=True):
        st.session_state.selected_province = selected_province
        st.session_state.current_step = 2
        st.rerun()

# STEP 2: DETAILED PROVINCIAL ANALYSIS
elif st.session_state.current_step == 2:
    province = st.session_state.selected_province
    province_data = PROVINCE_BASE_DATA[province]
    
    st.markdown(f'<div class="section-header">DETAILED ANALYSIS: {province}</div>', unsafe_allow_html=True)
    
    # Navigation
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        if st.button("← Back to Province Selection"):
            st.session_state.current_step = 1
            st.rerun()
    
    # Comprehensive Dashboard Layout
    tab1, tab2, tab3, tab4 = st.tabs(["Employment Analytics", "Water Supply & Quality", "Financial Transparency", "Infrastructure & Projects"])
    
    with tab1:
        st.markdown('<div class="subsection-header">Employment Opportunities and Workforce Analytics</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Employment Rate", f"{province_data['employment_rate']}%")
        with col2:
            st.metric("Unemployment Rate", f"{province_data['unemployment_rate']}%")
        with col3:
            st.metric("Available Engineers", province_data['engineers_available'])
        with col4:
            st.metric("Technical Staff", province_data['technical_staff'])
        
        st.markdown("#### Employment Projections by Project Scale")
        project_scale = st.selectbox("Select Project Scale:", options=list(EMPLOYMENT_PROJECTIONS.keys()))
        
        projections = EMPLOYMENT_PROJECTIONS[project_scale]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Professional Roles**")
            st.metric("Civil Engineers", projections['civil_engineers'])
            st.metric("Water Engineers", projections['water_engineers'])
            st.metric("Technicians", projections['technicians'])
        with col2:
            st.markdown("**Support Roles**")
            st.metric("Administrative Staff", projections['administrative'])
            st.metric("Skilled Trades", projections['skilled_trades'])
            st.metric("General Labor", projections['general_labor'])
        with col3:
            st.markdown("**Project Summary**")
            st.metric("Total Jobs", projections['total_jobs'])
            st.metric("Duration", f"{projections['duration_months']} months")
            st.metric("Estimated Cost", f"R {projections['estimated_cost']:,}")
    
    with tab2:
        st.markdown('<div class="subsection-header">Water Supply, Quality and Safety Monitoring</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Current Water Supply Status")
            supply_gap = province_data['demand_megalitres'] - province_data['current_supply_megalitres']
            st.metric("Current Supply", f"{province_data['current_supply_megalitres']} ML")
            st.metric("Current Demand", f"{province_data['demand_megalitres']} ML")
            st.metric("Supply Gap", f"{supply_gap} ML", delta=f"{-supply_gap} ML deficit" if supply_gap > 0 else "Surplus")
            st.metric("System Leakage Rate", f"{province_data['leakage_rate']*100:.1f}%")
        
        with col2:
            st.markdown("#### Water Quality and Safety")
            st.metric("Water Quality Score", f"{province_data['water_quality_score']}/100")
            st.metric("Contamination Incidents", province_data['contamination_incidents'])
            st.metric("Safety Status", province_data['water_safety'])
            
            if province in WATER_SAFETY_DATA:
                safety_data = WATER_SAFETY_DATA[province]
                st.markdown("**Detailed Contamination Analysis**")
                st.write(f"Bacterial: {safety_data['bacterial_contamination']}")
                st.write(f"Chemical: {safety_data['chemical_contamination']}")
                st.write(f"Heavy Metals: {safety_data['heavy_metals']}")
                st.write(f"Compliance Score: {safety_data['compliance_score']}/100")
    
    with tab3:
        st.markdown('<div class="subsection-header">Financial Transparency and Expenditure Tracking</div>', unsafe_allow_html=True)
        
        if province in FINANCIAL_TRANSPARENCY_DATA:
            financial_df = pd.DataFrame(FINANCIAL_TRANSPARENCY_DATA[province])
            
            # Summary metrics
            total_spent = sum(item['amount'] for item in FINANCIAL_TRANSPARENCY_DATA[province] if item['status'] == 'Completed')
            total_workers = sum(item['workers_employed'] for item in FINANCIAL_TRANSPARENCY_DATA[province] if item['status'] == 'Completed')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Expenditure", f"R {total_spent:,}")
            with col2:
                st.metric("Jobs Created", total_workers)
            with col3:
                st.metric("Active Contracts", len([x for x in FINANCIAL_TRANSPARENCY_DATA[province] if x['status'] == 'In Progress']))
            with col4:
                st.metric("Companies Engaged", len(FINANCIAL_TRANSPARENCY_DATA[province]))
            
            # Detailed expenditure table
            st.markdown("#### Detailed Expenditure Records")
            for expenditure in FINANCIAL_TRANSPARENCY_DATA[province]:
                with st.expander(f"{expenditure['company']} - {expenditure['service']} - R {expenditure['amount']:,}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Contractor Type:** {expenditure['contractor_type']}")
                        st.write(f"**Status:** {expenditure['status']}")
                        st.write(f"**Date:** {expenditure['date']}")
                    with col2:
                        st.write(f"**Workers Employed:** {expenditure['workers_employed']}")
                        st.write(f"**Amount:** R {expenditure['amount']:,}")
        else:
            st.info("Financial transparency data being updated for this province")
    
    with tab4:
        st.markdown('<div class="subsection-header">Infrastructure Status and Project Planning</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Infrastructure Assessment")
            st.metric("Infrastructure Score", f"{province_data['infrastructure_score']}/100")
            st.metric("Project Readiness", province_data['project_readiness'])
            st.metric("Available Funding", f"R {province_data['available_funding']:,}")
            
            # Leak detection status
            if province_data['leakage_rate'] > 0.25:
                st.error("CRITICAL: High leakage detected - Immediate infrastructure audit required")
            elif province_data['leakage_rate'] > 0.15:
                st.warning("WARNING: Moderate leakage - Schedule maintenance inspection")
            else:
                st.success("Leakage within acceptable operational limits")
        
        with col2:
            st.markdown("#### Rural Area Analysis")
            if province in RURAL_AREA_COORDINATES:
                rural_areas = list(RURAL_AREA_COORDINATES[province].keys())
                selected_rural = st.selectbox("Select Rural Area for Detailed View:", options=rural_areas)
                
                if province in RURAL_AREA_DETAILED_DATA and selected_rural in RURAL_AREA_DETAILED_DATA[province]:
                    rural_data = RURAL_AREA_DETAILED_DATA[province][selected_rural]
                    st.metric("Employment Rate", f"{rural_data['employment_rate']}%")
                    st.metric("Water Quality Risk", rural_data['water_quality'])
                    st.metric("Available Workforce", rural_data['available_workers'])
                    st.metric("Infrastructure Age", f"{rural_data['infrastructure_age']} years")
    
    # Interactive Rural Area Map
    if province in RURAL_AREA_COORDINATES:
        st.markdown('<div class="subsection-header">Rural Area Geographic Distribution</div>', unsafe_allow_html=True)
        
        rural_map_data = []
        for rural_name, coords in RURAL_AREA_COORDINATES[province].items():
            rural_map_data.append({
                'Rural_Area': rural_name,
                'Latitude': coords[0],
                'Longitude': coords[1],
                'Size': 25
            })
        
        rural_df = pd.DataFrame(rural_map_data)
        
        fig_rural = px.scatter_mapbox(
            rural_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Rural_Area",
            size="Size",
            size_max=25,
            zoom=7,
            center={"lat": province_data['coordinates'][0], "lon": province_data['coordinates'][1]},
            height=400,
            title=f"Rural Areas in {province} - Click for detailed analysis"
        )
        
        fig_rural.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
        st.plotly_chart(fig_rural, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**HydroTransparent Platform** - Department of Water and Sanitation | Real-time Water Management Analytics")
st.markdown("*Transparent. Accountable. Data-Driven.*")
