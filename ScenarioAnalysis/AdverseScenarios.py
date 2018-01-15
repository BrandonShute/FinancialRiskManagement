import ScenarioGeneration as gs


def generate_adverse_scenario(mkt_env):
    # step 1: shift global equity by -50% (relative)
    shift_factor_spec = 'MarketPrice'
    bps = -0.5
    mkt_env_as1 = gs.shifting_constant(mkt_env, shift_factor_spec, bps, abs_flag=False)
    # step 2: shift global credit spread by 0.0075 (absolute)
    shift_factor_spec = 'CreditSpreads-Ratings'
    bps = 0.0075
    mkt_env_as2 = gs.shifting_matrix(mkt_env_as1, shift_factor_spec, bps, abs_flag=True)
    # step 3: shift US risk free rate by 0.1% (absolute)
    shift_factor_spec = 'RiskFree-Gov-USD'
    bps = 0.001
    mkt_env_new = gs.shifting_curve(mkt_env_as2, shift_factor_spec, bps, abs_flag=True)
    return mkt_env_new
