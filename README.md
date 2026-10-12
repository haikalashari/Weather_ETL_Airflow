# Weather Data Pipeline — West Kalimantan

An automated weather data engineering pipeline that extracts 7-day daily weather forecasts from the [Open-Meteo API](https://open-meteo.com/), validates and transforms the data using Python, orchestrates the workflow with Apache Airflow, and stores raw API responses and structured forecast records in Supabase PostgreSQL.

The project is designed to demonstrate a practical ETL workflow, data validation, relational data modeling, workflow orchestration, and historical forecast tracking.

## Overview

Weather forecasts are updated over time, making it useful to collect and store forecast snapshots rather than relying solely on the latest available response.

This project collects daily weather forecast data for **14 locations across West Kalimantan, Indonesia**. Each pipeline run retrieves a seven-day forecast, transforms the API response into structured records, validates the data, and loads it into PostgreSQL.

The resulting dataset can support weather monitoring, forecast comparisons, and future analytics dashboards.

## Objectives

- Build an automated ETL pipeline using Apache Airflow.
- Extract weather forecast data from a public API.
- Transform nested JSON responses into structured daily records.
- Validate data before loading it into the database.
- Store raw API responses for traceability and reprocessing.
- Design relational tables for location metadata and daily forecast data.
- Preserve forecast snapshots across pipeline runs.
- Prepare structured data for downstream analytics and visualization.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data extraction, transformation, and validation |
| Open-Meteo API | Weather forecast data source |
| Apache Airflow | Workflow orchestration and scheduling |
| Astro CLI | Local Airflow development environment |
| Docker | Containerized execution environment |
| Supabase PostgreSQL | Relational database and data warehouse storage |
| SQL | Database queries, constraints, and data loading |
| Git & GitHub | Version control and project documentation |

## Architecture

```text
                  Open-Meteo API
                        |
                        v
                Extract Weather Data
                        |
                        v
             Transform JSON into Records
                        |
                        v
                 Validate Records
                        |
                        v
                  Load to PostgreSQL
                        |
             +----------+----------+
             |                     |
             v                     v
    raw_weather_responses   fact_daily_forecast
             ^                     ^
             |                     |
             +---- dim_location ---+
                        |
                        v
              Future Analytics Layer
               Power BI / Looker Studio
```

Apache Airflow orchestrates the tasks and manages their execution dependencies.

Location metadata is read from the `dim_location` table in Supabase, so the pipeline does not depend on a separate hardcoded location configuration file.

## Pipeline Workflow

### 1. Extract

The pipeline retrieves location metadata from PostgreSQL, including:

- `location_code`
- `latitude`
- `longitude`
- `timezone`

For each location, the pipeline requests a seven-day forecast from Open-Meteo.

The extracted daily weather variables include:

- Weather condition code
- Maximum and minimum temperature
- Maximum and minimum apparent temperature
- Rainfall and precipitation
- Maximum precipitation probability
- Maximum wind speed
- Dominant wind direction

The original API response is retained as a raw JSON payload.

### 2. Transform

The nested API response is transformed into a list of daily records, with one record per forecast date.

The transformation process checks that the expected daily fields exist and that their array lengths match the forecast dates.

### 3. Validate

The pipeline validates the transformed records before loading them into the database.

Validation helps detect malformed API responses and inconsistent data structures before they reach the fact table.

### 4. Load

The pipeline writes data into two tables:

- `raw_weather_responses`: stores raw API payloads and their associated run and location identifiers.
- `fact_daily_forecast`: stores structured daily weather forecast records.

The loader uses database transactions so that a loading failure can trigger a rollback of the current transaction.

A unique constraint on `(location_id, run_id, forecast_date)` prevents duplicate fact records for the same location, forecast date, and pipeline run.

### 5. Orchestrate

Apache Airflow coordinates the workflow through the `weather_etl` DAG.

The DAG is configured with a daily schedule (`@daily`) and retries failed tasks according to its default arguments.

## Database Design

The project uses three PostgreSQL tables.

### `dim_location`

Stores the locations monitored by the pipeline.

| Column | Description |
|---|---|
| `location_id` | Primary key |
| `location_code` | Unique location identifier |
| `location_name` | Location name |
| `administrative_level` | Administrative classification |
| `province_name` | Province name |
| `latitude` | Geographic latitude |
| `longitude` | Geographic longitude |
| `timezone` | Location timezone |

### `raw_weather_responses`

Stores the original API responses for traceability.

| Column | Description |
|---|---|
| `response_id` | Primary key |
| `run_id` | Pipeline run identifier |
| `location_id` | Reference to `dim_location` |
| `requested_at` | Request timestamp |
| `payload` | Original API response stored as JSONB |
| `created_at` | Record creation timestamp |

### `fact_daily_forecast`

Stores structured daily forecast records.

| Column | Description |
|---|---|
| `forecast_id` | Primary key |
| `location_id` | Reference to `dim_location` |
| `run_id` | Pipeline run identifier |
| `source_response_id` | Reference to the raw API response |
| `forecast_date` | Forecast date |
| `weather_code` | Weather condition code |
| `temperature_2m_max` | Maximum daily temperature |
| `temperature_2m_min` | Minimum daily temperature |
| `apparent_temperature_max` | Maximum apparent temperature |
| `apparent_temperature_min` | Minimum apparent temperature |
| `rain_sum` | Daily rain sum |
| `precipitation_sum` | Daily precipitation sum |
| `precipitation_probability_max` | Maximum daily precipitation probability |
| `wind_speed_10m_max` | Maximum daily wind speed |
| `wind_direction_10m_dominant` | Dominant daily wind direction |
| `ingested_at` | Timestamp when the record was ingested |

**Fact table grain:** one record per location, forecast date, and pipeline run.

This grain allows multiple forecast snapshots for the same location and forecast date to be retained across different runs.

## Project Structure

```text
weather-data-warehouse/
├── dags/
│   └── weather_etl.py
├── src/
│   └── weather_pipeline/
│       ├── extract.py
│       ├── transform.py
│       ├── validate.py
│       └── load.py
├── requirements.txt
└── Dockerfile
```

| File | Responsibility |
|---|---|
| `dags/weather_etl.py` | Defines and orchestrates the Airflow DAG |
| `extract.py` | Requests weather forecast data from Open-Meteo |
| `transform.py` | Converts API responses into structured daily records |
| `validate.py` | Validates transformed records |
| `load.py` | Loads raw responses and forecast records into PostgreSQL |
| `requirements.txt` | Declares Python dependencies |
| `Dockerfile` | Configures the container environment |

## Getting Started

### Prerequisites

Make sure the following tools and accounts are available:

- Python
- Docker Desktop
- Astro CLI
- A Supabase project with PostgreSQL access
- Git

The Open-Meteo forecast endpoint used in this project is publicly accessible and does not require an API key for standard non-commercial use. Review the provider's current terms before using the service for other purposes.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd weather-data-warehouse
```

### 2. Configure the Database

Create a Supabase project and configure the PostgreSQL tables:

- `dim_location`
- `raw_weather_responses`
- `fact_daily_forecast`

Add the 14 West Kalimantan locations to `dim_location`, including their location codes, coordinates, administrative levels, and timezones.

Use the database schema documented in this repository or create the tables using this SQL command in supabase or any postgres database from /sql file.


### 3. Configure the Airflow Connection

Start the local Airflow environment:

```bash
astro dev start
```

Open the Airflow UI at:

`http://localhost:8080`

Create a PostgreSQL connection with the following settings:

| Setting | Value |
|---|---|
| Connection ID | `weather_supabase` |
| Connection Type | `Postgres` |
| Host | Your Supabase PostgreSQL or pooler hostname |
| Database | `postgres` |
| Username | Your Supabase database username |
| Password | Your Supabase database password |
| Port | The port specified by your selected connection method |

Use the connection details provided by the Supabase dashboard. For a shared Supabase pooler, the username may need to include the project reference.

**Security:** Never commit database passwords, credentials, or secret connection strings to GitHub.

### 4. Install Dependencies

The project dependencies are declared in `requirements.txt` and installed as part of the Astro Docker environment.

If you modify the dependencies, rebuild or restart the local environment as appropriate for your Astro setup.

### 5. Run the Pipeline

Open the Airflow UI, locate the `weather_etl` DAG, and trigger it manually for the initial test.

Monitor the task execution through the Airflow Grid view and task logs.

The expected workflow is:

1. Read location metadata.
2. Extract weather forecasts.
3. Transform API responses.
4. Validate daily records.
5. Load raw responses and structured forecast data.

A successful run should complete all tasks and persist the resulting data in Supabase PostgreSQL.

## Scheduling and Snapshot Behavior

The DAG uses the `@daily` schedule.

Each pipeline run generates a `run_id` to identify its forecast snapshot. Since the fact table's uniqueness constraint includes `run_id`, a later run can store another snapshot for the same location and forecast date.

For example, two runs may store different forecasts for the same location and date if the API response changes between requests.

**Important:** Manually triggering the DAG also creates a new run and can add another snapshot. This is expected under the current historical snapshot design.

The current uniqueness constraint prevents duplicate records within the same location, run, and forecast date. It does not enforce one snapshot per location and forecast date across all runs.

## Data Quality and Reliability

The pipeline incorporates several data engineering practices:

- API response validation before transformation.
- Validation of required daily fields and matching array lengths.
- Database primary keys and foreign keys.
- A unique constraint to prevent duplicate fact records within a run.
- Parameterized SQL queries.
- Transaction handling and rollback on loading failures.
- Airflow task retries.
- Raw response retention for traceability.

These mechanisms help improve data consistency and make pipeline failures easier to investigate.

## Potential Analytics Use Cases

The resulting dataset can be extended to support:

- Daily minimum and maximum temperature monitoring.
- Rainfall and precipitation probability analysis.
- Comparisons of weather forecasts across locations.
- Changes in predicted weather conditions between snapshots.
- Forecast revision analysis.
- Weather dashboards using Power BI or Looker Studio.

## Future Improvements

Potential enhancements include:

- Add automated data quality checks for temperature ranges, null values, and duplicate records.
- Add a dedicated SQL setup script and sample seed data.
- Implement structured logging and pipeline monitoring.
- Add unit tests for extraction, transformation, and validation.
- Introduce a staging or analytics layer for dashboard-ready datasets.
- Build a Power BI or Looker Studio dashboard.
- Add historical forecast revision metrics and trend analysis.
- Add automated tests for retry behavior and idempotency.

## Data Source

Weather forecast data is provided by [Open-Meteo](https://open-meteo.com/).

Refer to the [Open-Meteo API documentation](https://open-meteo.com/en/docs) for endpoint parameters, available weather variables, and attribution or usage requirements.

## Author

**Haikal**

Informatics graduate interested in Data Engineering, Data Analytics, and Data Science.

This project is part of my Data Engineering portfolio, demonstrating API ingestion, Python-based ETL, workflow orchestration, relational data modeling, and PostgreSQL data loading.
