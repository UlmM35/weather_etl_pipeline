-- Schema for raw country data
CREATE TABLE IF NOT EXISTS raw.countries (
    id SERIAL PRIMARY KEY,
    name TEXT,
    capital TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    population BIGINT,
    area DOUBLE PRECISION,
    fetched_at TIMESTAMP DEFAULT NOW()
);

-- Schema for raw weather data
CREATE TABLE IF NOT EXISTS raw.weather (
    id SERIAL PRIMARY KEY,
    capital TEXT,
    date DATE,
    temp_max DOUBLE PRECISION,
    temp_min DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    windspeed_max DOUBLE PRECISION,
    sunshine_duration DOUBLE PRECISION,
    fetched_at TIMESTAMP DEFAULT NOW()
);

-- Schema for clean country data
CREATE TABLE IF NOT EXISTS clean.countries (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    capital TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    population BIGINT,
    area DOUBLE PRECISION
);

-- Schema for clean weather data
CREATE TABLE IF NOT EXISTS clean.weather (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES clean.countries(id),
    date DATE NOT NULL,
    temp_max DOUBLE PRECISION,
    temp_min DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    windspeed_max DOUBLE PRECISION,
    sunshine_duration DOUBLE PRECISION
);