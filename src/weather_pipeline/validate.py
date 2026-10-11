from extract import DAILY_VARIABLES

def validate_data_daily(records):
    
    if not records:
        raise ValueError("No Records to validate")

    for record in records:
        if "forecast_date" not in record:
            raise ValueError("Missing Field Forecast date")
        if record["forecast_date"] is None:
            raise ValueError("None Value in Forecast Date")
        
        for variable in DAILY_VARIABLES:
            if variable not in record:
                raise ValueError (f"Missing variable: {variable}")
            if record[variable] is None:
                raise ValueError (f"Null Value in: {variable} at {record}")
