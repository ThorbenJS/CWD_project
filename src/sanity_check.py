import datetime as dt
from datetime import timezone
from fmiopendata.wfs import download_stored_query
import psycopg2




def fetch_rajakari_forecast():

    latlon = "60.38,22.1"

    now = dt.datetime.now(timezone.utc)
    end_time = now + dt.timedelta(hours=1)
    start_time = now - dt.timedelta(hours=1000)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    forecast = download_stored_query(
        "fmi::forecast::harmonie::surface::point::multipointcoverage",
        args=[
            "latlon=" + latlon,
            "starttime=" + start_time,
            "endtime=" + end_time
          ]
    )
    times = list(forecast.data.keys())
    

def parse_parameters(obs_params, forecast_params):
    obs_wind_speed = obs_params["Wind Speed"]



def configure_db():
    conn = psycopg2.connect(
        dbname="weather_data", 
        user="postgres",
        password=''
    )
    cursor = conn.cursor()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        latitude FLOAT,
        longitude FLOAT
    );

    CREATE TABLE IF NOT EXISTS observations (
        id SERIAL PRIMARY KEY,
        location_id INTEGER REFERENCES locations(id)
        observation_time TIMESTAMP NOT NULL,
        air_temperature FLOAT,
        relative_humidity FLOAT,
        wind_speed FLOAT,
        wind_direction FLOAT,
        precipitation_amount FLOAT,
        air_pressure FLOAT
    );

    CREATE TABLE IF NOT EXISTS forecasts (
        id SERIAL PRIMARY KEY,
        location_id INTEGER REFERENCES locations(id),
        forecast_time TIMESTAMP NOT NULL,
        air_temperature FLOAT,
        relative_humidity FLOAT,
        wind_speed FLOAT,
        wind_direction FLOAT,
        precipitation_amount FLOAT,
        air_pressure FLOAT
    );
    """
    )
    conn.close()


fetch_rajakari_forecast()
