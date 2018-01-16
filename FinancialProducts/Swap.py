#
# Swap Object
#

from Derivative import Derivative


class Swap(Derivative):
    '''
    Swap(Derivative)

    Class for a building a generic swap.

    Attributes
    ==========
    ID : str
        unique identifier for the product
    currency : str
        currency denomination of the product
    country : str
        country of the product
    start_date : datetime
        date specifying when the contract started
    expiration_date : datetime
        date specifying when the contract expires
    underlying : object
         the object representing the underlying asset
    notional : double
        the dollar amount of the contract notional on the swap
    counterparty : str
        a string specifiying the counterparty of the contract
    pmt_freq : int
        the payment frequency of the swap defined as number of payments per
        year

    Methods
    =======
    get_notional :
        returns the notional of the swap
    set_notional :
        sets the notional of the swap
    get_counterparty :
        returns the counterparty of the swap
    set_counterparty :
        sets the counterparty of the swap
    get_pmt_freq :
        returns the payment frequency of the swap
    set_pmt_freq :
        sets the payment frequency of the swap
    get_exposure :
        returns the exposure of the product
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, expiration_date, underlying,
                 notional, counterparty, pmt_freq, country=None):
        super(Swap, self).__init__(ID, currency, start_date, expiration_date,
                                   underlying, country)
        self.notional = notional
        self.counterparty = counterparty
        self.pmt_freq = pmt_freq

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_notional(self):
        return self.notional

    def set_notional(self, new_notional):
        self.notional = new_notional

    def get_counterparty(self):
        return self.counterparty

    def set_counterparty(self, new_counterparty):
        self.counterparty = new_counterparty

    def get_pmt_freq(self):
        return self.pmt_freq

    def set_pmt_freq(self, new_pmt_freq):
        self.pmt_freq = new_pmt_freq

    # -------------------------------------------------------------------------
    # Method to return the exposure of the swap
    # -------------------------------------------------------------------------
    def get_exposure(self, market_environment):
        exposure = self.notional + self.value_product(market_environment)
        return exposure

    #    # -------------------------------------------------------------------------
    #    # Define methods for returning a set of market risk factors and credit risk
    #    # factors
    #    # -------------------------------------------------------------------------
    #    def get_market_risk_factors(self):
    #        risk_factors = set([])
    #        return risk_factors
    #
    #    def get_credit_risk_factors(self):
    #        risk_factors = set([])
    #        return risk_factors
    #
    #    # -------------------------------------------------------------------------
    #    # Method to value the underlying product
    #    # -------------------------------------------------------------------------
    #    def value_product(self, market_environment):)
    #        # ???????????????????????
    #        # finish this
    #        # ???????????????????????

    # -------------------------------------------------------------------------
    # Print out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 45 * '-'
        print('\n' + bar)
        print('SWAP DESCRIPTION')
        print(bar)
        print('ID:\t\t\t' + self.ID)
        print('Currency:\t\t' + self.currency)
        print('Start Date:\t\t' + (self.start_date).strftime(date_str))
        print('Expiration Date:\t' + (self.expiration_date).strftime(date_str))
        if type(self.underlying) == str:
            print('Underlying:\t\t' + self.underlying)
        else:
            print('Underlying:\t\t' + (self.underlying).get_ID())
        print('Notional:\t\t' + str(self.notional))
        print('Counterparty:\t\t' + self.counterparty)
        print('Payment Frequency:\t' + str(self.pmt_freq) + ' per annum')
        print('Country:\t\t' + self.country)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt

    print('\nTesting Swap.py...')
    ID = 'SwapTesting'
    currency = 'USD'
    country = 'Canada'
    start_date = dt.datetime.today()
    underlying = 'OIS'
    expiration_date = dt.datetime(start_date.year + 1, start_date.month,
                                  start_date.day, 00, 00)
    notional = 100000
    counterparty = 'Goldman Sachs'
    pmt_freq = 4
    swap_test = Swap(ID, currency, start_date, expiration_date, underlying,
                     notional, counterparty, pmt_freq, country)
    swap_test.to_string()
