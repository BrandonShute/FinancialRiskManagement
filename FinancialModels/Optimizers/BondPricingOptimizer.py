from dateutil.relativedelta import relativedelta
from Interpolators.InterpolatedYieldCurve import interpolated_yield_curve
import numpy as np
import pandas as pd


def optimize_bond_price(bond_market_price, first_coupon_date, coupon_frequency, maturity_date, val_date, coupon_rate,
                        face, yield_curve, z_spread):
    headers = list(yield_curve)
    yield_curve = z_spread + yield_curve.iloc[0, :]
    yield_curve = [kk for kk in yield_curve]
    yield_curve = pd.DataFrame(np.array([yield_curve]), columns=headers)
    # ------------------------------------

    coupon_rate = 1.0 * coupon_rate / coupon_frequency
    coupon_amount = coupon_rate / 100. * face

    num_months = 12. / coupon_frequency

    coupon_schedule = [first_coupon_date]

    j = 1
    while coupon_schedule[-1] < maturity_date:
        coupon_schedule.append(coupon_schedule[-1] + relativedelta(months=int(num_months)))
        j = j + 1

    if coupon_schedule[-1] > maturity_date:
        coupon_schedule[-1] = maturity_date

    coupon_schedule_temp = []
    for ii in range(0, len(coupon_schedule)):
        if coupon_schedule[ii] > val_date:
            coupon_schedule_temp.append(coupon_schedule[ii])
    coupon_schedule = coupon_schedule_temp

    # NumPmts=len(coupon_schedule)

    coupon_schedule_value = []
    for ii in range(0, len(coupon_schedule)):
        coupon_schedule_value.append(float((coupon_schedule[ii] - val_date).days) / 365)

    valuation_curve = interpolated_yield_curve(yield_curve, coupon_schedule_value)

    #    #ensure valuation curve only encompasses non-negative rates
    #    for ii in range(0,len(valuation_curve)):
    #        if valuation_curve[ii]<0:
    #            valuation_curve[ii]=0

    # price coupon stream
    price = 0
    for ii in range(0, len(valuation_curve)):
        price = price + coupon_amount / pow(1 + valuation_curve[ii], coupon_schedule_value[ii])

    # add value of Face value payment
    price = price + face / pow(1 + valuation_curve[-1], coupon_schedule_value[-1])

    # return squared error
    return pow(price - bond_market_price, 2)
