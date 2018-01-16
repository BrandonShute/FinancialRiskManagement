import pandas as pd
import FinancialProducts as finProds


def calculate_market_risk_capital(tot_mkt_VaR, tot_SVaR, tot_cred_VaR,
                                  adjustment_factor):
    MarketRiskCapital = -(
            (tot_mkt_VaR + tot_SVaR) * adjustment_factor + tot_cred_VaR)
    return MarketRiskCapital


def calculate_counterparty_credit_risk_capital(tot_port, mkt_env):
    RWValuesGov = [0, 0, 0.2, 0.2, 0.5, 0.5, 1, 1, 1, 1, 1]
    RWValuesCorp = [0.2, 0.2, 0.2, 0.5, 1, 1, 1, 1, 1.5, 1, 1]
    RatingName = ['AAA', 'AAu', 'AA', 'A', 'BBB+', 'BBB', 'BB+', 'BB', 'B',
                  'NR', 'N.A.']
    RWGov = pd.DataFrame([RWValuesGov], columns=RatingName)
    RWCorp = pd.DataFrame([RWValuesCorp], columns=RatingName)

    counterparty_credit_risk_capital__s_a = 0

    tot_port.remove_portfolio_nesting()

    RWA = {}

    for k, v in tot_port.positions.items():
        RWA = 0
        if isinstance(k, finProds.Option) or isinstance(k,
                                                        finProds.CreditDefaultSwap):
            add_on_factor = 0
            if isinstance(k, finProds.Option):
                add_on_factor = 0.06
                rating = k.get_underlying().get_rating('S&P')
                industry = k.get_underlying().get_industry()
            if isinstance(k, finProds.CreditDefaultSwap):
                rating = k.get_rating('S&P')
                industry = k.get_industry()
                if v > 0:
                    add_on_factor = 0.075  # add on factor for CDS protection buyer
            mtm = max(k.value_product(mkt_env), 0)
            if industry == 'Government':
                RWA[k] = v * RWGov[rating][0] * mtm * (1 + add_on_factor)
            else:
                RWA[k] = v * RWCorp[rating][0] * mtm * (1 + add_on_factor)
        counterparty_credit_risk_capital__s_a += RWA * 0.08

    return RWA, counterparty_credit_risk_capital__s_a


def calculate_regulatory_capital(market_risk_capital,
                                 counterparty_credit_risk_capital):
    RegulatoryCapital = market_risk_capital + counterparty_credit_risk_capital

    return RegulatoryCapital


def calculate_capital_factor(breaches):
    min_breach = 5.0
    max_breach = 9.0
    min_score = 3.0
    max_score = 4.0

    if breaches <= min_breach:
        factor = min_score
    elif breaches > max_breach:
        factor = max_score
    else:
        factor = min_score + (breaches - min_breach) / (max_breach - min_breach)

    return factor
