import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """Create a PostgreSQL connection from environment variables."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_raw_countries(countries):
    """Insert country API data into raw.countries."""
    rows = [
        (
            country["name"],
            country["capital"],
            country["latitude"],
            country["longitude"],
            country["population"],
            country["area"],
        )
        for country in countries
    ]

    with closing(get_connection()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO raw.countries
                    (country_name, capital, latitude, longitude, population, area)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                rows,
            )


def load_raw_weather(weather_records):
    """Insert weather API data into raw.weather."""
    rows = [
        (
            record["capital"],
            record["date"],
            record["temp_max"],
            record["temp_min"],
            record["precipitation"],
            record["windspeed_max"],
            record["sunshine_duration"],
        )
        for record in weather_records
    ]

    with closing(get_connection()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO raw.weather
                    (capital, date, temp_max, temp_min, precipitation,
                     windspeed_max, sunshine_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                rows,
            )


def load_clean_countries(countries):
    """Insert validated countries and return a capital-to-ID mapping."""
    capital_to_id = {}

    with closing(get_connection()) as connection:
        with connection, connection.cursor() as cursor:
            for country in countries:
                cursor.execute(
                    """
                    INSERT INTO clean.countries
                        (country_name, capital, latitude, longitude, population, area)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        country["name"],
                        country["capital"],
                        country["latitude"],
                        country["longitude"],
                        country["population"],
                        country["area"],
                    ),
                )
                capital_to_id[country["capital"]] = cursor.fetchone()[0]

    return capital_to_id


def load_clean_weather(weather_records, capital_to_id):
    """Insert transformed weather data using country foreign keys."""
    rows = []
    skipped = 0

    for record in weather_records:
        country_id = capital_to_id.get(record["capital"])
        if country_id is None:
            skipped += 1
            continue

        rows.append(
            (
                country_id,
                record["date"],
                record["temp_max"],
                record["temp_min"],
                record["precipitation"],
                record["windspeed_max"],
                record["sunshine_hours"],
            )
        )

    with closing(get_connection()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO clean.weather
                    (country_id, date, temp_max, temp_min, precipitation,
                     windspeed_max, sunshine_hours)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                rows,
            )

    print(f"Loaded {len(rows)} clean weather records; skipped {skipped}")


def clear_tables():
    """Remove previous pipeline results and reset generated IDs."""
    with closing(get_connection()) as connection:
        with connection, connection.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE
                    clean.weather,
                    clean.countries,
                    raw.weather,
                    raw.countries
                RESTART IDENTITY CASCADE
                """
            )

    print("Tables cleared")
