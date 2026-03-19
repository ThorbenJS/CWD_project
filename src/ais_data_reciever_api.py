import paho.mqtt.client as mqtt
import json
import ssl
import datetime as dt
from datetime import timezone
from fmiopendata.wfs import download_stored_query


ship_mmsi : str = "230704000"


def get_closest_forecast(forecasts, now):

    erotukset = []

    for forecast in forecasts.data.keys():
        print(forecast, '\n')
        forecast = forecast.replace(tzinfo=timezone.utc)
        erotus = abs(now - forecast)
        erotukset.append(erotus)

    smallest = min(erotukset)
    idx = erotukset.index(smallest)
    
    return list(forecasts.data.keys())[idx]


def get_forecast(latlon):

    now = dt.datetime.now(timezone.utc)

    end_time = now + dt.timedelta(hours=3)
    start_time = end_time - dt.timedelta(hours=10)

    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    forecasts = download_stored_query(
        "fmi::forecast::harmonie::surface::point::multipointcoverage",
        args=[
            "latlon=" + latlon,
            "parameters=temperature,windspeedms,winddirection,humidity",
            "starttime=" + start_time,
            "endtime=" + end_time
          ]
    )

    print(forecasts.data.keys(), '\n')

    closest_forecast_datetime = get_closest_forecast(forecasts, now)
    print(closest_forecast_datetime, '\n')



    closest_forecast = forecasts.data[closest_forecast_datetime]
    current_location = list(closest_forecast.keys())[0]
    
    parameters = forecasts.data[closest_forecast_datetime][current_location].items()
    
    for parameter, value in parameters:
        print(parameter, value)



def on_connect(client, userdata, flags, rc):
    client.subscribe("vessels-v2/" + ship_mmsi + "/location")
    print("Connection established.")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    latitude = round(data["lat"], 2)
    longitude = round(data["lon"], 2)
    latlon = str(latitude) + ',' + str(longitude)

    get_forecast(latlon)


client = mqtt.Client(transport="websockets")
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

client.connect("meri.digitraffic.fi", 443)
client.loop_forever()


