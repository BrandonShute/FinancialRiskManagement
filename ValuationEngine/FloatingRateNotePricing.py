import FinancialModels as finModels
from dateutil.relativedelta import relativedelta


def FRN_pricing_function(first_coupon_date, coupon_frequency, maturity_date,
                         val_date, coupon_rate, face, yield_curve,
                         reference_curve):
    # BondPricingFunction(FirstCouponDate,CouponFrequency,MaturityDate,ValDate,CouponRate,Face,yieldCurveInput):

    # yieldCurveInput=[] # 3m,6m,1y,2yr,3yr,4yr,5yr,7yr,10yr,15yr,20yr,25yr,30yr
    # CouponRate=10
    # Face=100
    # MaturityDate=datetime.datetime(2017,12,1,0,0)
    # ValDate=datetime.datetime(2016,12,1,0,0)

    coupon_rate = 1.0 * coupon_rate / coupon_frequency
    InitialCoupon = coupon_rate / 100. * face

    #######################################################################
    num_months = 12. / coupon_frequency

    coupon_schedule = [first_coupon_date]

    j = 1
    while coupon_schedule[-1] < maturity_date:
        coupon_schedule.append(
            coupon_schedule[-1] + relativedelta(months=int(num_months)))
        j = j + 1

    if coupon_schedule[-1] > maturity_date:
        coupon_schedule[-1] = maturity_date

    coupon_schedule_temp = []
    for ii in range(len(coupon_schedule)):
        if coupon_schedule[ii] > val_date:
            coupon_schedule_temp.append(coupon_schedule[ii])
    coupon_schedule = coupon_schedule_temp

    coupon_schedule_value = []
    for ii in range(len(coupon_schedule)):
        coupon_schedule_value.append(
            float((coupon_schedule[ii] - val_date).days) / 365)

    valuation_curve = finModels.interpolated_yield_curve(yield_curve,
                                                         coupon_schedule_value)

    #    #ensure valuation curve only encompasses non-negative rates
    #    for ii in range(len(valuation_curve)):
    #        if valuation_curve[ii]<0:
    #            valuation_curve[ii]=0

    #######################################################################

    interp_ref_curve = finModels.interpolated_yield_curve(reference_curve,
                                                          coupon_schedule_value)

    forward_curve = [interp_ref_curve[0]]
    for ii in range(len(interp_ref_curve) - 1):
        forward_curve.append(pow(((pow(1 + interp_ref_curve[ii + 1],
                                       coupon_schedule_value[ii + 1])) / (
                                      pow(1 + interp_ref_curve[ii],
                                          coupon_schedule_value[ii]))), 1. / (
                                         coupon_schedule_value[ii + 1] -
                                         coupon_schedule_value[ii])) - 1)

    # ensure forward curve only encompasses non-negative rates
    for ii in range(len(forward_curve)):
        if forward_curve[ii] < 0:
            forward_curve[ii] = 0

    #######################################################################

    coupon_pmts = [face * x / float(coupon_frequency) for x in forward_curve]

    timeto_maturity = (maturity_date - val_date).days / 365.

    FRN_price = 0
    for ii in range(0, len(coupon_pmts)):
        FRN_price = FRN_price + coupon_pmts[ii] / pow(1 + valuation_curve[ii],
                                                      coupon_schedule_value[ii])

    FRN_price = FRN_price + (
            face / pow(1 + valuation_curve[-1], timeto_maturity))

    return FRN_price
