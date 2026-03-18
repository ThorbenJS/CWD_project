import paho.mqtt.client as mqtt
import json
import ssl

line = "----------"

def on_connect(client, userdata, flags, rc):
    client.subscribe("vessels-v2/230704000/location")
    print("Connection established.")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(json.dumps(data))
    print(line * 15)

client = mqtt.Client(transport="websockets")
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

client.connect("meri.digitraffic.fi", 443)
client.loop_forever()