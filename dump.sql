--
-- PostgreSQL database dump
--

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: clean; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA clean;


ALTER SCHEMA clean OWNER TO postgres;

--
-- Name: raw; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA raw;


ALTER SCHEMA raw OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: countries; Type: TABLE; Schema: clean; Owner: postgres
--

CREATE TABLE clean.countries (
    id integer NOT NULL,
    country_name text NOT NULL,
    capital text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    population bigint,
    area double precision
);


ALTER TABLE clean.countries OWNER TO postgres;

--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: clean; Owner: postgres
--

CREATE SEQUENCE clean.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE clean.countries_id_seq OWNER TO postgres;

--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: clean; Owner: postgres
--

ALTER SEQUENCE clean.countries_id_seq OWNED BY clean.countries.id;


--
-- Name: weather; Type: TABLE; Schema: clean; Owner: postgres
--

CREATE TABLE clean.weather (
    id integer NOT NULL,
    country_id integer,
    date date NOT NULL,
    temp_max double precision NOT NULL,
    temp_min double precision NOT NULL,
    precipitation double precision NOT NULL,
    windspeed_max double precision,
    sunshine_duration double precision NOT NULL
);


ALTER TABLE clean.weather OWNER TO postgres;

--
-- Name: v_capitals_by_avg_temp; Type: VIEW; Schema: clean; Owner: postgres
--

CREATE VIEW clean.v_capitals_by_avg_temp AS
 SELECT c.capital,
    c.country_name AS country,
    round((avg(((w.temp_max + w.temp_min) / (2)::double precision)))::numeric, 2) AS avg_temperature
   FROM (clean.weather w
     JOIN clean.countries c ON ((w.country_id = c.id)))
  GROUP BY c.capital, c.country_name
  ORDER BY (round((avg(((w.temp_max + w.temp_min) / (2)::double precision)))::numeric, 2)) DESC;


ALTER VIEW clean.v_capitals_by_avg_temp OWNER TO postgres;

--
-- Name: v_countries_by_rainfall; Type: VIEW; Schema: clean; Owner: postgres
--

CREATE VIEW clean.v_countries_by_rainfall AS
 SELECT c.country_name AS country,
    c.capital,
    round((sum(w.precipitation))::numeric, 2) AS total_precipitation_mm
   FROM (clean.weather w
     JOIN clean.countries c ON ((w.country_id = c.id)))
  GROUP BY c.country_name, c.capital
  ORDER BY (round((sum(w.precipitation))::numeric, 2)) DESC;


ALTER VIEW clean.v_countries_by_rainfall OWNER TO postgres;

--
-- Name: v_country_summary; Type: VIEW; Schema: clean; Owner: postgres
--

CREATE VIEW clean.v_country_summary AS
 SELECT c.country_name AS country,
    c.capital,
    round((avg(w.temp_max))::numeric, 2) AS avg_temp_max,
    round((avg(w.temp_min))::numeric, 2) AS avg_temp_min,
    round((avg(w.precipitation))::numeric, 2) AS total_precipitation_mm,
    round((avg(w.windspeed_max))::numeric, 2) AS avg_windspeed,
    round((avg(w.sunshine_duration))::numeric, 2) AS avg_sunshine_hours,
    count(w.date) AS days_recorded
   FROM (clean.weather w
     JOIN clean.countries c ON ((w.country_id = c.id)))
  GROUP BY c.country_name, c.capital
  ORDER BY c.country_name;


ALTER VIEW clean.v_country_summary OWNER TO postgres;

--
-- Name: weather_id_seq; Type: SEQUENCE; Schema: clean; Owner: postgres
--

CREATE SEQUENCE clean.weather_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE clean.weather_id_seq OWNER TO postgres;

--
-- Name: weather_id_seq; Type: SEQUENCE OWNED BY; Schema: clean; Owner: postgres
--

ALTER SEQUENCE clean.weather_id_seq OWNED BY clean.weather.id;


--
-- Name: countries; Type: TABLE; Schema: raw; Owner: postgres
--

CREATE TABLE raw.countries (
    id integer NOT NULL,
    country_name text,
    capital text,
    latitude double precision,
    longitude double precision,
    population bigint,
    area double precision
);


ALTER TABLE raw.countries OWNER TO postgres;

--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: raw; Owner: postgres
--

CREATE SEQUENCE raw.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE raw.countries_id_seq OWNER TO postgres;

--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: raw; Owner: postgres
--

ALTER SEQUENCE raw.countries_id_seq OWNED BY raw.countries.id;


--
-- Name: weather; Type: TABLE; Schema: raw; Owner: postgres
--

CREATE TABLE raw.weather (
    id integer NOT NULL,
    capital text,
    date date,
    temp_max double precision,
    temp_min double precision,
    precipitation double precision,
    windspeed_max double precision,
    sunshine_duration double precision
);


ALTER TABLE raw.weather OWNER TO postgres;

--
-- Name: weather_id_seq; Type: SEQUENCE; Schema: raw; Owner: postgres
--

CREATE SEQUENCE raw.weather_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE raw.weather_id_seq OWNER TO postgres;

--
-- Name: weather_id_seq; Type: SEQUENCE OWNED BY; Schema: raw; Owner: postgres
--

ALTER SEQUENCE raw.weather_id_seq OWNED BY raw.weather.id;


--
-- Name: countries id; Type: DEFAULT; Schema: clean; Owner: postgres
--

ALTER TABLE ONLY clean.countries ALTER COLUMN id SET DEFAULT nextval('clean.countries_id_seq'::regclass);


--
-- Name: weather id; Type: DEFAULT; Schema: clean; Owner: postgres
--

ALTER TABLE ONLY clean.weather ALTER COLUMN id SET DEFAULT nextval('clean.weather_id_seq'::regclass);


--
-- Name: countries id; Type: DEFAULT; Schema: raw; Owner: postgres
--

ALTER TABLE ONLY raw.countries ALTER COLUMN id SET DEFAULT nextval('raw.countries_id_seq'::regclass);


--
-- Name: weather id; Type: DEFAULT; Schema: raw; Owner: postgres
--

ALTER TABLE ONLY raw.weather ALTER COLUMN id SET DEFAULT nextval('raw.weather_id_seq'::regclass);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: clean; Owner: postgres
--

ALTER TABLE ONLY clean.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: weather weather_pkey; Type: CONSTRAINT; Schema: clean; Owner: postgres
--

ALTER TABLE ONLY clean.weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (id);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: raw; Owner: postgres
--

ALTER TABLE ONLY raw.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: weather weather_pkey; Type: CONSTRAINT; Schema: raw; Owner: postgres
--

ALTER TABLE ONLY raw.weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (id);


--
-- Name: weather weather_country_id_fkey; Type: FK CONSTRAINT; Schema: clean; Owner: postgres
--

ALTER TABLE ONLY clean.weather
    ADD CONSTRAINT weather_country_id_fkey FOREIGN KEY (country_id) REFERENCES clean.countries(id);


--
-- PostgreSQL database dump complete
--