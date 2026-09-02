from utils.extract import fetch_countries, fetch_weather
from utils.load import (
    clear_tables,
    load_clean_countries,
    load_clean_weather,
    load_raw_countries,
    load_raw_weather,
)
from utils.transform import transform_countries, transform_weather
from utils.verify import verify
from utils.views import print_analytical_views


def run_pipeline():
    print("Starting ETL pipeline\n")

    # Extract and transform everything before replacing existing database data.
    raw_countries = fetch_countries()
    if not raw_countries:
        raise RuntimeError("No country data was returned by the API.")

    clean_countries = transform_countries(raw_countries)
    if not clean_countries:
        raise RuntimeError("No countries passed validation.")

    all_raw_weather = []
    for country in clean_countries:
        records = fetch_weather(
            country["capital"],
            country["latitude"],
            country["longitude"],
        )
        all_raw_weather.extend(records)

    if not all_raw_weather:
        raise RuntimeError("No weather data was returned by the API.")

    clean_weather = transform_weather(all_raw_weather)
    if not clean_weather:
        raise RuntimeError("No weather records passed validation.")

    # Existing data is cleared only after fresh data has been fetched successfully.
    clear_tables()
    load_raw_countries(raw_countries)
    load_raw_weather(all_raw_weather)

    capital_to_id = load_clean_countries(clean_countries)
    load_clean_weather(clean_weather, capital_to_id)

    print("Pipeline completed successfully\n")


if __name__ == "__main__":
    run_pipeline()
    print("----- Verifying the data -----\n")
    verify()
    print("----- Views for the countries -----\n")
    print_analytical_views()
