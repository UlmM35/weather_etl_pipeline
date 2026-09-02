import os
from datetime import date, timedelta

import requests
from dotenv import load_dotenv


load_dotenv()


COUNTRIES_URL = "https://api.restcountries.com/countries/v5"
WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"
REQUEST_TIMEOUT_SECONDS = 30


def _error_message(payload):
    """Extract a readable error message from a REST Countries response."""
    if not isinstance(payload, dict):
        return None

    errors = payload.get("errors", [])
    if isinstance(errors, list) and errors and isinstance(errors[0], dict):
        return errors[0].get("message")
    return payload.get("message")


def fetch_countries():
    """Fetch European countries and their capital coordinates."""
    print("Fetching European countries")
    api_key = os.getenv("REST_COUNTRIES_API_KEY")
    if not api_key:
        raise RuntimeError(
            "REST_COUNTRIES_API_KEY is missing. Add it to the .env file."
        )

    try:
        response = requests.get(
            COUNTRIES_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            params={
                "region": "Europe",
                "limit": 100,
                "response_fields": (
                    "names.common,capitals,population,area.kilometers"
                ),
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Could not connect to the REST Countries API: {error}"
        ) from error

    try:
        payload = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise RuntimeError(
            "The REST Countries API returned invalid JSON."
        ) from error

    if not response.ok:
        message = _error_message(payload) or response.reason
        raise RuntimeError(
            f"REST Countries API request failed ({response.status_code}): {message}"
        )

    if not isinstance(payload, dict):
        raise RuntimeError(
            "The REST Countries API returned an unexpected response structure."
        )

    data_container = payload.get("data", {})
    if not isinstance(data_container, dict):
        raise RuntimeError(
            "The REST Countries API returned an unexpected response structure."
        )

    data = data_container.get("objects", [])
    if not isinstance(data, list):
        raise RuntimeError(
            "The REST Countries API returned an unexpected response structure."
        )

    countries = []
    for country in data:
        if not isinstance(country, dict):
            continue

        capitals = country.get("capitals", [])
        primary_capital = (
            capitals[0]
            if isinstance(capitals, list)
            and capitals
            and isinstance(capitals[0], dict)
            else {}
        )
        coordinates = primary_capital.get("coordinates", {})
        area = country.get("area", {})
        coordinates = coordinates if isinstance(coordinates, dict) else {}
        area = area if isinstance(area, dict) else {}
        countries.append(
            {
                "name": country.get("names", {}).get("common"),
                "capital": primary_capital.get("name"),
                "latitude": coordinates.get("lat"),
                "longitude": coordinates.get("lng"),
                "population": country.get("population"),
                "area": area.get("kilometers"),
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
    except (
        requests.exceptions.RequestException,
        ValueError,
        TypeError,
    ) as error:
        print(f"Failed to fetch weather for {capital}: {error}")
        return []
