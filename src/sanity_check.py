import datetime as dt
from datetime import timezone
from fmiopendata.wfs import download_stored_query
import psycopg2




def fetch_rajakari_forecast():

    params = "Pressure,Temperature,Humidity,WindDirection,WindSpeedMS,PrecipitationAmount,TotalCloudCover,Visibility"

    latlons = [
    "60.286758,27.184825",
    "60.375377,26.958926",
    "60.274765,26.447587",
    "60.203820,25.625460",
    "59.985683,25.598788",
    "60.303725,25.549164",
    "60.101207,25.194394",
    "60.105120,24.975390",
    "59.919823,24.350229",
    "59.994639,23.995599",
    "59.931136,24.014082",
    "59.843831,23.248587",
    "59.773633,22.948683",
    "59.808642,22.912464",
    "59.869490,22.193427",
    "59.779094,21.374788",
    "60.111626,21.698278",
    "60.377880,22.096400",
    "60.386903,22.551826",
    "60.258229,20.746975",
    "60.115843,20.297649",
    "59.959108,19.953736",
    "60.091359,19.929101",
    "60.300980,19.131420",
    "60.722198,21.026810",
    "61.144750,21.302730",
    "61.630419,21.376203",
    "62.333816,21.190813",
    "62.934880,21.184850",
    "62.978388,20.740078",
    "63.098706,21.639378",
    "63.435083,21.068557",
    "63.751440,22.522820",
    "63.838822,23.097148",
    "63.951140,22.845370",
    "64.330730,23.446270",
    "64.611783,23.896737",
    "64.665890,24.406950",
    "65.039750,24.561180",
    "65.006370,25.393248",
    "65.385078,24.095684",
    "65.673180,24.515193",
]
    
    now = dt.datetime.utcnow()
    end_time = now + dt.timedelta(hours=2)
    start_time = now - dt.timedelta(hours=2)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    for latlon in latlons:
        forecast = download_stored_query(
            "fmi::forecast::harmonie::surface::point::multipointcoverage",
            args=[
                "latlon=" + latlon,
                "starttime=" + start_time,
                "endtime=" + end_time,
                "parameters=" + params
            ]
        )
        
        diffs = []
        for timestamp in forecast.data.keys():
            diff = abs(timestamp - now) 
            diffs.append(diff)

    
        idx_closest = diffs.index(min(diffs))
        closest_forecast = list(forecast.data.keys())[idx_closest]
        closest_forecast = forecast.data[closest_forecast]
        location = list(closest_forecast.keys())[0]
        sensor_values = closest_forecast[location].values()

    pass
    print(forecast.data.keys())
    print('\n' + str(diffs))
    print('\n' + str(idx_closest))
    print(f"\n{closest_forecast}")




def insert_data(sensor_values):
    data = []
    for value in sensor_values:
        value = value['value']
        data.append(value)

    conn = psycopg2.connect(
        dbname="weather_data", 
        user="postgres",
        password=''
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO forecasts VALUES (%s, %s, %s)"
    )





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

    CREATE TABLE IF NOT EXISTS forecasts (
        id SERIAL PRIMARY KEY,
        location_id INTEGER REFERENCES locations(id),
        forecast_time TIMESTAMP NOT NULL,
        air_pressure FLOAT,
        air_temperature FLOAT,
        humidity FLOAT,
        wind_speed FLOAT,
        wind_direction FLOAT,
        precipitation_amount FLOAT,
        total_cloud_cover FLOAT,
        air_pressure FLOAT,
        visibility FLOAT
    );
    """
    )
    conn.close()


fetch_rajakari_forecast()
