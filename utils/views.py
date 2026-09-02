from contextlib import closing

from utils.load import get_connection


def print_analytical_views():
    """Print example results from the analytical SQL views."""
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM clean.v_capitals_by_avg_temp LIMIT 5")
            warmest_capitals = cursor.fetchall()

            cursor.execute("SELECT * FROM clean.v_countries_by_rainfall LIMIT 5")
            rainiest_countries = cursor.fetchall()

            cursor.execute("SELECT * FROM clean.v_country_summary")
            country_summaries = cursor.fetchall()

    print("Top 5 capitals by average temperature:")
    for capital, country, average_temperature in warmest_capitals:
        print(f"  {capital}, {country}: {average_temperature} degrees Celsius")

    print("\nTop 5 countries by rainfall:")
    for country, capital, total_precipitation in rainiest_countries:
        print(f"  {country}, {capital}: {total_precipitation} mm")

    print("\nFull summaries for all countries:")
    for row in country_summaries:
        print(
            f"  {row[0]}, {row[1]}, avg max: {row[2]} degrees Celsius, "
            f"avg min: {row[3]} degrees Celsius, rainfall: {row[4]} mm, "
            f"wind: {row[5]} km/h, sunshine: {row[6]} h, days: {row[7]}"
        )
