#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.wabot import YowsupBotStack
from pymongo import MongoClient
from logging.handlers import TimedRotatingFileHandler


#this customer's config
global config
config = lambda: None
config.name = "bot1"
config.logLevel = logging.INFO
config.logFile = "/var/log/bot1.log"
config.responseDelay = 1
config.maxAttempts = 3 #same msg ignore
config.maxMsgsPerDay = 3 #-1 for infinite
config.dbString = "mongodb://localhost:27017"
config.dbName = "wabots"
config.collectionName = "puntosPago"
#############################################

def load():
    logger = logging.getLogger('')
    logger.setLevel(config.logLevel)
    handler = TimedRotatingFileHandler(config.logFile,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    logger.addHandler(handler)
    client = MongoClient(config.dbString) 
    db = getattr(client, config.dbName)
    config.oPuntosPago = getattr(db, collectionName).find_one()

def credential():
    return config.oPuntosPago[u'phone'],config.oPuntosPago[u'password']

load()

stack = YowsupBotStack(credential(), config)
stack.start()
