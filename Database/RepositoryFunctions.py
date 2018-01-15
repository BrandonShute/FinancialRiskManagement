#
# File for functions used to read from the repositories
#

import ast
import os
import pandas as pd
import numpy as np
import FinancialProducts as finProds
import MarketData as mktData

# TODO This now needs to be linked to a database when it is setup
def populate_portfolio_from_repository(port_currency):
    # Paths where the portfolio repository is stored
    SEARCH_STR = 'Dropbox'
    REPOSITORY_PATH = 'Risk Management Project!!/Repositories/'
    REPOSITORY_NAME = 'PortfolioRepository_v2'
    REPOSITORY_FILETYPE = '.xlsx'

    # Save each of the sheet names that need to be grabbed from the repository
    CASH_SHEET = 'CashAccounts'
    BOND_SHEET = 'Bonds'
    STOCK_SHEET = 'Stocks'
    OPTION_SHEET = 'Options'
    CDS_SHEET = 'CreditDefaultSwaps'
    # STRUCTURED_SHEET = 'StructuredProducts'

    # Specify the date format of the option details string
    opt_details_dformat = '%m-%d-%Y'

    # Specify the fill string to fill empty cells in the portfolio database
    fill_str = 'N/A'

    # Find the path on the local machine where dropbox is located
    curr_dir = os.getcwd()
    search_str_idx = curr_dir.find(SEARCH_STR) + len(SEARCH_STR) + 1
    user_path = curr_dir[:search_str_idx]

    # Specify the string of the path with file name and sheet names list
    path_w_file = user_path + REPOSITORY_PATH + REPOSITORY_NAME + REPOSITORY_FILETYPE

    # Save each sheet name into a list divided between underlying products and
    # derivative products. This allows the underlying products to be created
    # first to allow derivatives to reference the underlying object
    product_sheets = [BOND_SHEET, STOCK_SHEET]
    # product_sheets = [CASH_SHEET, BOND_SHEET, STOCK_SHEET]
    derivative_sheets = [OPTION_SHEET, CDS_SHEET]

    # Import each of the sheets
    product_data_dict = {}
    for s in product_sheets:
        temp_data = pd.read_excel(path_w_file, sheetname=s, header=0, true_values=['True'], false_values=['False'])
        mask = temp_data['Status'] == 'Open'
        temp_data = temp_data.loc[mask]
        temp_data = temp_data.reset_index()
        temp_data = temp_data.replace(np.nan, fill_str, regex=True)
        product_data_dict[s] = temp_data

    derivative_data_dict = {}
    for s in derivative_sheets:
        temp_data = pd.read_excel(path_w_file, sheetname=s, header=0, true_values=['True'], false_values=['False'])
        mask = temp_data['Status'] == 'Open'
        temp_data = temp_data.loc[mask]
        temp_data = temp_data.reset_index()
        temp_data = temp_data.replace(np.nan, fill_str, regex=True)
        derivative_data_dict[s] = temp_data

    # Create dictionaries to populate with the products
    products = {}
    derivatives = {}
    underlying_products = {}

    # Loop through the dictionary and create the underlying products
    for data_name, data in product_data_dict.items():

        for i in range(len(data)):
            # Get the parameters that are part of each product
            product_type = data['ProductType'][i]
            ID = data['ID'][i]
            currency = data['Currency'][i]
            country = data['Country'][i]
            position = data['Position'][i]

            # -----------------------------------------------------------------
            # Cash Accounts
            # -----------------------------------------------------------------
            #            if k == CASH_SHEET:
            #                # Create the product object and add it to the products
            #                # dictionary
            #                cash_temp = cash_account(ID, currency, country)
            #                products[cash_temp] = position
            #                continue

            # -----------------------------------------------------------------
            # Bonds
            # -----------------------------------------------------------------
            if data_name == BOND_SHEET:

                # Get product specific parameters
                start_date = data['StartDate'][i]
                start_date = start_date.to_pydatetime()
                maturity_date = data['MaturityDate'][i]
                maturity_date = maturity_date.to_pydatetime()
                face_value = data['FaceValue'][i]
                coupon_type = data['CouponType'][i]
                coupon_rate = data['CouponRate'][i]
                coupon_freq = data['CouponFrequency'][i]
                issuer = data['Issuer'][i]
                ratings = data['Ratings'][i]
                ratings = ast.literal_eval(ratings)
                tier = data['Tier'][i]
                day_count = data['DayCount'][i]
                first_coupon_date = data['FirstCouponDate'][i]
                first_coupon_date = first_coupon_date.to_pydatetime()
                floating_ref = data['FloatingRate'][i]
                floating_spread = data['FloatingSpread'][i]
                industry = data['Industry'][i]
                sector = data['Sector'][i]
                subsector = data['Subsector'][i]
                underlying_bool = data['Underlying'][i]
                option_details = data['OptionDetails'][i]

                # If the option details are not null, then save the option type
                # as a callable bond
                details_temp = {}
                if option_details != fill_str:
                    product_type = 'CallableBond'
                    option_details = ast.literal_eval(option_details)
                    # Convert the date strings to datetimes
                    for k, v in option_details.items():
                        date = dt.datetime.strptime(k, opt_details_dformat)
                        details_temp[date] = v
                    option_details = details_temp

                # Create the product depending on the product type of the bond
                if product_type == 'ZeroCouponBond':
                    bond_temp = finProd.sZeroCouponBond(ID, currency, start_date, maturity_date, face_value, issuer,
                                                        ratings, tier, day_count, industry, sector, subsector, country)

                elif product_type == 'FixedRateBond':
                    bond_temp = finProds.FixedRateBond(ID, currency, start_date, maturity_date, face_value, coupon_rate,
                                                       coupon_freq, issuer, ratings, tier, day_count, first_coupon_date,
                                                       industry, sector, subsector, country)

                elif product_type == 'FloatingRateBond':
                    bond_temp = finProds.FloatingRateBond(ID, currency, start_date, maturity_date, face_value,
                                                          coupon_rate, coupon_freq, floating_ref, floating_spread,
                                                          issuer, ratings, tier, day_count, first_coupon_date, industry,
                                                          sector, subsector, country)

                elif product_type == 'CallableBond':
                    bond_temp = finProds.CallableBond(ID, currency, start_date, maturity_date, face_value, coupon_type,
                                                      coupon_rate, coupon_freq, option_details, issuer, ratings, tier,
                                                      day_count, first_coupon_date, industry, sector, subsector,
                                                      country)


                else:
                    bond_temp = finProds.Bond(ID, currency, start_date, maturity_date, face_value, coupon_type,
                                              coupon_rate, coupon_freq, issuer, ratings, tier, day_count,
                                              first_coupon_date, industry, sector, subsector, country)

                # Create the bond and add it to the products dictionary
                if underlying_bool == True:
                    underlying_products[ID] = bond_temp
                else:
                    products[bond_temp] = position

                continue

            # -----------------------------------------------------------------
            # Stocks
            # -----------------------------------------------------------------
            if data_name == STOCK_SHEET:

                # Get product specific parameters
                company_name = data['Name'][i]
                ticker = data['Industry'][i]
                ratings = data['Ratings'][i]
                ratings = ast.literal_eval(ratings)
                industry = data['Industry'][i]
                sector = data['Sector'][i]
                subsector = data['Subsector'][i]
                CUSIP = data['CUSIP'][i]
                underlying_bool = data['Underlying'][i]

                # Create the stock and add it to the products dictionary
                stock_temp = finProds.Stock(ID, currency, company_name, ticker, ratings, industry, sector, subsector,
                                            country, CUSIP)

                if underlying_bool == True:
                    underlying_products[ID] = stock_temp
                else:
                    products[stock_temp] = position

                continue

    # Loop through the dictionary and create the derivative products
    for data_name, data in derivative_data_dict.items():

        for i in range(len(data)):
            # Get the parameters that are part of each product
            product_type = data['ProductType'][i]
            ID = data['ID'][i]
            currency = data['Currency'][i]
            country = data['Country'][i]
            position = data['Position'][i]
            start_date = data['StartDate'][i]
            start_date = start_date.to_pydatetime()
            expiration_date = data['ExpirationDate'][i]
            expiration_date = expiration_date.to_pydatetime()
            underlying = data['Underlying'][i]

            # Check if the underlying is an object in the underlying_products
            # dict
            if underlying in underlying_products.keys():
                underlying = underlying_products.get(underlying)

            # -----------------------------------------------------------------
            # Options
            # -----------------------------------------------------------------
            if data_name == OPTION_SHEET:

                # Get product specific parameters
                strike = data['Strike'][i]
                option_type = data['OptionType'][i]
                exercise_type = data['ExerciseType'][i]

                # Create the product depending on the product type of the option
                if product_type == 'EquityOption':
                    option_temp = finProds.EquityOption(ID, currency, start_date, expiration_date, underlying, strike,
                                                        option_type, exercise_type, country)


                else:
                    option_temp = finProds.Option(ID, currency, start_date, expiration_date, underlying, strike,
                                                  option_type, country)

                # Add the option to the derivatives dictionary
                derivatives[option_temp] = position
                continue

            # -----------------------------------------------------------------
            # Credit Defualt Swaps
            # -----------------------------------------------------------------
            if data_name == CDS_SHEET:
                # Get product specific parameters
                notional = data['Notional'][i]
                counterparty = data['CounterpartyName'][i]
                pmt_freq = data['PaymentFrequency'][i]
                coupon = data['Coupon'][i]
                contract_spread = data['ContractSpread'][i]
                accrued_on_default = data['AccruedonDefault'][i]
                discount_curve = data['DiscountCurve'][i]
                ratings = data['Ratings'][i]
                ratings = ast.literal_eval(ratings)
                tier = data['Tier'][i]
                day_count = data['DayCount'][i]
                industry = data['Industry'][i]
                sector = data['Sector'][i]
                subsector = data['Subsector'][i]

                # Create the CDS and add it to the derivatives dictionary
                CDS_temp = finProds.CreditDefaultSwap(ID, currency, start_date, expiration_date, underlying, notional,
                                                      counterparty, pmt_freq, coupon, contract_spread,
                                                      accrued_on_default, discount_curve, ratings, tier, day_count,
                                                      industry, sector, subsector, country)
                derivatives[CDS_temp] = position
                continue

    # Add the dictionaries of products into the positions and then save it into
    # a portfolio
    positions = {}
    positions.update(products)
    positions.update(derivatives)
    portfolio = finProds.Portfolio(positions, port_currency)

    # Return the portfolio
    return portfolio


