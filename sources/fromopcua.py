import yaml
from common import utils
from asyncua import ua, Client

class opcuasource():

    def __init__(self):
        pass
    
    config = utils.load_config()

    # Remember all subscriptions
    opcua_subscriptions = config['source']['opcua']['subscriptions']

    class SubscriptionHandler:
        def datachange_notification(self, node: Node, val, data):
            _logger.info('datachange_notification %r %s', node, val)

    def connect(self, sinkadapters):
        print(f"Connecting asyncua to {config['source']['opcua']['endpoint']}")
        client = Client(url=config['source']['opcua']['endpoint'])
        async with client:
            while True:
                idx = await client.get_namespace_index(uri="http://examples.freeopcua.github.io")
                var = await client.nodes.objects.get_child(f"{idx}:MyObject/{idx}:MyVariable")
                handler = SubscriptionHandler()
                # We create a Client Subscription.
                subscription = await client.create_subscription(500, handler)
                nodes = [
                    client.get_node(ua.ObjectIds.Server_ServerStatus_CurrentTime),
                ]
                # We subscribe to data changes for two nodes (variables).
                await subscription.subscribe_data_change(nodes)