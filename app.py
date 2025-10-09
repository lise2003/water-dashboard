# app.py - WATER INFRASTRUCTURE PLANNER (ARROW-COMPATIBLE)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

# Set up the page
st.set_page_config(page_title="Water Infrastructure Planner", layout="wide")
st.title("💧 South Africa Water Infrastructure Planner")
st.markdown("Empowering Communities Through Data: Tackling Water Inequality")

# Function to make DataFrame Arrow-compatible
def make_arrow_compatible(df):
    """
    Convert DataFrame to be PyArrow compatible by handling nested objects and mixed types
    """
    df_clean = df.copy()
    
    for col in df_clean.columns:
        # Try to convert to numeric first
        try:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='ignore')
        except:
            pass
        
        # Convert any remaining nested objects to strings
        try:
            # Check if column contains nested objects
            sample_value = df_clean[col].iloc[0] if len(df_clean) > 0 else None
            if isinstance(sample_value, (dict, list, tuple)):
                df_clean[col] = df_clean[col].astype(str)
        except:
            # Final fallback: convert to string
            df_clean[col] = df_clean[col].astype(str)
    
    return df_clean

# Load your data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('water_infrastructure_data.csv')
        # Clean the data for Arrow compatibility
        data_clean = make_arrow_compatible(data)
        return data_clean
    except Exception as e:
        st.error(f"Could not load data file: {e}")
        return None

data = load_data()

if data is not None:
    # Show what columns we actually have
    st.write("📋 **Available columns in your data:**", list(data.columns))
    
    # Show basic info
    st.success(f"✅ Successfully loaded data with {len(data)} rows and {len(data.columns)} columns")
    
    # Display the raw data first so we can see what we're working with
    st.subheader("📊 Raw Data Preview")
    
    # Use a try-except for dataframe display
    try:
        st.dataframe(data)
    except Exception as e:
        st.warning(f"Could not display full dataframe: {e}")
        st.write("Showing first 5 rows as text:")
        st.write(data.head())
    
    # Display key metrics - only for columns that exist
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'Total_Piped_Water_Percent' in data.columns:
            try:
                avg_water = pd.to_numeric(data['Total_Piped_Water_Percent'], errors='coerce').mean()
                st.metric("Average Water Access", f"{avg_water:.1f}%")
            except:
                st.metric("Water Access Data", "Check format")
        else:
            st.metric("Data Columns", len(data.columns))
    
    with col2:
        total_rows = len(data)
        st.metric("Total Records", total_rows)
    
    with col3:
        if 'Water_Need_Level' in data.columns:
            try:
                critical_need = len(data[data['Water_Need_Level'] == 'Critical Need'])
                st.metric("Critical Need Areas", critical_need)
            except:
                st.metric("Need Levels", "Check format")
        else:
            st.metric("Numeric Columns", len(data.select_dtypes(include=[np.number]).columns))
    
    with col4:
        if 'Dam_Count' in data.columns:
            try:
                total_dams = pd.to_numeric(data['Dam_Count'], errors='coerce').sum()
                st.metric("Total Dams", int(total_dams))
            except:
                st.metric("Dam Data", "Check format")
        else:
            st.metric("Data Loaded", "✅")
    
    # Create water access chart if we have the data
    if 'Total_Piped_Water_Percent' in data.columns:
        st.subheader("📈 Water Access Visualization")
        
        try:
            # Convert to numeric to ensure plotting works
            water_data = pd.to_numeric(data['Total_Piped_Water_Percent'], errors='coerce')
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Use index if Province column doesn't exist
            if 'Province' in data.columns:
                labels = data['Province']
            else:
                labels = [f"Region {i+1}" for i in range(len(data))]
            
            # Create bar chart
            bars = ax.bar(range(len(water_data)), water_data, alpha=0.7, color='skyblue', edgecolor='black')
            
            ax.set_xlabel('Provinces/Regions')
            ax.set_ylabel('Piped Water Access (%)')
            ax.set_title('Water Access Distribution')
            ax.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Could not create water access chart: {e}")
    
    # Simple data summary
    st.subheader("🔍 Data Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Shape:**", data.shape)
        st.write("**Column Types:**")
        st.write(data.dtypes.value_counts())
    
    with col2:
        st.write("**Missing Values:**")
        missing_data = data.isnull().sum()
        for col, missing in missing_data.items():
            if missing > 0:
                st.write(f"- {col}: {missing} missing")
    
    st.success("🎉 Your Water Infrastructure Planner is working!")
    
else:
    st.info("📝 Please make sure 'water_infrastructure_data.csv' is in the same folder as app.py")

# Add debug info at the bottom
with st.expander("🔧 Debug Information"):
    if data is not None:
        st.write("**First row sample values:**")
        for col in data.columns[:5]:  # Show first 5 columns
            sample_val = data[col].iloc[0] if len(data) > 0 else "No data"
            st.write(f"- {col}: {type(sample_val)} = {sample_val}")
