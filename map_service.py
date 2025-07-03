import folium
from streamlit_folium import st_folium
import plotly.express as px
from config import MAP_HEIGHT, MAP_WIDTH, DEFAULT_ZOOM, COUNTY_ZOOM, SOUTH_SUDAN_CENTER

class MapService:
    def __init__(self):
        self.default_height = MAP_HEIGHT
        self.default_width = MAP_WIDTH
        self.default_zoom = DEFAULT_ZOOM
        self.county_zoom = COUNTY_ZOOM

    def create_location_map(self, coords, county_name, state_name, all_counties, risk_color):
        """Create map centered on selected location with enhanced features"""
        # Create map centered on the county with higher zoom
        m = folium.Map(
            location=[coords['lat'], coords['lon']],
            zoom_start=self.county_zoom,
            tiles='OpenStreetMap'
        )

        # Add prominent marker for selected county
        folium.Marker(
            [coords['lat'], coords['lon']],
            popup=f"""
            <div style='width: 200px;'>
                <h4 style='color: #333; margin: 0;'>{county_name}</h4>
                <hr style='margin: 5px 0;'>
                <p style='margin: 2px 0;'><b>State:</b> {state_name}</p>
                <p style='margin: 2px 0;'><b>Coordinates:</b></p>
                <p style='margin: 2px 0; font-size: 12px;'>
                    Lat: {coords['lat']:.4f}<br>
                    Lon: {coords['lon']:.4f}
                </p>
            </div>
            """,
            tooltip=f"🏠 {county_name}, {state_name}",
            icon=folium.Icon(
                color=risk_color, 
                icon='map-marker',
                prefix='fa'
            )
        ).add_to(m)

        # Add smaller markers for other counties in the state
        for other_county, other_coords in all_counties.items():
            if other_county != county_name:
                folium.CircleMarker(
                    [other_coords['lat'], other_coords['lon']],
                    radius=4,
                    popup=f"""
                    <div style='width: 150px;'>
                        <h5 style='margin: 0;'>{other_county}</h5>
                        <p style='margin: 2px 0; font-size: 11px;'>
                            {other_coords['lat']:.3f}, {other_coords['lon']:.3f}
                        </p>
                    </div>
                    """,
                    tooltip=f"{other_county}",
                    color='darkblue',
                    fill=True,
                    fillColor='lightblue',
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)

        # Add a circle around the selected county for emphasis
        folium.Circle(
            [coords['lat'], coords['lon']],
            radius=5000,  # 5km radius
            popup=f"{county_name} - 5km radius",
            color=risk_color,
            weight=2,
            fill=False,
            opacity=0.8
        ).add_to(m)

        return m

    def create_regional_map(self, df):
        """Create regional temperature distribution map"""
        fig_map = px.scatter_map(
            df,
            lat='Latitude',
            lon='Longitude',
            color='Temperature',
            size='Confidence',
            hover_name='County',
            hover_data=['State', 'Risk_Level'],
            color_continuous_scale='RdYlBu_r',
            zoom=5,
            center=SOUTH_SUDAN_CENTER,
            title="Temperature Distribution Across South Sudan"
        )
        fig_map.update_layout(height=600)
        return fig_map

    def render_map(self, map_obj, height=None, width=None):
        """Render folium map with streamlit"""
        return st_folium(
            map_obj, 
            width=width or self.default_width, 
            height=height or self.default_height
        )