#
# Fixed Rate Bond Object
#

from Bond import Bond


class FixedRateBond(Bond):
    '''
    FixedRateBond(Bond)

    Class for building a fixed rate bond.

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
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, currency, start_date, maturity_date, face_value, coupon_rate, coupon_freq, issuer, ratings,
                 tier, day_count, first_coupon_date=None, industry=None, sector=None, subsector=None, country=None,
                 rf_ID=None, val_spec=None):
        super(FixedRateBond, self).__init__(ID, currency, start_date, maturity_date, face_value, 'Fixed', coupon_rate,
                                            coupon_freq, issuer, ratings, tier, day_count, first_coupon_date, industry,
                                            sector, subsector, country, rf_ID, val_spec)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt

    print('\nTesting FixedRateBond.py...')
    ID = 'FixedRateBondTesting'
    currency = 'USD'
    start_date = dt.datetime.today()
    maturity_date = dt.datetime(start_date.year + 1, start_date.month, start_date.day, 0, 0)
    face_value = 100
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
    first_coupon_date = dt.datetime(first_coupon_year, first_coupon_month, start_date.day, 0, 0)
    industry = 'technology'
    sector = 'information technology'
    subsector = 'information technology'
    country = 'Canada'
    fixed_rate_bond_test = FixedRateBond(ID, currency, start_date, maturity_date, face_value, coupon_rate, coupon_freq,
                                         issuer, ratings, tier, day_count, first_coupon_date, industry, sector,
                                         subsector, country)
    fixed_rate_bond_test.to_string()
