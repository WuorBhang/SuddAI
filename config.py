
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys (to be stored in .env file)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')  # Alternative name
NASA_API_KEY = os.getenv('NASA_API_KEY', '')
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN', '')

# App Configuration
APP_TITLE = "AgriWatch - South Sudan Weather Monitoring"
APP_ICON = "🌾"
DEFAULT_STATE = "Central Equatoria"
DEFAULT_COUNTY = "Juba"

# Map Configuration
MAP_HEIGHT = 800  # Increased height
MAP_WIDTH = 1000  # Increased width
DEFAULT_ZOOM = 8
COUNTY_ZOOM = 12  # Much closer zoom for individual counties
SOUTH_SUDAN_CENTER = {"lat": 7.0, "lon": 30.0}

# Weather thresholds
TEMP_NORMAL_RANGE = (20, 35)
HUMIDITY_OPTIMAL_RANGE = (40, 70)
DROUGHT_TEMP_THRESHOLD = 38
DROUGHT_HUMIDITY_THRESHOLD = 30
FLOOD_HUMIDITY_THRESHOLD = 80
FLOOD_RAIN_THRESHOLD = 70
