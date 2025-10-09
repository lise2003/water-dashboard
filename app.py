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
        if st.button("← Change Location", type="secondary", use_container_width=True):
            st.session_state.user_area_selected = False
            st.rerun()
    
    # Get all enterprise data
    watson_predictions, insights = watson_service.get_water_stress_prediction(province, rural_area)
    satellite_map = satellite_service.get_satellite_map(province, rural_area)
    iot_data, historical_data = iot_service.get_sensor_data(province, rural_area)
    compliance_data = regulatory_service.get_compliance_status(province, "Design")
    stakeholders = stakeholder_manager.get_stakeholders()
    jobs_data, wage_analysis, total_jobs, total_income = jobs_analyzer.get_jobs_breakdown(province, rural_area, "Large")
    
    # Show dependency warning only once at the top if folium is not available
    if not FOLIUM_AVAILABLE:
        st.warning("⚠️ **Mapping Features Limited**: Folium package not installed. Some satellite mapping features will be limited.")
        st.info("💡 **To enable full mapping capabilities**: Run the following command in your terminal:\n\n```bash\npip install folium streamlit-folium\n```")
    
    # Rest of the dashboard code remains the same...
