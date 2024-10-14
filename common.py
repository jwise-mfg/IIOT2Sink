import yaml
import os
from datetime import datetime, timezone

# Define a subscription
class subscription():
    def __init__(self):
        self.topic = None
        self.member = None
        self.sink = None
        self.label = None
        self.sinkargs = None

class utils():
    def __init__(self):
        pass

    def make_datetime_utc():
        return datetime.now(timezone.utc).replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def load_config():
        path = os.path.abspath(__file__)
        dirpath = os.path.dirname(path)
        configpath = os.path.join(dirpath, "config.yml")
        with open(configpath, 'r') as file:
            config = yaml.safe_load(file)
        return config
