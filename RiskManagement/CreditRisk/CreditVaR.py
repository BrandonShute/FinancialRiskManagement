###
# Basic functions for performing Credit Value-At-Risk (VaR) calculations
###

import copy
import scipy
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import FinancialProducts as finProds
import MarketRisk as mktRisk


def generate_credit_VaR_distrubtion(portfolio, mkt_env, num_sims, corrC):
    currency = portfolio.get_currency()
    credit_port = finProds.Portfolio({}, currency)
    for k, v in (portfolio.positions).items():
        x1 = type(k)
        if str(
                x1) == "<class 'credit_default_swap.credit_default_swap'>" or str(
                x1) == "<class 'fixed_rate_bond.fixed_rate_bond'>" or str(
            x1) == "<class 'callable_bond.callable_bond'>" or str(
            x1) == "<class 'floating_rate_bond.floating_rate_bond'>":
            credit_port.add_position(k, v)

    nCredits = len(credit_port.positions)
    tMatrix = mkt_env.get_matrix('CreditTransitionMatrix')

    mu = np.zeros(nCredits)
    std = np.eye(nCredits)
    corr = corrC * np.ones((nCredits, nCredits)) + (1 - corrC) * std
    cov = np.dot(np.dot(std, corr), std)

    tMatrix_transpose = np.transpose(tMatrix)

    current_AAA = tMatrix_transpose['AAA']
    current_AA = tMatrix_transpose['AA']
    current_A = tMatrix_transpose['A']
    current_BBB = tMatrix_transpose['BBB']
    current_BB = tMatrix_transpose['BB']
    current_B = tMatrix_transpose['B']
    current_CCC = tMatrix_transpose['CCC/C']
    current_NR = tMatrix_transpose['CCC/C']  # set as CCC for conservatism

    thresholds_AAA = scipy.stats.norm.ppf(current_AAA)
    thresholds_AA = scipy.stats.norm.ppf(current_AA)
    thresholds_A = scipy.stats.norm.ppf(current_A)
    thresholds_BBB = scipy.stats.norm.ppf(current_BBB)
    thresholds_BB = scipy.stats.norm.ppf(current_BB)
    thresholds_B = scipy.stats.norm.ppf(current_B)
    thresholds_CCC = scipy.stats.norm.ppf(current_CCC)
    thresholds_NR = scipy.stats.norm.ppf(current_NR)

    ratings = list(tMatrix)
    df_thresholds_AAA = pd.DataFrame([thresholds_AAA], columns=ratings)
    df_thresholds_AA = pd.DataFrame([thresholds_AA], columns=ratings)
    df_thresholds_A = pd.DataFrame([thresholds_A], columns=ratings)
    df_thresholds_BBB = pd.DataFrame([thresholds_BBB], columns=ratings)
    df_thresholds_BB = pd.DataFrame([thresholds_BB], columns=ratings)
    df_thresholds_B = pd.DataFrame([thresholds_B], columns=ratings)
    df_thresholds_CCC = pd.DataFrame([thresholds_CCC], columns=ratings)
    df_thresholds_NR = pd.DataFrame([thresholds_NR], columns=ratings)

    # Sort columns by value
    new_col_AAA = df_thresholds_AAA.columns[
        df_thresholds_AAA.iloc[df_thresholds_AAA.last_valid_index()].argsort()]
    df_thresholds_AAA_sorted = df_thresholds_AAA[new_col_AAA]

    new_col_AA = df_thresholds_AA.columns[
        df_thresholds_AA.iloc[df_thresholds_AA.last_valid_index()].argsort()]
    df_thresholds_AA_sorted = df_thresholds_AA[new_col_AA]

    new_col_A = df_thresholds_A.columns[
        df_thresholds_A.iloc[df_thresholds_A.last_valid_index()].argsort()]
    df_thresholds_A_sorted = df_thresholds_A[new_col_A]

    new_col_BBB = df_thresholds_BBB.columns[
        df_thresholds_BBB.iloc[df_thresholds_BBB.last_valid_index()].argsort()]
    df_thresholds_BBB_sorted = df_thresholds_BBB[new_col_BBB]

    new_col_BB = df_thresholds_BB.columns[
        df_thresholds_BB.iloc[df_thresholds_BB.last_valid_index()].argsort()]
    df_thresholds_BB_sorted = df_thresholds_BB[new_col_BB]

    new_col_B = df_thresholds_B.columns[
        df_thresholds_B.iloc[df_thresholds_B.last_valid_index()].argsort()]
    df_thresholds_B_sorted = df_thresholds_B[new_col_B]

    new_col_CCC = df_thresholds_CCC.columns[
        df_thresholds_CCC.iloc[df_thresholds_CCC.last_valid_index()].argsort()]
    df_thresholds_CCC_sorted = df_thresholds_CCC[new_col_CCC]

    new_col_NR = df_thresholds_NR.columns[
        df_thresholds_NR.iloc[df_thresholds_NR.last_valid_index()].argsort()]
    df_thresholds_NR_sorted = df_thresholds_NR[new_col_NR]

    dict_df_thresholds_sorted = {'AAA': df_thresholds_AAA_sorted,
                                 'AA': df_thresholds_AA_sorted,
                                 'A': df_thresholds_A_sorted,
                                 'BBB': df_thresholds_BBB_sorted,
                                 'BB': df_thresholds_BB_sorted,
                                 'B': df_thresholds_B_sorted,
                                 'CCC/C': df_thresholds_CCC_sorted,
                                 'NR': df_thresholds_NR_sorted}

    # Do Simulation and Change Rating Accordingly
    scenarios = np.random.multivariate_normal(mu, cov, num_sims)
    migration_loss_dist = []
    default_loss_dist = []
    tot_loss_dist = []
    for s in range(num_sims):
        loss_due_to_migration = 0
        ii = 0
        rv = scenarios[s]
        new_positions = copy.deepcopy(credit_port.positions)
        credit_port_new = finProds.Portfolio(new_positions, currency)
        for k, v in credit_port_new.positions.items():
            old_value = k.value_product(mkt_env)
            FX_rate = k.get_base_currency_conversion(mkt_env, currency)
            x1 = type(k)

            if str(x1) == "<class 'fixed_rate_bond.fixed_rate_bond'>" or str(
                    x1) == "<class 'callable_bond.callable_bond'>" or str(
                x1) == "<class 'floating_rate_bond.floating_rate_bond'>":
                rating = k.get_rating('S&P')
                if type(rating) == dict:
                    threshold = dict_df_thresholds_sorted[rating['S&P']]
                else:
                    threshold = dict_df_thresholds_sorted[rating]
                threshold_array = np.array(threshold)
                index_1 = len(threshold_array[0])
                threshold_ratings = list(threshold)
                z_score = rv[ii]
                new_rating = threshold_ratings[-1]
                for jj in range(index_1 - 1, -1,
                                -1):  # need reverse loop to keep updating rating until it doesn't change
                    if z_score < threshold_array[0][jj]:
                        new_rating = threshold_ratings[jj]
                # Set new rating
                k.set_rating('S&P', new_rating)

                if new_rating != 'D':
                    new_value = k.value_product(mkt_env)
                    loss_value = (old_value - new_value) * v * FX_rate
                    loss_due_to_migration = loss_due_to_migration + loss_value

            if str(x1) == "<class 'credit_default_swap.credit_default_swap'>":
                rating = k.get_rating('S&P')
                if type(rating) == dict:
                    threshold = dict_df_thresholds_sorted[rating['S&P']]
                else:
                    threshold = dict_df_thresholds_sorted[rating]
                threshold_array = np.array(threshold)
                index_1 = len(threshold_array[0])
                threshold_ratings = list(threshold)
                z_score = rv[ii]
                new_rating = threshold_ratings[-1]
                for jj in range(index_1 - 1, -1,
                                -1):  # need reverse loop to keep updating rating until it doesn't change
                    if z_score < threshold_array[0][jj]:
                        new_rating = threshold_ratings[jj]
                # Set new rating
                k.set_rating('S&P', new_rating)
                if new_rating != 'D':
                    new_value = k.value_product(mkt_env)
                    loss_value = (old_value - new_value) * v * FX_rate
                    loss_due_to_migration = loss_due_to_migration + loss_value

            ii = ii + 1

        # Split new portfolio into defaults and non-defaults
        non_default_port = finProds.Portfolio({}, currency)
        default_port = finProds.Portfolio({}, currency)
        for k, v in (credit_port_new.positions).items():
            x1 = type(k)
            if str(x1) == "<class 'fixed_rate_bond.fixed_rate_bond'>" or str(
                    x1) == "<class 'callable_bond.callable_bond'>" or str(
                x1) == "<class 'floating_rate_bond.floating_rate_bond'>":
                rating = k.get_rating('S&P')
                if rating == 'D':
                    default_port.add_position(k, v)
                else:
                    non_default_port.add_position(k, v)
            if str(x1) == "<class 'credit_default_swap.credit_default_swap'>":
                rating = k.get_rating('S&P')
                if rating == 'D':
                    default_port.add_position(k, v)
                else:
                    non_default_port.add_position(k, v)

        # Value Defaults
        default_port_loss_value = 0
        for k, v in (default_port.positions).items():
            x1 = type(k)
            FX_rate = k.get_base_currency_conversion(mkt_env, currency)
            if str(x1) == "<class 'fixed_rate_bond.fixed_rate_bond'>" or str(
                    x1) == "<class 'callable_bond.callable_bond'>" or str(
                x1) == "<class 'floating_rate_bond.floating_rate_bond'>":
                face_value = k.get_face_value()

                recovery_rate_list = mkt_env.get_list('RecoveryRates')
                tier = k.get_tier()
                try:
                    recovery_rate = recovery_rate_list.iloc[0][tier]
                # If the tier is not contained in the list. Be conservative and assume
                # the worst
                except:
                    recovery_rate = recovery_rate_list.iloc[0][-1]

                bond_loss = face_value * (
                        1.0 - recovery_rate) * v * FX_rate  # Need to multiply by position "v"

                default_port_loss_value = default_port_loss_value + bond_loss

            if str(x1) == "<class 'credit_default_swap.credit_default_swap'>":
                notional = k.get_notional()
                CDS_loss = -1.0 * notional * v * FX_rate  # Need to multiply by position "v". Buy position is positive, so that means you get large positive notional.
                # i.e. loss is negative since you experience a gain
                default_port_loss_value = default_port_loss_value + CDS_loss

        total__loss = loss_due_to_migration + default_port_loss_value
        migration_loss_dist.append(loss_due_to_migration)
        default_loss_dist.append(default_port_loss_value)
        tot_loss_dist.append(total__loss)

    # Convert the P&L distribution into a numpy array
    migration_loss_dist = np.asarray(migration_loss_dist)
    default_loss_dist = np.asarray(default_loss_dist)
    tot_loss_dist = np.asarray(tot_loss_dist)

    # Convert the loss distribution into a P&L Distribution
    tot_PnL_dist = -1.0 * tot_loss_dist
    migration_PnL_dist = -1.0 * migration_loss_dist
    default_PnL_dist = -1.0 * default_loss_dist

    return tot_PnL_dist, migration_PnL_dist, default_PnL_dist


def plot_credit_VaR_dist(PnL_dist, portfolio, mkt_env, scenario_horizon,
                         VaR_horizon, alpha, num_bins, port_name=None):
    '''
    plot_credit_VaR_dist(PnL_dist, portfolio, mkt_env, scenario_horizon,
                         VaR_horizon, alpha, num_bins, port_name=None)

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
        the credit Value-At-Risk (VaR) of the portfolio
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
    VaR_perc, ES_perc = mktRisk.calculate_VaR_from_PnL(PnL_perc, alpha)

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
