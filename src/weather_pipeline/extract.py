import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "rain_sum",
    "precipitation_sum",
    "precipitation_probability_max",
    "wind_speed_10m_max",
    "wind_direction_10m_dominant",
]

def fetch_api_weather(latitude, longitude, timezone):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": DAILY_VARIABLES,
        "timezone": timezone,
        "forecast_days": 7
        }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "daily" not in data:
        raise ValueError("API response does not contain data")

    return data