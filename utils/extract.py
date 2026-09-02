from datetime import date, timedelta

import requests


COUNTRIES_URL = "https://restcountries.com/v3.1/region/europe"
WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"
REQUEST_TIMEOUT_SECONDS = 30


def fetch_countries():
    """Fetch European countries and their capital coordinates."""
    print("Fetching European countries")
    response = requests.get(COUNTRIES_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("The countries API returned an unexpected response.")

    countries = []
    for country in data:
        if not isinstance(country, dict):
            continue

        capital_array = country.get("capital", [])
        coordinates = country.get("capitalInfo", {}).get("latlng", [])
        countries.append(
            {
                "name": country.get("name", {}).get("common"),
                "capital": capital_array[0] if capital_array else None,
                "latitude": coordinates[0] if len(coordinates) >= 1 else None,
                "longitude": coordinates[1] if len(coordinates) >= 2 else None,
                "population": country.get("population"),
                "area": country.get("area"),
            }
        )

    print(f"Fetched {len(countries)} countries")
    return countries


def _value_at(values, index):
    """Return a list value safely when an API field is missing or shorter."""
    return values[index] if isinstance(values, list) and index < len(values) else None


def fetch_weather(capital, latitude, longitude):
    """Fetch the previous 30 complete days of weather for one capital."""
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=29)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": (
            "temperature_2m_max,temperature_2m_min,precipitation_sum,"
            "wind_speed_10m_max,sunshine_duration"
        ),
        "timezone": "UTC",
    }

    try:
        response = requests.get(
            WEATHER_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("The weather API returned an unexpected response.")

        daily = payload.get("daily", {})
        if not isinstance(daily, dict):
            raise ValueError("The weather API returned an unexpected response.")

        days = daily.get("time", [])
        if not isinstance(days, list):
            raise ValueError("The weather API returned an unexpected response.")

        records = []
        for index, day in enumerate(days):
            records.append(
                {
                    "capital": capital,
                    "date": day,
                    "temp_max": _value_at(daily.get("temperature_2m_max"), index),
                    "temp_min": _value_at(daily.get("temperature_2m_min"), index),
                    "precipitation": _value_at(daily.get("precipitation_sum"), index),
                    "windspeed_max": _value_at(daily.get("wind_speed_10m_max"), index),
                    "sunshine_duration": _value_at(daily.get("sunshine_duration"), index),
                }
            )
        return records
    except (requests.RequestException, ValueError, TypeError) as error:
        print(f"Failed to fetch weather for {capital}: {error}")
        return []
