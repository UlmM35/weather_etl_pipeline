from utils.load import get_connection
from dotenv import load_dotenv
    
def views():
    conn = get_connection()
    cur = conn.cursor()
       
    # top 5 capitals by avg temp
    cur.execute("SELECT * FROM clean.v_capitals_by_avg_temp LIMIT 5\n")
    print("Top 5 capitals by average temperature:")
    for row in cur.fetchall():
        print(f"  {row[0]}, {row[1]}: {row[2]}°C")
    print("")
    
    # top 5 capitals by precipitation
    cur.execute("SELECT * FROM clean.v_countries_by_rainfall LIMIT 5\n")
    print("Top 5 countries by rainfall:")
    for row in cur.fetchall():
        print(f"  {row[0]}, {row[1]}: {row[2]}mm")
    print("")
    
    # summary for all countries
    cur.execute("SELECT * FROM clean.v_country_summary\n")
    print("Full summaries for all countries:")
    for row in cur.fetchall():
        print(f"  {row[0]}, {row[1]}, MAX: {row[2]}°C, MIN: {row[3]}°C, {row[4]}mm, {row[5]}km/h, {row[6]}h, {row[7]} days")
        