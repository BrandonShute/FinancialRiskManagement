#
# Option Object
#

from Derivative import Derivative


class Option(Derivative):
    '''
    Option(Derivative)

    Class for a building an option.

    Attributes
    ==========
    ID : str
        unique identifier for the product
    currency : str
        currency denomination of the product
    start_date : datetime
        date specifying when the contract started
    expiration_date : datetime
        date specifying when the contract expires
    underlying : object
         the object representing the underlying asset
    strike : double
        strike price of the option contract
    option_type : str
        option type (Call or Put)
    exercise_type : str
        type of exercise (European, American, Bermudan, etc.)
    country : str
        country of the product
    rf_ID : str
        string specifying the unique identifier of the risk-free curve to use
        for pricing
    val_spec : str
        string to specify the valuation specification when valuing the option

    Methods
    =======
    get_underlying_asset :
        returns the underlying asset of the derivative contract
    set_underlying_asset :
        sets the underlying asset of the derivative contract
    get_strike :
        returns the strike of the option contract
    set_strike :
        sets the strike of the option contract
    get_option_type :
        returns the option type of the option contract
    set_option_type :
        sets the option type of the option contract
    get_exercise_type :
        returns the exercise type of the option contract
    set_exercise_type :
        sets the exercise type of the option contract
    get_rf_ID :
        returns the risk-free curve ID to use for valuation
    set_rf_ID :
        sets the risk-free curve ID to use for valuation
    get_val_spec :
        returns the valuation specification to use when pricing the option
    set_val_spec :
        sets the valuation specification to use when pricing the option
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
    def __init__(self, ID, currency, start_date, expiration_date, underlying, strike, option_type, exercise_type,
                 country=None, rf_ID=None, val_spec=None):
        super(Option, self).__init__(ID, currency, start_date, expiration_date, underlying, country)
        self.strike = strike
        self.option_type = option_type
        self.exercise_type = exercise_type
        self.rf_ID = rf_ID

        # Set up default values for the risk-free rate and valuation
        # specification to use
        if rf_ID != None:
            self.rf_ID = rf_ID
        else:
            self.rf_ID = 'Gov'
        if val_spec != None:
            self.val_spec = val_spec
        elif (self.option_type).lower() != 'european':
            self.val_spec = 'BackwardsEvolution'
        else:
            self.val_spec = 'Black'

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_underlying_asset(self):
        return self.underlying_asset

    def set_underlying_asset(self, new_underlying_asset):
        self.underlying_asset = new_underlying_asset

    def get_strike(self):
        return self.strike

    def set_strike(self, new_strike):
        self.strike = new_strike

    def get_option_type(self):
        return self.option_type

    def set_option_type(self, new_option_type):
        self.option_type = new_option_type

    def get_exercise_type(self):
        return self.exercise_type

    def set_exercise_type(self, new_exercise_type):
        self.exercise_type = new_exercise_type

    def get_rf_ID(self):
        return self.rf_ID

    def set_rf_ID(self, new_rf_ID):
        self.rf_ID = new_rf_ID

    def get_val_spec(self):
        return self.val_spec

    def set_val_spec(self, new_val_spec):
        self.val_spec = new_val_spec

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

        # Risk-free
        curves.add('RiskFree-' + self.rf_ID + '-' + self.currency)
        # Underlying
        if type(self.underlying) == str:
            constants.add((self.underlying).get_ID() + (self.underlying).get_currency())
        else:
            constants.add('MarketPrice-' + (self.underlying).get_ID())
        # Implied Volatilities
        surfaces.add('ImpliedVols-' + (self.underlying).get_ID())

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists, 'Curves': curves, 'Matrices': matrices,
                        'Surfaces': surfaces}

        # Dividends are currently not considered a risk factor (assumes
        # constant dividend yield or discrete dividend grows at current growth
        # rate)

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
    # def value_product(self, market_environment):
    # ???????????????????????
    # finish this
    # ???????????????????????

    # -------------------------------------------------------------------------
    # Print out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 60 * '-'
        print('\n' + bar)
        print('OPTION DESCRIPTION')
        print(bar)
        print('ID:\t\t\t\t' + self.ID)
        print('Currency:\t\t\t' + self.currency)
        print('Start Date:\t\t\t' + (self.start_date).strftime(date_str))
        print('Expiration Date:\t\t' + (self.expiration_date).strftime(date_str))
        if type(self.underlying) == str:
            print('Underlying:\t\t\t' + self.underlying)
        else:
            print('Underlying:\t\t\t' + (self.underlying).get_ID())
        print('Strike:\t\t\t\t' + str(self.strike))
        print('Option Type:\t\t\t' + self.option_type)
        print('Exercise Type:\t\t\t' + self.exercise_type)
        print('Country:\t\t\t' + self.country)
        print('Risk-free Curve ID:\t\t' + self.rf_ID)
        print('Valuation Specification:\t' + self.val_spec)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt
    from Stock import Stock

    print('\nTesting Option.py...')
    ID = 'OptionTesting'
    currency = 'USD'
    country = 'Canada'
    start_date = dt.datetime.today()
    expiration_date = dt.datetime(start_date.year + 1, start_date.month, start_date.day, 0, 0)
    underlying = Stock('AAPL', 'USD', 'AAPLE', 'AAPL', 'AA')
    strike = 100
    option_type = 'Call'
    exercise_type = 'American'
    option_test = Option(ID, currency, start_date, expiration_date, underlying, strike, option_type, exercise_type,
                         country)
    option_test.to_string()
