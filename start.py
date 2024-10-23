import json
from common import utils
from sources import frommqtt
#from sources import fromopcua
from sinks import sinkadapters

config = utils.load_config()

# Determine source
mqttsource = frommqtt.mqttsource()
#opcuasource = fromopcua.opcuasource()
source = list(config['source'].keys())[0]
print ("-Using source:", str(source))

# Load sink adapters
print("Loading sinks...")
if __name__ == '__main__':
    for p in sinkadapters.sinks:
        inst = p()
        print('-', end='')
        inst.start()

if source == "mqtt" and "mqtt" in config['source']:
    mqttsource.connect(sinkadapters)
#if source == "opcua" and "opcua" in config['source']:
#    opcua.connect(sinkadapters)