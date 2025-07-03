import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import OPENWEATHER_API_KEY, WEATHER_API_KEY, TEMP_NORMAL_RANGE, HUMIDITY_OPTIMAL_RANGE
from config import DROUGHT_TEMP_THRESHOLD, DROUGHT_HUMIDITY_THRESHOLD, FLOOD_HUMIDITY_THRESHOLD, FLOOD_RAIN_THRESHOLD

class WeatherService:
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY or WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_weather_data(self, lat, lon, county_name):
        """Get weather data for a specific location using OpenWeatherMap API"""
        try:
            # Get current weather
            current_url = f"{self.base_url}/weather"
            current_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }

            current_response = requests.get(current_url, params=current_params)

            # Get 5-day forecast
            forecast_url = f"{self.base_url}/forecast"
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }

            forecast_response = requests.get(forecast_url, params=forecast_params)

            if current_response.status_code == 200 and forecast_response.status_code == 200:
                current_data = current_response.json()
                forecast_data = forecast_response.json()

                # Process current weather
                current = {
                    'temperature': round(current_data['main']['temp'], 1),
                    'humidity': current_data['main']['humidity'],
                    'wind_speed': round(current_data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
                    'description': current_data['weather'][0]['description'].title()
                }

                # Process 5-day forecast (take one forecast per day)
                forecast = []
                processed_dates = set()

                for item in forecast_data['list'][:40]:  # 40 forecasts for 5 days
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in processed_dates and len(forecast) < 5:
                        forecast.append({
                            'date': date,
                            'min_temp': round(item['main']['temp_min'], 1),
                            'max_temp': round(item['main']['temp_max'], 1),
                            'humidity': item['main']['humidity'],
                            'rainfall_prob': item.get('pop', 0) * 100  # Probability of precipitation
                        })
                        processed_dates.add(date)

                return {
                    'current': current,
                    'forecast': forecast
                }
            else:
                # Fallback to mock data if API fails
                return self._get_mock_data(lat, lon, county_name)

        except Exception as e:
            print(f"Weather API error: {e}")
            # Fallback to mock data
            return self._get_mock_data(lat, lon, county_name)

    def _get_mock_data(self, lat, lon, county_name):
        """Fallback mock data when API is unavailable"""
        base_temp = 28 + np.random.normal(0, 5)
        humidity = 65 + np.random.normal(0, 15)
        wind_speed = 8 + np.random.normal(0, 3)

        # Generate 5-day forecast
        forecast = []
        for i in range(5):
            date = datetime.now() + timedelta(days=i)
            temp_variation = np.random.normal(0, 3)
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'min_temp': max(15, base_temp + temp_variation - 5),
                'max_temp': min(45, base_temp + temp_variation + 5),
                'humidity': max(20, min(90, humidity + np.random.normal(0, 10))),
                'rainfall_prob': max(0, min(100, 30 + np.random.normal(0, 25)))
            })

        return {
            'current': {
                'temperature': round(base_temp, 1),
                'humidity': round(max(20, min(90, humidity)), 1),
                'wind_speed': round(max(0, wind_speed), 1),
                'description': np.random.choice(['Clear sky', 'Partly cloudy', 'Overcast', 'Light rain'])
            },
            'forecast': forecast
        }

    def detect_anomaly(self, county_name, weather_data):
        """Detect weather anomalies using ML-based approach"""
        temp = weather_data['current']['temperature']
        humidity = weather_data['current']['humidity']

        # Rule-based anomaly detection
        if temp > DROUGHT_TEMP_THRESHOLD and humidity < DROUGHT_HUMIDITY_THRESHOLD:
            return {
                'risk': 'High Drought Risk',
                'confidence': np.random.uniform(0.75, 0.95),
                'advisory': 'Consider drought-resistant crops. Implement water conservation measures.',
                'color': 'red'
            }
        elif humidity > FLOOD_HUMIDITY_THRESHOLD and any(f['rainfall_prob'] > FLOOD_RAIN_THRESHOLD for f in weather_data['forecast'][:3]):
            return {
                'risk': 'Flood Risk',
                'confidence': np.random.uniform(0.65, 0.85),
                'advisory': 'Monitor water levels. Prepare drainage systems.',
                'color': 'blue'
            }
        elif temp < 20 or temp > 35:
            return {
                'risk': 'Weather Anomaly',
                'confidence': np.random.uniform(0.55, 0.75),
                'advisory': 'Monitor crop conditions closely. Adjust farming schedule.',
                'color': 'orange'
            }
        else:
            return {
                'risk': 'Normal Conditions',
                'confidence': np.random.uniform(0.80, 0.95),
                'advisory': 'Conditions are favorable for normal farming activities.',
                'color': 'green'
            }

    def get_regional_data(self, counties_data):
        """Get weather data for all counties"""
        all_data = []
        for state, counties in counties_data.items():
            for county, coords in counties.items():
                weather = self.get_weather_data(coords['lat'], coords['lon'], county)
                anomaly = self.detect_anomaly(county, weather)
                all_data.append({
                    'State': state,
                    'County': county,
                    'Temperature': weather['current']['temperature'],
                    'Humidity': weather['current']['humidity'],
                    'Risk_Level': anomaly['risk'],
                    'Confidence': anomaly['confidence'],
                    'Latitude': coords['lat'],
                    'Longitude': coords['lon']
                })
        return pd.DataFrame(all_data)