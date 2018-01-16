import pandas as pd
import numpy as np
import GenericScenarios as gs


def shifting_market_data(mkt_env, market_data_type, shift_factor_spec, bps,
                         abs_flag):
    '''
    shifting_constant(mkt_env, shift_factor_spec, bps, abs_flag=False)

    Functionality
    =============
    This function generate a scenario by change a specific constant and output a
    new market environment

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenarios
    market_data_type : String
        the market data type (Constants, Lists, Curves, Matrices, Surfaces)
    shift_factor_spec : string input
         input should be consistent with format in market data repository
         e.g. 'FXRates-USDCAD'
    bps : double
         change that is going to be applied to the specific constant
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relative change (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''
    factor_vol = mkt_env.get_list('RiskFactorVolatilities')
    factor_names = list(factor_vol)
    shift_factor = market_data_type + '-' + shift_factor_spec
    shift_list = [x for x in factor_names if shift_factor in x]
    shift = bps * np.ones((1, len(shift_list)))
    scenario = pd.DataFrame(shift, columns=shift_list)
    scenario = scenario.iloc[0]
    mkt_env_new = gs.apply_mkt_scenario(mkt_env, scenario, abs_flag)

    return mkt_env_new


def shifting_curve(mkt_env, shift_factor_spec, bps, abs_flag):
    '''
    shifting_curve(mkt_env, shift_factor_spec, bps, abs_flag=True)

    Functionality
    =============
    This function generate a scenario by change a specific curve and output a
    new market environment

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    shift_factor_spec : string input
         input should be consistent with format in market data repository
         e.g. 'RiskFree-LIBOR-USD'
    bps : double
         change that is going to be applied to the specific curve
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relitive change (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''
    return shifting_market_data(mkt_env, 'Curves', shift_factor_spec, bps,
                                abs_flag)


def shifting_list(mkt_env, shift_factor_spec, bps, abs_flag):
    '''
    shifting_list(mkt_env, shift_factor_spec, bps, abs_flag=True)

    Functionality
    =============
    This function generate a scenario by change a specific list and output a
    new market environment

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    shift_factor_spec : string input
         input should be consistent with format in market data repository
         e.g. 'RiskFree-LIBOR-USD'
    bps : double
         change that is going to be applied to the specific curve
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relitive change (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''
    return shifting_market_data(mkt_env, 'Lists', shift_factor_spec, bps,
                                abs_flag)


def shifting_surface(mkt_env, shift_factor_spec, bps, abs_flag):
    '''
    shifting_surface(mkt_env, shift_factor_spec, bps, abs_flag=True)

    Functionality
    =============
    This function generate a scenario by change a specific surface and output a
    new market environment

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    shift_factor_spec : string input
         input should be consistent with format in market data repository
         e.g. 'RiskFree-LIBOR-USD'
    bps : double
         change that is going to be applied to the specific surface
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relitive change (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''
    return shifting_market_data(mkt_env, 'Surfaces', shift_factor_spec, bps,
                                abs_flag)


def shifting_matrix(mkt_env, shift_factor_spec, bps, abs_flag):
    '''
    shifting_matrix(mkt_env, shift_factor_spec, bps, abs_flag=True)

    Functionality
    =============
    This function generate a scenario by change a specific matrix and output a
    new market environment

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    shift_factor_spec : string input
         input should be consistent with format in market data repository
         e.g. 'CreditSpreads-Ratings-EUR-A'
    bps : double
         change that is going to be applied to the specific matrix
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relitive change (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''
    return shifting_market_data(mkt_env, 'Matrices', shift_factor_spec, bps,
                                abs_flag)


def shifting_constant(mkt_env, shift_factor_spec, bps, abs_flag):
    '''
    shifting_constant(mkt_env, shift_factor_spec, bps, abs_flag=False)

    Functionality
    =============
    This function generate a scenario by change a specific constant and output a
    new market environment

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    shift_factor_spec : string input
         input should be consistent with format in market data repository
         e.g. 'FXRates-USDCAD'
    bps : double
         change that is going to be applied to the specific constant
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relative change (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''
    return shifting_market_data(mkt_env, 'Constants', shift_factor_spec, bps,
                                abs_flag)
