from dotenv import load_dotenv
from moolahcommon.exchange import Exchange
from collections import OrderedDict
import asyncio
import os
import sys
import time
from bfxapi import Client
from bfxapi.models.order import OrderType

load_dotenv()

class Bitfinex(Exchange):

    ####################################################################################################################
    #
    # Class creation(Init)
    #
    def __init__(self):
        self._name = "Bitfinex"
        self._log = OrderedDict()
        self._bfx = Client( API_KEY=os.getenv('BFX_API_KEY'), API_SECRET=os.getenv('BFX_API_SECRET'))

    ####################################################################################################################
    #
    # Properties
    #
    @property
    def Name(self):
        return self._name

    @property
    def Wallets(self):
        wallets = asyncio.ensure_future(self.runWallets())
        asyncio.get_event_loop().run_until_complete(wallets)
        result = {}
        result["funding"]  = dict()
        result["exchange"] = dict()
        for wallet in wallets.result():
            # print(wallet.key, " has balance ",wallet.balance)
            if "funding" in wallet.key and wallet.balance > 0:
                result["funding"][str.replace(wallet.key,"funding_","")] = wallet
            elif "exchange" in wallet.key and wallet.balance > 0:
                result["exchange"][str.replace(wallet.key,"exchange_","")] = wallet
            else:
                print("ANOTHER WALLY FOUND - ",wallet.key)
        return result


    ####################################################################################################################
    #
    # Balances
    #
    def getBalance(self, coin, type):
        wallets = asyncio.ensure_future(self.runWallets())
        asyncio.get_event_loop().run_until_complete(wallets)
        balance = 0.0
        for wallet in wallets.result():
            if coin in wallet.key and type in wallet.key:
                balance += wallet.balance

        return {"coin": coin, "balance": float("{:16.8f}".format(balance).strip()), "type": type}

    ####################################################################################################################
    #
    # Order management
    #

    #
    # Add a single Order
    #
    def addOrder(self, coin, amount, price):
        assert amount is not None and amount != 0
        assert price is not None and price > 0
        assert coin is not None and len(coin) > 0

        order = asyncio.ensure_future(self.runAddOrder(coin, amount, price))
        asyncio.get_event_loop().run_until_complete(order)
        return order.result

    #
    # Retrieve a single Order
    #
    def getOrder(self, coin, orderId):
        assert orderId is not None and orderId > 0
        orders = []
        order = None
        ord = None
        orders = asyncio.ensure_future(self.runGetOrders(coin))
        asyncio.get_event_loop().run_until_complete(orders)
        for order in orders.result():
            # print("checking order {} against order Id {}".format(order.id, orderId))
            if order.id == orderId:
                print("found order {} using input {}".format(order.id, orderId))
                return order
        return ord

    #
    # Retrieve All Orders for a Coin
    #
    def getOrders(self, coin):
        assert coin is not None and len(coin) > 0
        orders = asyncio.ensure_future(self.runGetOrders(coin))
        asyncio.get_event_loop().run_until_complete(orders)
        return orders.result()
        # return [{"orderId": "X123434534", "status": "Active"},{"orderId": "axcver3452345", "status": "Cancelled"}]

    #
    # Cancel a singl Order using Order Id
    #
    def cancelOrder(self, orderId):
        assert orderId is not None and orderId > 0
        order = asyncio.ensure_future(self.runCancelOrder(orderId))
        asyncio.get_event_loop().run_until_complete(order)
        return order.result()
        # return {"action": "cancel order", "item": orderId, "status": "Success"}

    #
    # Cancel All Orders using Order Id
    #
    def cancelOrders(self):
        return {"action": "cancel all orders", "item": "All", "status": "Success"}


    ####################################################################################################################
    #
    # Execution methods
    #
    async def runWallets(self):
        return await self._bfx.rest.get_wallets()

    async def runAddOrder(self, coin, amount, price):
        print("Sending order for coin {} of {} @ {}".format(coin, amount, price))
        try:
            return await self._bfx.rest.submit_order(symbol=coin, price=price, amount=amount, market_type=OrderType. EXCHANGE_LIMIT)
        except Exception as exc:
            print(exc)

    async def runGetOrder(self, orderId):
        return await self._bfx.rest.get_order(orderId)

    async def runCancelOrder(self, orderId):
        return await self._bfx.rest.submit_cancel_order(orderId)

    async def runGetOrders(self, coin):
        return await self._bfx.rest.get_active_orders(coin)

    def execute(self, action, amount, coin):
        print("\nExecuting '{} of {} {} for exchange '{}'".format(action, amount, coin, self._name))
        self._log[time.time()] = action+" "+str(amount)+" pf "+coin


    ####################################################################################################################
    #
    # Session info & logs for this account
    #
    def dump(self):
        for item in self._log:
            print("["+self._name+"] "+"Trade ["+str(item)+"] to "+self._log[item])
