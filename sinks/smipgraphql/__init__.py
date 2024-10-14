import sinks
from common import utils
import json
import requests
from sinks.smipgraphql.smip import graphql

class smipgraphql(sinks.sinkadapters):

    name = "smipgraphql"
    config = utils.load_config()

    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using URL: {self.config['sinks']['smipgraphql']['url']}")

    def write(self, timestamp, value, sinkparam, subscription):
        if subscription['sinkparam'] != None and subscription['sinkparam'] != "":
            print(f"Mutating into {self.config['sinks']['smipgraphql']['url']}: {value}")
            self.update_smip(self, timestamp, sinkparam, value)
        else:
            print(f"{self.name} invoked without parameters. Nothing to do!")

    #TODO: SMIP is type-safe, MQTT is not, what do we do...
    def update_smip(self, currtime, currid, currvalue):
        config = self.config['sinks']['smipgraphql']
        smipconn = graphql(config['authenticator'], config['password'], config['username'], config['role'], config['url'], config['verbose'])
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
        
        if config['verbose'] == True:
            print("Response from SM Platform was...")
            print(json.dumps(smp_response, indent=2))
        else:
            print("SMIP Update Complete")