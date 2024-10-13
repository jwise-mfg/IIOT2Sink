#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo Starting MQTT2Sink
echo -n "Checking environment..."
if command -v python3 >/dev/null 2>&1 ; then
    if [ ! -f config.yml ]; then
        echo FAIL!
        echo "config.yml not found! Review the readme to setup your environment"
    else
        echo "OK"
        echo -n "Loading configuration."
        python3 -m venv .
        echo -n "."
        source $SCRIPT_DIR/bin/activate
        echo ".OK"
        /usr/bin/python3 $SCRIPT_DIR/start.py
    fi
else
    echo FAIL!
    echo "This tool requires Python3 and a venv for dependencies"
fi
