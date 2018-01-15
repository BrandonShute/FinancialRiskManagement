# Calculating DV01

from ScenarioGeneration import *
from GenericScenarios import *


def calculate_portfolio_sensitivities(mkt_env, portfolio):
    factor_vol = mkt_env.get_list('RiskFactorVolatilities')
    factor_names = list(factor_vol)
    orig_port_val = portfolio.value_product(mkt_env)
    sensitivities_dict = {}

    for factor in factor_names:
        ff = factor.split('-')
        ftype = ff[0]
        fsubtype = ff[1]

        if ftype == 'Curves':
            change = 0.0001

        elif ftype == 'Lists':
            change = 0.0001

        elif ftype == 'Matrices':
            change = 0.0001

        else:  # constants
            if fsubtype == 'FXRates':
                change = 0.0001
            elif fsubtype == 'MarketPrice':
                change = 0.01

        mkt_env_new = apply_mkt_shock(mkt_env, factor, change)
        sensitivity = portfolio.value_product(mkt_env_new) - orig_port_val
        sensitivities_dict[factor] = sensitivity

    return sensitivities_dict


def risk_factor_positive_bump(mkt_env):
    # shift all risk free rates by 1bps 0.0001 (absolute)
    shift_factor_spec = 'RiskFree-Govz'
    bps = 0.0001
    mkt_env_new = shifting_curve(mkt_env, shift_factor_spec, bps, abs_flag=True)
    return mkt_env_new


def risk_factor_negative_bump(mkt_env):
    # shift all risk free rates by 1bps -0.0001 (absolute)
    shift_factor_spec = 'RiskFree-Gov'
    bps = -0.0001
    mkt_env_new = shifting_curve(mkt_env, shift_factor_spec, bps, abs_flag=True)
    return mkt_env_new


def calculate_DV01_Convexity(mkt_env, FI_port):
    mkt_env_positive_change = risk_factor_positive_bump(mkt_env)
    mkt_env_negative_change = risk_factor_negative_bump(mkt_env)
    original_value = FI_port.value_product(mkt_env)
    positive_change_value = FI_port.value_product(mkt_env_positive_change)
    negitive_change_value = FI_port.value_product(mkt_env_negative_change)

    positive_scenario_change = positive_change_value - original_value
    negative_scenario_chang = original_value - negitive_change_value

    DV01 = (abs(positive_scenario_change) + abs(negative_scenario_chang)) / 2

    convexity = (positive_change_value - 2 * original_value + negitive_change_value) / (0.0001 ** 2)
    return DV01, convexity
