from utils.load import get_connection

def verify():
    conn = get_connection()
    cur = conn.cursor()

    # check rows
    cur.execute("SELECT COUNT(*) FROM raw.countries")
    raw_countries_count = cur.fetchone()[0]
    print(f"Raw countries: {raw_countries_count}")

    cur.execute("SELECT COUNT(*) FROM raw.weather")
    raw_weather_count = cur.fetchone()[0]
    print(f"Raw weather records: {raw_weather_count}")

    cur.execute("SELECT COUNT(*) FROM clean.countries")
    clean_countries_count = cur.fetchone()[0]
    print(f"Clean countries: {clean_countries_count}")

    cur.execute("SELECT COUNT(*) FROM clean.weather")
    clean_weather_count = cur.fetchone()[0]
    print(f"Clean weather records: {clean_weather_count}")

    print(f"More clean country rows than raw rows: {clean_countries_count > raw_countries_count}")
    print(f"More clean weather rows than raw rows: {clean_weather_count > raw_weather_count}")
    
    # check if there are any null fields
    cur.execute("SELECT COUNT(*) FROM clean.countries WHERE capital IS NULL OR latitude IS NULL OR longitude IS NULL")
    null_count = cur.fetchone()[0]
    print(f"Clean countries with null fields: {null_count}")
    
    # check that the temperature range looks reasonable
    cur.execute("SELECT MIN(temp_min), MAX(temp_max) FROM clean.weather")
    min_t, max_t = cur.fetchone()
    print(f"Temperature range: {min_t} - {max_t}")

    # check that sunshine duration looks right
    cur.execute("SELECT MIN(sunshine_duration), MAX(sunshine_duration) FROM clean.weather")
    min_s, max_s = cur.fetchone()
    print(f"Sunshine hours range: {min_s} - {max_s}\n")

    cur.close()
    conn.close()