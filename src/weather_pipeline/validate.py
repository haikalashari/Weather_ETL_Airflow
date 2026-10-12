from src.weather_pipeline.extract import DAILY_VARIABLES
from datetime import datetime

def validate_data_daily(records):
    
    if not records:
        raise ValueError("No Records to validate")

    seen_date =  set()

    for record in records:
        if "forecast_date" not in record:
            raise ValueError("Missing Field Forecast date")
        if record["forecast_date"] is None:
            raise ValueError("None Value in Forecast Date")

        try:
            datetime.strptime(record["forecast_date"], "%Y-%m-%d")
        except(ValueError, TypeError):
            raise ValueError(f"Invalid value type: {record['forecast_date']}")

        if record["forecast_date"] in seen_date:
            raise ValueError(f"Duplicate forecast date detected: {record["forecast_date"]}")

        seen_date.add(record["forecast_date"])

        for variable in DAILY_VARIABLES:
            if variable not in record:
                raise ValueError (f"Missing variable: {variable}")
            if record[variable] is None:
                raise ValueError (f"Null Value in: {variable} at {record}")

    return records