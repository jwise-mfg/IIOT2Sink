# IIOT to Sink

Its harder than it should be to get a lot of Industrial IoT messages into somewhere you can use them. This attempts to fix that. Supports MQTT with simple parsing of JSON payloads, OPCUA Client/Server (coming soon!) and a variety of destinations (called sinks) to send the data too. Sinks are extensible, and new ones can easily be added.
Hi Suellen.

## Requirements

- Python3 with venv

Tested on Debian-based Linux, but should be usable on other distros. Also works on Mac and Windows.

## Install
- Copy a config from the examples folder to the root as `config.py` then edit for your sources and sinks

Note that while you can have multiple sinks in use at one time, you can only have one source for each config. If more than one is present in the config, only the first one will be used.

## Run

### Easy on Linux or Mac (Hopefully Just Works)
- Start by executing the `start.sh` script

### Easy on Windows
- Launch a PowerShell window
- Execute `start.bat`

### Manual (If you want to tinker/edit/extend on any OS)
- Create a python3 virtual environment in this folder: `python3 -m venv .`
- Activate the environment: `source bin/activate`
- Install the dependencies:
    - `pip install -r requirements.txt`
- Run `python3 start.py`

### Clean Run
- If you move or rename the project folder, you may find your venv doesn't work any more. This can easily be fixed with a clean run: `start.sh --clean` (`start.bat --clean` on Windows)

## Install as a Service (Linux)

*After* you've successfully gotten everything running with `start.sh` you should be able to install as a service on systemd equipped Linux distros (eg: Ubunutu, Raspbian):

`sudo ./install-service.sh`

You can check status with:

`sudo systemctl status iiot-to-sink.service`

You can view logs with:

`sudo journalctl -u iiot-to-sink.service`

### Remove the Service

You can remove the service with:

`sudo ./install-service.sh --remove-service`
