
-- 1. Dimension: lokasi
CREATE TABLE public.dim_location (
    location_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    location_code TEXT NOT NULL UNIQUE,
    location_name TEXT NOT NULL,
    administrative_level TEXT NOT NULL,
    province_name TEXT NOT NULL DEFAULT 'Kalimantan Barat',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    timezone TEXT NOT NULL DEFAULT 'Asia/Jakarta',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Raw: respons API
CREATE TABLE public.raw_weather_responses (
    response_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id UUID NOT NULL,
    location_id BIGINT NOT NULL
        REFERENCES public.dim_location(location_id),
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Fact: forecast harian
CREATE TABLE public.fact_daily_forecast (
    forecast_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    location_id BIGINT NOT NULL
        REFERENCES public.dim_location(location_id),
    run_id UUID NOT NULL,
    source_response_id BIGINT NOT NULL
        REFERENCES public.raw_weather_responses(response_id),
    forecast_date DATE NOT NULL,
    weather_code INTEGER,
    temperature_2m_max DOUBLE PRECISION,
    temperature_2m_min DOUBLE PRECISION,
    apparent_temperature_max DOUBLE PRECISION,
    apparent_temperature_min DOUBLE PRECISION,
    rain_sum DOUBLE PRECISION,
    precipitation_sum DOUBLE PRECISION,
    precipitation_probability_max DOUBLE PRECISION,
    wind_speed_10m_max DOUBLE PRECISION,
    wind_direction_10m_dominant DOUBLE PRECISION,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (location_id, run_id, forecast_date)
);

-- 4. Indexes
CREATE INDEX idx_raw_run_id
    ON public.raw_weather_responses(run_id);

CREATE INDEX idx_raw_location_requested
    ON public.raw_weather_responses(location_id, requested_at);

CREATE INDEX idx_fact_forecast_date
    ON public.fact_daily_forecast(forecast_date);

CREATE INDEX idx_fact_run_id
    ON public.fact_daily_forecast(run_id);

CREATE INDEX idx_fact_location_date
    ON public.fact_daily_forecast(location_id, forecast_date);
