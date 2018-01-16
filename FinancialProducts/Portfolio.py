#
# Portfolio Object
#

class Portfolio(object):
    '''
    Portfolio(object)

    Class for building portfolios of securities.

    Attributes
    ==========
    positions : dict (product:double)
        dictionary of positions (instances of product class)
    currency :
        the currency to used for the denomination of all portfolio values

    Methods
    =======
    get_currency :
        returns the currency of the portfolio
    set_currency :
        sets the currency of the portfolio
    add_position :
        add a positon to the portfolio
    get_exposure :
        method used to get the exposure of a portfolio
    get_market_risk_factors :
        return a set of market risk factors underlying the portfolio
    get_credit_risk_factors :
        return a set of credit risk factors underlying the portfolio
    value_product
        determine the market value of the entire portfolio
    get_FX_rate :
        helper function to get the FX conversion rate to convert the product
        value to the currency of the portfolio
    to_string :
        prints out details about the portfolio
    '''

    # -------------------------------------------------------------------------
    # Object Definition
    # -------------------------------------------------------------------------
    def __init__(self, positions, currency='CAD'):
        self.positions = positions
        self.currency = currency

    # -------------------------------------------------------------------------
    # Basic Getter and Setter Methods for the bond attributes
    # -------------------------------------------------------------------------
    def get_currency(self):
        return self.currency

    def set_currency(self, new_currency):
        self.currency = new_currency

    # -------------------------------------------------------------------------
    # Add a position to the portfolio. If the object already exists then update
    # the number of units appropriately
    # -------------------------------------------------------------------------
    def add_position(self, product, units=1):
        if product in self.positions:
            current_units = (self.positions).get(product)
            # Check if the trades cancel out
            if (current_units + units) == 0:
                del (self.positions)[product]
            else:
                (self.positions)[product] = current_units + units
        else:
            (self.positions)[product] = units

    # -------------------------------------------------------------------------
    # Define methods for returning the exposure of the portfolio. This
    # implicitly uses recursion to allow a portfolio to be built from sub
    # portfolios
    # -------------------------------------------------------------------------
    def get_exposure(self, market_environment):
        exposure = 0
        for k, v in (self.positions).items():
            FX_rate = self.get_base_currency_conversion(k, market_environment)
            exposure += v * k.get_exposure(market_environment) * FX_rate
        return exposure

    # -------------------------------------------------------------------------
    # Define methods for returning a set of market risk factors and credit risk
    # factors (Currently ignores FX as risk factors since risk-free rates of
    # each currency is a risk factor and the FX rate would be implied by
    # interest rate parity)
    # -------------------------------------------------------------------------
    def get_market_risk_factors(self):
        # Create the empty sets to populate
        constants = set([])
        lists = set([])
        curves = set([])
        matrices = set([])
        surfaces = set([])
        risk_factors = set([])

        # Loop through the portfolio and add the risk factors into the
        # appropriate set. Sets were used to avoid repitition in risk factors
        for k in (self.positions).keys():
            factor_dict = k.get_market_risk_factors()
            constants.add(factor_dict.get('Constants'))
            lists.add(factor_dict.get('Lists'))
            curves.add(factor_dict.get('Curves'))
            matrices.add(factor_dict.get('Matrices'))
            surfaces.add(factor_dict.get('Surfaces'))

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
        risk_factors = set([])

        # Loop through the portfolio and add the risk factors into the
        # appropriate set. Sets were used to avoid repitition in risk factors
        for k in (self.positions).keys():
            factor_dict = k.get_credit_risk_factors()
            constants.add(factor_dict.get('Constants'))
            lists.add(factor_dict.get('Lists'))
            curves.add(factor_dict.get('Curves'))
            matrices.add(factor_dict.get('Matrices'))
            surfaces.add(factor_dict.get('Surfaces'))

        # Crete the dictionary of risk factors
        risk_factors = {'Constants': constants, 'Lists': lists,
                        'Curves': curves, 'Matrices': matrices,
                        'Surfaces': surfaces}

        # Return a dictionary of the risk factors
        return risk_factors

    # -------------------------------------------------------------------------
    # Method to value each of the underlying products. This implicilty uses
    # recursion to allow a portfolio to be built from sub portfolios
    # -------------------------------------------------------------------------
    def value_product(self, market_environment):

        val_date = market_environment.get_val_date()

        port_val = 0.0
        for k, v in (self.positions).items():

            # Get the FX Rate
            fx_rate = self.get_base_currency_conversion(k, market_environment)

            # Set the temporary valuation date to the actual valuation date
            val_date_temp = val_date

            # If the product has an maturity date that is less than the
            # (Simulated past the maturity date) then set the temporary
            # valuation date to the maturity date
            try:
                mat_date = k.get_maturity_date()
                if mat_date < val_date:
                    val_date_temp = mat_date
            except:
                pass

            # If the product has an expiration date that is less than the
            # (Simulated past the expiration date) then set the temporary
            # valuation date to the expiration date
            try:
                exp_date = k.get_expiration_date()
                if exp_date < val_date:
                    val_date_temp = exp_date
            except:
                pass

            # Set the valuation date of the market environment to be the
            # temporary valuation date to price the product and then set it
            # back
            market_environment.set_val_date(val_date_temp)
            price = k.value_product(market_environment)
            market_environment.set_val_date(val_date)

            # Add the product value to the portfolio value
            port_val += v * price * fx_rate

        return port_val

    # -------------------------------------------------------------------------
    # A function used to return a portfolio of products that remove the nesting
    # effects of creating a portfolio from sub portfolios
    # -------------------------------------------------------------------------
    def remove_portfolio_nesting(self):
        flat_positions = self.get_flat_positions()
        self.positions = flat_positions

    # -------------------------------------------------------------------------
    # A function used to return the the product positions of a portfolio by
    # using recursion to loop through the underlying portfolios if the
    # portfolio is created of sub portfolios
    # -------------------------------------------------------------------------
    def get_flat_positions(self, portfolio_units=1):
        flat_positions = {}
        # Use recursion to loop through and save the underlying positions into
        # flat positions one by one
        for k, v in (self.positions).items():
            try:
                inner_flat_positions = k.get_flat_positions(v)
                flat_positions.update(inner_flat_positions)
            except:
                flat_positions[k] = v * portfolio_units

        # Set the new positions as the portfolio positions
        return flat_positions

    # -------------------------------------------------------------------------
    # Helper function to determine the FX Spot rate used to convert the
    # product price to the currency of the portfolio
    # -------------------------------------------------------------------------
    def get_base_currency_conversion(self, product, market_environment):
        # If the product and portfolio currency do not match then
        # determine the spot rate from the market_environment
        prod_currency = product.get_currency()
        port_currency = self.currency
        if prod_currency == port_currency:
            base_currency_conversion = 1.0
        else:
            spot_str = 'FXRates-' + prod_currency + port_currency
            if spot_str in (market_environment.constants).keys():
                base_currency_conversion = market_environment.get_constant(
                    spot_str)
            # NOTE : This assumes that all spot rates we need are in
            # the market environment. Error handling still needs to be
            # added
            else:
                spot_str = 'FXRates-' + port_currency + prod_currency
                base_currency_conversion = 1.0 / market_environment.get_constant(
                    spot_str)

        return base_currency_conversion

    # -------------------------------------------------------------------------
    # Print out a table describing the product and number of units
    # -------------------------------------------------------------------------
    def to_string(self):
        bar = 35 * '-'
        print('\n' + bar)
        print('Product ID \t Position (units)')
        print(bar)
        for k, v in (self.positions).items():
            print(k.get_ID() + '\t' + '%12.4f' % (v))
        print(bar)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import random
    from Stock import Stock

    print('\nTesting Portfolio.py...')
    positions = {}
    for i in range(10):
        units = random.uniform(-1000, 1000)
        p = Stock('Position' + str(i), 'CAD', 'TestCompany' + str(i),
                  'XXX' + str(i), 'AA')
        positions[p] = units
    port_test = Portfolio(positions)
    port_test.to_string()
