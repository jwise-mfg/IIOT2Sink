import json
import paho.mqtt
import paho.mqtt.client as mqtt
from common import utils

class mqttsource():

    def __init__(self):
        print ("Loaded MQTT Source")
        pass
    
    config = utils.load_config()

    # Remember all subscriptions
    mqtt_subscriptions = config['source']['mqtt']['subscriptions']

    def search_json(self, data, member):
        for key, value in data.items():
            if key == member:
                return value

    # Main MQTT message handling
    def on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print(f"=== Received MQTT message at {utils.make_datetime_utc()}")
        print(msg)
        # Check if there's sink configuration
        for sub in self.mqtt_subscriptions:
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
            try:
                data = json.loads(msg)
                member_parts = msg_sub["member"].split(".")
                for member in member_parts:
                    data = self.search_json(data, member)
                value = data
                print ("Parsed value:", value)
            except Exception as e:
                print ("Could not parse MQTT Payload!")
                print (e)
                value = None

        # TODO: option to not post duplicate values
        if value != None:
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
                for sink in self.sinkadapters.sinks:
                    if sink.name.lower() == config_sink.lower():
                        sinkparam = None
                        if "sinkparam" in msg_sub:
                            sinkparam = msg_sub["sinkparam"]
                            if isinstance(sinkparam, list):
                                sinkparam = sinkparam[i]
                            print (f"Sending {value} to {sink.name} with params: {sinkparam}")
                            print(' ', end='')
                        else:
                            print (f"Sending {value} to {sink.name}")
                            print(' ', end='')
                        sink.write(sink, utils.make_datetime_utc(), value, sinkparam, msg_sub)
                i = i + 1
            print("=== Done processing message")
        else:
            print("=== Failed processing message")

    def connect(self, sinkadapters):
        # Connect to MQTT Broker (handle different library versions)
        self.sinkadapters = sinkadapters
        print(f"Connecting paho-mqtt version: {paho.mqtt.__version__} with client id {self.config['source']['mqtt']['clientid']}")
        if paho.mqtt.__version__[0] > '1':
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.config['source']['mqtt']['clientid'])
        else:
            client = mqtt.Client(self.config['source']['mqtt']['clientid'])
        client.connect(self.config['source']['mqtt']['broker'], self.config['source']['mqtt']['port'])
        for sub in self.mqtt_subscriptions:
            print("-Subscribing to:", sub["topic"])
            client.subscribe(str(sub["topic"]))
        print("Awaiting messages...")
        client.on_message=self.on_message
        client.loop_forever()