import math
import FinancialModels as finModels
from dateutil.relativedelta import relativedelta


def CDS_pricing_function(payment_frequency, contract_spread, notional, val_date,
                         maturity_date, buy_or_sell_protection, recovery_rate,
                         yield_curve, hazard_rate):
    # contractSpread=100 #in basis points
    # Notional=10000000
    # MaturityDate=datetime.datetime(2018,12,01,01,0,0)
    # ValDate=datetime.datetime(2016,06,01,0,0)
    # BuyOrSellProtection='Buy'
    # RecoveryRate=0.4
    # yieldCurveInput=[0.25,0.5,1,2,3,4,5,7,10,15,20,25,30]
    # HazardRate=0.011

    # TimeToMaturity=round((MaturityDate-ValDate).days/365.*4)/4 #round to nearest 0.25
    num_months = 12. / payment_frequency
    num_months = int(num_months)

    payment_schedule = [maturity_date]
    # factor_1=0
    # for ii in range(0,int(TimeToMaturity*4)):
    #    factor_1=factor_1+0.25
    #    payment_schedule.append(factor_1)
    while payment_schedule[-1] > val_date:
        payment_schedule.append(
            payment_schedule[-1] + relativedelta(months=-num_months))
    payment_schedule = payment_schedule[::-1]  # reverse list

    payment_schedule_value = []
    for ii in range(0, len(payment_schedule)):
        if (payment_schedule[ii] - val_date).days > 0:
            payment_schedule_value.append(
                ((payment_schedule[ii] - val_date).days) / 365.)

    valuation_curve = finModels.interpolated_yield_curve(yield_curve,
                                                         payment_schedule_value)

    # ensure valuation curve only encompasses non-negative rates
    for ii in range(0, len(valuation_curve)):
        if valuation_curve[ii] < 0:
            valuation_curve[ii] = 0

    payment_leg = 0
    for ii in range(0, len(payment_schedule_value)):
        payment_leg = payment_leg + notional * (1. / payment_frequency) * (
                (contract_spread / 100.) / 100.) * math.exp(
            -hazard_rate * payment_schedule_value[ii]) / (
                      pow((1 + valuation_curve[ii]),
                          payment_schedule_value[ii]))

    default_leg = 0
    for ii in range(0, len(payment_schedule_value)):
        if payment_schedule_value[ii] < (1. / payment_frequency):
            default_leg = default_leg + notional * (1 - recovery_rate) * (1 - (
            math.exp(-hazard_rate * ((payment_schedule_value[ii]))))) / (
                              pow((1 + valuation_curve[ii]),
                                  payment_schedule_value[ii]))
        else:
            default_leg = default_leg + notional * (
                    1 - recovery_rate) * math.exp(-hazard_rate * (
                    payment_schedule_value[ii] - (
            (1. / payment_frequency)))) * (1 - (
            math.exp(-hazard_rate * ((1. / payment_frequency))))) / (
                              pow((1 + valuation_curve[ii]),
                                  payment_schedule_value[ii]))

    if buy_or_sell_protection == 'Buy':
        CDS_price = default_leg - payment_leg
    elif buy_or_sell_protection == 'Sell':
        CDS_price = payment_leg - default_leg

    return CDS_price
