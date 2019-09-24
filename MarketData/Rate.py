import Tenor

class Rate(object):
    """Rate class for Financial Data."""

    def __init__(self, tenor, rate):
        self.tenor = tenor
        self.rate = rate

    def __init__(self, tenor_string, rate):
        self.tenor = Tenor(tenor_string)
        self.rate = rate

    # TODO: Add rate validation