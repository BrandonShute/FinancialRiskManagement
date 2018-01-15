#
# Valuation of European call options in Black-Scholes-Merton model
# incl. Vega function and implied volatility estimation
# bsm_functions.py
#
# Analytical Black-Scholes-Merton (BSM) Formula

from math import log, sqrt, exp
from scipy import stats


def bsm_value(S0, K, T, r, sigma, q, option):
    '''
    Valuation of European option and the Greeks in BSM model.
    Analytical formula.

    Parameters
    ==========
    S0 : initial stock/index level
    K : strike price
    T : maturity date (in year fractions)
    r : constant risk-free short rate
    sigma : volatility factor in diffusion term
    q: continuously compounded dividend yield
    option: call/put

    Returns
    =======
    value : present value of the European call/put option
    '''

    # ensure interest rate is non-negative
    if r < 0:
        r = 0

    S0 = float(S0)
    d1 = (log(S0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    # stats.norm.cdf -> cumulative distribution function
    # for normal distribution

    if option == 'call':
        value = (S0 * exp(-q * T) * stats.norm.cdf(d1, 0.0, 1.0) - K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))

        delta = exp(-q * T) * stats.norm.cdf(d1, 0.0, 1.0)

        theta = (-(S0 * sigma * exp(-q * T) / (2 * sqrt(T)) * stats.norm.pdf(d1, 0.0, 1.0)) - r * K * exp(
            -r * T) * stats.norm.cdf(d2, 0.0, 1.0) + q * S0 * exp(-q * T) * stats.norm.cdf(d1, 0.0, 1.0)) / (365 * T)

        rho = 0.01 * K * T * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0)

    else:
        value = (K * exp(-r * T) * stats.norm.cdf(-d2, 0.0, 1.0) - S0 * exp(-q * T) * stats.norm.cdf(-d1, 0.0, 1.0))

        delta = exp(-q * T) * (stats.norm.cdf(d1, 0.0, 1.0) - 1)

        theta = (-(S0 * sigma * exp(-q * T) / (2 * sqrt(T)) * stats.norm.pdf(d1, 0.0, 1.0)) + r * K * exp(
            -r * T) * stats.norm.cdf(-d2, 0.0, 1.0) - q * S0 * exp(-q * T) * stats.norm.cdf(-d1, 0.0, 1.0)) / (365 * T)

        rho = 0.01 * K * T * exp(-r * T) * stats.norm.cdf(-d2, 0.0, 1.0)

    vega = 0.01 * S0 * exp(-q * T) * sqrt(T) * stats.norm.pdf(d1, 0.0, 1.0)
    gamma = exp(-q * T) / (S0 * sigma * sqrt(T)) * stats.norm.pdf(d1, 0.0, 1.0)

    # return value

    return {'value': value, 'delta': delta, 'theta': theta, 'rho': rho, 'vega': vega, 'gamma': gamma}


def bsm_imp_vol(S0, K, T, r, C0, sigma_est, q, option, it):
    '''
    Parameters
    ==========
    sigma_est : estimate of impl. volatility
    it : number of iterations
    C0 : the option's price
    q : continuously compounded dividend yield
    option : call/put

    Returns
    =======
    simga_est : numerically estimated implied volatility
    '''

    MAX_JUMP = 0.5
    TOLERENCE = 0.000000000000001

    for i in range(it):
        bsm_result = bsm_value(S0, K, T, r, sigma_est, q, option)
        d_sigma = (bsm_result['value'] - C0) / (100 * bsm_result['vega'])

        if d_sigma > MAX_JUMP:
            d_sigma = MAX_JUMP
        elif d_sigma < -1 * MAX_JUMP:
            d_sigma = -1 * MAX_JUMP

        sigma_est -= d_sigma

        if sigma_est < TOLERENCE:
            sigma_est = TOLERENCE

    return sigma_est


def bsm_imp_strike_from_vol(S0, sig_impl, T, r, q, delta):
    '''
    Parameters
    ==========
    S0 : initial stock/index level
    sig_impl : implied volatility of the option
    T : maturity date (in year fractions)
    r : constant risk-free short rate
    q: continuously compounded dividend yield
    delta: the delta of the option

    Returns
    =======
    imp_strike : The implied strike calculated from delta
    '''

    denom = exp(stats.norm.ppf(delta * exp(q * T)) * sig_impl * sqrt(T) - (r - q - 0.5 * (sig_impl ** 2)) * T)

    imp_strike = S0 / denom

    return imp_strike

    # bsm_value(S0, K, T, r, sigma, q, option)  # bsm_imp_vol(S0, K, T, r, C0, sigma_est, q, option, it)


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
    imp_vol = bsm_imp_vol(S0, K, T, r, C0, sigma_est, q, option, it)
    print('Implied Vol: ' + str(imp_vol))
