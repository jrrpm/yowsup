#!/usr/bin/env python

import sys, argparse, yowsup, logging
from yowsup.wabot import YowsupBotStack

#todo log level at config file
logging.basicConfig(level=logging.INFO)

#todo db credential
def credential():
    return "59178503175","t3F+47AOq88gef34KvqHCSVpdQY="

stack = YowsupBotStack(credential())
stack.start()
