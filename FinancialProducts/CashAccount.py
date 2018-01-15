#
# Cash Account
#

from Product import Product


class CashAccount(Product):
    '''
    CashAccount(Product)

    Class for building a generic financial product.

    Attributes
    ==========
    ID : str
        unique identifier for the product
    currency : str
        currency denomination of the product
    country : str
        country of the product

    Methods
    =======
    get_asset_class :
        returns the asset class of the product
    get_exposure :
        returns the exposure of the product
    get_market_risk_factors :
        return a set of market risk factors underlying the product
    get_credit_risk_factors :
        return a set of credit risk factors underlying the product
    value_product :
        method used to determine the market value of the product

    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, country=None):
        super(CashAccount, self).__init__(ID, currency, country)

        # Set the asset class to Cash
        self._asset_class = 'Cash'

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_asset_class(self):
        return self._asset_class

    # -------------------------------------------------------------------------
    # Method to return the exposure of the cash account. This is always just
    # zero of the currency and the number of units are stored in the portfolio
    # object
    # -------------------------------------------------------------------------
    def get_exposure(self, market_environment):
        return 0.0

    # -------------------------------------------------------------------------
    # Define methods for returning a set of market risk factors and credit risk
    # factors
    # -------------------------------------------------------------------------
    def get_market_risk_factors(self):
        # Create the empty sets to populate
        constants = set([])
        lists = set([])
        curves = set([])
        matrices = set([])
        surfaces = set([])

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists, 'Curves': curves, 'Matrices': matrices,
                        'Surfaces': surfaces}

        # Return a dictionary of the risk factors
        return risk_factors

    def get_credit_risk_factors(self):
        # Create the empty sets to populate
        constants = set([])
        lists = set([])
        curves = set([])
        matrices = set([])
        surfaces = set([])

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists, 'Curves': curves, 'Matrices': matrices,
                        'Surfaces': surfaces}

        # Return a dictionary of the risk factors
        return risk_factors

    # -------------------------------------------------------------------------
    # Method to value the underlying product. This should always be one unit of
    # the currency. Interest is dealt with by the portflio object
    # -------------------------------------------------------------------------
    def value_product(self, market_environment=None):
        return 1.0


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print('\nTesting CashAccount.py...')
    ID = 'Cash'
    currency = 'USD'
    country = 'Canada'
    cash_account_test = CashAccount(ID, currency, country)
    cash_account_test.to_string()
