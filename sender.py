import sys, argparse, yowsup, logging
from yowsup.demos.sendclient import YowsupSendStack
from yowsup.env import YowsupEnv
#import os, subprocess, yowsup, logging
#from wasend import YowsupSendStack

#import logging
logging.basicConfig(level=logging.DEBUG)

def credential():
    return "",""


def startSendClient():
        try:
            #self.printInfoText()
            stack=YowsupSendStack(("",""), [("", "hola mundoo")])
            stack.start()
        except KeyboardInterrupt:
            print("\nYowsdown")
            #sys.exit(0)


startSendClient()
#Answer("Updating...")
