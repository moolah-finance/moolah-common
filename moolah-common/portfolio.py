class Portfolio():
    def __init__(self, name, description, positions=[], cash=555, status="NEW", id=None):
        self._id = id
        self._cash = cash
        self._name = name
        self._description = description
        self._status = status
        self._positions = positions

    def __repr__(self):
        return "Portfolio()"

    def __str__(self):
        return "Portfolio '{}' which is '{}' has {} cash and '{}' status".format(self._name, self._description, self._cash, self._status)

    @property
    def Description(self):
        return self._description

    @property
    def Name(self):
        return self._name

    @property
    def Cash(self):
        return self._cash

    @property
    def Id(self):
        return self._id if id else -1

    @property
    def Positions(self):
        return self._positions

    @property
    def Status(self):
        return self._status
