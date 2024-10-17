import sinks
from common import utils
import json
import requests
from sinks.smipgraphql.smip import graphql

class smipgraphql(sinks.sinkadapters):

    name = "smipgraphql"
    batch_mutations = ""
    batch_items = 0
    config = utils.load_config()

    def __init__(self):
        pass

    def start(self):
        print(f"Starting {self.name} using URL: {self.config['sinks']['smipgraphql']['url']}")

    def write(self, timestamp, value, sinkparam, subscription):
        if subscription['sinkparam'] != None and subscription['sinkparam'] != "":
            self.update_smip(self, timestamp, sinkparam, value)
        else:
            print(f"{self.name} invoked without parameters. Nothing to do!")

    #TODO: SMIP is type-safe, MQTT is not, what do we do...
    def update_smip(self, timestamp, currid, currvalue):
        config = self.config['sinks']['smipgraphql']
        smipconn = graphql(config['authenticator'], config['password'], config['username'], config['role'], config['url'], config['verbose'])
        self.batch_items += 1
        self.batch_mutations += graphql.build_alias_ts_mutation(graphql, timestamp, self.batch_items, currid, currvalue)
        if (self.batch_items >= config['batchuntil']):
            print(f"Posting batch of {config['batchuntil']} mutations to {config['url']}")
            smp_response = graphql.multi_tsmutate_aliases(graphql, self.batch_mutations)
            self.batch_items = 0
            self.batch_mutations = ""
        else:
            print(f"Mutation batched ({self.batch_items} of {config['batchuntil']})")
        
        if config['verbose'] == True:
            print("Response from SM Platform was...")
            print(json.dumps(smp_response, indent=2))
        else:
            print("SMIP Update Complete")