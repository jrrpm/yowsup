from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities    import *
from copy import deepcopy
from haversine import haversine

class BotLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))
        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)      


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())


    def onTextMessage(self,messageProtocolEntity):
        to = messageProtocolEntity.getFrom()
        msg = 'Hola {}, bienvenido a noticell, Tu mensaje es: "{}"'.format(to, messageProtocolEntity.getBody())
        respMsg = deepcopy(messageProtocolEntity)
        respMsg.to = to
        respMsg._from = None
        respMsg._id = respMsg._generateId()
        respMsg.body = msg
        self.toLower(respMsg)      
        #self.cbSend(messageProtocolEntity.getFrom(False), messageProtocolEntity.getBody())


    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            ofi = (float(-17.780843), float(-63.185648))
            ori = (float(messageProtocolEntity.getLatitude()), float(messageProtocolEntity.getLongitude()))
            to = messageProtocolEntity.getFrom()
            distance = haversine(ori, ofi)
            msg = 'Noticell informa a {}, que se encuentra a "{}" Km de la oficina del morrito pinto'.format(messageProtocolEntity.getFrom(False), distance)
            respMsg = TextMessageProtocolEntity(msg, to = to)
            respMsg._from = None
            respMsg._id = respMsg._generateId()
            #dir(respMsg)
            self.toLower(respMsg)      
            respMsg = deepcopy(messageProtocolEntity)
            respMsg.to = to
            respMsg._from = None
            respMsg.latitude = "-17.780843"
            respMsg.longitude = "-63.185648"
            respMsg._id = respMsg._generateId()
            self.toLower(respMsg)
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
