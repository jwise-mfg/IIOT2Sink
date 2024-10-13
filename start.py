from datetime import datetime, timezone
import paho.mqtt
import paho.mqtt.client as mqtt
import json
import random
import yaml
from sinks import sinkadapters

# Load config
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Load sink adapters
print("Loading sinks...")
if __name__ == '__main__':
    for p in sinkadapters.sinks:
        inst = p()
        print('-', end='')
        inst.start()

# Define a subscription
class subscription():
    def __init__(self):
        self.topic = None
        self.member = None
        self.sink = None
        self.label = None
        self.sinkargs = None

# Remember all subscriptions
mqtt_subscriptions = config['mqtt']['subscriptions']

def make_datetime_utc():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') 

def search_json(data, member):
    for key, value in data.items():
        if key == member:
            return value

# Main MQTT message handling
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print(f"=== Received MQTT message at {make_datetime_utc()}")
    print(msg)
    # Check if there's sink configuration
    for sub in mqtt_subscriptions:
        if sub["topic"] == message.topic:
            msg_sub = sub
            # Make sure there's a label, default to topic name
            if msg_sub["label"] == None:
                msg_sub["label"] = msg_sub["topic"]

    # Figure out what kind of value to extract
    if msg_sub["member"] == None or msg_sub["member"] == "":
        print ("No message member defined, using raw value")
        value = msg
    else:
        # Check if the payload contains the configured member and parse out its avlue
        print ("Searching for JSON payload member: " + msg_sub["member"])
        data = json.loads(msg)
        #TODO: error handling
        member_parts = msg_sub["member"].split(".")
        for member in member_parts:
            data = search_json(data, member)
        value = data
        print ("Discovered value:", value)

    # TODO: option to not post duplicate values

    # Check if we have a place to send the data
    if isinstance(msg_sub["sink"], list):
        print ("Using multiple sinks:", json.dumps(msg_sub["sink"]))
    else:
        print ("Using sink: ", msg_sub["sink"])
    
    # Check if that requested sink adapter exists and write to it
    config_sinks = msg_sub["sink"]
    if not isinstance(config_sinks, list):
        config_sinks = [msg_sub["sink"]]
    i = 0
    for config_sink in config_sinks:
        for sink in sinkadapters.sinks:
            if sink.name.lower() == config_sink.lower():
                sinkparam = msg_sub["sinkparam"]
                if isinstance(sinkparam, list):
                    sinkparam = sinkparam[i]
                print (f"Sending {value} to {sink.name} with params: {sinkparam}")
                sink.write(sink, make_datetime_utc(), value, sinkparam, msg_sub)
        i = i + 1
    print("=== Done processing message")

# Connect to MQTT Broker (handle different library versions)
print(f"Connecting paho-mqtt version: {paho.mqtt.__version__} with client id {config['mqtt']['clientid']}")
if paho.mqtt.__version__[0] > '1':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, config['mqtt']['clientid'])
else:
    client = mqtt.Client(config['mqtt']['clientid'])
client.connect(config['mqtt']['broker'], config['mqtt']['port'])
for sub in mqtt_subscriptions:
    print("-Subscribing to:", sub["topic"])
    client.subscribe(str(sub["topic"]))
print("Awaiting messages...")
client.on_message=on_message
client.loop_forever()
