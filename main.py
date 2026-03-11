from utils.extract import fetch_countries, fetch_weather
from utils.transform import transform_countries, transform_weather
from utils.load import clear_tables, load_raw_countries, load_raw_weather, load_clean_countries, load_clean_weather
from utils.verify import verify
from utils.views import views

def run_pipeline():
    print("Starting ETL pipeline\n")
    
    # clear data before fetching
    clear_tables()
    
    # extract
    raw_countries = fetch_countries()
    
    # transform countries first
    clean_countries = transform_countries(raw_countries)
    
    # fetch weather only for clean countries
    all_raw_weather = []
    for country in clean_countries:
        records = fetch_weather(country["capital"], country["latitude"], country["longitude"])
        all_raw_weather.extend(records)
        
    load_raw_countries(raw_countries)
    load_raw_weather(all_raw_weather)
    
    clean_weather = transform_weather(all_raw_weather)
    
    capital_to_id = load_clean_countries(clean_countries)
    load_clean_weather(clean_weather, capital_to_id)
    
    print("Pipeline completed successfully\n")
    
if __name__ == "__main__":
    run_pipeline()
    print("----- Verifying the data -----\n")
    verify()
    print("----- Views for the countries -----\n")
    views()