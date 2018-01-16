#
# Floating Rate Bond Object
#

import pandas as pd
import numpy as np
import ValuationEngine as valEng
import FinancialModels as finModels
from Bond import Bond


class FlaotingRateBond(Bond):
    '''
    FlaotingRateBond(Bond)

    Class for building a floating rate bond.

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
    coupon_rate : double
        the annual coupon rate in percentage terms (Ex. For 5% coupon enter 5)
    coupon_freq: int
        the coupon frequency of the coupon bond defined as number of payments
        per year
    floating_ref : str
        a string specifying the rate to use as the floating rate
    floating_spread : double
        the spread in basis points over the floating rate reference that is
        paid as a coupon
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
    get_floating_ref :
        returns the floating rate reference of the bond
    set_floating_ref :
        sets the floating rate reference of the bond
        coupon bond
    get_floating_spread :
        returns the spread over the floating rate for the bond
    set_floating_spread :
        sets the spread over the floating rate for the bond
    value_product :
        method used to determine the market value of the product
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, maturity_date, face_value,
                 coupon_rate, coupon_freq, floating_ref, floating_spread,
                 issuer, ratings, tier, day_count, first_coupon_date=None,
                 industry=None, sector=None, subsector=None, country=None,
                 rf_ID=None, val_spec=None):

        # Set up the dafault valuation specification for a floating rate bond
        # to be backwards evolution if no val_spec is specified
        if val_spec == None:
            val_spec = 'BackwardsEvolution'

        super(FlaotingRateBond, self).__init__(ID, currency, start_date,
                                               maturity_date, face_value,
                                               'Floating', coupon_rate,
                                               coupon_freq, issuer, ratings,
                                               tier, day_count,
                                               first_coupon_date, industry,
                                               sector, subsector, country,
                                               rf_ID, val_spec)
        self.floating_ref = floating_ref
        self.floating_spread = floating_spread

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the new product attributes
    # -------------------------------------------------------------------------
    def get_floating_ref(self):
        return self.floating_ref

    def set_floating_ref(self, new_floating_ref):
        self.floating_ref = new_floating_ref

    def get_floating_spread(self):
        return self.floating_spread

    def set_floating_spread(self, new_floating_spread):
        self.floating_spread = new_floating_spread

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

        # referenceCurveInput
        string4 = self.floating_ref
        referenceCurveInput = market_environment.get_curve(string4)

        floating_spread = self.floating_spread
        floating_spread = floating_spread / 100. / 100.  # convert from basis points to decimal value

        referenceCurveInput = referenceCurveInput + floating_spread  # layer constant floating spread on top of reference curve

        # calculate price
        price = valEng.FRN_pricing_function(FirstCouponDate, CouponFrequency,
                                            MaturityDate, ValDate, CouponRate,
                                            Face, yieldCurveInput,
                                            referenceCurveInput)
        return price

    # -------------------------------------------------------------------------
    # Print out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 60 * '-'
        print('\n' + bar)
        print('FLOATING RATE BOND DESCRIPTION')
        print(bar)
        print('ID:\t\t\t\t' + self.ID)
        print('Currency:\t\t\t' + self.currency)
        print('Country:\t\t\t' + self.country)
        print('Start Date:\t\t\t' + (self.start_date).strftime(date_str))
        print('Maturity Date:\t\t\t' + (self.maturity_date).strftime(date_str))
        print('Face Value:\t\t\t' + str(self.face_value))
        print('Issuer:\t\t\t\t' + self.issuer)
        for agency in self.ratings:
            print(agency + ':\t\t\t\t' + (self.ratings).get(agency))
        print('First Coupon Date:\t\t' + (self.first_coupon_date).strftime(
            date_str))
        print('Industry:\t\t\t' + self.industry)
        print('Sector:\t\t\t\t' + self.sector)
        print('Subsector:\t\t\t' + self.subsector)
        print('Coupon Type:\t\t\t' + self.coupon_type)
        print('Coupon Rate:\t\t\t' + str(self.coupon_rate) + '%')
        print('Coupon Frequency:\t\t' + str(self.coupon_freq) + ' per annum')
        print('Tier:\t\t\t\t' + self.tier)
        print('Day Count:\t\t\t' + self.day_count)
        print('Floating Index:\t\t\t' + self.floating_ref)
        print('Spread:\t\t\t\t' + str(self.floating_spread) + ' basis pts')
        print('Risk-free Curve ID:\t\t' + self.rf_ID)
        print('Valuation Specification:\t' + self.val_spec)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt

    print('\nTesting FloatingRateBond.py...')
    ID = 'FloatingRateBondTesting'
    currency = 'USD'
    start_date = dt.datetime.today()
    maturity_date = dt.datetime(start_date.year + 1, start_date.month,
                                start_date.day, 0, 0)
    face_value = 100
    coupon_rate = 5
    coupon_freq = 2
    floating_ref = 'LIBOR6M'
    floating_spread = 50
    issuer = 'IBM'
    ratings = {'Moodys': 'Aa', 'S&P': 'AA', 'Fitch': 'A'}
    tier = 'Senior'
    day_count = 'ACT/360'
    industry = 'technology'
    sector = 'information technology'
    subsector = 'information technology'
    country = 'Canada'
    rf_ID = 'Govt'
    val_spec = 'DCF'
    floating_rate_bond_test = FlaotingRateBond(ID, currency, start_date,
                                               maturity_date, face_value,
                                               coupon_rate, coupon_freq,
                                               floating_ref, floating_spread,
                                               issuer, ratings, tier, day_count)
    floating_rate_bond_test.to_string()
