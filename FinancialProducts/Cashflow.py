import math

class Cashflow(object):
    """ Cashflow Object. """

    def __init__(self, notional, direction, currency, value_date):
        self.notional = notional
        self.direction = direction
        self.currency = currency
        self.value_date = value_date

    def value_product(self, market_environment):
        risk_free_curve_str = 'RiskFree-Gov-' + self.currency
        risk_free_curve = market_environment.get_curve(risk_free_curve_str)

        # TODO Build Curve to Interpolate Over
        #risk_free_rate = risk_free_curve.get_rate(self.value_date)
        risk_free_rate = 0

        return math.exp(-1 * risk_free_rate) * self.Notional