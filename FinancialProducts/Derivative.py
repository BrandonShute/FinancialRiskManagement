#
# Derivative Object
#

from Product import Product


class Derivative(Product):
    '''
    Derivative(Product)

    Class for a building a derivative

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
    underlying : Obj
        the object representing the underlying of the derivative contract

    Methods
    =======
    get_start_date :
        returns the start date of the derivative contract
    set_start_date :
        sets the start date of the derivative contract
    get_expiration_date :
        returns the expiration date of the derivative contract
    set_expiration_date :
        sets the expiration date of the derivative contract
    get_underlying :
        returns the underlying of the derivative contract
    set_underlying :
        sets the underlying of the derivative contract
    get_asset_class :
        gets the asset class of the derivative
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, expiration_date, underlying,
                 country=None):
        super(Derivative, self).__init__(ID, currency, country)
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.underlying = underlying
        self._asset_class = 'Derivative'

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_start_date(self):
        return self.start_date

    def set_start_date(self, new_start_date):
        self.start_date = new_start_date

    def get_expiration_date(self):
        return self.expiration_date

    def set_expiration_date(self, new_expiration_date):
        self.expiration_date = new_expiration_date

    def get_underlying(self):
        return self.underlying

    def set_underlying(self, new_underlying):
        self.underlying = new_underlying

    def get_asset_class(self):
        return self._asset_class

    #    # -------------------------------------------------------------------------
    #    # Method to return the exposure of the stock
    #    # -------------------------------------------------------------------------
    #    def get_exposure(self, market_environment):
    #
    #    # -------------------------------------------------------------------------
    #    # Define methods for returning a set of market risk factors and credit risk
    #    # factors
    #    # -------------------------------------------------------------------------
    #    def get_market_risk_factors(self):
    #        risk_factors = set(self.ID)
    #        return risk_factors
    #
    #    def get_credit_risk_factors(self):
    #        risk_factors = set(self.ID)
    #        return risk_factors
    #
    #    # -------------------------------------------------------------------------
    #    # Method to value the underlying product
    #    # -------------------------------------------------------------------------
    #    def value_product(self, market_environment):

    # -------------------------------------------------------------------------
    # print(out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 45 * '-'
        print('\n' + bar)
        print('DERIVATIVE DESCRIPTION')
        print(bar)
        print('ID:\t\t\t' + self.ID)
        print('Currency:\t\t' + self.currency)
        print('Start Date:\t\t' + (self.start_date).strftime(date_str))
        print('Expiration Date:\t' + (self.expiration_date).strftime(date_str))
        if type(underlying) == str:
            print('Underlying:\t\t' + underlying)
        else:
            print('Underlying:\t\t' + underlying.get_ID())
        print('Country:\t\t' + self.country)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    from Stock import Stock
    import datetime as dt

    print('\nTesting Derivative.py...')
    ID = 'DerivativeTesting'
    currency = 'USD'
    start_date = dt.datetime.today()
    expiration_date = dt.datetime(start_date.year + 1, start_date.month,
                                  start_date.day, 0, 0)
    underlying = Stock('AAPL', 'USD', 'AAPLE', 'AAPL', 'AA')
    derivative_test = Derivative(ID, currency, start_date, expiration_date,
                                 underlying)
    derivative_test.to_string()
