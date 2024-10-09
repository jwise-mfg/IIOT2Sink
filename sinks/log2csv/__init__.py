import sinks

class log2csv(sinks.sinkadapters):

    name = "log2csv"

    def __init__(self):
        pass

    def start(self):
        print("log2csv for real!")

    def write(timestamp, value, subscription):
        print("log2csv is writing", value)
        """
        with open('mqtt_log.csv', 'a') as f:
        print ("Writing to mqtt_log.csv: ", str(value))
        f.write(make_datetime_utc() + "," + label + "," + str(value) + "\r\n")
        """