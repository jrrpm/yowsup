from yowsup.stacks import  YowStackBuilder
from .layer import BotLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer

class YowsupBotStack(object):  

    def __init__(self, credentials, config, encryptionEnabled = True):
        stackBuilder = YowStackBuilder()
        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(BotLayer)\
            .build()
        self.stack.setCredentials(credentials)
        sLayer = stack.getLayer(8)
        sLayer.hPath = {} 
        sLayer.config = config

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
