###
# Basic functions for performing Value-At-Risk (VaR) calculations
###

import math
import matplotlib.pyplot as plt
import numpy as np
import ScenarioAnalysis as finScenarios


def generate_PnL_distribution(portfolio, scenarios, mkt_env, static=False):
    '''
        generate_PnL_distribution(portfolio, scenarios)

        Functionality
        =============
        This gives distribtuion of PnL given portfolio and scenarios

        Parameters
        ==========
        portfolio : portfolio object
        the portfolio to value
        scenarios : pandas matrix of doubles
        scenarios of forecasted risk factors. (Rows=Scenerios; Col=Factors)
        mkt_env : market_environment object
        a market environment object of current market data to apply the
        scenarios
        static : Bool
        a boolean stating whether the valuation is static or time-varying

        Returns
        =======
        dist : vector of doubles
        profit and loss from each scenario
        '''
    orig_port_val = portfolio.value_product(mkt_env)

    N = len(scenarios)
    PnL_dist = []
    for ii in range(N):
        scenario = scenarios.iloc[ii]
        mkt_env_new = finScenarios.apply_mkt_scenario(mkt_env, scenario,
                                                      abs_flag=False)
        PnL = portfolio.value_product(mkt_env_new) - orig_port_val
        PnL_dist.append(PnL)

    # Convert the P&L distribution into a numpy array
    PnL_dist = np.asarray(PnL_dist)

    return PnL_dist


def generate_mkt_env_distribution(scenarios, mkt_env):
    '''
        generate_mkt_env_distribution(scenarios, mkt_env)

        Functionality
        =============
        This concerts a set of scenarios into a dictionary of market environments
        with the sceneraios appied

        Parameters
        ==========
        scenarios : pandas matrix of doubles
        scenarios of forecasted risk factors. (Rows=Scenerios; Col=Factors)
        mkt_env : market_environment object
        a market environment object of current market data to apply the
        scenerios

        Returns
        =======
        mkt_env_dict  : dictionary
        dictionary of new market environments created from the scenarios
        '''

    N = len(scenarios)
    mkt_env_dict = {}

    for ii in range(N):
        scenario = scenarios.iloc[ii]
        mkt_env_new = finScenarios.apply_mkt_scenario(mkt_env, scenario,
                                                      abs_flag=False)
        name = 'Scenario ' + str(ii + 1)
        mkt_env_dict[name] = mkt_env_new

    return mkt_env_dict


def generate_PnL_distribution_from_mkt_envs(portfolio, mkt_env_dict, mkt_env,
                                            static=False):
    '''
        generate_PnL_distribution_from_mkt_envs(portfolio, mkt_env_dict, mkt_env,
        static=False)

        Functionality
        =============
        This gives distribtuion of PnL given portfolio and scenarios

        Parameters
        ==========
        portfolio : portfolio object
        the portfolio to value
        scenarios : pandas matrix of doubles
        scenarios of forecasted risk factors. (Rows=Scenerios; Col=Factors)
        mkt_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
        static : Bool
        a boolean stating whether the valuation is static or time-varying

        Returns
        =======
        dist : vector of doubles
        profit and loss from each scenario
        '''
    orig_port_val = portfolio.value_product(mkt_env)

    N = len(mkt_env_dict)
    PnL_dist = []
    for mkt_env_new in mkt_env_dict.values():
        PnL = portfolio.value_product(mkt_env_new) - orig_port_val
        PnL_dist.append(PnL)

    # Convert the P&L distribution into a numpy array
    PnL_dist = np.asarray(PnL_dist)

    return PnL_dist


def calculate_scenario_VaR(portfolio, mkt_env, scenarios, scenario_horizon,
                           VaR_horizon, alpha):
    '''
        calculateVaR(portfolio, scenarios, scenario_horizon, VaR_horizon,alpha)

        Functionality
        =============
        This calculates the Value-at-Risk (VaR) and Expected Shortfall
        (ES) of a portfolio at alpha percentile

        Parameters
        ==========
        portfolio : portfolio object
            the portfolio to value
        scenarios : pandas matrix of doubles
            scenarios of forecasted risk factors. (Rows=Scenerios; Col=Factors)
        scenario_horizon : int
            the time horizon that applies to the scenarios in days
        VaR_horizon : int
            the time horizon that applies to the VaR calculation in days
        alpha : double
            quantile used for the VaR calculation (between 0 and 1)

        Returns
        =======
        VaR : double
        the Value-At-Risk (VaR) of the portfolio
        ES : double
        the Expected Shortfall (ES) of the portfolio
        '''
    if scenario_horizon != VaR_horizon:
        scenarios = scenarios * np.sqrt(1.0 * VaR_horizon / scenario_horizon)

    portValues = generate_PnL_distribution(portfolio, scenarios, mkt_env)

    VaR = np.percentile(portValues, 100.0 * alpha)
    ES = np.mean(portValues[portValues < VaR])

    return VaR, ES


