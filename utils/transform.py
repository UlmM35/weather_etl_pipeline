import pandas as pd


def transform_countries(raw_countries):
    """Remove countries that cannot be used for weather extraction."""
    dataframe = pd.DataFrame(raw_countries)
    before = len(dataframe)

    dataframe = dataframe.dropna(
        subset=["name", "capital", "latitude", "longitude"]
    )

    print(
        f"Dropped {before - len(dataframe)} countries with missing "
        "name, capital or coordinates"
    )
    print(f"{len(dataframe)} countries passed transformation")
    return dataframe.to_dict(orient="records")


def transform_weather(raw_weather):
    """Remove incomplete records and convert sunshine seconds to hours."""
    dataframe = pd.DataFrame(raw_weather)
    before = len(dataframe)

    dataframe = dataframe.dropna(
        subset=["temp_max", "temp_min", "precipitation"]
    )

    print(f"Dropped {before - len(dataframe)} incomplete weather records")
    print(f"{len(dataframe)} weather records passed transformation")

    dataframe["sunshine_hours"] = (
        dataframe["sunshine_duration"].fillna(0) / 3600
    ).round(2)
    dataframe = dataframe.drop(columns=["sunshine_duration"])
    return dataframe.to_dict(orient="records")
