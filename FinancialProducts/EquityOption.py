#
# Equity Option Object
#

import ValuationEngine as valEng
import FinancialModels as finModels
from Option import Option


class EquityOption(Option):
    '''
    EquityOption(Option)

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
    get_exposure :
        returns the exposure of the product
    value_product :
        method used to determine the market value of the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, expiration_date, underlying, strike, option_type, exercise_type,
                 country=None, rf_ID=None, val_spec=None):

        super(EquityOption, self).__init__(ID, currency, start_date, expiration_date, underlying, strike, option_type,
                                           exercise_type, country, rf_ID, val_spec)

    # -------------------------------------------------------------------------
    # Method to return the exposure of the underlying
    # -------------------------------------------------------------------------
    def get_exposure(self, market_environment):

        OptionType = self.option_type
        if OptionType == 'Call':
            option = 'call'
        if OptionType == 'Put':
            option = 'put'

        ExerciseType = self.exercise_type

        S0 = self.underlying.value_product(market_environment)
        K = self.strike
        ID_underlying = self.underlying.get_ID()

        # Risk-Free Rate
        currency = self.currency
        string1 = 'RiskFree-Gov-' + currency
        r = market_environment.get_curve(string1)
        r = r.iloc[0, 0]

        # Time to Maturity
        MaturityDate = self.expiration_date
        ValDate = market_environment.get_val_date()
        T = (MaturityDate - ValDate).days / 365.

        # Volatility
        string2 = 'ImpliedVols-' + currency + '-' + ID_underlying
        volSurface = market_environment.get_surface(string2)
        K_as_percentage_of_stockprice = float(K) / S0
        sigma = finModels.volatility_surface_interpolation(volSurface, T, K_as_percentage_of_stockprice)

        # Dividend Yield
        string3 = 'DividendYields-' + ID_underlying
        q = market_environment.get_constant(string3)

        # Get the delta and gamma of the option
        if ExerciseType == 'European':
            price_info = valEng.bsm_value(S0, K, T, r, sigma, q, option)
        elif ExerciseType == 'American':
            american = True
            N = 100
            price_info = valEng.binomial_tree(S0, K, r, sigma, T, q, N, option, american)

        # Get the delta and gamma of the option
        delta = price_info.get('delta')
        gamma = price_info.get('gamma')

        # Calculate the exposure
        exposure = delta * S0

        return exposure

    # -------------------------------------------------------------------------
    # Method to value the underlying product
    # -------------------------------------------------------------------------
    def value_product(self, market_environment):

        OptionType = self.option_type
        if OptionType == 'Call':
            option = 'call'
        if OptionType == 'Put':
            option = 'put'

        ExerciseType = self.exercise_type

        S0 = self.underlying.value_product(market_environment)
        K = self.strike
        ID_underlying = self.underlying.get_ID()

        # Risk-Free Rate
        currency = self.currency
        string1 = 'RiskFree-Gov-' + currency
        r = market_environment.get_curve(string1)
        r = r.iloc[0, 0]

        # Time to Maturity
        MaturityDate = self.expiration_date
        ValDate = market_environment.get_val_date()
        T = (MaturityDate - ValDate).days / 365.

        # Volatility
        string2 = 'ImpliedVols-' + currency + '-' + ID_underlying
        volSurface = market_environment.get_surface(string2)
        K_as_percentage_of_stockprice = float(K) / S0
        sigma = finModels.volatility_surface_interpolation(volSurface, T, K_as_percentage_of_stockprice)

        # Dividend Yield
        string3 = 'DividendYields-' + ID_underlying
        q = market_environment.get_constant(string3)

        # calculate price
        if ExerciseType == 'European':
            price_info = valEng.bsm_value(S0, K, T, r, sigma, q, option)
            price = price_info.get('value')
        if ExerciseType == 'American':
            american = True
            N = 100
            price_info = valEng.binomial_tree(S0, K, r, sigma, T, q, N, option, american)
            price = price_info.get('value')
        return price


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt
    from Stock import Stock

    print('\nTesting EquityOption.py...')
    ID = 'EquityOptionTesting'
    currency = 'USD'
    start_date = dt.datetime.today()
    expiration_date = dt.datetime(start_date.year + 1, start_date.month, start_date.day, 00, 00)
    underlying = Stock('AAPL', 'USD', 'AAPLE', 'AAPL', 'AA')
    strike = 100
    option_type = 'Call'
    exercise_type = 'European'
    equity_option_test = EquityOption(ID, currency, start_date, expiration_date, underlying, strike, option_type,
                                      exercise_type)
    equity_option_test.to_string()
