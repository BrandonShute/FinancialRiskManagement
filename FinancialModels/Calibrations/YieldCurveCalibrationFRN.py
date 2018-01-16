from functools import partial
from scipy.optimize import minimize
from Optimizers.FRNPricingOptimizer import optimize_FRN_price


def yield_curve_calibration_FRN(FRN_market_price, first_coupon_date,
                                coupon_frequency, maturity_date, val_date,
                                coupon_rate, face, yield_curve, reference_curve,
                                z_spread):
    FRN_pricing_function = partial(optimize_FRN_price, FRN_market_price,
                                   first_coupon_date, coupon_frequency,
                                   maturity_date, val_date, coupon_rate, face,
                                   yield_curve, reference_curve)

    res = minimize(FRN_pricing_function, z_spread, method='SLSQP')

    return res.x[0]
