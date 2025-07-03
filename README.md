
# 🌱 SuddAI - AgriWatch AI for South Sudan

![SuddAI Screenshot](https://via.placeholder.com/800x400?text=SuddAI+Screenshot) *(Replace with actual screenshot)*

An AI-powered agricultural monitoring system providing early warnings and intelligence for South Sudanese farmers and policymakers.

## 🌟 Features

- Real-time weather monitoring across all South Sudan counties
- AI-powered anomaly detection (droughts, floods, extreme weather)
- Satellite imagery analysis (NDVI, land temperature, soil moisture)
- Farming advisories based on weather predictions
- Policy dashboard for regional overviews

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- API keys (NASA, OpenWeatherMap)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WuorBhang/SuddAI.git
   cd suddai
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

Create a `.env` file:
```ini
NASA_API_KEY=your_nasa_api_key
OPENWEATHER_API_KEY=your_openweather_key
MAPBOX_ACCESS_TOKEN=your_mapbox_token
STREAMLIT_DISABLE_EMAIL=1
```

### Running Locally
```bash
streamlit run main.py
```
The app will be available at [http://localhost:8501](http://localhost:8501)

## 🌍 Deployment Options

### 1. Streamlit Community Cloud (Recommended)
- Push your code to GitHub
- Go to Streamlit Community Cloud
- Click "New App" and connect your repository
- Set:
  - Main file path: `main.py`
  - Branch: `main`

### 2. Docker Deployment
```bash
docker build -t suddai .
docker run -p 8501:8501 suddai
```

## 📂 Project Structure

```
suddai/
├── main.py               # Main application
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── config.py             # Configuration settings
├── data.py               # County geographic data
├── map_service.py        # Mapping functionality
├── satellite_service.py  # Satellite data processing
├── ui_components.py      # UI elements
└── weather_service.py    # Weather data processing
```

## 🔐 API Keys Required

| Service        | How to Get             |
|----------------|------------------------|
| NASA GIBS      | api.nasa.gov           |
| OpenWeatherMap | openweathermap.org     |
| Mapbox         | mapbox.com             |

## 🤝 Contributing

1. Fork the project  
2. Create your feature branch  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes  
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. Push to the branch  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request  

## 📜 License

Distributed under the MIT License. See LICENSE for more information.

## 📧 Contact

Project Maintainer - Wuor Bhang
