#
# Valuation of European call options in Black-Scholes-Merton model
# incl. Vega function and implied volatility estimation
# bsm_functions.py
#
# Analytical Black-Scholes-Merton (BSM) Formula

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

    # ensure interest rate is non-negative
    if risk_free < 0:
        risk_free = 0

    index_price = float(index_price)
    d_plus = (log(index_price / strike) + (risk_free - div_yield + 0.5 * sigma ** 2) * time) / (sigma * sqrt(time))
    d_minus = d_plus - (sigma * sqrt(time))

    if option_type == 'call':
        eta = 1
    else:
        eta = -1

    value = (index_price * exp(-div_yield * time) * stats.norm.cdf(eta * d_plus, 0.0, 1.0) - strike * exp(
        -risk_free * time) * stats.norm.cdf(eta * d_minus, 0.0, 1.0))

    delta = exp(-div_yield * time) * eta * stats.norm.cdf(eta * d_plus, 0.0, 1.0)

    gamma = exp(-div_yield * time) / (index_price * sigma * sqrt(time)) * stats.norm.pdf(d_plus, 0.0, 1.0)

    theta = (-(index_price * sigma * exp(-div_yield * time) / (2 * sqrt(time)) * stats.norm.pdf(d_plus, 0.0,
                                                                                                1.0)) - eta * (
                     risk_free * strike * exp(-risk_free * time) * stats.norm.cdf(eta * d_minus, 0.0,
                                                                                  1.0) + div_yield * index_price * exp(
                 -div_yield * time) * stats.norm.cdf(eta * d_plus, 0.0, 1.0)) / (365 * time))

    rho = eta * (0.01 * strike * time * exp(-risk_free * time) * stats.norm.cdf(eta * d_minus, 0.0, 1.0))

    vega = 0.01 * index_price * exp(-div_yield * time) * sqrt(time) * stats.norm.pdf(d_plus, 0.0, 1.0)

    return {'value': value, 'delta': delta, 'theta': theta, 'rho': rho, 'vega': vega, 'gamma': gamma}


def calculate_implied_vol(index_price, strike, time, risk_free, option_price, sigma_est, div_yield, option_type,
                          iterations):
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
    iterations : number of iterations

    Returns
    =======
    simga_est : numerically estimated implied volatility
    '''

    MAX_JUMP = 0.5
    TOLERENCE = 0.000000000000001

    for i in range(iterations):
        bsm_result = black_scholes_value(index_price, strike, time, risk_free, sigma_est, div_yield, option_type)
        d_sigma = (bsm_result['value'] - option_price) / (100 * bsm_result['vega'])

        if d_sigma > MAX_JUMP:
            d_sigma = MAX_JUMP
        elif d_sigma < -1 * MAX_JUMP:
            d_sigma = -1 * MAX_JUMP

        sigma_est -= d_sigma

        if sigma_est < TOLERENCE:
            sigma_est = TOLERENCE

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
