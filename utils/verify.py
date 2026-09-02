from contextlib import closing

from utils.load import get_connection


def verify():
    """Run basic data-quality checks against the clean data."""
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM raw.countries")
            raw_countries_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM raw.weather")
            raw_weather_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM clean.countries")
            clean_countries_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM clean.weather")
            clean_weather_count = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM clean.countries
                WHERE capital IS NULL
                   OR latitude IS NULL
                   OR longitude IS NULL
                """
            )
            null_country_fields = cursor.fetchone()[0]

            cursor.execute("SELECT MIN(temp_min), MAX(temp_max) FROM clean.weather")
            minimum_temperature, maximum_temperature = cursor.fetchone()

            cursor.execute(
                "SELECT MIN(sunshine_hours), MAX(sunshine_hours) FROM clean.weather"
            )
            minimum_sunshine, maximum_sunshine = cursor.fetchone()

    print(f"Raw countries: {raw_countries_count}")
    print(f"Raw weather records: {raw_weather_count}")
    print(f"Clean countries: {clean_countries_count}")
    print(f"Clean weather records: {clean_weather_count}")
    print(
        "Temperature range: "
        f"{minimum_temperature} to {maximum_temperature} degrees Celsius"
    )
    print(f"Sunshine range: {minimum_sunshine} to {maximum_sunshine} hours\n")

    checks = {
        "clean country count does not exceed raw count": (
            0 < clean_countries_count <= raw_countries_count
        ),
        "clean weather count does not exceed raw count": (
            0 < clean_weather_count <= raw_weather_count
        ),
        "required country fields contain no null values": null_country_fields == 0,
        "temperature values are within a plausible range": (
            minimum_temperature is not None
            and maximum_temperature is not None
            and -100 <= minimum_temperature <= maximum_temperature <= 70
        ),
        "sunshine duration is between 0 and 24 hours": (
            minimum_sunshine is not None
            and maximum_sunshine is not None
            and 0 <= minimum_sunshine <= maximum_sunshine <= 24
        ),
    }

    for description, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {description}")

    if not all(checks.values()):
        raise RuntimeError("One or more data-quality checks failed.")
