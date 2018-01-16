#
# Bond Object
#

import datetime as dt
import pandas as pd
import numpy as np
import ValuationEngine as valEng
import FinancialModels as finModels
from Product import Product


class Bond(Product):
    '''
    Bond(Product)

    Class for building a bond.

    Attributes
    ==========
    ID : str
        unique identifier for the product
    currency : str
        currency denomination of the product
    start_date : datetime
        date specifying when the bond was created
    maturity_date : datetime
        date specifying when the bond matures
    face_value : double
        the face value of the bond contract
    coupon_type : str
        string specifying if the coupon rate is fixed or floating
    coupon_rate : double
        the annual coupon rate in percentage terms (Ex. For 5% coupon enter 5)
    coupon_freq: int
        the coupon frequency of the coupon bond defined as number of payments
        per year
    issuer : str
        the issuer of the bond
    ratings : dict
        a dictionary of ratings of the bond from different ratings agencies
    tier : str
        string specifying the tier (seniority) of the bond
    day_count : str
        the day count convention used for accruing interest
    first_coupon_date : datetime
        the date of the first coupon payment
    industry : str
        the industry of the company
    sector : str
        the sector of the company
    subsector : str
        the subsector of the company
    country : str
        country of the product
    rf_ID : str
        string specifying the unique identifier of the risk-free curve to use
        for pricing
    val_spec : str
        string to specify the valuation specification when valuing the option

    Methods
    =======
    get_start_date :
        returns the start date of the bond
    set_start_date :
        sets the start date of the bond
    get_maturity_date :
        returns the maturity date of the bond
    set_maturity_date :
        sets the maturity date of the bond
    get_face_value :
        returns the face value of the bond
    set_face_value :
        sets the face value of the bond
    get_coupon_type :
        returns the coupon type of the coupon bond
    set_coupon_type :
        sets the coupon type of the coupon bond
    get_coupon_rate :
        returns the coupon rate of the coupon bond
    set_coupon_rate :
        sets the coupon rate of the coupon bond
    get_coupon_freq :
        returns the coupon frequency of the coupon bond
    set_coupon_freq :
        sets the coupon frequency of the coupon bond
    get_issuer :
        returns the issuer of the bond
    set_issuer :
        sets the issuer of the bond
    get_rating :
        sets the rating of the bond by specifying the ratings agency
    set_rating :
        returns the rating of the bond by specifying the ratings agency
    get_tier :
        returns the tier of the coupon bond
    set_tier :
        sets the tier of the coupon bond
    get_day_count :
        returns the day count of the coupon bond
    set_day_count :
        sets the day count of the coupon bond
    get_first_coupon_date :
        returns the first coupon date of the bond
    set_first_coupon_date :
        sets the first coupon date of the bond
    get_industry :
        returns the industry of the bond
    set_industry :
        sets the industry of the bond
    get_sector :
        returns the sector of the bond
    set_sector :
        sets the sector of the bond
    get_subsector :
        returns the subsector of the bond
    set_subsector :
        sets the subsector of the bond
    get_rf_ID :
        returns the risk-free curve ID to use for valuation
    set_rf_ID :
        sets the risk-free curve ID to use for valuation
    get_val_spec :
        returns the valuation specification to use when pricing the bond
    set_val_spec :
        sets the valuation specification to use when pricing thebond
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
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, maturity_date, face_value,
                 coupon_type, coupon_rate, coupon_freq, issuer, ratings, tier,
                 day_count, first_coupon_date=None, industry=None, sector=None,
                 subsector=None, country=None, rf_ID=None, val_spec=None):
        super(Bond, self).__init__(ID, currency, country)
        self.start_date = start_date
        self.maturity_date = maturity_date
        self.face_value = face_value
        self.coupon_type = coupon_type
        self.coupon_rate = coupon_rate
        self.coupon_freq = coupon_freq
        self.issuer = issuer
        self.ratings = ratings
        self.tier = tier
        self.day_count = day_count
        self.rf_ID = rf_ID
        self.val_spec = val_spec

        # Set the asset class to Fixed Income
        self._asset_class = 'Fixed Income'

        # Set the first coupon to the date of the next business day which is
        # exactly one coupon frequency from the start date
        if first_coupon_date != None:
            self.first_coupon_date = first_coupon_date
        else:
            first_coupon_month = int(start_date.month + 12 / coupon_freq)
            first_coupon_year = start_date.year
            if first_coupon_month > 12:
                first_coupon_month -= 12
                first_coupon_year += 1
            self.first_coupon_date = dt.datetime(first_coupon_year,
                                                 first_coupon_month,
                                                 start_date.day, 0, 0)

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

        # Set up default values for the risk-free rate and valuation
        # specification to use
        if rf_ID != None:
            self.rf_ID = rf_ID
        else:
            self.rf_ID = 'OIS'
        if val_spec != None:
            self.val_spec = val_spec
        else:
            self.val_spec = 'DCF'

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_start_date(self):
        return self.start_date

    def set_start_date(self, new_start_date):
        self.start_date = new_start_date

    def get_maturity_date(self):
        return self.maturity_date

    def set_maturity_date(self, new_maturity_date):
        self.maturity_date = new_maturity_date

    def get_face_value(self):
        return self.face_value

    def set_face_value(self, new_face_value):
        self.face_value = new_face_value

    def get_coupon_type(self):
        return self.coupon_type

    def set_coupon_type(self, new_coupon_type):
        self.coupon_type = new_coupon_type

    def get_coupon_rate(self):
        return self.coupon_rate

    def set_coupon_rate(self, new_coupon_rate):
        self.coupon_rate = new_coupon_rate

    def get_coupon_freq(self):
        return self.coupon_freq

    def set_coupon_freq(self, new_coupon_freq):
        self.coupon_freq = new_coupon_freq

    def get_issuer(self):
        return self.issuer

    def set_issuer(self, new_issuer):
        self.issuer = new_issuer

    def get_rating(self, agency):
        return (self.ratings).get(agency)

    def set_rating(self, agency, new_rating):
        (self.ratings)[agency] = new_rating

    def get_tier(self):
        return self.tier

    def set_tier(self, new_tier):
        self.tier = new_tier

    def get_day_count(self):
        return self.day_count

    def set_day_count(self, new_day_count):
        self.day_count = new_day_count

    def get_first_coupon_date(self):
        return self.first_coupon_date

    def set_first_coupon_date(self, new_first_coupon_date):
        self.first_coupon_date = new_first_coupon_date

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

    def get_rf_ID(self):
        return self.rf_ID

    def set_rf_ID(self, new_rf_ID):
        self.rf_ID = new_rf_ID

    def get_val_spec(self):
        return self.val_spec

    def set_val_spec(self, new_val_spec):
        self.val_spec = new_val_spec

    def get_asset_class(self):
        return self._asset_class

    # -------------------------------------------------------------------------
    # Method to return the exposure of the stock
    # -------------------------------------------------------------------------
    def get_exposure(self, market_environment):
        return self.value_product(market_environment)

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

        # Risk-free rate
        curves.add('RiskFree-' + self.rf_ID + '-' + self.currency)
        # Credit Spreads
        lists.add('CreditSpreads')
        # Idiosyncratic Spread
        constants.add('IdiosyncraticSpread-' + self.ID)

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists,
                        'Curves': curves, 'Matrices': matrices,
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

        # Add the risk factors to the correct sets

        # Probability of Default
        lists.add('DefualtProbability')
        # Transition Matrix
        matrices.add('TransitionMatrix')

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists,
                        'Curves': curves, 'Matrices': matrices,
                        'Surfaces': surfaces}

        # Return a dictionary of the risk factors
        return risk_factors

    # -------------------------------------------------------------------------
    # Method to value the underlying product
    # -------------------------------------------------------------------------
    def value_product(self, market_environment):
        FirstCouponDate = self.first_coupon_date
        CouponFrequency = self.coupon_freq
        MaturityDate = self.maturity_date
        ValDate = market_environment.get_val_date()
        CouponRate = self.coupon_rate
        Face = self.face_value

        # yieldCurveInput
        rating = self.ratings['S&P']
        currency = self.currency
        ID = self.ID

        string1 = 'RiskFree-Gov-' + currency
        risk_free_curve = market_environment.get_curve(string1)

        string2 = 'CreditSpreads-Ratings-' + currency
        credit_spread_matrix = market_environment.get_matrix(string2)
        if rating == 'AAA':
            credit_spreads_vector = pd.DataFrame([[0, 0]], columns=[0.25, 30])
        else:
            credit_spreads_vector = pd.DataFrame(
                np.array([credit_spread_matrix.loc[rating]]),
                columns=list(credit_spread_matrix))

        string3 = 'IdiosyncraticSpread-' + ID
        idiosyncratic_spread = market_environment.get_constant(string3)

        # want to layer spread curve over risk-free curve, hence need to ensure they have same terms.
        # Use interpolation function to ensure same terms.
        payment_timing = [0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 25,
                          30]  # represents Key Rates

        risk_free_curve_interp = finModels.interpolated_yield_curve(
            risk_free_curve, payment_timing)
        risk_free_curve_interp = pd.DataFrame(
            np.array([risk_free_curve_interp]), columns=payment_timing)

        credit_spreads_vector_interp = finModels.interpolated_yield_curve(
            credit_spreads_vector, payment_timing)
        credit_spreads_vector_interp = pd.DataFrame(
            np.array([credit_spreads_vector_interp]), columns=payment_timing)

        yieldCurveInput = risk_free_curve_interp + credit_spreads_vector_interp + idiosyncratic_spread

        # calculate price
        price = valEng.bond_pricing_function(FirstCouponDate, CouponFrequency,
                                             MaturityDate, ValDate, CouponRate,
                                             Face, yieldCurveInput)
        return price

    # -------------------------------------------------------------------------
    # print(out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 60 * '-'
        print('\n' + bar)
        print('BOND DESCRIPTION')
        print(bar)
        print('ID:\t\t\t\t' + self.ID)
        print('Currency:\t\t\t' + self.currency)
        print('Start Date:\t\t\t' + (self.start_date).strftime(date_str))
        print('Maturity Date:\t\t\t' + (self.maturity_date).strftime(date_str))
        print('Face Value:\t\t\t' + str(self.face_value))
        print('Coupon Type:\t\t\t' + self.coupon_type)
        print('Coupon Rate:\t\t\t' + str(self.coupon_rate) + '%')
        print('Coupon Frequency:\t\t' + str(self.coupon_freq) + ' per annum')
        print('Issuer:\t\t\t\t' + self.issuer)
        for agency in self.ratings:
            print(agency + ':\t\t\t\t' + (self.ratings).get(agency))
        print('Tier:\t\t\t\t' + self.tier)
        print('Day Count:\t\t\t' + self.day_count)
        print('First Coupon Date:\t\t' + (self.first_coupon_date).strftime(
            date_str))
        print('Industry:\t\t\t' + self.industry)
        print('Sector:\t\t\t\t' + self.sector)
        print('Subsector:\t\t\t' + self.subsector)
        print('Country:\t\t\t' + self.country)
        print('Risk-free Curve ID:\t\t' + self.rf_ID)
        print('Valuation Specification:\t' + self.val_spec)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print('\nTesting Bond.py...')
    ID = 'BondTesting'
    currency = 'USD'
    start_date = dt.datetime.today()
    maturity_date = dt.datetime(start_date.year + 1, start_date.month,
                                start_date.day, 0, 0)
    face_value = 100
    coupon_type = 'Fixed'
    coupon_rate = 5
    coupon_freq = 2
    issuer = 'IBM'
    ratings = {'Moodys': 'Aa', 'S&P': 'AA', 'Fitch': 'A'}
    tier = 'Senior'
    day_count = 'ACT/360'
    first_coupon_month = int(start_date.month + 12 / coupon_freq)
    first_coupon_year = start_date.year
    if first_coupon_month > 12:
        first_coupon_month -= 12
        first_coupon_year += 1
    first_coupon_date = dt.datetime(first_coupon_year, first_coupon_month,
                                    start_date.day, 0, 0)
    industry = 'technology'
    sector = 'information technology'
    subsector = 'information technology'
    country = 'Canada'
    rf_ID = 'Govt'
    bond_test = Bond(ID, currency, start_date, maturity_date, face_value,
                     coupon_type, coupon_rate, coupon_freq, issuer, ratings,
                     tier, day_count, first_coupon_date, industry, sector,
                     subsector, country, rf_ID)
    bond_test.to_string()
