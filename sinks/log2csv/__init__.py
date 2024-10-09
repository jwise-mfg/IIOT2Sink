import sinks

class log2csv(sinks.sinkadapters):

    name = "log2csv"

    def __init__(self):
        pass

    def start(self):
        print("log2csv for real!")

    def write(timestamp, value, subscription):
        with open('mqtt_log.csv', 'a') as f:
            print ("Writing to mqtt_log.csv: ", str(value))
            f.write(timestamp + "," + subscription.label + "," + str(value) + "\r\n")