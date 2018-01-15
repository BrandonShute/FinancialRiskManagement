#
# Callable Bond Object
#

import numpy as np
import ValuationEngine as valEng
from Bond import Bond


class CallableBond(Bond):
    '''
    CallableBond(Bond)

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
    coupon_type : str
        string specifying if the coupon rate is fixed or floating
    coupon_rate : double
        the annual coupon rate in percentage terms (Ex. For 5% coupon enter 5)
    coupon_freq: int
        the coupon frequency of the coupon bond defined as number of payments
        per year
    option_details : dict
        a dictionary specifying the exercise details of the bond optionality.
        It has the date as the key and the details as an inner dictionary. The
        inner dictionary includes strike price, option type, and call on or
        after feature
    issuer : str
        the issuer of the bond
    ratings : dict
        a dictionary of ratings of the bond from different ratings agencies
    tier : str
        string specifying the tier (seniority) of the bond
    day_count : str
        the day count convention used for accruing interest
    industry : str
        the industry of the company
    first_coupon_date : datetime
        the date of the first coupon payment
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
    get_exercise_dates :
        returns a list of the exercise dates of the bond
    get_strikes :
        returns a list of the bond strikes
    get_option_types :
        returns a list of option types of the bond
    get_after_features :
        returns a list of Booleans indicating whether the call optionality is
        available after the call date for the given price
    get_option_details :
        returns the dictionary of the detials about bond optionality
    set_option_details :
        sets the dictionary of the detials about bond optionality
        coupon bond
    value_product :
        method used to determine the market value of the product
    to_string :
        prints out details about the product
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, maturity_date, face_value, coupon_type, coupon_rate, coupon_freq,
                 option_details, issuer, ratings, tier, day_count, first_coupon_date=None, industry=None, sector=None,
                 subsector=None, country=None, rf_ID=None, val_spec=None):

        # Set up the dafault valuation specification for a callable bond
        # to be backwards evolution if no val_spec is specified
        if val_spec == None:
            val_spec = 'BackwardsEvolution'

        super(CallableBond, self).__init__(ID, currency, start_date, maturity_date, face_value, coupon_type,
                                           coupon_rate, coupon_freq, issuer, ratings, tier, day_count,
                                           first_coupon_date, industry, sector, subsector, country, rf_ID, val_spec)
        self.option_details = option_details

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the new product attributes
    # -------------------------------------------------------------------------
    def get_option_details(self):
        return (self.option_details).keys()

    def get_strikes(self):
        strikes = []
        for k in self.option_details:
            inner_dict = (self.option_details).get(k)
            strikes.add(inner_dict.get('strike'))
        return strikes

    def get_option_types(self):
        option_types = []
        for k in self.option_details:
            inner_dict = (self.option_details).get(k)
            option_types.add(inner_dict.get('option_type'))
        return option_types

    def get_after_features(self):
        after_features = []
        for k in self.option_details:
            inner_dict = (self.option_details).get(k)
            after_features.add(inner_dict.get('after_feature'))
        return after_features

    def get_option_details(self):
        return self.option_details

    def set_option_details(self, new_option_details):
        self.option_details = new_option_details

    # -------------------------------------------------------------------------
    # Method to value the underlying product
    # -------------------------------------------------------------------------
    def value_product(self, market_environment):

        # Initial Short Rate
        currency = self.currency
        string1 = 'RiskFree-Gov-' + currency
        initial_short_rate = market_environment.get_curve(string1)
        initial_short_rate = initial_short_rate.iloc[0, 0]

        string2 = 'Curves-RiskFree-Gov-' + currency + '-0.25'
        mean_vect = market_environment.get_list('RiskFactorMeans')
        vol_vect = market_environment.get_list('RiskFactorVolatilities')
        mu = mean_vect[string2][0]
        vol = vol_vect[string2][0]

        FirstCouponDate = self.first_coupon_date
        CouponFrequency = self.coupon_freq
        CouponRate = self.coupon_rate
        Face = self.face_value
        ValDate = market_environment.get_val_date()
        MaturityDate = self.maturity_date

        # callSchedule
        from datetime import datetime, date, time
        callSchedule = self.option_details
        exercise_time_list = []
        for key in callSchedule:
            exercise_time_list.append(key)
        strike_list = []
        for key in callSchedule:
            strike_list.append(callSchedule[key]['strike'])
        key_list = []
        for key in callSchedule:
            key_list.append(key)
        after_feature = callSchedule[key_list[0]]['after_feature']

        temp1 = []
        for ii in range(0, len(strike_list)):
            temp1.append([exercise_time_list[ii], strike_list[ii]])
        callSchedule = np.matrix(temp1)

        # CallScheduleExerciseType
        if after_feature == 'True':
            CallScheduleExerciseType = 'American'
        else:
            CallScheduleExerciseType = 'Bermudan'

        # calculate price
        price = valEng.callable_bond_pricing_function(initial_short_rate, mu, vol, FirstCouponDate, CouponFrequency,
                                                      CouponRate, Face, callSchedule, CallScheduleExerciseType, ValDate,
                                                      MaturityDate)
        return price

    # -------------------------------------------------------------------------
    # print(out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 60 * '-'
        print('\n' + bar)
        print('CALLABLE BOND DESCRIPTION')
        print(bar)
        print('ID:\t\t\t\t' + self.ID)
        print('Currency:\t\t\t' + self.currency)
        print('Country:\t\t\t' + self.country)
        print('Start Date:\t\t\t' + (self.start_date).strftime(date_str))
        print('Maturity Date:\t\t\t' + (self.maturity_date).strftime(date_str))
        print('Face Value:\t\t\t' + str(self.face_value))
        print('Coupon Type:\t\t\t' + self.coupon_type)
        print('Coupon Rate:\t\t\t' + str(self.coupon_rate) + '%')
        print('Coupon Frequency:\t\t' + str(self.coupon_freq) + ' per annum')
        print('Issuer:\t\t\t\t' + self.issuer)
        print('First Coupon Date:\t\t' + (self.first_coupon_date).strftime(date_str))
        for agency in self.ratings:
            print(agency + ':\t\t\t\t' + (self.ratings).get(agency))
        print('Industry:\t\t\t' + self.industry)
        print('Sector:\t\t\t\t' + self.sector)
        print('Subsector:\t\t\t' + self.subsector)
        print('Tier:\t\t\t\t' + self.tier)
        print('Day Count:\t\t\t' + self.day_count)
        print('Risk-free Curve ID:\t\t' + self.rf_ID)
        print('Valuation Specification:\t' + self.val_spec)
        print(bar)

        print('\n\nCALL SCHEDULE:')
        print(bar)
        print(' Date \t\tStrike \t\tType \t  Exercise After')
        print(bar)
        for k in self.option_details:
            inner_dict = (self.option_details).get(k)
            print(k.strftime(date_str) + '\t' + str(inner_dict.get('strike')) + '\t\t' + inner_dict.get(
                'option_type') + '\t\t' + inner_dict.get('after_feature'))
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
    maturity_date = dt.datetime(start_date.year + 1, start_date.month, start_date.day, 0, 0)
    face_value = 100
    coupon_type = 'Fixed'
    coupon_rate = 5
    coupon_freq = 2
    option_details = {dt.datetime(2017, 5, 17): {"strike": 104.125, "option_type": "Call", "after_feature": "True"},
                      dt.datetime(2018, 5, 17): {"strike": 102.750, "option_type": "Call", "after_feature": "True"},
                      dt.datetime(2019, 5, 17): {"strike": 101.375, "option_type": "Call", "after_feature": "True"},
                      dt.datetime(2020, 5, 17): {"strike": 100.000, "option_type": "Call", "after_feature": "True"}}
    issuer = 'IBM'
    ratings = {'Moodys': 'Aa', 'S&P': 'AA', 'Fitch': 'A'}
    tier = 'Senior'
    day_count = 'ACT/360'
    callable_bond_test = CallableBond(ID, currency, start_date, maturity_date, face_value, coupon_type, coupon_rate,
                                      coupon_freq, option_details, issuer, ratings, tier, day_count)
    callable_bond_test.to_string()
