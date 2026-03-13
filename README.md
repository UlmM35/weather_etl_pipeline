# Weather ETL Pipeline

Python ETL Pipeline that collects 30 days of weather data for European capitals and stores it in a PostgreSQL database.

## How to set up

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

## Database Dump

Located in `dump.sql`.
