import paho.mqtt.client as mqtt
import json
import ssl
import datetime as dt
from datetime import timezone
from fmiopendata.wfs import download_stored_query


end_time = dt.datetime.now(timezone.utc)
start_time = end_time - dt.timedelta(minutes=5)

start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_forecast(latlon):

    forecast = download_stored_query(
        "fmi::forecast::harmonie::surface::point::multipointcoverage",
        args=["latlon=" + latlon,
          "parameters=temperature,windspeedms,winddirection,humidity"]
    )

    current_forecast = min(forecast.data.keys())
    current_grid = sorted(forecast.data[current_forecast].keys())[0]
    print(forecast.data[current_forecast][current_grid].items())



def on_connect(client, userdata, flags, rc):
    client.subscribe("vessels-v2/230703000/location")
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


