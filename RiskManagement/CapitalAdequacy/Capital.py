import pandas as pd
import FinancialProducts as finProds


def calculate_market_risk_capital(tot_mkt_VaR, tot_SVaR, tot_cred_VaR,
                                  adjustment_factor):
    MarketRiskCapital = -(
            (tot_mkt_VaR + tot_SVaR) * adjustment_factor + tot_cred_VaR)
    return MarketRiskCapital


def calculate_counterparty_credit_risk_capital(tot_port, mkt_env):
    defualt_rating_provider = 'S&P'

    rating_names = ['AAA', 'AAu', 'AA', 'A', 'BBB+', 'BBB', 'BB+', 'BB', 'B',
                    'NR', 'N.A.']

    gov_risk_weighting = [0, 0, 0.2, 0.2, 0.5, 0.5, 1, 1, 1, 1, 1]
    corporation_risk_weighting = [0.2, 0.2, 0.2, 0.5, 1, 1, 1, 1, 1.5, 1, 1]

    gov_risk_weighting_df = pd.DataFrame([gov_risk_weighting],
                                         columns=rating_names)
    corporation_risk_weighting_df = pd.DataFrame([corporation_risk_weighting],
                                                 columns=rating_names)

    counterparty_credit_risk_capital = 0

    tot_port.remove_portfolio_nesting()

    RWA = {}

    for product, units in tot_port.positions.items():
        RWA = 0.0
        add_on_factor = 0.0

        if isinstance(product, finProds.Option):
            add_on_factor = 0.06
            rating = product.get_underlying().get_rating(
                defualt_rating_provider)
            industry = product.get_underlying().get_industry()
        if isinstance(product, finProds.CreditDefaultSwap):
            rating = product.get_rating(defualt_rating_provider)
            industry = product.get_industry()
            # add on factor for CDS protection buyer (0 for selling
            if units > 0:
                add_on_factor = 0.075

        mtm = max(product.value_product(mkt_env), 0)

        if industry == 'Government':
            RWA[product] = units * gov_risk_weighting_df[rating][0] * mtm * (
                    1 + add_on_factor)
        else:
            RWA[product] = units * corporation_risk_weighting_df[rating][
                0] * mtm * (1 + add_on_factor)

        counterparty_credit_risk_capital += RWA * 0.08

    return RWA, counterparty_credit_risk_capital


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
