#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.wabot import YowsupBotStack
from pymongo import MongoClient

#todo log level at config file
logging.basicConfig(level=logging.INFO)



def loadData():
    client = MongoClient("mongodb://localhost:27017") #todo db auth+config file
    db = client.wabots
    global oPuntosPago
    oPuntosPago = db.puntosPago.find_one()


#todo db credential
def credential():
    return oPuntosPago[u'phone'],oPuntosPago[u'password']


loadData()

for punto in oPuntosPago[u'puntos']:
    print punto[u'nombre']
    print "\n"


stack = YowsupBotStack(credential(), oPuntosPago)
stack.start()
