from datetime import date
from dateutil.relativedelta import relativedelta
import random
import time
import uuid
import moolahcommon.util as util

class MSignal():

    ##################################################################################################
    def __init__(self, symbol, exchange, market, side, value, price, portfolio, strategy, comment=None, description=None, signalId=None, ts=None, id = None, expiry = None):
        self._id = id
        self._symbol = symbol
        self._exchange = exchange
        self._market = market
        self._side = side if side in ["BUY","SELL"] else None
        self._value = float(value)
        self._price = float(price)
        self._filled = 0
        self._status = "NEW"
        self._portfolio = portfolio
        self._strategy = strategy
        self._comment = comment
        self._signalId = signalId if signalId else "{}".format(uuid.uuid4())
        self._description = description if description else "[ Signal/{} ] {} {} {} coin @ {} exchange {} market for portfolio '{}'".format(self._signalId,side,value,symbol,exchange,market,portfolio)
        self._expiry = expiry if expiry else date.today() + relativedelta(months=3)
        self._ts = ts if ts else int(time.time())

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
        allStatus = ["NEW", "OPEN", "CLOSED", "COMPLETE", "FAIL"]
        valid = status in allStatus
        assert valid, "new Status value is not valid - supplied value was '{}' which is not in '{}'".format(status, allStatus)
        self._status = status
        print("New status for order '{}' is '{}'".format(self._signalId, self.Status))

    @property
    def Comment(self):
        return self._comment

    @property
    def Strategy(self):
        return self._strategy

    @property
    def Timestamp(self):
        return self._ts

    @Comment.setter
    def Comment(self, comment):
        assert comment and len(comment) > 0
        self._comment = comment
        print("New Comment for signal '{}' is '{}'".format(self._signalId, self.Comment))

    @property
    def Filled(self):
        return self._filled

    @Filled.setter
    def Filled(self, fill):
        assert fill and fill > 0
        assert fill + self._filled <= self._value, "Cannot fill more than value {} this Signal. Attempted to fill {}".format(self._value, fill)
        self._filled = self._filled + fill
        print("New Fill for signal '{}' is '{}' after fill update of '{}'".format(self._signalId, self._filled,fill))

    @property
    def Description(self):
        return self._description

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
    def Portfolio(self):
        return self._portfolio

    @property
    def SignalId(self):
        return self._signalId

    @property
    def Price(self):
        return self._price

    @property
    def Value(self):
        return self._value

    @property
    def Expiry(self):
        return self._expiry

    def __repr__(self):
        return "Signal({!r})".format(self.__dict__)

    ##################################################################################################
    #
    # Methods
    #
    def getFilled(self):
        return self._filled

    def getUnfilled(self):
        return self._value - self._filled

    def store(self):
        status, msg = util.addSignal(self)
        print("Saved Signal '{}' to Moolah DB OK ".format(self._signalId))
