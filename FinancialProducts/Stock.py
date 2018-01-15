#
# Stock Object
#

from Product import Product


class Stock(Product):
    '''
    Stock(Product)

    Class for a building a stock.

    Attributes
    ==========
    ID : str
        unique identifier for the product
    currency : str
        currency denomination of the product
    company_name : str
        the company name of the stock
    ticker : str
        the stock ticker for trading
    industry : str
        the industry of the company
    sector : str
        the sector of the company
    subsector : str
        the subsector of the company
    country : str
        country of the product
    CUSIP : int
        the CUSIP number of the company

    Methods
    =======
    get_company_name :
        returns the company name of the stock
    set_company_name :
        sets the company name of the stock
    get_ticker :
        returns the ticker of the stock
    set_ticker :
        sets the ticker of the stock
    get_rating :
        sets the rating of the bond by specifying the ratings agency
    set_rating :
        returns the rating of the bond by specifying the ratings agency
    get_industry :
        returns the industry of the stock
    set_industry :
        sets the industry of the stock
    get_sector :
        returns the sector of the stock
    set_sector :
        sets the sector of the stock
    get_subsector :
        returns the subsector of the stock
    set_subsector :
        sets the subsector of the stock
    get_CUSIP :
        returns the CUSIP number of the stock
    set_CUSIP :
        sets the CUSIP number of the stock
    get_asset_class :
        gets the asset class of the derivative
    get_exposure :
        returns the exposure of the product
    get_market_risk_factors :
        return a set of market risk factors underlying the product
    get_credit_risk_factors :
        return a set of credit risk factors underlying the product
    value_product :
        method used to determine the market value of the product
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, company_name, ticker, ratings, industry=None, sector=None, subsector=None,
                 country=None, CUSIP=None):
        super(Stock, self).__init__(ID, currency, country)
        self.company_name = company_name
        self.ticker = ticker
        self.ratings = ratings
        self._asset_class = 'Equity'

        # Set non-given aggregation parameters to 'N/A' if not given
        if industry != None:
            self.industry = industry
        else:
            self.industry = 'N/A'
        if sector != None:
            self.sector = sector
        else:
            self.sector = 'N/A'
        if subsector != None:
            self.subsector = subsector
        else:
            self.subsector = 'N/A'
        if CUSIP != None:
            self.CUSIP = CUSIP
        else:
            self.CUSIP = 'N/A'

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_company_name(self):
        return self.company_name

    def set_company_name(self, new_company_name):
        self.company_name = new_company_name

    def get_ticker(self):
        return self.ticker

    def set_ticker(self, new_ticker):
        self.ticker = new_ticker

    def get_rating(self, agency):
        return (self.ratings).get(agency)

    def set_rating(self, agency, new_rating):
        (self.ratings)[agency] = new_rating

    def get_industry(self):
        return self.industry

    def set_industry(self, new_industry):
        self.industry = new_industry

    def get_sector(self):
        return self.sector

    def set_sector(self, new_sector):
        self.sector = new_sector

    def get_subsector(self):
        return self.subsector

    def set_subsector(self, new_subsector):
        self.subsector = new_subsector

    def get_CUSIP(self):
        return self.CUSIP

    def set_CUSIP(self, new_CUSIP):
        self.CUSIP = new_CUSIP

    def get_asset_class(self):
        return self._asset_class

    # -------------------------------------------------------------------------
    # Method to return the exposure of the stock
    # -------------------------------------------------------------------------
    def get_exposure(self, market_environment):
        # Value the product
        return market_environment.get_constant('MarketPrice-' + self.ID)

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

        # Add the risk factors to the correct sets

        # Stock price
        constants.add(self.ID)

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
    # Method to value the underlying product
    # -------------------------------------------------------------------------
    def value_product(self, market_environment):
        return market_environment.get_constant('MarketPrice-' + self.ID)

    # -------------------------------------------------------------------------
    # print(out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self):
        bar = 40 * '-'
        print('\n' + bar)
        print('STOCK DESCRIPTION')
        print(bar)
        print('ID:\t\t' + self.ID)
        print('Currency:\t' + self.currency)
        print('Country:\t' + self.country)
        print('Company:\t' + self.company_name)
        print('Ticker:\t\t' + self.ticker)
        for agency in self.ratings:
            print(agency + ':\t\t' + (self.ratings).get(agency))
        print('Industry:\t' + self.industry)
        print('Sector:\t\t' + self.sector)
        print('Subsector:\t' + self.subsector)
        print('CUSIP Number:\t' + str(self.CUSIP))
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print('Testing Stock.py...')
    ID = 'StockTesting'
    currency = 'USD'
    country = 'Canada'
    company_name = 'AAPLE'
    ticker = 'AAPL'
    ratings = {'Moodys': 'Aa', 'S&P': 'AA', 'Fitch': 'A'}
    industry = 'technology'
    sector = 'information technology'
    subsector = 'information technology'
    CUSIP = 37833100
    stock_test = Stock(ID, currency, company_name, ticker, ratings, industry, sector, subsector, country, CUSIP)
    stock_test.to_string()
