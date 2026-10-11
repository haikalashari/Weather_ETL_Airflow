from airflow.sdk import dag, task
from datetime import datetime
@dag(
    dag_id = "weather_etl",
    start_date = datetime(2026,8,11),
    schedule = "@daily",
    default_args = {"retries": 2},
    catchup=False
)
def weather_etl():

weather_etl()

