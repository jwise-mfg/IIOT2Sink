import sinks
import json
import requests
from sinks.smipgraphql import config
from smip import graphql

class smipgraphql(sinks.sinkadapters):

    name = "smipgraphql"
    url = config.smip["url"]

    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using URL: {self.url}")

    def write(self, timestamp, value, sinkparam, subscription):
        if subscription["sinkparam"] != None and subscription["sinkparam"] != "":
            print(f"Sending to {self.url}: {value}")
            self.update_smip(self, timestamp, sinkparam, value)
        else:
            print(f"{self.name} invoked without parameters. Nothing to do!")

    #TODO: SMIP is type-safe, MQTT is not, what do we do...
    def update_smip(self, currtime, currid, currvalue):
        print(f"self.name is {self.name}")
        smipconn = graphql(config.smip["authenticator"], config.smip["password"], config.smip["username"], config.smip["role"], config.smip["url"])
        smp_query = f"""
                    mutation updateTimeSeries {{
                    replaceTimeSeriesRange(
                        input: {{attributeOrTagId: "{currid}", entries: [ {{timestamp: "{currtime}", value: "{currvalue}", status: "0"}} ] }}
                        ) {{
                        clientMutationId,
                        json
                    }}
                    }}
                """
        smp_response = ""
        try:
            smp_response = graphql.post(graphql, smp_query)
        except requests.exceptions.HTTPError as e:
            print("An error occured accessing the SM Platform!")
            print(e)
            
        print("Response from SM Platform was...")
        print(json.dumps(smp_response, indent=2))