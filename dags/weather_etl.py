from airflow.sdk import dag, task
from datetime import datetime

@dag(
    start_date = datetime(2026,8,11),
    schedule = "@daily",
)
def weather_etl():
    @task
    def import_data():
        return {
            "city": "Pontianak",
            "temperature": "80",
            "humidity": "30"
        }
    @task
    def transform_data(data):
        print (data)
        return {
            "city": data["city"],
            "temperature": data["temperature"]
        }

    data_load = import_data()
    display_data = transform_data(data_load)

weather_etl()

