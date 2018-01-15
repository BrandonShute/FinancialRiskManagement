#
# Credit Default Swap Object
#

import ValuationEngine as valEng
from Swap import Swap


class CreditDefaultSwap(Swap):
    '''
    CreditDefaultSwap(Swap)

    Class for a building a credit default swap (CDS).

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
    notional : double
        the dollar amount of the contract notional on the swap
    counterparty : str
        a string specifiying the counterparty of the contract
    pmt_freq : int
        the payment frequency of the swap defined as number of payments per
        year (-1 = continuous compounding)
    coupon : double
        the annual coupon rate in percentage terms (Ex. For 5% coupon enter 5)
    contract_spread : double
        the contract spread on the CDS contract quotes in basis points
    accrued_on_default : Bool
        a Boolean specifying whether payment is accrued on defualt
    ratings : dict
        a dictionary of ratings of the bond from different ratings agencies
    discount_curve : str
        string specifying the name of the discount curve
    tier : str
        string specifying the tier (seniority) of the bond
    day_count : str
        the day count convention used for accruing interest
    industry : str
        the industry of the company
    sector : str
        the sector of the company
    subsector : str
        the subsector of the company
    country : str
        country of the product

    Methods
    =======
    get_coupon :
        returns the coupon of the credit default swap
    set_coupon :
        sets the coupon of the credit default swap
    get_contract_spread :
        returns the contract spread of the credit default swap
    set_contract_spread :
        sets the contract spread of the credit default swap
    get_accrued_on_default :
        returns the accrued on defualt of the credit default swap
    set_accrued_on_default :
        sets the accrued on defualt of the credit default swap
    get_ratings :
        returns the ratings of the credit default swap
    set_ratings :
        sets the ratings of the credit default swap
    get_tier :
        returns the tier of the credit default swap
    set_tier :
        sets the tier of the credit default swap
    get_day_count :
        returns the day count of the credit default swap
    set_day_count :
        sets the day count of the credit default swap
    get_industry :
        returns the industry of the swap
    set_industry :
        sets the industry of the swap
    get_sector :
        returns the sector of the swap
    set_sector :
        sets the sector of the swap
    get_subsector :
        returns the subsector of the swap
    set_subsector :
        sets the subsector of the swap
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
    def __init__(self, ID, currency, start_date, expiration_date, underlying, notional, counterparty, pmt_freq, coupon,
                 contract_spread, accrued_on_default, discount_curve, ratings, tier, day_count, industry=None,
                 sector=None, subsector=None, country=None):
        super(CreditDefaultSwap, self).__init__(ID, currency, start_date, expiration_date, underlying, notional,
                                                counterparty, pmt_freq, country)
        self.coupon = coupon
        self.contract_spread = contract_spread
        self.accrued_on_default = accrued_on_default
        self.discount_curve = discount_curve
        self.tier = tier
        self.ratings = ratings
        self.day_count = day_count

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

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_coupon(self):
        return self.coupon

    def set_coupon(self, new_coupon):
        self.coupon = new_coupon

    def get_contract_spread(self):
        return self.contract_spread

    def set_contract_spread(self, new_contract_spread):
        self.contract_spread = new_contract_spread

    def get_accrued_on_default(self):
        return self.accrued_on_default

    def set_accrued_on_default(self, new_accrued_on_default):
        self.accrued_on_default = new_accrued_on_default

    def get_discount_curve(self):
        return self.discount_curve

    def set_discount_curve(self, new_discount_curve):
        self.discount_curve = new_discount_curve

    def get_tier(self):
        return self.tier

    def set_tier(self, new_tier):
        self.tier = new_tier

    def get_rating(self, agency):
        return (self.ratings).get(agency)

    def set_rating(self, agency, new_rating):
        (self.ratings)[agency] = new_rating

    def get_day_count(self):
        return self.day_count

    def set_day_count(self, new_day_count):
        self.day_count = new_day_count

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
        # Default Probability
        lists.add('DefualtProbability')
        # Recovery Rate
        constants.add('RecoveryRate-' + self.ID)

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

        # Add the risk factors to the correct sets

        # Probability of Default
        lists.add('DefualtProbability')
        # Transition Matrix
        matrices.add('TransitionMatrix')

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists, 'Curves': curves, 'Matrices': matrices,
                        'Surfaces': surfaces}

        # Return a dictionary of the risk factors
        return risk_factors

    # -------------------------------------------------------------------------
    # Method to value the underlying product
    # -------------------------------------------------------------------------
    def value_product(self, market_environment):
        PaymentFrequency = self.pmt_freq
        contractSpread = self.contract_spread
        Notional = self.notional
        ValDate = market_environment.get_val_date()
        MaturityDate = self.expiration_date
        BuyOrSellProtection = 'Buy'  # 'Sell' is reflected in the negative position in the portfolio

        # RecoveryRate
        RecoveryRateList = market_environment.get_list('RecoveryRates')
        tier = self.tier
        try:
            RecoveryRate = RecoveryRateList.iloc[0][tier]
        # If the tier is not contained in the list. Be conservative and assume
        # the worst
        except:
            RecoveryRate = RecoveryRateList.iloc[0][-1]

        # yieldCurveInput
        rating = self.ratings['S&P']
        currency = self.currency
        ID = self.ID

        # Discount Curve
        string1 = self.discount_curve
        yieldCurveInput = market_environment.get_curve(string1)

        # HazardRate
        string2 = 'IdiosyncraticHazardRate-' + ID
        string3 = 'HazardRates-Ratings'
        IdiosyncraticHazardRate = market_environment.get_constant(string2)
        HazardRateByRating = market_environment.get_matrix(string3)
        HazardRateByRating = HazardRateByRating.loc[rating][0]

        HazardRate = IdiosyncraticHazardRate + HazardRateByRating
        HazardRate = max(HazardRate, 0)

        # calculate price
        price = valEng.CDS_pricing_function(PaymentFrequency, contractSpread, Notional, ValDate, MaturityDate,
                                            BuyOrSellProtection, RecoveryRate, yieldCurveInput, HazardRate)
        return price

    # -------------------------------------------------------------------------
    # Print out a table describing the product
    # -------------------------------------------------------------------------
    def to_string(self, date_str='%Y-%m-%d'):
        bar = 45 * '-'
        print('\n' + bar)
        print('CDS DESCRIPTION')
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
        for agency in self.ratings:
            print(agency + ':\t\t\t' + (self.ratings).get(agency))
        print('Tier:\t\t\t' + self.tier)
        print('TDiscount Curve:\t' + self.discount_curve)
        print('Day Count:\t\t' + self.day_count)
        print('Industry:\t\t' + self.industry)
        print('Sector:\t\t\t' + self.sector)
        print('Subsector:\t\t' + self.subsector)
        print('Country:\t\t' + self.country)
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt

    print('\nTesting CreditDefaultSwap.py...')
    ID = 'CDSTesting'
    currency = 'USD'
    start_date = dt.datetime.today()
    expiration_date = dt.datetime(start_date.year + 1, start_date.month, start_date.day, 00, 00)
    underlying = 'IBM'
    notional = 100000
    counterparty = 'Goldman Sachs'
    pmt_freq = 4
    coupon = 1
    contract_spread = 69.09
    accrued_on_defualt = True
    discount_curve = 'TestCurve'
    ratings = {'Moodys': 'Aa', 'S&P': 'AA', 'Fitch': 'A'}
    tier = 'Senior'
    day_count = 'ACT/360'
    credit_default_swap_test = CreditDefaultSwap(ID, currency, start_date, expiration_date, underlying, notional,
                                                 counterparty, pmt_freq, coupon, contract_spread, accrued_on_defualt,
                                                 discount_curve, ratings, tier, day_count)
    credit_default_swap_test.to_string()
