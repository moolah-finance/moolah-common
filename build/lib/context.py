from common.config import Config

class Context():

    Config = None

    def __init__(self, name, status):
        self._Actions = ["Buy", "Sell", "Cancel"]
        self._Name = name
        self._Status = status
        self.Config = Config()
        # print(f"Context object has config object : {Config}")
        # print(f"Context has config value for 'Name' : {Config.Name}")
        # print(f"Context has config value for 'Version' : {Config.Version}")
        # print("Context has config holding {} ".format(Config.Exchanges))

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, status):
        print("Current status for Context is {}".format(self.Status))
        self._Status = status
        print("New status for Context is {}".format(self.Status))

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, name):
        assert name and len(name) > 0
        self._Name = name

    def Execute(self, exchange, action, amount, coin):
        if not self.__checkExchange(exchange):
            return
        if not self.__checkAction(action):
            return
        self.__execute(exchange, action, amount, coin)

    def __checkExchange(self, exchange):
       if exchange in self.Config.Exchanges:
           return True
       else:
           print("Invalid exchange - '{}' not in exchange list {}".format(exchange, list(self.Config.Exchanges.keys())))
           return False

    def __checkAction(self, action):
       if action not in self._Actions:
           print("Invalid trade action - '{}' not in allowed actions list {}".format(action, self.Actions))
           return False
       else:
           return True

    def __execute(self, exchange, action, amount, coin):
       if exchange in self.Config.Exchanges.keys():
           self.Config.Exchanges[exchange].execute(action, amount, coin)
       else:
           raise Exception("Invalid exchange -> {}".format(exchange))
