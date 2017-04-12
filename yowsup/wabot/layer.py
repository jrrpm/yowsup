from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities    import *
from yowsup.layers.protocol_iq.protocolentities          import *
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from copy import deepcopy
from haversine import haversine
import sys
import os
import logging
import time

class BotLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        mediaType = messageProtocolEntity.getMediaType()
        msg = 'Mensaje recibido de: {}, tipo: {}.'.format(messageProtocolEntity.getFrom(), mediaType)
        logging.info(msg)
        time.sleep(config.responseDelay)
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))
        if mediaType == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif mediaType == 'media':
            self.onMediaMessage(messageProtocolEntity)      

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())


    def onTextMessage(self,messageProtocolEntity):
        to = messageProtocolEntity.getFrom()
        body = messageProtocolEntity.getBody()
        msg = 'Texto recibido de {}: {}.'.format(to, body)
        logging.info(msg)        
        #self.to = to #todo: see if this affects 
        recMsg = body.lower() 
        if recMsg == "pruebadir":
            msg = 'Resultados de la busqueda:'
            msg += '\nNombre: PRUEBA DIRECTION'
            msg += '\nDireccion: XXXXX'
            msg += '\nTelefono: 789456'
            msg += '\nPoblacion: SCZ'
            respMsg = TextMessageProtocolEntity(msg, to = to)
            respMsg._from = None
            respMsg._id = respMsg._generateId()
            self.toLower(respMsg)
            self.requestImageUpload('/home/pi/co.jpeg')
        elif recMsg == "promo":     
            msg = 'Promociones del dia:'
            respMsg = TextMessageProtocolEntity(msg, to = to)
            respMsg._from = None
            respMsg._id = respMsg._generateId()
            self.toLower(respMsg)
            self.requestImageUpload('/home/pi/m1.jpg')            
            self.requestImageUpload('/home/pi/m2.jpg')            
            self.requestImageUpload('/home/pi/m3.jpg')       
        elif recMsg == "comedor":
            msg = '_Juegos de Comedor:_'
            msg += '\nJuego de comedor California *Bs.9.990,00*'
            msg += '\nJuego de comedor Toronto *Bs.9.990,00*'
            respMsg = TextMessageProtocolEntity(msg, to = to)
            respMsg._from = None
            respMsg._id = respMsg._generateId()
            self.toLower(respMsg)          
            self.requestImageUpload('/home/pi/m1.jpg')      
        #else:
        #    msg = 'Hola {}, bienvenido a sou, Tu mensaje es: "{}"'.format(to, recMsg)
        #    respMsg = deepcopy(messageProtocolEntity)
        #    respMsg.to = to
        #    respMsg._from = None
        #    respMsg._id = respMsg._generateId()
        #    respMsg.body = msg
        #    self.toLower(respMsg)      


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
        for punto in self.config.oPuntosPago[u'puntos']:
            loc = (float(punto[u'latitud']), float(punto[u'longitud']))
            distance = round(haversine(point, loc), 1)
            oPunto = { "nombre": punto[u'nombre'], "distancia": distance,  "latitud": punto[u'latitud'], "longitud": punto[u'longitud'] }
            sortedPoints.append(oPunto)
        sortedPoints.sort(key=lambda x: x["distancia"])
        return sortedPoints


    def requestImageUpload(self, imagePath):
        self.demoContactJid = "59178503175@s.whatsapp.net" #only for the sake of simplicity of example, shoudn't do this
        requestUploadEntity = RequestUploadIqProtocolEntity("image", filePath = imagePath)
        self.hPath[requestUploadEntity.getId()] = imagePath
        self._sendIq(requestUploadEntity, self.onRequestUploadResult, self.onRequestUploadError)

    def onRequestUploadResult(self, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        fkey = requestUploadIqProtocolEntity.getId()
        fPath = self.hPath[fkey]
        del self.hPath[fkey]
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(fPath, 
                resultRequestUploadIqProtocolEntity.getUrl(), None, self.to)
            self.toLower(entity)
        else:
            mediaUploader = MediaUploader(self.demoContactJid, self.getOwnJid(), fPath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, self.onUploadProgress)
            mediaUploader.start()

    def onRequestUploadError(self, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        print("Error requesting upload url")

    def onUploadProgress(self, filePath, jid, url, progress):
        print('Path: {}, url: {}, progress: {}.'.format(filePath, url, progress))
        #sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        #sys.stdout.flush()    

    def onUploadSuccess(self, filePath, jid, url):
        #convenience method to detect file/image attributes for sending, requires existence of 'pillow' library
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, self.to)
        self.toLower(entity)

    def onUploadError(self, filePath, jid, url):
        print("Upload file failed!")