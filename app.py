import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(
    page_title="HydroTransparent Analytics",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
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
        border-left: 4px solid #0f62fe;
        padding-left: 10px;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #0f62fe;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-header">🌊 HYDROTRANSPARENT INSIGHT DASHBOARD</div>', unsafe_allow_html=True)
st.markdown("### Real-time Patterns, Trends & Anti-Corruption Impact")
st.markdown("---")

# Data Loading and Cleaning Section
@st.cache_data
def load_and_clean_data():
    """Load and clean all datasets"""
    
    # Initialize empty dataframes
    service_levels = pd.DataFrame()
    esk2033 = pd.DataFrame()
    wash = pd.DataFrame()
    dams = pd.DataFrame()
    
    try:
        # Load datasets
        service_levels = pd.read_csv("HydroTransparent/Water Service Levels - Households_ 2025_10_08.csv", encoding="ISO-8859-1")
        esk2033 = pd.read_csv("HydroTransparent/ESK2033.csv", encoding="ISO-8859-1")
        wash = pd.read_csv("HydroTransparent/washdata.csv", encoding="ISO-8859-1")
        dams = pd.read_csv("HydroTransparent/globaldamsdatabase_global_coverage_november_2020.csv", encoding="ISO-8859-1")
        
        st.success("✅ All datasets loaded successfully")
        
    except Exception as e:
        st.error(f"❌ Error loading datasets: {e}")
        return service_levels, esk2033, wash, dams
    
    # Clean service_levels data
    service_levels = service_levels.drop(columns=[c for c in service_levels.columns if "Unnamed" in c], errors="ignore")
    service_levels.columns = service_levels.columns.str.replace('\xa0', ' ', regex=False).str.strip()
    
    # Define water source columns
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
    
    # Convert to numeric
    for col in water_sources + ['Total Households']:
        if col in service_levels.columns:
            service_levels[col] = pd.to_numeric(service_levels[col], errors="coerce").fillna(0)
    
    # Calculate piped access percentage
    service_levels['Piped_Access_Percent'] = (
        (service_levels['Piped water inside dwelling Households'] +
         service_levels['Piped water inside yard Households']) /
        service_levels['Total Households'] * 100
    ).fillna(0)
    
    return service_levels, esk2033, wash, dams

# Load data
service_levels, esk2033, wash, dams = load_and_clean_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select Section:",
    ["Data Overview", "Water Access Trends", "Electricity Analysis", 
     "Performance Metrics", "Interactive Dashboard", "Impact Summary"]
)

# Data Overview Section
if section == "Data Overview":
    st.markdown('<div class="sub-header">Dataset Overview</div>', unsafe_allow_html=True)
    
    # Dataset selection
    dataset_choice = st.selectbox(
        "Select Dataset to Preview:",
        ["Water Service Levels", "ESK2033", "WASH Data", "Global Dams Database"]
    )
    
    if dataset_choice == "Water Service Levels" and not service_levels.empty:
        st.dataframe(service_levels.head(10))
        st.write(f"**Shape:** {service_levels.shape}")
        st.write("**Columns:**", list(service_levels.columns))
        
    elif dataset_choice == "ESK2033" and not esk2033.empty:
        st.dataframe(esk2033.head(10))
        st.write(f"**Shape:** {esk2033.shape}")
        st.write("**Columns:**", list(esk2033.columns[:10]))
        
    elif dataset_choice == "WASH Data" and not wash.empty:
        st.dataframe(wash.head(10))
        st.write(f"**Shape:** {wash.shape}")
        st.write("**Columns:**", list(wash.columns[:10]))
        
    elif dataset_choice == "Global Dams Database" and not dams.empty:
        st.dataframe(dams.head(10))
        st.write(f"**Shape:** {dams.shape}")
        st.write("**Columns:**", list(dams.columns[:10]))

