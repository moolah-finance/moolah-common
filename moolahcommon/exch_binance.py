from dotenv import load_dotenv
from moolahcommon.exchange import Exchange
from collections import OrderedDict
from binance import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException

import os
import time

load_dotenv()

ORDER_TYPE_LIMIT='LIMIT'


class Binance(Exchange):

    ####################################################################################################################
    #
    # Class creation(Init)
    #
    def __init__(self):
        self._name = "Binance"
        self._status = "Active"
        self._version = "0.01"
        self._client = Client(os.getenv('BIN_API_KEY'), os.getenv('BIN_API_SECRET'))
        self._log = OrderedDict()

    ####################################################################################################################
    #
    # Properties
    #
    @property
    def Name(self):
        return self._name

    @property
    def Version(self):
        return self._version

    @property
    def Status(self):
        return self._status

    #######################################################################################################
    #
    # Get list of Coins on Binance
    #
    def Wallets(self, type=Client.SYMBOL_TYPE_SPOT):
        assert type is not None and len(type) > 0
        return self._client.get_account_snapshot(type=type)

    #######################################################################################################
    #
    # Get Coin balance on Binance
    #
    def getCoinBalance(self, coin):
        assert coin is not None and len(coin) > 0
        return self._client.get_asset_balance(asset=coin)

    #######################################################################################################
    #
    # Get Info for listed Coin on Binance
    #
    def getCoinInfo(self, coin):
        assert coin is not None and len(coin) > 0
        try:
            return self._client.get_symbol_info("MATICBNB")
        except BinanceAPIException as exc:
            print("get Info error -> {}".format(exc))

    ########################################################################################
    #
    # Get all symbol prices(default limit is 100 prices)
    #
    @staticmethod
    def getTickers(count=100):
        prices = Client(os.getenv('BIN_API_KEY'), os.getenv('BIN_API_SECRET')).get_all_tickers()
        return prices[:count]

    ########################################################################################
    #
    # Get a deposit address for BTC(default value)
    #
    def getAddress(self, coin="BTC"):
        assert coin is not None and len(coin) > 0
        return(self._client.get_deposit_address(coin=coin))

    ########################################################################################
    #
    # Create single Order
    #
    def addOrder(self, coin, side, type, quantity, price):
        assert coin is not None and len(coin) > 0, "Method 'getOrder' not provided with valid Coin value - must be non-empty string"
        assert quantity is not None and quantity > 0
        assert price is not None and price > 0
        assert side is not None and len(side) > 0 and side in ["buy", "sell"]
        assert type is not None and len(type) > 0 and type in ["LIMIT"]

        response = None
        try:
            TIMEINFORCE_GTC="GTC"
            response = self._client.create_order(symbol=coin, side=side, type=type, quantity=quantity, price=price, timeInForce=TIMEINFORCE_GTC)
            status = response
        except BinanceAPIException as exc:
            print("Create Order API error -> {}".format(exc))
        except Exception as exc:
            print("Create Order error -> {}".format(exc))
        finally:
            return response


    ########################################################################################
    #
    # Retrieve details for a single open order
    #
    def getOrder(self, coin, orderId):
        assert coin is not None and len(coin) > 0, "Method 'getOrder' not provided with valid Coin value - must be non-empty string"
        assert orderId is not None and orderId > 0
        order = None
        try:
            order = self._client.get_order(orderId=orderId,symbol=coin)
            # print("Found order \n", order)
        except BinanceAPIException as exc:
            print("Get Order error -> {}".format(exc))
        except Exception as exc:
            print("Get Order error -> {}".format(exc))
        finally:
            return order


    ########################################################################################
    #
    # Get list of open orders
    #
    def getOrders(self, coin):
        assert coin is not None and len(coin) > 0, "Method 'getOrder' not provided with valid Coin value - must be non-empty string"
        print("Getting open orders for {}".format(coin))
        orders = []
        try:
            orders = self._client.get_open_orders(symbol=coin)
            if len(orders) > 0:
                print(" -> Found {} open orders for {}".format(len(orders),coin))
            else:
                print(" -> No open orders for coin {}".format(coin))
        except BinanceAPIException as exc:
            print("Get Orders API error for coin {} : {}".format(coin, exc))
        except Exception as exc:
            print("Get Orders error for coin {} : {}".format(coin, exc))
        finally:
            return orders


    ########################################################################################
    #
    # Cancel single order
    #
    def cancelOrder(self, coin, orderId):
        assert coin is not None and len(coin) > 0, "Method 'cancelOrder' not provided with valid Coin value - must be non-empty string"
        assert orderId is not None and orderId > 0
        status = False
        try:
            print("Cancel single order {} for coin {}".format(orderId, coin))
            resp = self._client.cancel_order(symbol=coin, orderId=orderId)
            status = resp["Status"] == "Cancelled"
        except BinanceAPIException as exc:
            print("Get Order error -> {}".format(exc))
            status = False
        finally:
            return status

    ########################################################################################
    #
    # Cancel all orders
    #
    def cancelOrders(self, coin):
        assert coin is not None and len(coin) > 0, "Method 'cancelOrder' not provided with valid Coin value - must be non-empty string"
        orders = []
        try:
            print("cancel all orderis for coin {}".format(coin))
            orders = self._client.get_open_orders(symbol=coin)
            if len(orders) > 0:
                for order in orders:
                    print(order)
                    if order["orderId"]:
                        print("Cancelling order {} for coin {}".format(orderId, coin))
                        resp = self._client.cancel_order(symbol=coin, orderId=order["orderId"])
                        print("Order {} has status {}".format(order["orderId"],resp["status"]))
            else:
                print(" -> No open orders for {}".format(coin))
        except BinanceAPIException as exc:
            print("Cancel ALL Order API error -> {}".format(exc))
        except Exception as exc:
            print("Cancell ALL Orders error for coin {} : {}".format(coin, exc))
        finally:
            return {"Status": "Completed", "Count": len(orders)}

    def execute(self, action, amount, coin):
        print("Executing '{} of {} {} for exchange '{}'".format(action, amount, coin, self._name))
        self._log[time.time()] = action+" "+str(amount)+" pf "+coin

    def dump(self):
        for item in self._log:
            print("["+self._name+"]  "+"Trade ["+str(item)+"] to "+self._log[item])

