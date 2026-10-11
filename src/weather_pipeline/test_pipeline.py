from extract import fetch_api_weather
from transform import transform_daily_weather
import json

def main():
    latitude = -0.0263
    longitude = 109.3425
    timezone = "Asia/Jakarta" 

    try:
        data = fetch_api_weather(latitude=latitude, longitude=longitude, timezone=timezone)
        transform_data = transform_daily_weather(data=data)
        print(transform_data)
    except Exception as error:
        print("Extract Gagal!")

if __name__ == "__main__":
    main()