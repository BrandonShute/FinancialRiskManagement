#
# DX Library Frame
# market_environment.py
#

import datetime as dt


class MarketEnvironment(object):
    """
    MarketEnvironment(object)

    Class to model a market environment relevant for valuation.

    Attributes
    ==========
    ID: str
        ID of the market environment
    val_date : datetime object
        date of the market environment
    constants : dict (Str:double)
        dictionary of constants for the market environment (e.g. Stock Prices)
    lists : dict (Str:(pandas dataframe))
        dictionary of generic lists for the market environment
        (e.g. Default Probability by Rating)
    curves : dict (Str:(pandas dataframe))
        dictionary of curves for the market environment (e.g. OIS Curve)
    matrices : dict (Str:(pandas dataframe))
        dictionary of generic matrices for the market environment
        (e.g. Transition Matrix)
    surfaces : dict (Str:(pandas dataframe))
        dictionary of surfaces for the market environment (e.g. Vol Surface)

    Methods
    =======
    get_ID :
        returns the ID of the market environment
    get_val_date :
        return the valuation date of the market environment
    set_val_date :
        set the valuation date of the market environment
    get_constant :
        gets a constant (e.g. Stock Prices)
    add_constant :
        adds a constant
    get_list :
        gets a list (e.g. Default Probability by Rating)
    add_list :
        adds a list
    get_curve :
        gets a market curve (e.g. OIS Curve)
    add_curve :
        adds a market curve
    get_matrix :
        gets a matrix of market data (e.g. Transition Matrix)
    add_matrix :
        adds a matrix of market data (e.g. Transition Matrix)
    get_surface :
        gets a market surface (e.g. volatility surface)
    add_surface :
        adds a market surface

    update_environment :
        updates the entire market environment
    """

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, ID, val_date=None):
        self.ID = ID
        self.constants = {}
        self.lists = {}
        self.curves = {}
        self.matrices = {}
        self.surfaces = {}

        # if the valuation date is not given assume it is today
        if val_date != None:
            self.val_date = val_date
        else:
            self.val_date = dt.datetime.today()

    # -------------------------------------------------------------------------
    # Basic getter functions and functions to add market data to the market environment
    # -------------------------------------------------------------------------
    def get_ID(self):
        return self.ID

    def get_val_date(self):
        return self.val_date

    def set_val_date(self, new_val_date):
        self.val_date = new_val_date

    def get_constant(self, key):
        return self.constants[key]

    def add_constant(self, key, constant):
        self.constants[key] = constant

    def get_list(self, key):
        return self.lists[key]

    def add_list(self, key, list_object):
        self.lists[key] = list_object

    def get_curve(self, key):
        return self.curves[key]

    def add_curve(self, key, curve):
        self.curves[key] = curve

    def get_matrix(self, key):
        return self.matrices[key]

    def add_matrix(self, key, matrix):
        self.matrices[key] = matrix

    def get_surface(self, key):
        return self.surfaces[key]

    def add_surface(self, key, surface):
        self.surfaces[key] = surface

    # -------------------------------------------------------------------------
    # Initialize a new empty environment from an existing environment
    # -------------------------------------------------------------------------
    def initialize_from_env(self, new_mkt_env):
        self.constants = (new_mkt_env.constants).copy()
        self.lists = (new_mkt_env.lists).copy()
        self.curves = (new_mkt_env.curves).copy()
        self.matrices = (new_mkt_env.matrices).copy()
        self.surfaces = (new_mkt_env.surfaces).copy()


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print('\nTesting market_environment.py...')
