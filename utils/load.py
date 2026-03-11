import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# creates and returns a db connection
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# inserts raw country data into raw.countries
def load_raw_countries(countries):
    connection = get_connection()
    current = connection.cursor()

    for country in countries:
        current.execute("""
            INSERT INTO raw.countries (country_name, capital, latitude, longitude, population, area)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            country["name"],
            country["capital"],
            country["latitude"],
            country["longitude"],
            country["population"],
            country["area"]
        ))

    connection.commit()
    current.close()
    connection.close()

# inserts raw weather data into raw.weather
def load_raw_weather(weather_records):
    conn = get_connection()
    cur = conn.cursor()

    for record in weather_records:
        cur.execute("""
            INSERT INTO raw.weather (capital, date, temp_max, temp_min, precipitation, windspeed_max, sunshine_duration)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            record["capital"],
            record["date"],
            record["temp_max"],
            record["temp_min"],
            record["precipitation"],
            record["windspeed_max"],
            record["sunshine_duration"]
        ))

    conn.commit()
    cur.close()
    conn.close()

# inserts cleaned country data and returns a capital to id mapping (required for foreign key)
def load_clean_countries(countries):
    conn = get_connection()
    cur = conn.cursor()

    capital_to_id = {}

    for country in countries:
        cur.execute("""
            INSERT INTO clean.countries (country_name, capital, latitude, longitude, population, area)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            country["name"],
            country["capital"],
            country["latitude"],
            country["longitude"],
            country["population"],
            country["area"]
        ))
        country_id = cur.fetchone()[0]
        capital_to_id[country["capital"]] = country_id

    conn.commit()
    cur.close()
    conn.close()
    return capital_to_id

# inserts cleeaned weather data using the id mapping
def load_clean_weather(weather_records, capital_to_id):
    conn = get_connection()
    cur = conn.cursor()

    skipped = 0
    loaded = 0

    for record in weather_records:
        country_id = capital_to_id.get(record["capital"])
        if not country_id:
            skipped += 1
            continue

        cur.execute("""
            INSERT INTO clean.weather (country_id, date, temp_max, temp_min, precipitation, windspeed_max, sunshine_duration)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            country_id,
            record["date"],
            record["temp_max"],
            record["temp_min"],
            record["precipitation"],
            record["windspeed_max"],
            record["sunshine_hours"]
        ))
        loaded += 1

    conn.commit()
    cur.close()
    conn.close()
    
# truncate all tables before loading in new data, uses truncate because it's faster   
def clear_tables():
    conn = get_connection()
    cur = conn.cursor()

    # truncates and sets id-s back to 1
    cur.execute("TRUNCATE TABLE clean.weather, clean.countries, raw.weather, raw.countries RESTART IDENTITY CASCADE")
    
    conn.commit()
    cur.close()
    conn.close()
    print("Tables cleared")