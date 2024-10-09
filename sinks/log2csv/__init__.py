import sinks
import os
from sinks.log2csv import config

class log2csv(sinks.sinkadapters):

    name = "log2csv"
    logpath = config.logfile["path"]
    maxsize = config.logfile["maxsize"]
    maxflush = config.logfile["flushonmax"]
    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using log file: {self.logpath}")

    def write(self, timestamp, value, subscription):
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