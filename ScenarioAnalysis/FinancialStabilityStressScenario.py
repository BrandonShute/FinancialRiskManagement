# Generate a FS Vulnerability Stress Scenario

from ScenarioGeneration import *


def generate_vulnerability_stress_scenario(mkt_env):
    # step 1: shift US FX by -20% (relative)
    shift_factor_spec = 'FXRates-USDCAD'
    bps = -0.2
    mkt_env_fs1 = shifting_constant(mkt_env, shift_factor_spec, bps,
                                    abs_flag=False)
    # step 2: shift global equity by -5% (relative)
    shift_factor_spec = 'MarketPrice'
    bps = -0.05
    mkt_env_fs2 = shifting_constant(mkt_env_fs1, shift_factor_spec, bps,
                                    abs_flag=False)
    # step 3: shift global credit spread by 0.0085 (absolute)
    shift_factor_spec = 'CreditSpreads-Ratings'
    bps = 0.0085
    mkt_env_new = shifting_matrix(mkt_env_fs2, shift_factor_spec, bps,
                                  abs_flag=True)
    return mkt_env_new
