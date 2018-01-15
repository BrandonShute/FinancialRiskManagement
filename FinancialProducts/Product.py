#
# Product Object
#

class Product(object):
    '''
    Product(Object)

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
    get_ID :
        returns the ID of the product
    get_currency :
        returns the currency of the product
    set_currency :
        sets the currency of the product
    get_country :
        returns the country of the product
    set_country :
        sets the country of the product
    get_FX_rate :
        returns the FX rate of the product
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, country=None):
        self.ID = ID
        self.currency = currency

        # Set non-given aggregation parameters to 'N/A' if not given
        if country != None:
            self.country = country
        else:
            self.country = 'N/A'

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the product attributes
    # -------------------------------------------------------------------------
    def get_ID(self):
        return self.ID

    def get_currency(self):
        return self.currency

    def set_currency(self, new_currency):
        self.currency = new_currency

    def get_country(self):
        return self.country

    def set_country(self, new_country):
        self.country = new_country

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
    #        return set([])
    #
    #    def get_credit_risk_factors(self):
    #        return set([])
    #
    #    # -------------------------------------------------------------------------
    #    # Method to value the underlying product
    #    # -------------------------------------------------------------------------
    #    def value_product(self, market_environment):

    # -------------------------------------------------------------------------
    # Helper function to determine the FX Spot rate used to convert the
    # product price to the currency of the product
    # -------------------------------------------------------------------------
    def get_base_currency_conversion(self, market_environment, to_currency):
        # If the product and portfolio currency do not match then
        # determine the spot rate from the market_environment
        prod_currency = self.get_currency()
        if prod_currency == to_currency:
            base_currency_conversion = 1.0
        else:
            spot_str = 'FXRates-' + prod_currency + to_currency
            if spot_str in (market_environment.constants).keys():
                FX_rate = market_environment.get_constant(spot_str)
            # NOTE : This assumes that all spot rates we need are in
            # the market environment. Error handling still needs to be
            # added
            else:
                spot_str = 'FXRates-' + to_currency + prod_currency
                base_currency_conversion = 1.0 / market_environment.get_constant(spot_str)

        return base_currency_conversion

    # -------------------------------------------------------------------------
    # print(out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self):
        bar = 35 * '-'
        print('\n' + bar)
        print('PRODUCT DESCRIPTION')
        print(bar)
        print('ID:\t\t' + self.ID)
        print('Currency:\t' + self.currency)
        print('Country:\t' + self.country)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print('\nTesting Product.py...')
    ID = 'ProductTesting'
    currency = 'USD'
    country = 'Canada'
    product_test = Product(ID, currency, country)
    product_test.to_string()
