# Source2Sink

Its harder than it should be to get a lot of Industrial IoT messages into somewhere you can use them. This attempts to fix that. Supports MQTT with simple parsing of JSON payloads, OPCUA Client/Server and a variety of destinations (called sinks) to send the data too. Sinks are extensible, and new ones can easily be added.

## Requirements
Python3 with venv

Tested on Debian-based Linux, but should be usable on other distros and Mac. Windows will work, but you'll need to set up the venv yourself, and start manually.

## Install
- Copy a config from the examples folder to the root as `config.py` then edit for your sinks

Note that while you can have multiple sinks in use at one time, you can only have one source for each config. If more than one is present in the config, only the first one will be used.

## Run

### Easy (Hopefully Just Works)
- Start by executing the start.sh script OR

### Manual (Do this if you want to tinker/edit/extend)
- Create a python3 virtual environment in this folder: `python3 -m venv .`
- Activate the environment: `source bin/activate`
- Install the dependencies (including dependencies for any sinks you wish to use):
    - `pip install paho-mqtt`
    - `pip install pyyaml`
    - mysqlsink
        - `pip install mysql-connector`
    - smipgraphql
        - `pip install requests`
- Run `python3 start.py`