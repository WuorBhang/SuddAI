
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from config import TEMP_NORMAL_RANGE, HUMIDITY_OPTIMAL_RANGE

class UIComponents:
    def __init__(self):
        self.setup_custom_css()
    
    def setup_custom_css(self):
        """Setup custom CSS styling"""
        st.markdown("""
        <style>
            .main-header {
                background: linear-gradient(90deg, #2E8B57, #228B22);
                padding: 1rem;
                border-radius: 10px;
                color: white;
                text-align: center;
                margin-bottom: 2rem;
            }
            .metric-card {
                background: white;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-left: 4px solid #2E8B57;
            }
            .risk-card {
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
            .sidebar .sidebar-content {
                background: linear-gradient(180deg, #f0f8f0, #e8f5e8);
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 24px;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: #f0f8f0;
                border-radius: 8px 8px 0px 0px;
                padding-left: 20px;
                padding-right: 20px;
            }
            .stTabs [aria-selected="true"] {
                background-color: #2E8B57;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self, title, subtitle):
        """Render main header"""
        st.markdown(f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p style="margin: 0; font-size: 1.2em;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_weather_metrics(self, weather_data):
        """Render weather metrics cards"""
        cols = st.columns(4)
        
        with cols[0]:
            temp = weather_data['current']['temperature']
            delta_text = 'Normal' if TEMP_NORMAL_RANGE[0] <= temp <= TEMP_NORMAL_RANGE[1] else 'Extreme'
            st.metric("Temperature", f"{temp}°C", delta=delta_text)
        
        with cols[1]:
            humidity = weather_data['current']['humidity']
            delta_text = 'Optimal' if HUMIDITY_OPTIMAL_RANGE[0] <= humidity <= HUMIDITY_OPTIMAL_RANGE[1] else 'Alert'
            st.metric("Humidity", f"{humidity}%", delta=delta_text)
        
        with cols[2]:
            st.metric("Wind Speed", f"{weather_data['current']['wind_speed']} km/h")
        
        with cols[3]:
            st.metric("Condition", weather_data['current']['description'])
    
    def render_anomaly_card(self, anomaly):
        """Render anomaly detection card"""
        risk_color = anomaly['color']
        bg_color = {
            'red': '#ffebee',
            'blue': '#e3f2fd',
            'orange': '#fff3e0',
            'green': '#e8f5e8'
        }.get(risk_color, '#f5f5f5')
        
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 10px; border-left: 5px solid {risk_color}; background-color: {bg_color};">
            <h4 style="margin: 0; color: {risk_color};">{anomaly['risk']}</h4>
            <p style="margin: 5px 0;"><strong>Confidence:</strong> {anomaly['confidence']:.1%}</p>
            <p style="margin: 5px 0;"><strong>Advisory:</strong> {anomaly['advisory']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_forecast_chart(self, forecast_data):
        """Render temperature forecast chart"""
        forecast_df = pd.DataFrame(forecast_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['max_temp'],
            mode='lines+markers',
            name='Max Temp',
            line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['min_temp'],
            mode='lines+markers',
            name='Min Temp',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title='5-Day Temperature Forecast',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            height=400
        )
        return fig
    
    def render_rainfall_chart(self, forecast_data):
        """Render rainfall probability chart"""
        forecast_df = pd.DataFrame(forecast_data)
        
        fig = px.bar(
            forecast_df,
            x='date',
            y='rainfall_prob',
            title='Rainfall Probability (%)',
            color='rainfall_prob',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=300)
        return fig
    
    def render_risk_distribution_chart(self, risk_counts):
        """Render risk distribution chart"""
        fig = px.bar(
            risk_counts,
            x='State',
            y='Count',
            color='Risk_Level',
            title="Weather Risk Distribution Across States",
            barmode='stack',
            color_discrete_map={
                'Normal Conditions': '#2E8B57',
                'Weather Anomaly': '#FFA500', 
                'High Drought Risk': '#DC143C',
                'Flood Risk': '#4169E1'
            }
        )
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=500)
        return fig
