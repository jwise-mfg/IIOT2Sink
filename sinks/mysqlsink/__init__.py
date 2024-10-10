import sinks
import mysql
import mysql.connector
from datetime import datetime
import calendar
from sinks.mysqlsink import config

class mysqlsink(sinks.sinkadapters):

    name = "mysqlsink"
    host = config.database["host"]
    database = config.database["database"]
    dbuser = config.database["user"]
    dbpass = config.database["password"]

    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using database: {self.host}.{self.database}")

    def write(self, timestamp, value, subscription):
        if subscription["command"] != None and subscription["command"] != "":
            dbconn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.dbuser,
                password=self.dbpass
            )

            ts = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

            dbcursor = dbconn.cursor()
            sqlcmd = subscription["command"]
            sqlval = (ts, value, subscription["label"])
            dbcursor.execute(sqlcmd, sqlval)
            dbconn.commit()
            print(f"Inserted into {self.database}: {value}")