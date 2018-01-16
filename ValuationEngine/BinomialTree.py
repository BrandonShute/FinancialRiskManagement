import numpy as np
import math


def binomial_tree(S0, K, r, sigma, T, q, N, option, american):
    '''
        BinomialTree(S0, K, r, sigma, T, q, N, option, american)

        Functionality:
        ==========
        Valuation of (American) Options using the Binomial Tree.

        Parameters
        ==========
        S0 : initial stock/index level
        K : strike price
        T : maturity date (in year fractions)
        r : constant risk-free short rate
        sigma : volatility factor in diffusion term
        div: continuously compounded dividend yield
        N: number of branches in the binomial tree
        option: call/put
        american: true/false

        Returns
        =======
        price_info: a dictionary of the option price and sensitivities
        '''
    # ensure interest rate is non-negative
    if r < 0:
        r = 0

    # Basic Calculations
    h = 1.0 * T / N
    u = math.exp(sigma * math.sqrt(h))
    d = math.exp(-1.0 * sigma * math.sqrt(h))
    drift = math.exp((r - q) * h)
    p = (drift - d) / (u - d)

    if option == 'call':
        cp = 1.0
    else:
        cp = -1.0

    # Process the terminal stock price
    stkval = np.zeros((N + 1, N + 1))
    optval = np.zeros((N + 1, N + 1))
    stkval[0, 0] = S0
    for ii in range(1, N + 1):
        stkval[ii, 0] = stkval[ii - 1, 0] * u
        for jj in range(1, ii + 1):
            stkval[ii, jj] = stkval[ii - 1, jj - 1] * d

    # Backward recursion of option price
    for jj in range(N + 1):
        optval[N, jj] = max(0, cp * (stkval[N, jj] - K))
    for ii in range(N - 1, -1, -1):
        for jj in range(ii + 1):
            optval[ii, jj] = (p * optval[ii + 1, jj] + (1 - p) * optval[
                ii + 1, jj + 1]) / drift
            if american:
                optval[ii, jj] = max(optval[ii, jj], cp * (stkval[ii, jj] - K))

    # Calculate price and sensitivities
    value = optval[0, 0]

    delta = (optval[1, 0] - optval[1, 1]) / (stkval[1, 0] - stkval[1, 1])

    g_num1 = (optval[2, 0] - optval[3, 2]) / (stkval[2, 0] - stkval[3, 2])
    g_num2 = (optval[2, 1] - optval[3, 3]) / (stkval[2, 1] - stkval[3, 3])
    g_denom = 0.5 * (stkval[3, 1] - stkval[3, 3])
    gamma = (g_num1 - g_num2) / g_denom

    price_info = {'value': value, 'delta': delta, 'gamma': gamma}

    return price_info


if __name__ == '__main__':
    S0 = 100
    K = 100
    T = 1
    r = 0.02
    sigma = 0.2
    q = 0.03
    N = 200
    option = 'call'
    american = 'true'

    americanoption = binomial_tree(S0, K, r, sigma, T, q, N, option, american)
    print('American Option Price: ' + str(americanoption))
