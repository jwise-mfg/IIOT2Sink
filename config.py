#!/usr/bin/env python
mqtt = {
    "broker": "192.168.10.5",
    "username": "",
    "password": "",
    "clientid": "MqttClientToSink_",
}
subscriptions = [
    {
        "topic": "energy/growatt",
        "member": "values.batterySoc",
        "sink": "log2csv",
        "label": "Solar Battery %",
    },
    {
        "topic": "gateway/34:94:54:C8:4C:40/sensor/00:13:A2:00:41:FA:EF:FB",
        "member": "00:13:A2:00:41:FA:EF:FB.temperature",
        "sink": ["log2csv", "sql"],
        "label": "Solar Shed Temp",
    },
]