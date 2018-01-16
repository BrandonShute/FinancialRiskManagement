#
# Function for creating the marginal VaR of a set of sub-portfolios
#

import numpy as np
import pandas as pd
from MarketRisk import MarketVaR
import ScenarioAnalysis as finScenarios


def marginal_VaR_from_sub_dists(combined_dist, weights, alpha, name_list=None):
    '''
    marginal_VaR_from_sub_dists(combined_dist, weights, alpha)

    Functionality
    =============
    This calculates the risk contribution and marginal VaR at alpha percentile

    Parameters
    ==========
    combined_dist : numpy matrix
         P&L distribution of each instrument consisting of the total portfolio.
         The columns refer to the simulated scenario and the rows correspond
         to the sub portfolio
    weights : numpy array
         weights of each element in total portfolio to calculate marginal VaR
    alpha : double
         quantile used for the VaR calculation (between 0 and 1)

    Returns
    =======
    RC : dataframe
        the risk contribution of each element of the total portfolio
    MVaR : dataframe
        the marginal VaR of each element in the total portfolio
    '''

    # Calculate the correlation matrix of the assets
    Q = np.cov(combined_dist)

    # Determine the total portfolio distribtuin and calculate VaR
    total_dist = sum(combined_dist)
    VaR, _ = MarketVaR.calculate_VaR_from_PnL(total_dist, alpha)

    # Calculate the risk contribution and marginal VaR
    numer = np.dot(Q, weights)
    denom = np.dot(np.transpose(weights), numer)
    MVaR = (numer / denom) * VaR
    RC = weights * MVaR

    # Convert the arrays to dataframes
    RC = pd.DataFrame(RC)
    MVaR = pd.DataFrame(MVaR)
    if name_list != None:
        MVaR.index = name_list
        RC.index = name_list

    return RC, MVaR


def marginal_VaR_from_total_port(portfolio, mkt_env, scenarios, alpha):
    '''
    marginal_VaR_from_sub_dists(combined_dist, weights, alpha)

    Functionality
    =============
    This calculates the risk contribution and marginal VaR at alpha percentile

    Parameters
    ==========
    combined_dist : numpy matrix
         P&L distribution of each instrument consisting of the total portfolio.
         The columns refer to the simulated scenario and the rows correspond
         to the sub portfolio
    weights : numpy array
         weights of each element in total portfolio to calculate marginal VaR
    alpha : double
         quantile used for the VaR calculation (between 0 and 1)

    Returns
    =======
    RC : dataframe
        the risk contribution of each element of the total portfolio
    MVaR : dataframe
        the marginal VaR of each element in the total portfolio
    '''

    N = len(scenarios)
    M = len(portfolio.positions.keys())
    port_currency = portfolio.get_currency()

    # Calculate the portfolio Value
    portfolio_val = portfolio.value_product(mkt_env)

    # Populate the current values of the assets and the asset name list
    old_vals = np.zeros(M)
    name_list = []
    idx = 0
    weights = np.zeros(M)
    for k, v in portfolio.positions.items():
        FX_rate = k.get_base_currency_conversion(mkt_env, port_currency)
        val = k.value_product(mkt_env)
        old_vals[idx] = val * v * FX_rate
        name_list.append(k.get_ID())
        idx += 1

    # Calculate the current weights of the assets
    weights = old_vals / portfolio_val

    # Populate a matrix with the distributions of the underlying assets
    asset_dist = np.zeros((M, N))
    row_idx = 0
    for ii in range(N):
        scenario = scenarios.iloc[ii]
        mkt_env_new = finScenarios.apply_mkt_scenario(mkt_env, scenario,
                                                      abs_flag=False)
        for k, v in portfolio.positions.items():
            old_price = old_vals[row_idx]

            new_FX_rate = k.get_base_currency_conversion(mkt_env_new,
                                                         port_currency)
            new_val = k.value_product(mkt_env_new)
            new_price = new_val * v * new_FX_rate

            asset_dist[row_idx][ii] = new_price - old_price
            row_idx += 1
        row_idx = 0

    # Calculate the correlation matrix of the assets
    Q = np.cov(asset_dist)

    # Determine the total portfolio distribtuin and calculate VaR
    total_dist = sum(asset_dist)
    VaR, _ = MarketVaR.calculate_VaR_from_PnL(total_dist, alpha)

    # Calculate the risk contribution and marginal VaR
    numer = np.dot(Q, weights)
    denom = np.dot(np.transpose(weights), numer)
    MVaR = (numer / denom) * VaR
    RC = weights * MVaR

    # Convert the arrays to dataframes
    RC = pd.DataFrame(RC)
    RC.index = name_list
    MVaR = pd.DataFrame(MVaR)
    MVaR.index = name_list

    return RC, MVaR