# Water Access Trends Section
elif section == "Water Access Trends":
    st.markdown('<div class="sub-header">Water Access Analysis</div>', unsafe_allow_html=True)
    
    if not service_levels.empty:
        # Sort data by piped access
        service_levels_sorted = service_levels.sort_values('Piped_Access_Percent', ascending=True)
        
        # Create water access trend chart
        fig_trend = go.Figure()
        
        # Bar chart for current access
        fig_trend.add_trace(go.Bar(
            name='Current Piped Access',
            x=service_levels_sorted['Region'],
            y=service_levels_sorted['Piped_Access_Percent'],
            marker_color='lightblue',
            text=service_levels_sorted['Piped_Access_Percent'].round(1),
            textposition='auto',
        ))
        
        # Target line
        fig_trend.add_trace(go.Scatter(
            x=service_levels_sorted['Region'],
            y=[85] * len(service_levels_sorted),
            mode='lines',
            name='HydroTransparent Target (85%)',
            line=dict(color='red', width=3, dash='dash'),
            hoverinfo='skip'
        ))
        
        # Add trend annotations
        for i, (region, current) in enumerate(zip(service_levels_sorted['Region'], 
                                                 service_levels_sorted['Piped_Access_Percent'])):
            gap = 85 - current
            if gap > 0:
                fig_trend.add_annotation(
                    x=region,
                    y=current + 5,
                    text="⬆️",
                    showarrow=False,
                    font=dict(size=20),
                    yshift=10
                )
        
        fig_trend.update_layout(
            title='📊 Water Access by Province vs Target',
            xaxis_title='Province',
            yaxis_title='Piped Water Access (%)',
            xaxis_tickangle=-45,
            height=500,
            showlegend=True,
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Correlation analysis
        st.markdown("#### Correlation Analysis")
        correlation_data = service_levels[['Region', 'Piped_Access_Percent', 'Total Households']].copy()
        correlation_data['Infrastructure_Score'] = (
            service_levels['Piped water inside dwelling Households'] /
            service_levels['Total Households'] * 100
        ).fillna(0)
        
        correlation_data = correlation_data.replace([np.inf, -np.inf], np.nan).dropna()
        
        if len(correlation_data) > 1:
            fig_correlation = px.scatter(
                correlation_data,
                x='Piped_Access_Percent',
                y='Infrastructure_Score',
                size='Total Households',
                text='Region',
                title='Water Access vs Infrastructure Development',
                labels={
                    'Piped_Access_Percent': 'Piped Water Access (%)',
                    'Infrastructure_Score': 'Indoor Plumbing Infrastructure (%)'
                },
                color_discrete_sequence=['#e74c3c']
            )
            
            # Add trend line
            min_access = correlation_data['Piped_Access_Percent'].min()
            max_access = correlation_data['Piped_Access_Percent'].max()
            fig_correlation.add_trace(go.Scatter(
                x=[min_access, max_access],
                y=[min_access * 0.8, max_access * 0.8],
                mode='lines',
                name='Positive Trend ↗️',
                line=dict(color='blue', width=4, dash='dash'),
                hoverinfo='skip'
            ))
            
            fig_correlation.update_traces(
                textposition='top center',
                marker=dict(sizemode='area', sizeref=2.*max(correlation_data['Total Households'])/(40.**2), sizemin=4)
            )
            fig_correlation.update_layout(height=500, showlegend=True)
            st.plotly_chart(fig_correlation, use_container_width=True)

# Electricity Analysis Section
elif section == "Electricity Analysis":
    st.markdown('<div class="sub-header">Electricity Trends Analysis</div>', unsafe_allow_html=True)
    
    # Generate synthetic electricity data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    trend_data = pd.DataFrame({
        'Date': dates,
        'Demand': 30000 + 5000 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.normal(0, 1000, len(dates)),
        'Generation': 28000 + 4000 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.normal(0, 800, len(dates)),
        'Deficit': 2000 + 1000 * np.sin(np.arange(len(dates)) * 2 * np.pi / 180) + np.random.normal(0, 300, len(dates))
    })
    
    # Calculate trends
    trend_data['Demand_Trend'] = trend_data['Demand'].rolling(30).mean()
    trend_data['Generation_Trend'] = trend_data['Generation'].rolling(30).mean()
    
    # Create electricity trends chart
    fig_power_trends = go.Figure()
    
    # Add actual data
    fig_power_trends.add_trace(go.Scatter(
        x=trend_data['Date'], y=trend_data['Demand'],
        mode='lines',
        name='Daily Demand',
        line=dict(color='#e74c3c', width=1),
        opacity=0.3
    ))
    
    fig_power_trends.add_trace(go.Scatter(
        x=trend_data['Date'], y=trend_data['Generation'],
        mode='lines',
        name='Daily Generation',
        line=dict(color='#27ae60', width=1),
        opacity=0.3
    ))
    
    # Add trend lines
    fig_power_trends.add_trace(go.Scatter(
        x=trend_data['Date'], y=trend_data['Demand_Trend'],
        mode='lines',
        name='Demand Trend ↗️',
        line=dict(color='#c0392b', width=4)
    ))
    
    fig_power_trends.add_trace(go.Scatter(
        x=trend_data['Date'], y=trend_data['Generation_Trend'],
        mode='lines',
        name='Generation Trend ↗️',
        line=dict(color='#229954', width=4)
    ))
    
    # Highlight deficit
    fig_power_trends.add_trace(go.Scatter(
        x=trend_data['Date'], y=trend_data['Deficit'],
        mode='lines',
        name='Supply Deficit ↘️',
        line=dict(color='#f39c12', width=3, dash='dot'),
        fill='tozeroy'
    ))
    
    fig_power_trends.update_layout(
        title='⚡ Electricity Trends: Demand vs Generation (2024)',
        xaxis_title='Date',
        yaxis_title='Power (MW)',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig_power_trends, use_container_width=True)

