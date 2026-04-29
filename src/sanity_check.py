import datetime as dt
from datetime import timezone
from fmiopendata.wfs import download_stored_query
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

stations = [
    {"name": "Kotka Haapasaari", "fmisid": 101042, "lat": 60.286758, "lon": 27.184825},
    {"name": "Kotka Rankki", "fmisid": 101030, "lat": 60.375377, "lon": 26.958926},
    {"name": "Loviisa Orrengrund", "fmisid": 101039, "lat": 60.274765, "lon": 26.447587},
    {"name": "Porvoo Emäsalo", "fmisid": 101023, "lat": 60.203820, "lon": 25.625460},
    {"name": "Porvoo Kalbådagrund", "fmisid": 101022, "lat": 59.985683, "lon": 25.598788},
    {"name": "Porvoo Kilpilahti", "fmisid": 100683, "lat": 60.303725, "lon": 25.549164},
    {"name": "Sipoo Itätoukki", "fmisid": 105392, "lat": 60.101207, "lon": 25.194394},
    {"name": "Helsinki Harmaja", "fmisid": 100996, "lat": 60.105120, "lon": 24.975390},
    {"name": "Kirkkonummi Mäkiluoto", "fmisid": 100997, "lat": 59.919823, "lon": 24.350229},
    {"name": "Inkoo Jakobramsjö", "fmisid": 108020, "lat": 59.994639, "lon": 23.995599},
    {"name": "Inkoo Bågaskär", "fmisid": 100969, "lat": 59.931136, "lon": 24.014082},
    {"name": "Hanko Tvärminne", "fmisid": 100953, "lat": 59.843831, "lon": 23.248587},
    {"name": "Hanko Russarö", "fmisid": 100932, "lat": 59.773633, "lon": 22.948683},
    {"name": "Hanko Tulliniemi", "fmisid": 100946, "lat": 59.808642, "lon": 22.912464},
    {"name": "Kemiönsaari Vänö", "fmisid": 100945, "lat": 59.869490, "lon": 22.193427},
    {"name": "Parainen Utö", "fmisid": 100908, "lat": 59.779094, "lon": 21.374788},
    {"name": "Parainen Fagerholm", "fmisid": 100924, "lat": 60.111626, "lon": 21.698278},
    {"name": "Turku Rajakari", "fmisid": 100947, "lat": 60.377880, "lon": 22.096400},
    {"name": "Kaarina Yltöinen", "fmisid": 100934, "lat": 60.386903, "lon": 22.551826},
    {"name": "Kumlinge kirkonkylä", "fmisid": 100928, "lat": 60.258229, "lon": 20.746975},
    {"name": "Lumparland Långnäs", "fmisid": 151048, "lat": 60.115843, "lon": 20.297649},
    {"name": "Lemland Nyhamn", "fmisid": 100909, "lat": 59.959108, "lon": 19.953736},
    {"name": "Maarianhamina Länsisatama", "fmisid": 151029, "lat": 60.091359, "lon": 19.929101},
    {"name": "Hammarland Märket", "fmisid": 100919, "lat": 60.300980, "lon": 19.131420},
    {"name": "Kustavi Isokari", "fmisid": 101059, "lat": 60.722198, "lon": 21.026810},
    {"name": "Rauma Kylmäpihjala", "fmisid": 101061, "lat": 61.144750, "lon": 21.302730},
    {"name": "Pori Tahkaluoto", "fmisid": 101267, "lat": 61.630419, "lon": 21.376203},
    {"name": "Kaskinen Sälgrund", "fmisid": 101256, "lat": 62.333816, "lon": 21.190813},
    {"name": "Korsnäs Bredskäret", "fmisid": 101479, "lat": 62.934880, "lon": 21.184850},
    {"name": "Maalahti Strömmingsbådan", "fmisid": 101481, "lat": 62.978388, "lon": 20.740078},
    {"name": "Vaasa Klemettilä", "fmisid": 101485, "lat": 63.098706, "lon": 21.639378},
    {"name": "Mustasaari Valassaaret", "fmisid": 101464, "lat": 63.435083, "lon": 21.068557},
    {"name": "Pietarsaari Kallan", "fmisid": 101660, "lat": 63.751440, "lon": 22.522820},
    {"name": "Kokkola Santahaka", "fmisid": 101675, "lat": 63.838822, "lon": 23.097148},
    {"name": "Kokkola Tankar", "fmisid": 101661, "lat": 63.951140, "lon": 22.845370},
    {"name": "Kalajoki Ulkokalla", "fmisid": 101673, "lat": 64.330730, "lon": 23.446270},
    {"name": "Raahe Nahkiainen", "fmisid": 101775, "lat": 64.611783, "lon": 23.896737},
    {"name": "Raahe Lapaluoto", "fmisid": 101785, "lat": 64.665890, "lon": 24.406950},
    {"name": "Hailuoto Marjaniemi", "fmisid": 101784, "lat": 65.039750, "lon": 24.561180},
    {"name": "Oulu Vihreäsaari", "fmisid": 101794, "lat": 65.006370, "lon": 25.393248},
    {"name": "Kemi majakka", "fmisid": 101783, "lat": 65.385078, "lon": 24.095684},
    {"name": "Kemi Ajos", "fmisid": 101846, "lat": 65.673180, "lon": 24.515193},
]

