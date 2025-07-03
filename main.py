import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Import our custom modules
from config import APP_TITLE, APP_ICON, DEFAULT_STATE, DEFAULT_COUNTY, MAP_HEIGHT, MAP_WIDTH
from data import SOUTH_SUDAN_COUNTIES
from weather_service import WeatherService
from satellite_service import SatelliteService
from map_service import MapService
from ui_components import UIComponents

# Disable Streamlit email requirement
os.environ['STREAMLIT_DISABLE_EMAIL'] = '1'

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
weather_service = WeatherService()
satellite_service = SatelliteService()
map_service = MapService()
ui = UIComponents()

def main():
    # Render header
    ui.render_header("SuddAi - an AgriWatch ai for South Sudan",
    subtitle="Early warning and agri-intelligence for South Sudanese farmers and policymakers")

    # Sidebar
    st.sidebar.header("📍 Location Selection")

    # State and county selection
    selected_state = st.sidebar.selectbox(
        "Select State:",
        list(SOUTH_SUDAN_COUNTIES.keys()),
        index=list(SOUTH_SUDAN_COUNTIES.keys()).index(DEFAULT_STATE)
    )

    selected_county = st.sidebar.selectbox(
        "Select County:",
        list(SOUTH_SUDAN_COUNTIES[selected_state].keys()),
        index=0
    )

    # Show county info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Info")
    coords = SOUTH_SUDAN_COUNTIES[selected_state][selected_county]
    st.sidebar.markdown(f"**Coordinates:** {coords['lat']:.3f}, {coords['lon']:.3f}")
    st.sidebar.markdown(f"**Counties in {selected_state}:** {len(SOUTH_SUDAN_COUNTIES[selected_state])}")
    st.sidebar.markdown(f"**Total Counties:** {sum(len(counties) for counties in SOUTH_SUDAN_COUNTIES.values())}")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "🛰️ Satellite View", "📊 Policy Dashboard", "ℹ️ About"])

    with tab1:
        render_dashboard_tab(selected_state, selected_county, coords)

    with tab2:
        render_satellite_tab(selected_county, selected_state)

    with tab3:
        render_policy_tab()

    with tab4:
        render_about_tab()

def render_dashboard_tab(selected_state, selected_county, coords):
    """Render the main dashboard tab"""
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Weather Monitor - {selected_county}, {selected_state}")

        # Get weather data
        weather_data = weather_service.get_weather_data(coords['lat'], coords['lon'], selected_county)
        anomaly = weather_service.detect_anomaly(selected_county, weather_data)

        # Current weather metrics
        st.markdown("### 🌤️ Current Conditions")
        ui.render_weather_metrics(weather_data)

        # Anomaly detection
        st.markdown("### 🔍 Anomaly Detection")
        ui.render_anomaly_card(anomaly)

        # Forecast charts
        st.markdown("### 📅 5-Day Forecast")

        # Temperature forecast
        fig_temp = ui.render_forecast_chart(weather_data['forecast'])
        st.plotly_chart(fig_temp, use_container_width=True)

        # Rainfall probability
        fig_rain = ui.render_rainfall_chart(weather_data['forecast'])
        st.plotly_chart(fig_rain, use_container_width=True)

    with col2:
        st.subheader("🗺️ Location Map")

        # Create and render map with increased size
        m = map_service.create_location_map(
            coords, selected_county, selected_state, 
            SOUTH_SUDAN_COUNTIES[selected_state], anomaly['color']
        )
        map_service.render_map(m, height=MAP_HEIGHT, width=MAP_WIDTH)

        # Farming advisory
        st.markdown("### 🌱 Farming Advisory")
        st.info(anomaly['advisory'])

        # Quick stats
        st.markdown("### 📈 Quick Stats")
        forecast_data = weather_data['forecast']
        avg_temp = np.mean([(f['max_temp'] + f['min_temp']) / 2 for f in forecast_data])
        avg_humidity = np.mean([f['humidity'] for f in forecast_data])
        total_rain_prob = np.mean([f['rainfall_prob'] for f in forecast_data])

        st.metric("Avg Temperature (5-day)", f"{avg_temp:.1f}°C")
        st.metric("Avg Humidity (5-day)", f"{avg_humidity:.1f}%")
        st.metric("Avg Rain Probability", f"{total_rain_prob:.1f}%")

