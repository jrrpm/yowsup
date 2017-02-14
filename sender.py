#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.demos.sendclient import YowsupSendStack
from yowsup.env import YowsupEnv
#import os, subprocess, yowsup, logging
#from wasend import YowsupSendStack

#import logging
logging.basicConfig(level=logging.DEBUG)

def credential():
    return "59178503175","ytp8UDps0CRhUD1yOoIDu1avGKA="


def send(phone, msg):
        try:
            #self.printInfoText()
            stack=YowsupSendStack(credential(), [(phone, msg)])
            stack.start()
        except KeyboardInterrupt:
            print("\nYowsdown")
            #sys.exit(0)


send("59176048595","Hola, rodrigo, como estas? XD")
