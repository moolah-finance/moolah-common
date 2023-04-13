class Position():
    def __init__(self, symbol, quantity, price):
        self._symbol = symbol
        self._price = price
        self._quantity = quantity
        self._latest = -1
        self._concentration = 0

    def __repr__(self):
        return "Position()"

    def __str__(self):
        return "Position {} for coin '{}' based on {} coins at price {} [conc. {}]".format(self._price * self._quantity, self._symbol, self._quantity, self._price, self._concentration)

    @property
    def Symbol(self):
        return self._symbol

    @property
    def Price(self):
        return self._price

    @property
    def Quantity(self):
        return self._quantity

    @property
    def Latest(self):
        return self._latest

    @property
    def Concentration(self):
        return self._concentration

    @Latest.setter
    def Latest(self, latest):
        assert latest and latest > 0
        self._latest = latest
        print("latest price for Coin is {}".format(self.Latest))

    @Concentration.setter
    def Concentration(self, concentration):
        assert concentration,"Concentration must be a valid value"
        self._concentration = concentration
