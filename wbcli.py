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
config.maxAttempts = 3 #same msg ignore, -1 for infinite #todo yet
config.maxMsgsPerDay = 3 #-1 for infinite #todo yet
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
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)                                       
    logger.addHandler(handler)
    client = MongoClient(config.dbString) 
    db = getattr(client, config.dbName)
    config.oPuntosPago = getattr(db, config.collectionName).find_one()

def credential():
    return config.oPuntosPago[u'phone'],config.oPuntosPago[u'password']

load()

stack = YowsupBotStack(credential(), config)
stack.start()
