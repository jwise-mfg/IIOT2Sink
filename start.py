from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import requests
import json

class subscription():
	def __init__(self):
		self.topic = None
		self.member = None
		self.sink = None
		self.command = None

#TODO: Load from a Config File
mqtt_broker = "192.168.10.5"			#Address of the MQTT Broker
mqtt_client = "MqttClientToServer"
mqtt_subscriptions = []
sub = subscription()
sub.topic = "energy/growatt"
sub.member = "values.batterySoc"
sub.sink = "log"
#TODO: Make sinks extensible
#sub.sink = "database"
#sub.command = "insert into tbl_values (batterySoc) values (%value%)"
#sub.sink = "graphql"
#etc...
mqtt_subscriptions.append(sub)

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
		with open('log.txt', 'a') as f:
			print ("Writing to log.txt: ", str(value))
			f.write(make_datetime_utc() + " - " + str(value) + "\r\n")
	if sink == "database":
		if command != None:
			command = command.replace("%value%", str(value))
			print ("Using command: ", command)

client = mqtt.Client(mqtt_client)
client.connect(mqtt_broker)
for sub in mqtt_subscriptions:
	print("subscribing to: " + sub.topic)
	client.subscribe(str(sub.topic))
client.on_message=on_message
client.loop_forever()