def render_satellite_tab(selected_county, selected_state):
    """Render satellite analysis tab"""
    st.subheader(f"🛰️ Satellite Image Analysis - {selected_county}, {selected_state}")
    st.info(f"Real-time satellite imagery analysis for {selected_county} county")

    # Controls
    col_control, col_info = st.columns([3, 1])

    with col_control:
        analysis_type = st.selectbox(
            "Select Analysis Type:",
            ["NDVI Analysis", "Land Surface Temperature", "Soil Moisture", "Precipitation"]
        )

        date_range = st.date_input(
            "Select Date Range:",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )

    with col_info:
        st.markdown("### 📊 Analysis Info")
        info_messages = {
            "NDVI Analysis": ("🌱 Vegetation Health: Good", "NDVI values > 0.3 indicate healthy vegetation"),
            "Land Surface Temperature": ("🌡️ Temperature: Elevated", "Monitor for heat stress conditions"),
            "Soil Moisture": ("💧 Moisture: Low", "Consider irrigation recommendations"),
            "Precipitation": ("🌧️ Precipitation: Normal", "Recent rainfall detected")
        }

        status, info = info_messages.get(analysis_type, ("", ""))
        if "Good" in status or "Normal" in status:
            st.success(status)
        elif "Elevated" in status:
            st.warning(status)
        else:
            st.error(status)
        st.info(info)

    # Satellite visualization
    st.markdown(f"### {analysis_type} for {selected_county}")

    col1, col2 = st.columns(2)

    with col1:
        # Generate and display satellite data for selected county
        coords = SOUTH_SUDAN_COUNTIES[selected_state][selected_county]
        data, color_scale, title, color_label = satellite_service.generate_satellite_data(
            analysis_type, coords, selected_county
        )
        fig = satellite_service.create_satellite_plot(data, color_scale, title, color_label)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Time series analysis
        st.markdown(f"### 📈 Temporal Analysis - {selected_county}")
        time_series_df, ylabel = satellite_service.generate_time_series(analysis_type, selected_county)

        fig_time = satellite_service.create_time_series_plot(time_series_df, analysis_type)
        st.plotly_chart(fig_time, use_container_width=True)

def render_policy_tab():
    """Render policy dashboard tab"""
    st.subheader("📊 Policy Dashboard - Regional Overview")
    st.markdown("*Aggregated data for policymakers and government officials*")

    # Get regional data
    df = weather_service.get_regional_data(SOUTH_SUDAN_COUNTIES)

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        high_risk = len(df[df['Risk_Level'].str.contains('High|Flood')])
        st.metric("High Risk Counties", high_risk, delta=f"{high_risk/len(df)*100:.1f}%")

    with col2:
        avg_temp = df['Temperature'].mean()
        st.metric("Average Temperature", f"{avg_temp:.1f}°C")

    with col3:
        avg_humidity = df['Humidity'].mean()
        st.metric("Average Humidity", f"{avg_humidity:.1f}%")

    with col4:
        anomaly_count = len(df[df['Risk_Level'] != 'Normal Conditions'])
        st.metric("Counties with Anomalies", anomaly_count)

    # Risk distribution chart
    st.markdown("### Risk Distribution by State")
    risk_counts = df.groupby(['State', 'Risk_Level']).size().reset_index(name='Count')
    fig_risk = ui.render_risk_distribution_chart(risk_counts)
    st.plotly_chart(fig_risk, use_container_width=True)

    # Regional map
    st.markdown("### Temperature Distribution Map")
    fig_map = map_service.create_regional_map(df)
    st.plotly_chart(fig_map, use_container_width=True)

    # Data table
    st.markdown("### Detailed County Data")
    st.dataframe(df.round(2), use_container_width=True)

def render_about_tab():
    """Render about tab"""
    st.subheader("ℹ️ About AgriWatch")

    st.markdown("""
    ### 🎯 Mission
    SuddAI is an AgriWatch designed ai that will help farmers and policymakers in South Sudan by providing early warning systems for weather anomalies that could impact agriculture.

    ### 🔧 Features
    - **Real-time Weather Monitoring**: Current conditions and 5-day forecasts for all South Sudan counties
    - **AI-Powered Anomaly Detection**: Machine learning algorithms detect drought, flood, and extreme weather risks
    - **Satellite Image Analysis**: NDVI and land surface temperature monitoring
    - **Farming Advisory System**: Localized recommendations based on weather predictions
    - **Policy Dashboard**: Aggregated regional data for government decision-making

    ### 📍 Coverage
    AgriWatch monitors **{total_counties}** counties across **{total_states}** states in South Sudan:
    """.format(
        total_counties=sum(len(counties) for counties in SOUTH_SUDAN_COUNTIES.values()),
        total_states=len(SOUTH_SUDAN_COUNTIES)
    ))

    for state, counties in SOUTH_SUDAN_COUNTIES.items():
        st.markdown(f"**{state}**: {', '.join(counties.keys())}")

    st.markdown("""
    ### 🛠️ Technology Stack
    - **Frontend**: Streamlit
    - **Maps**: Folium, Plotly
    - **Data APIs**: NASA GIBS, OpenWeatherMap, Mapbox
    - **ML Framework**: Scikit-learn, TensorFlow
    - **Deployment**: Vercel, Streamlit Cloud

    ### 📧 Contact
    For technical support or partnership opportunities, please contact the development team.
    """)

if __name__ == "__main__":
    main()