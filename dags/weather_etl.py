from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from src.weather_pipeline.extract import fetch_api_weather
from src.weather_pipeline.load import save_weather_data
from src.weather_pipeline.transform import transform_daily_weather
from src.weather_pipeline.validate import validate_data_daily
from datetime import datetime
from uuid import uuid4


@dag(
    dag_id = "weather_etl",
    start_date = datetime(2026,8,11),
    schedule = "@daily",
    default_args = {"retries": 2},
    catchup=False
)
def weather_etl():
    @task
    def read_location():
        hook = PostgresHook(
            postgres_conn_id = "weather_supabase"
        )
        sql = """
            SELECT
                location_code,
                latitude,
                longitude,
                timezone
            FROM 
                dim_location
            ORDER BY
                location_id;
            """
        rows = hook.get_records(sql)
        return [
            {
                "location_code": row[0],
                "latitude": row[1],
                "longitude": row[2],
                "timezone": row[3]
            }
            for row in rows
        ]

    @task
    def extract_weather_data(locations):
        extracted_data = []
        for location in locations:
            payload = fetch_api_weather(latitude=location["latitude"], longitude=location["longitude"], timezone=location["timezone"])

            extracted_data.append({
                "location_code": location["location_code"],
                "payload": payload,
            })
        return extracted_data
    @task
    def transform_weather_data(data):
        transform_data = []
        
        for item in data:
            location_code = item["location_code"]
            payload = item["payload"]
            records = transform_daily_weather(payload)

            transform_data.append({
                "location_code": location_code,
                "records": records
            })
        return transform_data
    @task
    def validate_weather_date(data):
        for item in data:
            records = item["records"]

            validate_data_daily(records)
        return data
    @task
    def load_weather_data(data):
        run_id = str(uuid4())
        for item in data:
            location_code = item["location_code"]
            payload = item["payload"]
            records = item["records"]

            save_weather_data(
                location_code=location_code,
                run_id=run_id,
                payload=payload,
                records=records,
            )



    locations = read_location()
    weather_data = extract_weather_data(locations)
    records_data = transform_weather_data(weather_data)
    validated_data = validate_weather_date(records_data)
    load_data = load_weather_data(validated_data)

weather_etl()

