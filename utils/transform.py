import pandas as pd

# clean the countries data and drop rows with missing values
def transform_countries(raw_countries):
    df = pd.DataFrame(raw_countries)
    
    before = len(df)
    
    # if name, capital, latitude or longitude doesnt exist, then you can't even fetch weather data, so it's best to drop those rows
    df = df.dropna(subset=["name", "capital", "latitude", "longitude"])
    
    after = len(df)
    
    print(f"Dropped {before - after} countries with missing name, capital or coordinates")
    print(f"{after} countries passed transformation")
    
    return df.to_dict(orient="records")
    
# does the same but with weather data, also transforms the sunshine duration    
def transform_weather(raw_weather):
    df = pd.DataFrame(raw_weather)
    
    before = len(df)
    
    df = df.dropna(subset=["temp_max", "temp_min", "precipitation", "windspeed_max"], how="all")
    
    after = len(df)
    
    print(f"Dropped {before - after} weather records with missing values")
    print(f"{after} weather records passed transformation")
    
    # if sunshine duration doesn't exist, then make it  0
    df["sunshine_hours"] = (df["sunshine_duration"].fillna(0) / 3600).round(2)
    df = df.drop(columns=["sunshine_duration"])

    return df.to_dict(orient="records")
