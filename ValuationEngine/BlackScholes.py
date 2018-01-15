#
# Valuation of European call options in Black-Scholes-Merton model
# incl. Vega function and implied volatility estimation
# bsm_functions.py
#
# Analytical Black-Scholes-Merton (BSM) Formula

import numpy as np
from math import log, sqrt, exp
from scipy import stats


def black_scholes_value(index_price, strike, time, risk_free, sigma, div_yield, option_type):
    '''
    Valuation of European option and the Greeks in BSM model.
    Analytical formula.

    Parameters
    ==========
    index_price : initial stock/index level
    strike : strike price
    time : maturity date (in year fractions)
    risk_free : constant risk-free short rate
    sigma : volatility factor in diffusion term
    div_yield: continuously compounded dividend yield
    option_type: call/put

    Returns
    =======
    value : present value of the European call/put option
    '''

    days_in_year = 365

    # ensure interest rate is non-negative
    if risk_free < 0:
        risk_free = 0

    index_price = float(index_price)

    d_plus = (log(index_price / strike) + (risk_free - div_yield + 0.5 * sigma ** 2) * time) / (sigma * sqrt(time))
    d_minus = d_plus - (sigma * sqrt(time))

    discount_factor_risk_free = exp(-risk_free * time)
    discount_factor_div_yield = exp(-div_yield * time)

    norm_pdf_d_plus = stats.norm.pdf(d_plus, 0.0, 1.0)

    if option_type == 'call':
        eta = 1
    else:
        eta = -1

    eta_norm_cdf_d_plus = stats.norm.cdf(eta * d_plus, 0.0, 1.0)
    eta_norm_cdf_d_minus = stats.norm.cdf(eta * d_minus, 0.0, 1.0)

    value = eta * (
            index_price * discount_factor_div_yield * eta_norm_cdf_d_plus - strike * discount_factor_risk_free * eta_norm_cdf_d_minus)

    delta = eta * discount_factor_div_yield * eta_norm_cdf_d_plus

    gamma = discount_factor_div_yield / (index_price * sigma * sqrt(time)) * norm_pdf_d_plus

    theta = (-(index_price * sigma * discount_factor_div_yield / (2 * sqrt(time)) * norm_pdf_d_plus) - eta * (
            risk_free * strike * discount_factor_risk_free * eta_norm_cdf_d_minus + div_yield * index_price * discount_factor_div_yield * eta_norm_cdf_d_plus) / (
            days_in_year * time))

    rho = eta * (0.01 * strike * time * discount_factor_risk_free * eta_norm_cdf_d_minus)

    vega = 0.01 * index_price * discount_factor_div_yield * sqrt(time) * norm_pdf_d_plus

    return {'value': value, 'delta': delta, 'theta': theta, 'rho': rho, 'vega': vega, 'gamma': gamma}


def calculate_implied_vol(index_price, strike, time, risk_free, option_price, sigma_est, div_yield, option_type,
                          max_iterations=10000):
    '''
    Parameters
    ==========
    index_price : initial stock/index level
    strike : strike price
    time : maturity date (in year fractions)
    risk_free : constant risk-free short rate
    option_price : the option's price
    sigma_est : estimate of impl. volatility
    div_yield : continuously compounded dividend yield
    option_type : call/put
    max_iterations : the maximum number of iterations

    Returns
    =======
    simga_est : numerically estimated implied volatility
    '''

    MAX_JUMP = 0.5
    TOLERENCE = 0.000000000000001

    for i in range(max_iterations):
        bsm_result = black_scholes_value(index_price, strike, time, risk_free, sigma_est, div_yield, option_type)

        price_difference = bsm_result['value'] - option_price
        d_sigma = price_difference / (100 * bsm_result['vega'])

        if d_sigma < TOLERENCE:
            break
        elif abs(d_sigma) > MAX_JUMP:
            d_sigma = np.sign(d_sigma) * MAX_JUMP

        sigma_est -= d_sigma
        sigma_est = max(sigma_est, 0)


    return sigma_est


def get_implied_strike_from_implied_vol(index_price, sigma_implied, time, risk_free, div_yield, delta):
    '''
    Parameters
    ==========
    index_price : initial stock/index level
    sigma_implied : implied volatility of the option
    time : maturity date (in year fractions)
    risk_free : constant risk-free short rate
    div_yield: continuously compounded dividend yield
    delta: the delta of the option

    Returns
    =======
    imp_strike : The implied strike calculated from delta
    '''

    denom = exp(stats.norm.ppf(delta * exp(div_yield * time)) * sigma_implied * sqrt(time) - (
            risk_free - div_yield - 0.5 * (sigma_implied ** 2)) * time)

    imp_strike = index_price / denom

    return imp_strike


if __name__ == '__main__':
    S0 = 100
    K = 100
    T = 1
    r = 0.02
    sigma = 0.2
    q = 0.03
    C0 = 7.29
    it = 20
    option = 'call'
    sigma_est = 0.2
    imp_vol = calculate_implied_vol(S0, K, T, r, C0, sigma_est, q, option, it)
    print('Implied Vol: ' + str(imp_vol))