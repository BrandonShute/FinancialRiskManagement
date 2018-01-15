from functools import partial
from scipy.optimize import minimize
from BondPricingOptimizer import optimize_bond_price


def yield_curve_calibration(bond_market_price, first_coupon_date, coupon_frequency, maturity_date, val_date,
                            coupon_rate, face, yield_curve, z_spread):

    bond_pricing_function = partial(optimize_bond_price, bond_market_price, first_coupon_date, coupon_frequency,
                                    maturity_date, val_date, coupon_rate, face, yield_curve)

    res = minimize(bond_pricing_function, z_spread, method='SLSQP')

    return res.x[0]
