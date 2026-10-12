from airflow.providers.postgres.hooks.postgres import PostgresHook
import json

def load_weather_data(location_code, run_id, payload, records):

    try:
        pg_hook = PostgresHook(postgres_conn_id = "weather_supabase")
        status, message = pg_hook.test_connection()
        conn = pg_hook.get_conn()
        if not status:
            raise ValueError(f"Database Connection is down {message}")
        print("Connection Check Pass!")
        print("Loading the data")
        
        with conn.cursor() as cursor:
            #Ambil Location_id sesuai dengan location_code yang dipakai
            location_query = "SELECT location_id FROM dim_location WHERE location_code = %s;"
            cursor.execute(location_query, (location_code,))
            fetch_location = cursor.fetchone()

            if not fetch_location:
                raise ValueError("Location is not in the database")

            location_id = fetch_location[0]

            #Raw data insert dari payload ke tabel raw data
            payload_query = """
                            INSERT INTO raw_weather_responses (run_id, location_id, payload)
                            VALUES (%s, %s, %s::jsonb)
                            RETURNING response_id;
                            """
            cursor.execute(payload_query, (run_id, location_id, json.dumps(payload)))
            insert_raw_data = cursor.fetchone()
            if not insert_raw_data:
                raise ValueError("Raw data fail to load")
            response_id = insert_raw_data[0]
            print("Raw data succesfully load")
        

            #Records daily forecast insert ke tabel facts
            facts_query =   """
                            INSERT INTO fact_daily_forecast (
                            location_id,
                            run_id,
                            source_response_id,
                            forecast_date,
                            weather_code,
                            temperature_2m_max,
                            temperature_2m_min,
                            apparent_temperature_max,
                            apparent_temperature_min,
                            rain_sum,
                            precipitation_sum,
                            precipitation_probability_max,
                            wind_speed_10m_max,
                            wind_direction_10m_dominant
                            )
                            VALUES (
                            %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s
                            )
                            ON CONFLICT (location_id, run_id, forecast_date)
                            DO NOTHING;
                            """
            for record in records:
                row_data = (
                    location_id,
                    run_id,
                    response_id,
                    record["forecast_date"],
                    record["weather_code"],
                    record["temperature_2m_max"],
                    record["temperature_2m_min"],
                    record["apparent_temperature_max"],
                    record["apparent_temperature_min"],
                    record["rain_sum"],
                    record["precipitation_sum"],
                    record["precipitation_probability_max"],
                    record["wind_speed_10m_max"],
                    record["wind_direction_10m_dominant"]
                )

                cursor.execute(facts_query, row_data)
                #raise error disini jika fail pg_hooknya maka auto
            
            conn.commit()
            print("Forecast daily data load complete")
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
        
        