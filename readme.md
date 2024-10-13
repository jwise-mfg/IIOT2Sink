# Mqtt2Sink

Its harder than it should be to get a lot of MQTT messages into somewhere you can use them. This attempts to fix that. Supports simple parsing of JSON payloads, and a variety of destinations (called sinks) to send the data too. Sinks are extensible, and new ones can easily be added.

## Requirements
Python3 with venv

Tested on Debian-based Linux, but should be usable on other distros and Mac. Windows will work, but you'll need to set up the venv yourself, and start manually.

## Install
- Copy `config-example.py` to `config.py` then edit for your sinks

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