import Tenor

class Rate(object):
    """Rate class for Financial Data."""

    def __init__(self, tenor, strike, volatility):
        self.tenor = tenor
        self.strike = strike
        self.volatility = volatility

    def __init__(self, tenor_string, strike, volatility):
        self.tenor = Tenor(tenor_string)
        self.strike = strike
        self.volatility = volatility

    # TODO: Add Vol validation [0, 1]
