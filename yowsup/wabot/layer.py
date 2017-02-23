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
            ori = (float(messageProtocolEntity.getLatitude()), float(messageProtocolEntity.getLongitude()))
            to = messageProtocolEntity.getFrom()
            nearPoints = self.getDistances(ori)
            msg = 'Punto de pago mas cercano: {}, se encuentra a {} Km de distancia.'.format(nearPoints[0]['nombre'], nearPoints[0]['distancia'])
            respMsg = TextMessageProtocolEntity(msg, to = to)
            respMsg._from = None
            respMsg._id = respMsg._generateId()
            self.toLower(respMsg)
            respMsg = deepcopy(messageProtocolEntity)
            respMsg.to = to
            respMsg._from = None
            respMsg.latitude = nearPoints[0]['latitud']
            respMsg.longitude = nearPoints[0]['longitud']
            respMsg.name = nearPoints[0]['nombre']
            respMsg._id = respMsg._generateId()
            self.toLower(respMsg)
            length = len(nearPoints)
            if nearPoints>1:
                msg = 'Otros puntos cercanos: \n  {} a {} Km'.format(nearPoints[1]['nombre'], nearPoints[1]['distancia'])
                if nearPoints>2:
                    msg += '\n  {} a {} Km'.format(nearPoints[2]['nombre'], nearPoints[2]['distancia'])
                respMsg = TextMessageProtocolEntity(msg, to = to)
                respMsg._from = None
                respMsg._id = respMsg._generateId()
                self.toLower(respMsg)
        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

    
    def getDistances(self, point):
        sortedPoints = []
        #todo: filter horarios first
        for punto in self.oPuntosPago[u'puntos']:
            loc = (float(punto[u'latitud']), float(punto[u'longitud']))
            distance = round(haversine(point, loc), 1)
            oPunto = { "nombre": punto[u'nombre'], "distancia": distance,  "latitud": punto[u'latitud'], "longitud": punto[u'longitud'] }
            sortedPoints.append(oPunto)
        sortedPoints.sort(key=lambda x: x["distancia"])
        return sortedPoints
