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
    @task
    def import_api_data():

    import_api_data()

weather_etl()

