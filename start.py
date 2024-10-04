from datetime import datetime
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
sub.topic = "test/jon"
sub.member = "values.batterySoc"
sub.sink = "log"
#TODO: Make sinks extensible
#sub.sink = "database"
#sub.command = "insert into tbl_values (batterySoc) values (%value%)"
mqtt_subscriptions.append(sub)

def make_datetime_utc():
	utc_time = str(datetime.utcnow())
	time_parts = utc_time.split(" ")
	utc_time = "T".join(time_parts)
	time_parts = utc_time.split(".")
	utc_time = time_parts[0] + "Z"
	return utc_time

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
		print ("Could not find message member, using raw value")
		value = msg
	else:
		print ("Searching for JSON payload member: " + member)
		data = json.loads(msg)
		parse_members = member.split(".")
		for member in parse_members:
			data = search_json(data, member)
		value = data
		print ("Value:", value)

	print ("Using sink: ", sink)
	if sink == "log":
		with open('log.txt', 'a') as f:
			print ("Writing to log.txt", str(value))
			f.write(str(value) + "\r\n")
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
