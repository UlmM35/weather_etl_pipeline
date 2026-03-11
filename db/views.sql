-- capitals ranked by average temperature over 30 days
CREATE OR REPLACE VIEW clean.v_capitals_by_avg_temp AS
SELECT 
    c.capital,
    c.country_name AS country,
    ROUND(AVG((w.temp_max + w.temp_min) / 2)::numeric, 2) AS avg_temperature
FROM clean.weather w
INNER JOIN clean.countries c ON w.country_id = c.id
GROUP BY c.capital, c.country_name
ORDER BY avg_temperature DESC;

-- countries with the most rainfall
CREATE OR REPLACE VIEW clean.v_countries_by_rainfall AS
SELECT 
    c.country_name AS country,
    c.capital,
    ROUND(SUM(w.precipitation)::numeric, 2) AS total_precipitation
FROM clean.weather w
INNER JOIN clean.countries c ON w.country_id = c.id
GROUP BY c.country_name, c.capital
ORDER BY total_precipitation DESC;

-- full 30 day summary per country
CREATE OR REPLACE VIEW clean.v_country_summary AS
SELECT
    c.country_name AS country,
    c.capital,
    ROUND(AVG(w.temp_max)::numeric, 2) AS avg_temp_max,
    ROUND(AVG(w.temp_min)::numeric, 2) AS avg_temp_min,
    ROUND(AVG(w.precipitation)::numeric, 2) AS total_precipitation,
    ROUND(AVG(w.windspeed_max)::numeric, 2) AS avg_windspeed,
    ROUND(AVG(w.sunshine_duration)::numeric, 2) AS avg_sunshine_hours,
    COUNT(w.date) AS days_recorded
FROM clean.weather w
INNER JOIN clean.countries c ON w.country_id = c.id
GROUP BY c.country_name, c.capital
ORDER BY c.country_name;