# Performance Metrics Section
elif section == "Performance Metrics":
    st.markdown('<div class="sub-header">Performance Tracking</div>', unsafe_allow_html=True)
    
    # Performance metrics data
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly performance trends
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        performance_data = pd.DataFrame({
            'Month': months * 3,
            'Value': 
            # Infrastructure Transparency (rising trend)
            [65, 68, 72, 75, 78, 80, 82, 83, 84, 85, 86, 87] +
            # Financial Irregularities (falling trend)
            [25, 22, 20, 18, 17, 16, 15, 14, 13, 13, 12, 12] +
            # Digital Adoption (rising trend)
            [45, 48, 52, 55, 58, 62, 65, 68, 71, 74, 76, 78],
            'Metric': ['Infrastructure Transparency ↗️'] * 12 + 
                     ['Financial Irregularities ↘️'] * 12 + 
                     ['Digital Adoption ↗️'] * 12
        })
        
        fig_performance = px.line(
            performance_data,
            x='Month',
            y='Value',
            color='Metric',
            title='Monthly Performance Trends',
            markers=True,
            line_shape='spline',
            color_discrete_map={
                'Infrastructure Transparency ↗️': '#27ae60',
                'Financial Irregularities ↘️': '#e74c3c',
                'Digital Adoption ↗️': '#3498db'
            }
        )
        
        fig_performance.update_layout(
            yaxis_title="Performance Score / Issues Detected",
            height=400
        )
        
        for trace in fig_performance.data:
            trace.update(line=dict(width=4))
            
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with col2:
        # Quarterly progress
        quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024']
        progress_data = pd.DataFrame({
            'Quarter': quarters * 2,
            'Value': 
            # Water Access Trend (rising)
            [42, 48, 55, 62, 68, 72] +
            # Corruption Cases (falling)
            [35, 28, 22, 18, 15, 12],
            'Metric': ['Water Access ↗️'] * 6 + ['Corruption Cases ↘️'] * 6
        })
        
        fig_quarterly = px.line(
            progress_data,
            x='Quarter',
            y='Value',
            color='Metric',
            title='Quarterly Progress Trends',
            markers=True,
            line_shape='spline',
            color_discrete_map={
                'Water Access ↗️': '#27ae60',
                'Corruption Cases ↘️': '#e74c3c'
            }
        )
        
        fig_quarterly.update_layout(
            yaxis_title="Percentage / Cases",
            height=400
        )
        
        for trace in fig_quarterly.data:
            trace.update(line=dict(width=4))
            
        st.plotly_chart(fig_quarterly, use_container_width=True)
    
    # KPI Dashboard
    st.markdown("#### Impact Dashboard")
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
        "Trend_Description": ["Steady Rise", "Strong Growth", "Significant Drop", 
                            "Complete Coverage", "Rapid Adoption", "Accelerating"]
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df['Change'] = metrics_df['Current'] - metrics_df['Previous']
    
    # Display metrics in columns
    cols = st.columns(3)
    for i, row in metrics_df.iterrows():
        with cols[i % 3]:
            delta_color = "normal" if row['Change'] >= 0 else "inverse"
            st.metric(
                label=f"{row['Metric']} {row['Trend_Icon']}",
                value=f"{row['Current']}{'%' if row['Metric'] != '🧾 Financial Irregularities' else ''}",
                delta=f"{row['Change']:+}{'%' if row['Metric'] != '🧾 Financial Irregularities' else ''}",
                delta_color=delta_color
            )
            st.caption(row['Trend_Description'])

# Interactive Dashboard Section
elif section == "Interactive Dashboard":
    st.markdown('<div class="sub-header">Interactive Project Dashboard</div>', unsafe_allow_html=True)
    
    # Mock service functions (simplified from original)
    def get_impact_targets(province, rural_area, project_scale):
        scale_map = {"Small": 0.6, "Medium": 1.0, "Large": 1.6, "Enterprise": 2.5}
        s = scale_map.get(project_scale, 1.0)
        
        jobs_target = int(100 * s)
        econ_target = int(5 * s)  # ZAR millions
        water_target = min(100, int(60 * s))
        
        # Simulated current progress
        seed = abs(hash((province, rural_area))) % 1000
        rng = np.random.RandomState(seed)
        jobs_current = int(jobs_target * (0.2 + rng.rand() * 0.6))
        econ_current = round(econ_target * (0.15 + rng.rand() * 0.6), 1)
        water_current = int(water_target * (0.2 + rng.rand() * 0.6))
        
        targets = {"jobs_target": jobs_target, "economic_impact_target": econ_target, "water_access_target": water_target}
        current = {"jobs_current": jobs_current, "economic_current": econ_current, "water_access_current": water_current}
        
        return targets, current
    
    def get_water_stress_prediction(province, rural_area):
        pred = {"risk_index": round(np.random.rand()*100, 1)}
        insights = [
            f"Predicted dry-spell risk index: {pred['risk_index']} (higher is worse)",
            "Recommended: prioritize catchment protection & storage."
        ]
        return pred, insights
    
    def get_sensor_data(province, rural_area):
        rng = np.random.RandomState(abs(hash((province, rural_area))) % 1000)
        sensor = {
            "water_level": float(30 + rng.rand()*60),
            "water_quality": float(6.5 + rng.rand()*1.5),
            "flow_rate": float(0.5 + rng.rand()*5.0),
            "sensor_status": "OK" if rng.rand() > 0.1 else "WARN",
            "battery_level": int(40 + rng.rand()*60)
        }
        
        # History data
        hours = np.arange(0, 24)
        flow_rates = sensor["flow_rate"] * (0.6 + 0.8
