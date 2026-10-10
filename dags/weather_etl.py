from airflow.sdk import dag, task
from datetime import datetime
import requests
@dag(
    dag_id = "weather_etl",
    start_date = datetime(2026,8,11),
    schedule = "@daily",
    default_args = {"retries": 2},
    catchup=False
)
def weather_etl():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 1,
        "longitude": 114,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset",
                    "daylight_duration", "sunshine_duration", "apparent_temperature_min", 
                    "apparent_temperature_max", "uv_index_clear_sky_max", "uv_index_max", 
                    "showers_sum", "rain_sum", "snowfall_sum", "precipitation_hours", "precipitation_sum", 
                    "precipitation_probability_max", "moonrise", "moonset", "moon_phase", "wind_speed_10m_max", 
                    "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
        "timezone": "auto",
        "forecast_day": 1
    } 
    @task
    def import_api_data():
        try:
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            print(data)
        except requests.exceptions.HTTPError as e:
            print("Http error:", e)
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

    import_api_data()

weather_etl()