def calculate_VaR_from_PnL(PnL_dist, alpha):
    '''
        calculate_VaR_from_PnL(PnL_dist, alpha)

        Functionality
        =============
        This calculates the Value-at-Risk (VaR) and Expected Shortfall
        (ES) of a portfolio at alpha percentile from a distribtuion of the portfolio
        P&L

        Parameters
        ==========
        PnL_dist : array
        this is an array of portfolio profit and losses
        alpha : double
        quantile used for the VaR calculation (between 0 and 1)

        Returns
        =======
        VaR : double
        the Value-At-Risk (VaR) of the portfolio
        ES : double
        the Expected Shortfall (ES) of the portfolio
        '''

    VaR = np.percentile(PnL_dist, 100.0 * alpha)
    ES = np.mean(PnL_dist[PnL_dist < VaR])

    return VaR, ES


def backtest_VaR_from_historic(portfolio, mkt_env, VaR, num_days,
                               end_date=None):
    '''
        backtest_VaR_from_historic(portfolio, mkt_env, VaR, num_days)

        Functionality
        =============
        Backtest the calculated VaR from the historic market repository and
        output the number of breachs

        Parameters
        ==========
        portfolio : portfolio object
            the portfolio to value
        mkt_env : market_environment object
            a market environment object of current market data to apply the
        scenerios
        VaR : float
            The VaR number to backtest against
        num_days : int
            the number of days to use in the backtesting period

        Returns
        =======
        breachs : int
            the Value-At-Risk (VaR) of the portfolio
        '''

    num_days = int(num_days)

    # Generate a historic PnL distribution
    historic_scenarios = finScenarios.historic_specified_amt(num_days, end_date)
    PnL_dist = generate_PnL_distribution(portfolio, historic_scenarios, mkt_env)

    # Count the number of breachs
    breachs = 0
    for ii in range(num_days):
        if PnL_dist[ii] < VaR:
            breachs += 1

    return breachs


def plot_market_VaR_dist(PnL_dist, portfolio, mkt_env, scenario_horizon,
                         VaR_horizon, alpha, num_bins, port_name=None):
    '''
        calculateVaR(portfolio, scenarios, scenario_horizon, VaR_horizon,alpha)

        Functionality
        =============
        This calculates the Value-at-Risk (VaR) and Expected Shortfall
        (ES) of a portfolio at alpha percentile

        Parameters
        ==========
        PnL_dist : numpy array
        The Profit and Loss Distribtuion of the Portfolio
        portfolio : portfolio object
        the portfolio of the PnL distribution
        mkt_env : market_environment object
        a market environment object of current market data to value the portfolio
        scenario_horizon : int
        the time horizon that applies to the scenarios in days
        VaR_horizon : int
        the time horizon that applies to the VaR calculation in days
        alpha : double
        quantile used for the VaR calculation (between 0 and 1)
        num_bins : int
        the number of bins used in the distribution plot

        Returns
        =======
        fig_out : double
        the Value-At-Risk (VaR) of the portfolio
        '''

    # Create the strings for the plots
    N = len(PnL_dist)
    VaR_lbl_str = str(100 * (1 - alpha)) + '% VaR'
    ES_lbl_str = str(100 * (1 - alpha)) + '% ES'
    if port_name == None:
        title_str = 'Distribution of ' + str(
            VaR_horizon) + '-day Portfolio Returns'
    else:
        title_str = 'Distribution of ' + str(
            VaR_horizon) + '-day ' + port_name + ' Portfolio Returns'

    # Calculate the Profit and Loss Distribtuion in percentages
    port_value = portfolio.value_product(mkt_env)
    PnL_perc = PnL_dist / port_value
    PnL_perc = math.sqrt(1.0 * VaR_horizon / scenario_horizon) * PnL_perc
    VaR_perc, ES_perc = calculate_VaR_from_PnL(PnL_perc, alpha)

    # Total Portfolio plot
    fig, ax = plt.subplots()
    freq = plt.hist(PnL_perc, bins=num_bins)
    freq_max = freq[0].max()
    plt.xlabel('Portfolio Returns (%)');
    plt.ylabel('Frequency');
    plt.title(title_str);
    VaR_line, = plt.plot([VaR_perc, VaR_perc], [0, freq_max], color='r',
                         label=VaR_lbl_str);
    ES_line, = plt.plot([ES_perc, ES_perc], [0, freq_max], color='k',
                        label=ES_lbl_str);
    plt.legend(handles=[VaR_line, ES_line])
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:2.1f}%'.format(x * 100) for x in vals])
    fig_out = plt.grid(True);

    return fig_out
