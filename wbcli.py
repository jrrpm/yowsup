#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.wabot import YowsupBotStack
from pymongo import MongoClient

#todo log level at config file
logging.basicConfig(level=logging.INFO)

global oPuntopagos

client = MongoClient("mongodb://localhost:27017") #todo db auth+config file
db = client.wabots
oPuntopagos = db.puntosPago.find_one()

#todo db credential
def credential():
    return oPuntopagos[u'phone'],oPuntopagos[u'password']

stack = YowsupBotStack(credential())
stack.start()
