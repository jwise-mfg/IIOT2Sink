from datetime import datetime, timezone
import paho.mqtt
import paho.mqtt.client as mqtt
import requests
import json
import random
import os
from pprint import pprint
from sinks import sinkadapters

if __name__ == '__main__':
    for p in sinkadapters.sinks:
        inst = p()
        inst.start()

class subscription():
    def __init__(self):
        self.topic = None
        self.member = None
        self.sink = None
        self.command = None

#TODO: Load from a Config File
mqtt_broker = "192.168.10.5"
mqtt_client = f'MqttClientToSink-{random.randint(0, 1000)}'
mqtt_subscriptions = []

#TODO: Load from a Subscriptions Config file
sub1 = subscription()
sub1.topic = "energy/growatt"
sub1.member = "values.batterySoc"
sub1.sink = "log2csv"
sub1.label = "Solar Battery %"
mqtt_subscriptions.append(sub1)

sub2 = subscription()
sub2.topic = "gateway/34:94:54:C8:4C:40/sensor/00:13:A2:00:41:FA:EF:FB"
sub2.member = "00:13:A2:00:41:FA:EF:FB.temperature"
sub2.sink = ["log2csv","sql"]
sub2.label = "Solar Shed Temp"
mqtt_subscriptions.append(sub2)

def make_datetime_utc():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') 

def search_json(data, member):
    for key, value in data.items():
        if key == member:
            return value

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("Received MQTT message: ", msg)
    # Check if there's sink configuration
    for sub in mqtt_subscriptions:
        if sub.topic == message.topic:
            msg_sub = sub
            if msg_sub.label == None:
                msg_sub.label = msg_sub.topic
    if msg_sub.member == None or msg_sub.member == "":
        print ("No message member defined, using raw value")
        value = msg
    else:
        # Check if the payload contains the configured member and parse out its avlue
        print ("Searching for JSON payload member: " + msg_sub.member)
        data = json.loads(msg)
        #TODO: error handling
        member_parts = msg_sub.member.split(".")
        for member in member_parts:
            data = search_json(data, member)
        value = data
        print ("Using discovered value:", value)

    # Check if we have a place to send the data
    if isinstance(msg_sub.sink, list):
        print ("using multiple sinks:", json.dumps(msg_sub.sink))
    else:
        print ("Using sink: ", msg_sub.sink)
    
    # Check if that requested sink adapter exists and write to it
    for config_sink in msg_sub.sink:
        for sink in sinkadapters.sinks:
            if sink.name.lower() == config_sink.lower():
                print ("sending to sink", sink.name)
                sink.write(make_datetime_utc(), value, msg_sub)

print("Using paho-mqtt version: ", paho.mqtt.__version__)
if paho.mqtt.__version__[0] > '1':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, mqtt_client)
else:
    client = mqtt.Client(mqtt_client)

client.connect(mqtt_broker)
for sub in mqtt_subscriptions:
    print("subscribing to: ", sub.topic)
    client.subscribe(str(sub.topic))
client.on_message=on_message
client.loop_forever()
