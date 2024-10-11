#!/bin/bash
if [ "$EUID" -ne 0 ]
      then echo "Please run as root"
      exit 1
fi

installservice() {
    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
    echo This will install a systemd service for this script using $SCRIPT_DIR. 
    read -p "Do you want to proceed (Y/N)? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo Installation cancelled.
        exit 0
    fi

    UNIT_PATH=/etc/systemd/system/mqtt-to-sink
    if [ -f "$UNIT_PATH"".service" ]; then
        echo Service already installed!
        echo Remove with --remove-service
        exit 1
    fi
    if [ $(which systemctl) ]; then
        # Create the Service
        echo "[Unit]" > "$UNIT_PATH"".service"
        echo "Description=MQTT to Sink Service" >> "$UNIT_PATH"".service"
        echo "Wants = network-online.target" >> "$UNIT_PATH"".service"
        echo "After = network.target network-online.target" >> "$UNIT_PATH"".service"
        echo "" >> "$UNIT_PATH"".service"
        echo "[Service]" >> "$UNIT_PATH"".service"
        echo "ExecStart=$SCRIPT_DIR""/start.sh" >> "$UNIT_PATH"".service"
        echo "Restart=always" >> "$UNIT_PATH"".service"
        echo "" >> "$UNIT_PATH"".service"
        echo "[Install]" >> "$UNIT_PATH"".service"
        echo "WantedBy=multi-user.target" >> "$UNIT_PATH"".service"
        # Install
        systemctl daemon-reload
        systemctl enable mqtt-to-sink.service
        systemctl start mqtt-to-sink.service
        echo Installation complete!
    else
        echo Installation not currently supported on environments without systemd
        exit 2
    fi
}

removeservice() {
    UNIT_PATH=/etc/systemd/system/mqtt-to-sink
    if [ $(which systemctl) ]; then
      if [ -f "$UNIT_PATH"".service" ]; then
         systemctl stop mqtt-to-sink.service
         systemctl disable mqtt-to-sink.service
         rm "$UNIT_PATH"".service"
         systemctl daemon-reload
         echo Service removed!
      else
         echo Service not found to remove!
         exit 1
      fi
    else
        echo Removal not currently supported on environments without systemd
        exit 2
    fi
}

if [ "$1" == "--remove-service" ]; then
   removeservice
   exit 0
fi
installservice
exit 0

