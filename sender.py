import sys, argparse, yowsup, logging
from yowsup.demos.sendclient import YowsupSendStack
from yowsup.env import YowsupEnv
#import os, subprocess, yowsup, logging
#from wasend import YowsupSendStack

#import logging
logging.basicConfig(level=logging.DEBUG)

def credential():
    return "59176329787","zTh+17TK6rGpK//zrj1FKQMFDjw="

def Answer(risp):
    try:
        stack=YowsupSendStack(credential(), ["59176048595", risp], True)
        stack.start()
    except:
        pass
    return

def startSendClient():
        try:
            #self.printInfoText()
            stack=YowsupSendStack(("59176329787","zTh+17TK6rGpK//zrj1FKQMFDjw="), [("59176048595", "hola mundoo")])
            stack.start()
        except KeyboardInterrupt:
            print("\nYowsdown")
            #sys.exit(0)


startSendClient()
#Answer("Updating...")
