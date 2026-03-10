COUNTRIES_URL = "https://restcountries.com/v3.1/region/europe"
WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"

import requests

def fetch_countries():
    """Fetch European countries."""
    print("Fetching EU countries")
    response = requests.get(COUNTRIES_URL)
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

    print(f"Fetched {len(countries)} countries.")
    return countries

if __name__ == "__main__":
    countries = fetch_countries()
    for c in countries:
        print(c)