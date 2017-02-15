#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.wabot import YowsupBotStack

#todo log level at config file
logging.basicConfig(level=logging.INFO)

#todo db credential
def credential():
    return "",""

stack = YowsupBotStack(credential())
stack.start()
