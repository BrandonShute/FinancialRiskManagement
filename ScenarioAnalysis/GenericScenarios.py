###
# Class of functions used to apply shocks to risk factors, calculate
# sensitivities, and scenario analysis
###

from MarketData import MarketEnvironment


def apply_mkt_shock(mkt_env, strspec, change, abs_flag=True):
    '''
    apply_mkt_shock(mkt_env, strspec, change, abs_flag=True)

    Functionality
    =============
    This gives distribution of PnL given portfolio and scenarios

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    strspec : string input
         input should be consistent with format in market data repository
         e.g. "Curves-RiskFree-CDOR-CAD-0.25"
    change : double
         change that is going to be applied to the specific piece of a parameter
         e.g. RiskFree rate
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relitive chnage (multiply by rate)

    Returns
    =======
    a new market environment with the change applied
    '''

    val_date = mkt_env.get_val_date()
    mkt_env_new = MarketEnvironment('Output_Environment', val_date)
    mkt_env_new.initialize_from_env(mkt_env)

    ss = strspec.split('-')
    stype = ss[0]
    skey = ''

    if stype == 'Curves':
        for s in ss[1:-1]:
            skey += s + '-'
        skey = skey[:-1]
        srow = ss[-1]
        curve = mkt_env_new.get_curve(skey)
        val = (curve.iloc[0]).loc[srow]
        if abs_flag:
            new_val = val + change
        else:
            new_val = val * (1 + change)
        new_curve = curve.copy()
        (new_curve.iloc[0]).loc[srow] = new_val
        mkt_env_new.add_curve(skey, new_curve)

    elif stype == 'Lists':
        for s in ss[1:-1]:
            skey += s + '-'
        skey = skey[:-1]
        srow = ss[-1]
        slist = mkt_env_new.get_list(skey)
        val = (slist.iloc[0]).loc[srow]
        if abs_flag:
            new_val = val + change
        else:
            new_val = val * (1 + change)
        new_list = slist.copy()
        (new_list.iloc[0]).loc[srow] = new_val
        mkt_env_new.add_list(skey, new_list)

    elif stype == 'Surfaces':
        for s in ss[1:-2]:
            skey += s + '-'
        skey = skey[:-1]
        scol = ss[-1]
        srow = ss[-2]
        surf = mkt_env_new.get_surface(skey)
        val = (surf.loc[srow]).loc[scol]
        if abs_flag:
            new_val = val + change
        else:
            new_val = val * (1 + change)
        new_surf = surf.copy()
        (new_surf.loc[srow]).loc[scol] = new_val
        mkt_env_new.add_surface(skey, new_surf)

    elif stype == 'Matrices':
        for s in ss[1:-2]:
            skey += s + '-'
        skey = skey[:-1]
        scol = ss[-1]
        srow = ss[-2]
        mat = mkt_env_new.get_matrix(skey)
        val = (mat.loc[srow]).loc[scol]
        if abs_flag:
            new_val = val + change
        else:
            new_val = val * (1 + change)
        new_mat = mat.copy()
        (new_mat.loc[srow]).loc[scol] = new_val
        mkt_env_new.add_matrix(skey, new_mat)

    else:  # constants
        for s in ss[1:]:
            skey += s + '-'
        skey = skey[:-1]
        val = mkt_env_new.get_constant(skey)
        if abs_flag:
            new_val = val + change
        else:
            new_val = val * (1 + change)
        mkt_env_new.add_constant(skey, new_val)

    return mkt_env_new


def apply_mkt_scenario(mkt_env, scenario, abs_flag=True):
    '''
    apply_mkt_scenario(mkt_env, scenario)

    Functionality
    =============
    This gives distribtuion of PnL given portfolio and scenarios

    Parameters
    ==========
    market_env : market_environment object
        a market environment object of current market data to apply the
        scenerios
    scenario : dataframe
         a dataframe of relative chnages to risk factors
    abs_flag : Boolean
        whether the change is an absolute change (add to current value) or a
        relitive chnage (multiply by rate)
    Returns
    =======
    a new market environment with the scenario applied
    '''
    val_date = mkt_env.get_val_date()
    mkt_env_new = MarketEnvironment('Output_Environment', val_date)
    mkt_env_new.initialize_from_env(mkt_env)

    for name, change in scenario.items():
        # for example, strspec = Curves-RiskFree-CDOR-CAD-0.25
        ss = name.split('-')
        stype = ss[0]
        skey = ''

        if stype == 'Curves':
            for s in ss[1:-1]:
                skey += s + '-'
            skey = skey[:-1]
            srow = ss[-1]
            curve = mkt_env_new.get_curve(skey)
            val = (curve.iloc[0]).loc[srow]
            if abs_flag:
                new_val = val + change
            else:
                new_val = val * (1 + change)
            new_curve = curve.copy()
            (new_curve.iloc[0]).loc[srow] = new_val
            mkt_env_new.add_curve(skey, new_curve)

        elif stype == 'Lists':
            for s in ss[1:-1]:
                skey += s + '-'
            skey = skey[:-1]
            srow = ss[-1]
            slist = mkt_env_new.get_list(skey)
            val = (slist.iloc[0]).loc[srow]
            if abs_flag:
                new_val = val + change
            else:
                new_val = val * (1 + change)
            new_list = slist.copy()
            (new_list.iloc[0]).loc[srow] = new_val
            mkt_env_new.add_list(skey, new_list)

        elif stype == 'Surfaces':
            for s in ss[1:-2]:
                skey += s + '-'
            skey = skey[:-1]
            scol = ss[-1]
            srow = ss[-2]
            surf = mkt_env_new.get_surface(skey)
            val = (surf.loc[srow]).loc[scol]
            if abs_flag:
                new_val = val + change
            else:
                new_val = val * (1 + change)
            new_surf = surf.copy()
            (new_surf.loc[srow]).loc[scol] = new_val
            mkt_env_new.add_surface(skey, new_surf)

        elif stype == 'Matrices':
            for s in ss[1:-2]:
                skey += s + '-'
            skey = skey[:-1]
            scol = ss[-1]
            srow = ss[-2]
            mat = mkt_env_new.get_matrix(skey)
            val = (mat.loc[srow]).loc[scol]
            if abs_flag:
                new_val = val + change
            else:
                new_val = val * (1 + change)
            new_mat = mat.copy()
            (new_mat.loc[srow]).loc[scol] = new_val
            mkt_env_new.add_matrix(skey, new_mat)

        else:  # constants
            for s in ss[1:]:
                skey += s + '-'
            skey = skey[:-1]
            val = mkt_env_new.get_constant(skey)
            if abs_flag:
                new_val = val + change
            else:
                new_val = val * (1 + change)
            mkt_env_new.add_constant(skey, new_val)

    return mkt_env_new
