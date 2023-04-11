import random
import time
import uuid

class Order():

    ##################################################################################################
    def __init__(self, symbol, exchange, market, side, amount, fund, price=0, type="MARKET", orderId=None):
        self._symbol = symbol
        self._exchange = exchange
        self._market = market
        self._side = side
        self._amount = amount
        self._unfilled = amount
        self._price = price
        self._type = type
        self._fund = fund
        self._status = "NEW"
        self._orderId = orderId if orderId else "{}".format(uuid.uuid4())
        self._ts = time.time()

    ##################################################################################################
    #
    # Properties
    #
    @property
    def Status(self):
        return self._status

    @Status.setter
    def Status(self, status):
        assert status and len(status) > 0
        self._status = status
        print("New status for order {} is {}".format(self._orderId, self.Status))

    @property
    def Symbol(self):
        return self._symbol

    @property
    def Exchange(self):
        return self._exchange

    @property
    def Market(self):
        return self._market

    @property
    def Side(self):
        return self._side

    @property
    def OrderId(self):
        return self._orderId

    @property
    def Fund(self):
        return self._fund

    @property
    def Amount(self):
        return self._amount

    @property
    def Price(self):
        return self._price

    @property
    def Type(self):
        return self._type

    @property
    def OrderId(self):
        return self._orderId

    ##################################################################################################
    #
    # Methods
    #
    def getFilled(self):
        return self._amount - self._unfilled

    def getUnfilled(self):
        return self._unfilled

    def getType(self):
        return self._type