params = "Pressure,Temperature,Humidity,WindSpeedMS,WindDirection,PrecipitationAmount,TotalCloudCover,Visibility"


 

def fetch_rajakari_forecast():
    now = dt.datetime.utcnow()
    end_time = now + dt.timedelta(hours=2)
    start_time = now - dt.timedelta(hours=2)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    for station in stations:
        latlon = str(station["lat"]) + ',' +  str(station["lon"])
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
        closest_forecast_time = list(forecast.data.keys())[idx_closest]
        closest_forecast = forecast.data[closest_forecast_time]
        location = list(closest_forecast.keys())[0]
        sensor_values = closest_forecast[location].values()

        insert_data(sensor_values, station["fmisid"], closest_forecast_time)




def insert_data(sensor_values, fmisid, time):
    data = []
    for value in sensor_values:
        value = value['value']
        data.append(value)
    
    data.insert(0, fmisid)
    data.insert(0, time)
    
    conn = psycopg.connect(
        host="localhost",
        dbname="weather", 
        user=os.getenv("PSQL_USER"),
        password=os.getenv("PSQL_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO forecasts (forecast_time, fmisid, air_pressure, air_temperature, humidity, wind_speed,
        wind_direction, precipitation_amount, total_cloud_cover, visibility) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data)
    )
    conn.commit()
    conn.close()



def insert_stations():
    conn = psycopg.connect(
        host="localhost",
        dbname="weather", 
        user=os.getenv("PSQL_USER"),
        password=os.getenv("PSQL_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO stations (fmisid, name, latitude, longitude) VALUES (%s, %s, %s, %s)
        ON CONFLICT (fmisid) DO NOTHING
        """,
        ([(s["fmisid"], s["name"], s["lat"], s["lon"]) for s in stations])
    )
    conn.commit()
    conn.close()




def configure_db():
    conn = psycopg.connect(
        host="localhost",
        dbname="weather", 
        user=os.getenv("PSQL_USER"),
        password=os.getenv("PSQL_PASSWORD")
    )
    cursor = conn.cursor()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stations (
        fmisid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL
    );

    CREATE TABLE IF NOT EXISTS forecasts (
        id SERIAL PRIMARY KEY,
        forecast_time TIMESTAMP NOT NULL,
        fmisid INTEGER REFERENCES stations(fmisid),
        air_pressure FLOAT,
        air_temperature FLOAT,
        humidity FLOAT,
        wind_speed FLOAT,
        wind_direction FLOAT,
        precipitation_amount FLOAT,
        total_cloud_cover FLOAT,
        visibility FLOAT
    );
    """
    )
    conn.commit()
    conn.close()


configure_db()
insert_stations()
fetch_rajakari_forecast()
