#
# from BondPricingOptimizer import OptimizeBondPrice
# from YieldCurveCalibration import YieldCurveCalibration
# from FRNPricingOptimizer import OptimizeFRNPrice
# from YieldCurveCalibrationFRN import YieldCurveCalibrationFRN
# from Portfolio import *
#
# market_prices = {'02155DAA8': 101.4, '783549AZ1': 123.024, 'COCC0000498': 143.492, 'COCC0008178': 99,
#                  'COCC0019696': 141.992, '078167AZ6  ': 135.86, \
#                  'CO563469CX1': 189.835, 'COEC2323102': 143.043, 'COEC8601758': 142.947, 'COEC9978544': 132.873,
#                  'COED3115760': 145.608, \
#                  'COED5694978': 139.874, 'COEF2970731': 113.224, '74926HAA6': 100.775, 'COEG2531135': 100.04,
#                  '783764AN3': 100.2, \
#                  'COEC0192244': 106.627, '032511BC0': 111.202, '406216AX9': 110.089, '459200HH7': 103.534,
#                  '15672JAA1': 102.628, \
#                  '146900AN5': 104, 'COEF5798261': 113.83, '88158UAA6': 102.184, 'COEG2166353': 113.726,
#                  '12527GAG8': 101.375, \
#                  'COEC9656140': 140.292, '48121CYK6  ': 101.465, '06367XVL2': 100.401, '064151JT1': 100.43}
#
# calculated_z_spread_dict = {}
# price_diff_dict = {}
#
# for k, v in (portfolio.positions).items():
#     x1 = type(k)
#     if str(x1) == "<class 'fixed_rate_bond_cls.fixed_rate_bond_cls'>":
#         ID = k.get_ID()
#         BondMarketPrice = 10.0 * market_prices[ID]
#         FirstCouponDate = k.get_first_coupon_date()
#         CouponFrequency = k.get_coupon_freq()
#         MaturityDate = k.get_maturity_date()
#         ValDate = market_environment.get_val_date()
#         CouponRate = k.get_coupon_rate()
#         Face = k.get_face_value()
#         z_spread = 0.1  # initial guess
#
#         # yieldCurveInput
#         rating = k.get_rating('S&P')
#         currency = k.get_currency()
#
#         string1 = 'RiskFree-Gov-' + currency
#         risk_free_curve = market_environment.get_curve(string1)
#
#         string2 = 'CreditSpreads-Ratings-' + currency
#         credit_spread_matrix = market_environment.get_matrix(string2)
#         if rating == 'AAA':
#             credit_spreads_vector = pd.DataFrame([[0, 0]], columns=[0.25, 30])
#         else:
#             credit_spreads_vector = pd.DataFrame(np.array([credit_spread_matrix.loc[rating]]),
#                                                  columns=list(credit_spread_matrix))
#
#         string3 = 'IdiosyncraticSpread-' + ID
#         idiosyncratic_spread = market_environment.get_constant(string3)
#
#         # want to layer spread curve over risk-free curve, hence need to ensure they have same terms. Use interpolation function to ensure same terms.
#         payment_timing = [0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30]  # represents Key Rates
#
#         risk_free_curve_interp = InterpolatedYieldCurve(risk_free_curve, payment_timing)  # list
#         risk_free_curve_interp = pd.DataFrame(np.array([risk_free_curve_interp]),
#                                               columns=payment_timing)  # pandas DataFrame array
#
#         credit_spreads_vector_interp = InterpolatedYieldCurve(credit_spreads_vector, payment_timing)  # list
#         credit_spreads_vector_interp = pd.DataFrame(np.array([credit_spreads_vector_interp]),
#                                                     columns=payment_timing)  # pandas DataFrame array
#
#         yieldCurveInput = risk_free_curve_interp + credit_spreads_vector_interp + idiosyncratic_spread
#
#         # Run calibration routine
#         try:
#             calculated_z_spread = YieldCurveCalibration(BondMarketPrice, FirstCouponDate, CouponFrequency, MaturityDate,
#                                                         ValDate, CouponRate, Face, yieldCurveInput, z_spread)
#             calculated_z_spread_dict[ID] = calculated_z_spread
#         except:
#             calculated_z_spread_dict[ID] = 0
#
#         # check: theoretical price - actual price
#         theoretical_price = k.value_product(mkt_env)
#         actual_price = 10.0 * market_prices[ID]
#         price_diff = theoretical_price - actual_price
#         price_diff_dict[ID] = price_diff
#
#     if str(x1) == "<class 'floating_rate_bond_cls.floating_rate_bond_cls'>":
#
#         ID = k.get_ID()
#         FRN_MarketPrice = 10.0 * market_prices[ID]
#         FirstCouponDate = k.get_first_coupon_date()
#         CouponFrequency = k.get_coupon_freq()
#         MaturityDate = k.get_maturity_date()
#         ValDate = market_environment.get_val_date()
#         CouponRate = k.get_coupon_rate()
#         Face = k.get_face_value()
#         z_spread = 0.1  # initial guess
#
#         # yieldCurveInput
#         rating = k.get_rating('S&P')
#         currency = k.get_currency()
#
#         string1 = 'RiskFree-Gov-' + currency
#         risk_free_curve = market_environment.get_curve(string1)
#
#         string2 = 'CreditSpreads-Ratings-' + currency
#         credit_spread_matrix = market_environment.get_matrix(string2)
#         if rating == 'AAA':
#             credit_spreads_vector = pd.DataFrame([[0, 0]], columns=[0.25, 30])
#         else:
#             credit_spreads_vector = pd.DataFrame(np.array([credit_spread_matrix.loc[rating]]),
#                                                  columns=list(credit_spread_matrix))
#
#         string3 = 'IdiosyncraticSpread-' + ID
#         idiosyncratic_spread = market_environment.get_constant(string3)
#
#         # want to layer spread curve over risk-free curve, hence need to ensure they have same terms. Use interpolation function to ensure same terms.
#         payment_timing = [0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30]  # represents Key Rates
#
#         risk_free_curve_interp = InterpolatedYieldCurve(risk_free_curve, payment_timing)  # list
#         risk_free_curve_interp = pd.DataFrame(np.array([risk_free_curve_interp]),
#                                               columns=payment_timing)  # pandas DataFrame array
#
#         credit_spreads_vector_interp = InterpolatedYieldCurve(credit_spreads_vector, payment_timing)  # list
#         credit_spreads_vector_interp = pd.DataFrame(np.array([credit_spreads_vector_interp]),
#                                                     columns=payment_timing)  # pandas DataFrame array
#
#         yieldCurveInput = risk_free_curve_interp + credit_spreads_vector_interp + idiosyncratic_spread
#
#         # referenceCurveInput
#         string4 = k.get_floating_ref()
#         referenceCurveInput = market_environment.get_curve(string4)
#
#         floating_spread = k.get_floating_spread()
#         floating_spread = floating_spread / 100. / 100.  # convert from basis points to decimal value
#
#         referenceCurveInput = referenceCurveInput + floating_spread  # layer constant floating spread on top of reference curve
#
#         # Run calibration routine
#         try:
#             calculated_z_spread = YieldCurveCalibration_FRN(FRN_MarketPrice, FirstCouponDate, CouponFrequency,
#                                                             MaturityDate, ValDate, CouponRate, Face, yieldCurveInput,
#                                                             referenceCurveInput, z_spread)
#             calculated_z_spread_dict[ID] = calculated_z_spread
#         except:
#             calculated_z_spread_dict[ID] = 0
#
#             # check: theoretical price - actual price
#         theoretical_price = k.value_product(mkt_env)
#         actual_price = 10.0 * market_prices[ID]
#         price_diff = theoretical_price - actual_price
#         price_diff_dict[ID] = price_diff
