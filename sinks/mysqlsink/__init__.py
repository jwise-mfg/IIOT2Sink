import sinks
import yaml
import mysql
import mysql.connector
from datetime import datetime
import calendar

class mysqlsink(sinks.sinkadapters):

    # Load config
    # TODO: It would be nice if this could be passed into the sink constructor somehow...
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    name = "mysqlsink"
    host = config['sinks']['mysqlsink']['host']
    database = config['sinks']['mysqlsink']['database']
    dbuser = config['sinks']['mysqlsink']['user']
    dbpass = config['sinks']['mysqlsink']['password']

    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using database: {self.host}.{self.database}")

    def write(self, timestamp, value, sinkparam, subscription):
        if subscription["sinkparam"] != None and subscription["sinkparam"] != "":
            dbconn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.dbuser,
                password=self.dbpass
            )

            ts = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

            dbcursor = dbconn.cursor()
            sqlcmd = sinkparam
            sqlval = (ts, value, subscription["label"])
            dbcursor.execute(sqlcmd, sqlval)
            dbconn.commit()
            print(f"Inserted into {self.database}: {value}")
        else:
            print(f"{self.name} invoked without parameters. Nothing to do!")