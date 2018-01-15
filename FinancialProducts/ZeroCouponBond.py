#
# Zero Coupon Bond Object
#

from Bond import Bond


class ZeroCouponBond(Bond):
    '''
    ZeroCouponBond(Bond)

    Class for building a zero coupon bond.

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
    def __init__(self, ID, currency, start_date, maturity_date, face_value, issuer, ratings, tier, day_count,
                 industry=None, sector=None, subsector=None, country=None, rf_ID=None, val_spec=None):
        super(ZeroCouponBond, self).__init__(ID, currency, start_date, maturity_date, face_value, 'None', 0, 0, issuer,
                                             ratings, tier, day_count, maturity_date, industry, sector, subsector,
                                             country, rf_ID, val_spec)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import datetime as dt

    print('\nTesting ZeroCouponBond.py...')
    ID = 'ZeroCouponBondTesting'
    currency = 'USD'
    country = 'Canada'
    start_date = dt.datetime.today()
    maturity_date = dt.datetime(start_date.year + 1, start_date.month, start_date.day, 0, 0)
    face_value = 100
    issuer = 'IBM'
    ratings = {'Moodys': 'Aa', 'S&P': 'AA', 'Fitch': 'A'}
    tier = 'Junior'
    day_count = '30/360'
    rf_ID = 'Govt'
    zero_coupon_bond_test = ZeroCouponBond(ID, currency, start_date, maturity_date, face_value, issuer, ratings, tier,
                                           day_count, rf_ID=rf_ID)
    zero_coupon_bond_test.to_string()
