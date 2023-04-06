from common.exch_binance import Binance
from common.exch_bitfinex import Bitfinex

class Config():

    def __init__(self, exchanges=[]):
        self._company = "Moolah"
        self._exchanges = dict()
        self._exchanges["Binance"]  = Binance()
        self._exchanges["Bitfinex"] = Bitfinex()
        self._name = "Config.test"
        self._status="Active"
        self._system = "MATE"
        self._version = "0.01"

    @property
    def Company(self):
        return self._company

    @property
    def Exchanges(self):
        return self._exchanges

    @property
    def Name(self):
        return self._name

    @property
    def System(self):
        return self._system

    @property
    def Version(self):
        return self._version

