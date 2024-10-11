#!/bin/bash
echo Starting MQTT Client to Sink
#TODO check for python3 and dependencies
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
/usr/bin/python3 $SCRIPT_DIR/start.py