# TODO This now needs to be linked to a database when it is setup
def populate_mkt_env_from_repository(val_date):
    # Paths where the portfolio repository is stored
    SEARCH_STR = 'Dropbox'
    REPOSITORY_PATH = 'Risk Management Project!!/Repositories/MarketDataRepository/'
    REPOSITORY_FILETYPE = '.xlsx'

    # File Names
    SWAP_DISC_FILE = 'SwapDiscountCurves'
    SPREADS_RATING_FILE = 'CreditSpreads-Ratings - Current'
    RECOVERY_FILE = 'RecoveryRates'
    PRICES_FILE = 'MarketPrices'
    IBOR_FILE = 'IBOR'
    IMPLIED_VOL_FILE = 'ImpliedVols - Current'
    HAZARD_FILE = 'IdiosyncraticHazardRates'
    GOV_YIELDS_FILE = 'GovYields'
    FX_RATES_FILE = 'FXRates'
    DIV_YIELD_FILE = 'DividendYield'
    DFLT_PROBABILITIES_FILE = 'DefaultProbabilities-Ratings - Current'
    CREDIT_TRANSITION_FILE = 'CreditTransitionMatrix'
    IDIOSYNCRATIC_FILE = 'IdiosyncraticSpread - Current'
    FACTOR_CORRELATION_FILE = 'CorrelationMatrix - Current'
    FACTOR_VOL_FILE = 'VolatilityVector - Current'
    FACTOR_MEAN_FILE = 'MeanVector - Current'

    # Find the path on the local machine where dropbox is located
    curr_dir = os.getcwd()
    search_str_idx = curr_dir.find(SEARCH_STR) + len(SEARCH_STR) + 1
    user_path = curr_dir[:search_str_idx]

    # Specify the string of the path
    path = user_path + REPOSITORY_PATH

    # Create an empty market environment
    ID = 'Real-Environment-' + str(val_date)
    mkt_env = mktData.MarketEnvironment(ID, val_date)

    # -------------------------------------------------------------------------
    # Import the files
    # -------------------------------------------------------------------------

    # Discount Swap Curve
    swap_disc = pd.ExcelFile(path + SWAP_DISC_FILE + REPOSITORY_FILETYPE)
    swap_disc_USD = swap_disc.parse('USD')
    swap_disc_EUR = swap_disc.parse('EUR')
    swap_disc_USD = swap_disc_USD.set_index('Date')
    swap_disc_EUR = swap_disc_EUR.set_index('Date')
    swap_disc_USD = swap_disc_USD / 100.0
    swap_disc__EUR = swap_disc_EUR / 100.0
    swap_disc = {'USD': swap_disc_USD, 'EUR': swap_disc_EUR}

    # Credit Spreads by Rating
    spreads_by_rating = pd.ExcelFile(path + SPREADS_RATING_FILE + REPOSITORY_FILETYPE)
    spreads_by_rating_USD = spreads_by_rating.parse('USD')
    spreads_by_rating_CAD = spreads_by_rating.parse('CAD')
    spreads_by_rating_EUR = spreads_by_rating.parse('EUR')
    spreads_by_rating_USD = spreads_by_rating_USD.set_index('Date')
    spreads_by_rating_CAD = spreads_by_rating_CAD.set_index('Date')
    spreads_by_rating_EUR = spreads_by_rating_EUR.set_index('Date')
    spreads_by_rating_USD = spreads_by_rating_USD / 100.0
    spreads_by_rating_CAD = spreads_by_rating_CAD / 100.0
    spreads_by_rating_EUR = spreads_by_rating_EUR / 100.0
    spreads_by_rating = {'USD': spreads_by_rating_USD, 'CAD': spreads_by_rating_CAD, 'EUR': spreads_by_rating_EUR}

    # Recovery Rates
    recovery_rates = pd.ExcelFile(path + RECOVERY_FILE + REPOSITORY_FILETYPE)
    recovery_rates = recovery_rates.parse('RecoveryRates')
    del recovery_rates['Year']

    # Market Prices
    market_prices = pd.ExcelFile(path + PRICES_FILE + REPOSITORY_FILETYPE)
    stock_prices = market_prices.parse('Stocks')
    bond_prices = market_prices.parse('Bonds')
    stock_prices = stock_prices.set_index('Date')
    bond_prices = bond_prices.set_index('Date')
    market_prices = [stock_prices, bond_prices]

    # IBOR Curves
    IBOR_curves = pd.ExcelFile(path + IBOR_FILE + REPOSITORY_FILETYPE)
    LIBOR = IBOR_curves.parse('LIBOR')
    CDOR = IBOR_curves.parse('CDOR')
    LIBOR = LIBOR.set_index('Date')
    CDOR = CDOR.set_index('Date')
    LIBOR = LIBOR / 100.0
    CDOR = CDOR / 100.0
    IBOR = {'LIBOR-USD': LIBOR, 'CDOR-CAD': CDOR}

    # Implied Volatility Surfaces
    vol_surfaces = pd.ExcelFile(path + IMPLIED_VOL_FILE + REPOSITORY_FILETYPE)
    vol_surfaces_BA = vol_surfaces.parse('BA')
    vol_surfaces_CAT = vol_surfaces.parse('CAT')
    vol_surfaces_BA = vol_surfaces_BA.set_index('Date')
    vol_surfaces_CAT = vol_surfaces_CAT.set_index('Date')
    temp_index = ['0.8', '0.9', '0.95', '1', '1.05', '1.1']
    vol_surfaces_BA.index = temp_index
    vol_surfaces_CAT.index = temp_index
    vol_surfaces_BA = vol_surfaces_BA / 100.0
    vol_surfaces_CAT = vol_surfaces_CAT / 100.0
    vol_surfaces = {'USD-IQT2565239': vol_surfaces_BA, 'USD-IQT2545284': vol_surfaces_CAT}

    # Idiosyncratic Hazard Rates
    idiosyncratic_hazard_rates = pd.ExcelFile(path + HAZARD_FILE + REPOSITORY_FILETYPE)
    idiosyncratic_hazard_rates = idiosyncratic_hazard_rates.parse('IdiosyncraticHazardRates')
    idiosyncratic_hazard_rates = idiosyncratic_hazard_rates.set_index('Date')

    # Government Yields
    gov_curves = pd.ExcelFile(path + GOV_YIELDS_FILE + REPOSITORY_FILETYPE)
    gov_yields_USD = gov_curves.parse('USD')
    gov_yields_CAD = gov_curves.parse('CAD')
    gov_yields_EUR = gov_curves.parse('EUR')
    gov_yields_USD = gov_yields_USD.set_index('Date')
    gov_yields_CAD = gov_yields_CAD.set_index('Date')
    gov_yields_EUR = gov_yields_EUR.set_index('Date')
    gov_yields_USD = gov_yields_USD / 100.0
    gov_yields_CAD = gov_yields_CAD / 100.0
    gov_yields_EUR = gov_yields_EUR / 100.0
    gov_curves = {'USD': gov_yields_USD, 'CAD': gov_yields_CAD, 'EUR': gov_yields_EUR}

    # FX Rates
    FX_rates = pd.ExcelFile(path + FX_RATES_FILE + REPOSITORY_FILETYPE)
    FX_rates = FX_rates.parse('FXRates')
    FX_rates = FX_rates.set_index('Date')

    # Dividend Yields
    div_yields = pd.ExcelFile(path + DIV_YIELD_FILE + REPOSITORY_FILETYPE)
    div_yields = div_yields.parse('DividendYield')
    div_yields = div_yields.set_index('Date')

    # Default Probabilities
    dflt_probs = pd.ExcelFile(path + DFLT_PROBABILITIES_FILE + REPOSITORY_FILETYPE)
    dflt_probs = dflt_probs.parse('DefaultProbabilities')
    dflt_probs = dflt_probs.set_index('Year')
    dflt_probs = dflt_probs / 100.0

    # Hazard Rates by Rating
    hazard_rates_rating = pd.ExcelFile(path + DFLT_PROBABILITIES_FILE + REPOSITORY_FILETYPE)
    hazard_rates_rating = hazard_rates_rating.parse('HazardRates')
    hazard_rates_rating = hazard_rates_rating.set_index('Year')

    # Credit Transition Matrix
    credit_transition = pd.ExcelFile(path + CREDIT_TRANSITION_FILE + REPOSITORY_FILETYPE)
    credit_transition = credit_transition.parse('CreditTransition')
    credit_transition = credit_transition.set_index('From/To')
    credit_transition = credit_transition / 100.0

    # Idiosyncratic Spreads
    idiosyncratic_spreads = pd.ExcelFile(path + IDIOSYNCRATIC_FILE + REPOSITORY_FILETYPE)
    idiosyncratic_spreads = idiosyncratic_spreads.parse('IdiosyncraticSpread')
    idiosyncratic_spreads = idiosyncratic_spreads.set_index('Date')

    # Factor Correlation File
    factor_corr = pd.ExcelFile(path + FACTOR_CORRELATION_FILE + REPOSITORY_FILETYPE)
    factor_corr = factor_corr.parse('Sheet1')
    factor_corr = factor_corr.set_index('Date')
    col_names = list(factor_corr.columns.values)
    factor_corr = np.nan_to_num(factor_corr)
    factor_corr = factor_corr + np.transpose(factor_corr) - np.identity(len(factor_corr))
    factor_corr = pd.DataFrame(factor_corr, index=col_names, columns=col_names)

    # Factor Volatility File
    factor_vol = pd.ExcelFile(path + FACTOR_VOL_FILE + REPOSITORY_FILETYPE)
    factor_vol = factor_vol.parse('Sheet1')
    del factor_vol['Volatility']

    # Factor Mean File
    factor_mean = pd.ExcelFile(path + FACTOR_MEAN_FILE + REPOSITORY_FILETYPE)
    factor_mean = factor_mean.parse('Sheet1')
    del factor_mean['Mean']

    # -------------------------------------------------------------------------
    # Populate the Market Environment
    # -------------------------------------------------------------------------

    # Discount Swap Curve
    for k, df in swap_disc.items():
        series = df.loc[val_date]
        vals = series.values
        names = []
        for s in series.index:
            names.append(s[s.rfind('-') + 1:])
        curve = pd.DataFrame([vals], columns=names)
        curve_name = 'SwapDiscountCurve-' + k
        mkt_env.add_curve(curve_name, curve)

    # ?????????????????????????????????????????????
    # Credit Spreads by Rating
    # ?????????????????????????????????????????????
    for k, df in spreads_by_rating.items():
        ID_string = 'CreditSpreads-Ratings-' + k
        mkt_env.add_matrix(ID_string, df)

    # Recovery Rates
    mkt_env.add_list('RecoveryRates', recovery_rates)

    # Market Prices
    for df in market_prices:
        series = df.loc[val_date]
        vals = series.values
        for s in series.index:
            name = s[s.rfind('-') + 1:]
            price = series[s]
            ID_string = 'MarketPrice-' + name
            mkt_env.add_constant(ID_string, price)

    # IBOR Curves
    for k, df in IBOR.items():
        series = df.loc[val_date]
        vals = series.values
        names = []
        for s in series.index:
            names.append(s[s.rfind('-') + 1:])
        curve = pd.DataFrame([vals], columns=names)
        curve_name = 'RiskFree-' + k
        mkt_env.add_curve(curve_name, curve)

    # ?????????????????????????????????????????????
    # Implied Volatility Surfaces
    # ?????????????????????????????????????????????
    for k, df in vol_surfaces.items():
        ID_string = 'ImpliedVols-' + k
        mkt_env.add_surface(ID_string, df)

    # Idiosycratic Hazard Rates
    series = idiosyncratic_hazard_rates.loc[val_date]
    for s in series.index:
        price = series[s]
        ID_string = 'IdiosyncraticHazardRate-' + s
        mkt_env.add_constant(ID_string, price)

    # Government Yields
    for k, df in gov_curves.items():
        series = df.loc[val_date]
        vals = series.values
        names = []
        for s in series.index:
            names.append(s[s.rfind('-') + 1:])
        curve = pd.DataFrame([vals], columns=names)
        curve_name = 'RiskFree-Gov-' + k
        mkt_env.add_curve(curve_name, curve)

    # FX Rates
    series = FX_rates.loc[val_date]
    for s in series.index:
        name = s[s.rfind('-') + 1:]
        rate = series[s]
        ID_string = 'FXRates-' + name
        mkt_env.add_constant(ID_string, rate)

    # Dividend Yields
    series = div_yields.loc[val_date]
    for s in series.index:
        name = s[s.rfind('-') + 1:]
        div = series[s]
        ID_string = 'DividendYields-' + name
        mkt_env.add_constant(ID_string, div)

    # ?????????????????????????????????????????????
    # Default Probabilities
    # ?????????????????????????????????????????????
    mkt_env.add_matrix('DefaultProbabilities-Ratings', dflt_probs)

    # Hazard Rates by Rating
    mkt_env.add_matrix('HazardRates-Ratings', hazard_rates_rating)

    # Credit Transition Matrix
    mkt_env.add_matrix('CreditTransitionMatrix', credit_transition)

    # Idiosyncratic Spreads
    series = idiosyncratic_spreads.loc[val_date]
    for s in series.index:
        name = s[s.rfind('-') + 1:]
        spread = series[s]
        ID_string = 'IdiosyncraticSpread-' + name
        mkt_env.add_constant(ID_string, spread)

    # Factor Correlation File
    mkt_env.add_matrix('RiskFactorCorrelationMatrix', factor_corr)

    # Factor Volatility File
    mkt_env.add_list('RiskFactorVolatilities', factor_vol)

    # Factor Mean File
    mkt_env.add_list('RiskFactorMeans', factor_mean)

    # Return the market environment
    return mkt_env
