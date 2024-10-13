import sinks
import os
import yaml

class log2csv(sinks.sinkadapters):

    # Load config
    # TODO: It would be nice if this could be passed into the sink constructor somehow...
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    name = "log2csv"
    logpath = config['sinks']['log2csv']['path']
    maxsize = config['sinks']['log2csv']['maxsize']
    maxflush = config['sinks']['log2csv']['flushonmax']

    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using log file: {self.logpath}")

    def write(self, timestamp, value, sinkparam, subscription):
        if os.path.getsize(self.logpath) > self.maxsize:
            if self.maxflush == True:
                print(f"Log file at {self.logpath} exceeded max size of {self.maxsize} bytes and has been flushed!")
                open(self.logpath, 'w').close()
            else:
                print(f"Log file at {self.logpath} exceeds max size of {self.maxsize} bytes and is not configured to flush. Cannot log {value}.")
                return
        with open(self.logpath, 'a') as f:
            value = str(value)
            print (f"Logging to {self.logpath}: {value}")
            f.write(timestamp + "," + subscription["label"] + "," + str(value) + "\r\n")