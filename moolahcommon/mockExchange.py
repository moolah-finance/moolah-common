from bfxapi import Client
from bfxapi.models.order import OrderType
from dotenv import load_dotenv
from common.exchange import Exchange
from collections import OrderedDict
import asyncio
import os
import sys
import time

load_dotenv()

class mockExchange(Exchange):

    ####################################################################################################################
    #
    # Class creation(Init)
    #
    def __init__(self):
        self._name = "Mock"
        self._status = "New"
        self._log = OrderedDict()

    ####################################################################################################################
    #
    # Properties
    #
    @property
    def Name(self):
        return self._name

    @property
    def Status(self):
        return self._status

    ####################################################################################################################
    #
    # Execute a Trade (buy/sell)
    #
    def execute(self, action, amount, price, coin):
        print("Do nothing as this is a mock class for testing purposes")
        return True

    ####################################################################################################################
    #
    # Print out all session info & logs for the account
    #
    def dump(self):
        return []
        # for item in self._log:
        #    print("["+self._name+"] "+"Trade ["+str(item)+"] to "+self._log[item])
