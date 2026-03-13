# Weather ETL Pipeline

Python ETL Pipeline that collects 30 days of weather data for European capitals and stores it in a PostgreSQL database.

## Tech Stack

- Python
- PostgreSQL
- Pandas

## Setup

1. Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
```

2. Fill out your .env file like the one in the .env.example

## How to run the pipeline

Run the full pipeline:
```bash
python main.py
```

## Database structure

The database uses two schemas:

- `raw` — stores data exactly as it comes from the APIs
- `clean` — stores transformed and clean data

## Features

- Fetches all European countries and their capital coordinates from the RestCountries API
- Collects 30 days of historical weather data per capital from the Open-Meteo Archive API
- Includes three analytical SQL views: Capitals ranked by average
temperature, countries with the most rainfall and a full 30-day summary per country.

## Database Dump

Located in `dump.sql`.
