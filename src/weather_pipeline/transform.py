from extract import DAILY_VARIABLES

def transform_daily_weather(data):
    if "daily" not in data:
        raise ValueError("There is no daily data in response")

    daily = data["daily"]

    if "time" not in daily:
        raise ValueError("There is no date time data in response")

    dates = daily["time"]

    for variable in DAILY_VARIABLES:
        if variable not in daily:
            raise ValueError(
                f"Missing variable in daily data: {variable}"
            )

        if len(daily[variable]) != len(dates):
            raise ValueError(
                f"Data length mismatch for variable: {variable}"
            )

    records = []

    for i, forecast_date in enumerate(dates):
        record = {
            "forecast_date": forecast_date
        }

        for variable in DAILY_VARIABLES:
            record[variable] = daily[variable][i]

        records.append(record)

    return records

    