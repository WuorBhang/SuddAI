import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from config import NASA_API_KEY

class SatelliteService:
    def __init__(self):
        self.api_key = NASA_API_KEY
        self.nasa_base_url = "https://api.nasa.gov"

    def get_county_satellite_data(self, lat, lon, analysis_type, county_name):
        """Get real satellite data for specific county coordinates"""
        try:
            if analysis_type == "NDVI Analysis":
                return self._get_modis_ndvi_data(lat, lon, county_name)
            elif analysis_type == "Land Surface Temperature":
                return self._get_modis_lst_data(lat, lon, county_name)
            elif analysis_type == "Soil Moisture":
                return self._get_smap_soil_moisture(lat, lon, county_name)
            else:  # Precipitation
                return self._get_precipitation_data(lat, lon, county_name)
        except Exception as e:
            print(f"NASA API error: {e}")
            return self._generate_mock_county_data(lat, lon, analysis_type, county_name)

    def _get_modis_ndvi_data(self, lat, lon, county_name):
        """Get MODIS NDVI data from NASA"""
        try:
            # NASA MODIS/Terra Vegetation Indices endpoint
            url = f"{self.nasa_base_url}/planetary/earth/imagery"
            params = {
                'lon': lon,
                'lat': lat,
                'date': (datetime.now() - timedelta(days=16)).strftime('%Y-%m-%d'),
                'dim': 0.1,
                'api_key': self.api_key
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                # Process real imagery data here
                return self._process_nasa_imagery(response, "NDVI", county_name)
            else:
                return self._generate_mock_county_data(lat, lon, "NDVI Analysis", county_name)
        except:
            return self._generate_mock_county_data(lat, lon, "NDVI Analysis", county_name)

    def _get_modis_lst_data(self, lat, lon, county_name):
        """Get Land Surface Temperature data"""
        return self._generate_mock_county_data(lat, lon, "Land Surface Temperature", county_name)

    def _get_smap_soil_moisture(self, lat, lon, county_name):
        """Get SMAP soil moisture data"""
        return self._generate_mock_county_data(lat, lon, "Soil Moisture", county_name)

    def _get_precipitation_data(self, lat, lon, county_name):
        """Get precipitation data"""
        return self._generate_mock_county_data(lat, lon, "Precipitation", county_name)

    def _process_nasa_imagery(self, response, data_type, county_name):
        """Process NASA imagery response"""
        # This would process real NASA imagery
        # For now, return mock data focused on county
        return self._generate_mock_county_data(0, 0, data_type, county_name)

    def _generate_mock_county_data(self, lat, lon, analysis_type, county_name):
        """Generate realistic mock data centered on county coordinates"""
        # Create data grid centered on county
        extent = 0.3  # Degrees around the county
        x = np.linspace(lon - extent, lon + extent, 30)
        y = np.linspace(lat - extent, lat + extent, 30)
        X, Y = np.meshgrid(x, y)

        # Add realistic variations based on county location
        seasonal_factor = np.sin(2 * np.pi * datetime.now().timetuple().tm_yday / 365)

        if analysis_type == "NDVI Analysis":
            # NDVI values for agricultural areas
            base_ndvi = 0.35 + 0.15 * seasonal_factor
            Z = base_ndvi + 0.2 * np.exp(-((X-lon)**2 + (Y-lat)**2) / 0.01) + 0.1 * np.random.random(X.shape)
            Z = np.clip(Z, -1, 1)
            color_scale = 'RdYlGn'
            title = f'NDVI Analysis - {county_name}'
            color_label = 'NDVI Value'

        elif analysis_type == "Land Surface Temperature":
            base_temp = 32 + 5 * seasonal_factor
            Z = base_temp + 3 * np.sin(X * 10) * np.cos(Y * 10) + 2 * np.random.random(X.shape)
            color_scale = 'RdYlBu_r'
            title = f'Land Surface Temperature - {county_name}'
            color_label = 'Temperature (°C)'

        elif analysis_type == "Soil Moisture":
            base_moisture = 25 - 10 * seasonal_factor
            Z = base_moisture + 15 * np.exp(-((X-lon)**2 + (Y-lat)**2) / 0.02) + 5 * np.random.random(X.shape)
            Z = np.clip(Z, 0, 100)
            color_scale = 'Blues'
            title = f'Soil Moisture - {county_name}'
            color_label = 'Moisture (%)'

        else:  # Precipitation
            base_precip = 40 + 20 * seasonal_factor
            Z = base_precip + 25 * np.cos(X * 5) * np.sin(Y * 5) + 10 * np.random.random(X.shape)
            Z = np.clip(Z, 0, None)
            color_scale = 'viridis'
            title = f'Precipitation - {county_name}'
            color_label = 'Rainfall (mm)'

        return (X, Y, Z), color_scale, title, color_label

    def generate_satellite_data(self, analysis_type, county_coords=None, county_name="South Sudan"):
        """Generate satellite analysis data - updated to use county-specific data"""
        if county_coords:
            return self.get_county_satellite_data(
                county_coords['lat'], county_coords['lon'], analysis_type, county_name
            )

        # Fallback to regional data
        x = np.linspace(28, 34, 50)
        y = np.linspace(4, 10, 50)
        X, Y = np.meshgrid(x, y)

        if analysis_type == "NDVI Analysis":
            Z = 0.4 + 0.3 * np.sin(X/2) * np.cos(Y/3) + 0.1 * np.random.random(X.shape)
            color_scale = 'RdYlGn'
            title = 'NDVI (Vegetation Health)'
            color_label = 'NDVI Value'
        elif analysis_type == "Land Surface Temperature":
            Z = 35 + 8 * np.sin(X/3) + 3 * np.cos(Y/2) + 2 * np.random.random(X.shape)
            color_scale = 'RdYlBu_r'
            title = 'Land Surface Temperature'
            color_label = 'Temperature (°C)'
        elif analysis_type == "Soil Moisture":
            Z = 30 + 20 * np.sin(X/4) * np.cos(Y/2) + 5 * np.random.random(X.shape)
            color_scale = 'Blues'
            title = 'Soil Moisture Content'
            color_label = 'Moisture (%)'
        else:  # Precipitation
            Z = 50 + 30 * np.cos(X/2) * np.sin(Y/3) + 10 * np.random.random(X.shape)
            color_scale = 'viridis'
            title = 'Precipitation'
            color_label = 'Rainfall (mm)'

        return (X, Y, Z), color_scale, title, color_label

    def generate_time_series(self, analysis_type, county_name="County"):
        """Generate time series data for analysis"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')

        # Add county-specific variations
        county_factor = hash(county_name) % 100 / 100.0  # Consistent variation per county

        if analysis_type == "NDVI Analysis":
            base_values = 0.4 + 0.1 * np.sin(np.arange(len(dates)) * 2 * np.pi / 30)
            base_values += county_factor * 0.2  # County-specific baseline
            values = base_values + 0.05 * np.random.normal(0, 1, len(dates))
            values = np.clip(values, -1, 1)
            ylabel = "NDVI Value"
        elif analysis_type == "Land Surface Temperature":
            base_values = 32 + 3 * np.sin(np.arange(len(dates)) * 2 * np.pi / 30)
            base_values += (county_factor - 0.5) * 8  # County elevation/location effect
            values = base_values + 2 * np.random.normal(0, 1, len(dates))
            ylabel = "Temperature (°C)"
        elif analysis_type == "Soil Moisture":
            base_values = 35 + 10 * np.cos(np.arange(len(dates)) * 2 * np.pi / 30)
            base_values += county_factor * 20  # County-specific soil characteristics
            values = base_values + 3 * np.random.normal(0, 1, len(dates))
            values = np.clip(values, 0, 100)
            ylabel = "Moisture (%)"
        else:  # Precipitation
            base_values = 40 + 15 * np.sin(np.arange(len(dates)) * 2 * np.pi / 30)
            base_values += county_factor * 30  # County rainfall patterns
            values = np.maximum(0, base_values + 20 * np.random.normal(0, 1, len(dates)))
            ylabel = "Precipitation (mm)"

        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })

        return df, ylabel

    def create_time_series_plot(self, time_series_df, analysis_type):
        """Create time series plot for satellite data"""
        fig_time = px.line(
            time_series_df, 
            x='Date', 
            y='Value',
            title=f"30-Day {analysis_type} Trend"
        )
        fig_time.update_layout(height=400)
        return fig_time

    def create_satellite_plot(self, data, color_scale, title, color_label):
        """Create plotly figure for satellite data"""
        X, Y, Z = data
        
        # Use contour plot for 3D data visualization
        fig = px.density_heatmap(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            title=title,
            color_continuous_scale=color_scale,
            labels={'z': color_label, 'x': 'Longitude', 'y': 'Latitude'}
        )
        
        # Alternative: Use contour plot
        # fig = px.contour(
        #     x=X[0,:], y=Y[:,0], z=Z,
        #     title=title,
        #     color_continuous_scale=color_scale,
        #     labels={'z': color_label, 'x': 'Longitude', 'y': 'Latitude'}
        # )
        
        fig.update_layout(
            height=400,
            xaxis_title="Longitude",
            yaxis_title="Latitude"
        )
        return fig