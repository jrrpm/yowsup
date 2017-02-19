#!/usr/bin/env python

from circus import get_arbiter

myprogram = {"cmd": "sudo ./wbcli.py", "numprocesses": 1}

arbiter = get_arbiter([myprogram])
try:
    arbiter.start()
finally:
    arbiter.stop()
