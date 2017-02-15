#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.demos.sendclient import YowsupSendStack
from yowsup.env import YowsupEnv


logging.basicConfig(level=logging.DEBUG)

def credential():
    return "",""


def send(phone, msg):
        try:
            #self.printInfoText()
            stack=YowsupSendStack(credential(), [(phone, msg)])
            stack.start()
        except KeyboardInterrupt:
            print("\nYowsdown")
            #sys.exit(0)


send("","Hola, !!, como estas? XD")
