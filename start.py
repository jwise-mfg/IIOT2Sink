import json
import yaml
from sources import frommqtt
from sources import fromopcua
from sinks import sinkadapters

name="Jon is cool"

# Load config
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Determine source
mqttsource = frommqtt.mqttsource()
opcuasource = fromopcua.opcuasource()
source = list(config['source'].keys())[0]
print ("-Using source:", str(source))

# Load sink adapters
print("Loading sinks...")
if __name__ == '__main__':
    for p in sinkadapters.sinks:
        inst = p()
        print('-', end='')
        inst.start()

if source == "mqtt":
    mqttsource.connect(sinkadapters)