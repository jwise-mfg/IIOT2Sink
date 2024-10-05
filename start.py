from datetime import datetime, timezone
import paho.mqtt
import paho.mqtt.client as mqtt
import requests
import json
import random

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
sub1.sink = "log"
sub1.label = "Solar Battery %"
mqtt_subscriptions.append(sub1)

sub2 = subscription()
sub2.topic = "gateway/34:94:54:C8:4C:40/sensor/00:13:A2:00:41:FA:EF:FB"
sub2.member = "00:13:A2:00:41:FA:EF:FB.temperature"
sub2.sink = "log"
sub2.label = "Solar Shed Temp"
mqtt_subscriptions.append(sub2)
#TODO: Make sinks extensible
#sub.sink = "database"
#sub.command = "insert into tbl_values (batterySoc) values (%value%)"
#sub.sink = "graphql"
#etc...

def make_datetime_utc():
	return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') 

def search_json(data, member):
	for key, value in data.items():
		if key == member:
			return value

def on_message(client, userdata, message):
	msg = str(message.payload.decode("utf-8"))
	print("Received MQTT message: ", msg)
	for sub in mqtt_subscriptions:
		if sub.topic == message.topic:
			member = sub.member
			sink = sub.sink
			command = sub.command
			topic = sub.topic
			label = sub.topic
			if sub.label != None:
				label = sub.label

	if member == None:
		print ("No message member defined, using raw value")
		value = msg
	if member == "":
		print ("No message member defined, using raw value")
		value = msg
	else:
		print ("Searching for JSON payload member: " + member)
		data = json.loads(msg)
		#TODO: error handling
		member_parts = member.split(".")
		for member in member_parts:
			data = search_json(data, member)
		value = data
		print ("Using discovered value:", value)

	print ("Using sink: ", sink)
	if sink == "log":
		with open('mqtt_log.csv', 'a') as f:
			print ("Writing to mqtt_log.csv: ", str(value))
			f.write(make_datetime_utc() + "," + label + "," + str(value) + "\r\n")
	if sink == "database":
		if command != None:
			command = command.replace("%value%", str(value))
			print ("Using command: ", command)

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
