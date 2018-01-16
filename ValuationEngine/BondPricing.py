from dateutil.relativedelta import relativedelta
import FinancialModels as finModels


def bond_pricing_function(first_coupon_date, coupon_frequency, maturity_date,
                          val_date, coupon_rate, face, yield_curve):
    coupon_rate = 1.0 * coupon_rate / coupon_frequency
    coupon_amount = coupon_rate / 100. * face

    num_months = 12. / coupon_frequency

    coupon_schedule = [first_coupon_date]

    j = 1
    while coupon_schedule[-1] < maturity_date:
        coupon_schedule.append(
            coupon_schedule[-1] + relativedelta(months=int(num_months)))
        j = j + 1

    if coupon_schedule[-1] > maturity_date:
        coupon_schedule[-1] = maturity_date

    CouponSchedule_temp = []
    for ii in range(0, len(coupon_schedule)):
        if coupon_schedule[ii] > val_date:
            CouponSchedule_temp.append(coupon_schedule[ii])
    coupon_schedule = CouponSchedule_temp

    coupon_schedule_value = []
    for ii in range(0, len(coupon_schedule)):
        coupon_schedule_value.append(
            float((coupon_schedule[ii] - val_date).days) / 365)

    valuation_curve = finModels.interpolated_yield_curve(yield_curve,
                                                         coupon_schedule_value)

    #    #ensure valuation curve only encompasses non-negative rates
    #    for ii in range(0,len(valuation_curve)):
    #        if valuation_curve[ii]<0:
    #            valuation_curve[ii]=0

    # price coupon stream
    price = 0
    for ii in range(0, len(valuation_curve)):
        price = price + coupon_amount / pow(1 + valuation_curve[ii],
                                            coupon_schedule_value[ii])

    # add value of Face value payment
    price = price + face / pow(1 + valuation_curve[-1],
                               coupon_schedule_value[-1])

    return price
