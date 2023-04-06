import random

class Fund():

    def __init__(self, status):
        self._status = "Test"
        self._name = "Default"
        self._items = []

    @property
    def Status(self):
        return self._status

    @Status.setter
    def Status(self, status):
        assert status and len(status) > 0
        self._status = status
        print("New status for Context is {}".format(self.Status))

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, name):
        assert name and len(name) > 0
        self._name = name

    def getPosition(self):
        return self._items

    def getPosition(self):
        return random.randint()
