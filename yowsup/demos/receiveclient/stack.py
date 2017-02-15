from yowsup.stacks import  YowStackBuilder
from .layer import SendLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.network import YowNetworkLayer


class YowsupReceiveStack(object):
    def __init__(self, credentials, messages, encryptionEnabled = True):
        """
        :param credentials:
        :param messages: list of (jid, message) tuples
        :param encryptionEnabled:
        :return:
        """
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(ReceiveLayer)\
            .build()

        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)
        self.stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
        self.stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        self.stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())      


    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop(count=4)
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
            


 
