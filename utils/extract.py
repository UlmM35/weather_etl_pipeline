COUNTRIES_URL = "https://restcountries.com/v3.1/region/europe"
WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"

import requests
from datetime import date, timedelta

# get the countries from the api
def fetch_countries():
    print("Fetching EU countries")
    response = requests.get(COUNTRIES_URL)
    # raises HTTP error if it occurs
    response.raise_for_status()
    data = response.json()

    countries = []
    for country in data:
        try:
            name = country.get("name", {}).get("common")
            capital_array = country.get("capital", [])
            capital = capital_array[0] if (len(capital_array)) > 0 else None
            latlng = country.get("capitalInfo", {}).get("latlng", [])
            latitude = latlng[0] if len(latlng) >= 1 else None
            longitude = latlng[1] if len(latlng) >= 2 else None
            population = country.get("population", None)
            area = country.get("area", None)

            countries.append({
                "name": name,
                "capital": capital,
                "latitude": latitude,
                "longitude": longitude,
                "population": population,
                "area": area
            })
            
        except Exception as e:
            print(f"Error, skipping country: {e}")

    print(f"Fetched {len(countries)} countries")
    return countries

# get the weather from the api
def fetch_weather(capital, latitude, longitude):
    # if u dont do this, then the weather data will be over last 31 days not 30
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=29)
    
    # params for query
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,sunshine_duration",
        "timezone": "UTC"
    }

    try:
        response = requests.get(WEATHER_URL, params=params)
        # raises HTTP error if it occurs
        response.raise_for_status()
        data = response.json().get("daily", {})

        records = []
        for i, day in enumerate(data.get("time", [])):
            records.append({
                "capital": capital,
                "date": day,
                "temp_max": data.get("temperature_2m_max", [None])[i],
                "temp_min": data.get("temperature_2m_min", [None])[i],
                "precipitation": data.get("precipitation_sum", [None])[i],
                "windspeed_max": data.get("windspeed_10m_max", [None])[i],
                "sunshine_duration": data.get("sunshine_duration", [None])[i]
            })
        return records

    except Exception as e:
        print(f"Failed to fetch weather for {capital}: {e}")
        return []
    
    
# for testing the functions

"""if __name__ == "__main__":
    countries = fetch_countries()
    for c in countries[:3]:
        print(c)
        print(fetch_weather(c.get("capital"), c.get("latitude"), c.get("longitude")))
        """