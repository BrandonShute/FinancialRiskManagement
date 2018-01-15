#
# Driver Script for Report Generation
#


import math
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Database as finDB
import FinancialProducts as finProds
import FinancialModels as finModels
import ScenarioAnalysis as finScenarios
import RiskManagement as finRisk

# Specify the valuation date and currency of the portfolio
val_date = dt.datetime(2017, 6, 1)
currency = 'CAD'

# Specify the parameters for market VaR
num_sims_mkt = 10000
sim_delta_t = 1 / 252.0
alpha_mkt = 0.01
num_bins = 20
scenario_horizon_mkt = sim_delta_t * 252
VaR_horizon_mkt = 10

# Specify the parameters for credit VaR
rho = 0.2
stressed_rho = 0.9
num_sims_crd = 10000
alpha_crd = 0.001
scenario_horizon_crd = 252.0
VaR_horizon_crd = 252.0

# Set the names of the sub-portfolios
names = ['Equity Portfolio', 'Fixed Income Portfolio', 'Equity Option Portfolio', 'CDS Portfolio']
currency_names = ['CAD', 'USD', 'EUR']

# -----------------------------------------------------------------------------
# Populate the market environment and import the portfolio
# -----------------------------------------------------------------------------
print('Populating Market Environment..')
mkt_env = finDB.populate_mkt_env_from_repository(val_date)
print('Populating Portfolio Object..')
tot_port = finDB.populate_portfolio_from_repository(currency)

# Specify the correlation matrix and volatilities of the risk factors
corr_mat = mkt_env.get_matrix('RiskFactorCorrelationMatrix')
factor_vol = mkt_env.get_list('RiskFactorVolatilities')

# -----------------------------------------------------------------------------
# Breakdown the portfolio into various sub-portfolios
# -----------------------------------------------------------------------------
print('Decomposing Portfolio into Sub-portfolios..')

# Long and Short Total portfolios
tot_port_long = finProds.finProds.Portfolio({}, currency)
tot_port_short = finProds.finProds.Portfolio({}, currency)

# Total Asset Class Portfolios
FI_port = finProds.finProds.Portfolio({}, currency)
equity_port = finProds.finProds.Portfolio({}, currency)
eo_port = finProds.finProds.Portfolio({}, currency)
CDS_port = finProds.finProds.Portfolio({}, currency)

# Long Asset Class Portfolios
FI_port_long = finProds.Portfolio({}, currency)
equity_port_long = finProds.Portfolio({}, currency)
eo_port_long = finProds.Portfolio({}, currency)
CDS_port_long = finProds.Portfolio({}, currency)

# Short Asset Class Portfolios
FI_port_short = finProds.Portfolio({}, currency)
equity_port_short = finProds.Portfolio({}, currency)
eo_port_short = finProds.Portfolio({}, currency)
CDS_port_short = finProds.Portfolio({}, currency)

# Currency Type Portfolios
CAD_port = finProds.Portfolio({}, currency)
USD_port = finProds.Portfolio({}, currency)
EUR_port = finProds.Portfolio({}, currency)

# Currency Type Long Portfolios
CAD_port_long = finProds.Portfolio({}, currency)
USD_port_long = finProds.Portfolio({}, currency)
EUR_port_long = finProds.Portfolio({}, currency)

# Currency Type Short Portfolios
CAD_port_short = finProds.Portfolio({}, currency)
USD_port_short = finProds.Portfolio({}, currency)
EUR_port_short = finProds.Portfolio({}, currency)

for k, v in tot_port.positions.items():
    asset = k.get_asset_class()
    currency = k.get_currency()

    # Asset Class Breakdown
    if asset == 'Fixed Income':
        FI_port.add_position(k, v)
        if v > 0:
            FI_port_long.add_position(k, v)
        else:
            FI_port_short.add_position(k, v)

    elif asset == 'Equity':
        equity_port.add_position(k, v)
        if v > 0:
            equity_port_long.add_position(k, v)
        else:
            equity_port_short.add_position(k, v)

    elif asset == 'Derivative':
        if isinstance(k, finProds.CreditDefaultSwap):
            CDS_port.add_position(k, v)
            if v > 0:
                CDS_port_long.add_position(k, v)
            else:
                CDS_port_short.add_position(k, v)
        else:
            eo_port.add_position(k, v)
            if v > 0:
                eo_port_long.add_position(k, v)
            else:
                eo_port_short.add_position(k, v)

    # Currency Breakdown
    if currency == 'CAD':
        CAD_port.add_position(k, v)
        if v > 0:
            CAD_port_long.add_position(k, v)
        else:
            CAD_port_short.add_position(k, v)
    elif currency == 'USD':
        USD_port.add_position(k, v)
        if v > 0:
            USD_port_long.add_position(k, v)
        else:
            USD_port_short.add_position(k, v)
    if currency == 'EUR':
        EUR_port.add_position(k, v)
        if v > 0:
            EUR_port_long.add_position(k, v)
        else:
            EUR_port_short.add_position(k, v)

    if v > 0:
        tot_port_long.add_position(k, v)
    else:
        tot_port_short.add_position(k, v)

# -----------------------------------------------------------------------------
# Calculate Exposure of each sub-portfolio relitive to the total portfolio
# -----------------------------------------------------------------------------

# --------
# Total Portfolio Net Exposure
# --------
tot_expos = tot_port.get_exposure(mkt_env)
equity_expos = equity_port.get_exposure(mkt_env)
FI_expos = FI_port.get_exposure(mkt_env)
eo_expos = eo_port.get_exposure(mkt_env)
CDS_expos = CDS_port.get_exposure(mkt_env)

# Determine the weight of exposure of each sub-portfolio
equity_expos_weight = equity_expos / tot_expos
FI_expos_weight = FI_expos / tot_expos
eo_expos_weight = eo_expos / tot_expos
CDS_expos_weight = CDS_expos / tot_expos

# Plot the sub-portfolio percetages of exposure
expos_weights = np.array([equity_expos_weight, FI_expos_weight, eo_expos_weight, CDS_expos_weight])
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(expos_weights, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%', labels=names)
plt.axis('equal')
plt.tight_layout()
plt.title('Total Portfolio Exposures Relative to Asset Classes')
plt.show()

# --------
# Long Portfolio Exposure
# --------
tot_expos_long = tot_port_long.get_exposure(mkt_env)
equity_expos_long = equity_port_long.get_exposure(mkt_env)
FI_expos_long = FI_port_long.get_exposure(mkt_env)
eo_expos_long = eo_port_long.get_exposure(mkt_env)
CDS_expos_long = CDS_port_long.get_exposure(mkt_env)

# Determine the weight of exposure of each sub-portfolio
equity_expos_weight_long = equity_expos_long / tot_expos_long
FI_expos_weight_long = FI_expos_long / tot_expos_long
eo_expos_weight_long = eo_expos_long / tot_expos_long
CDS_expos_weight_long = CDS_expos_long / tot_expos_long

# Plot the sub-portfolio percetages of exposure
expos_weights_long = np.array(
    [equity_expos_weight_long, FI_expos_weight_long, eo_expos_weight_long, CDS_expos_weight_long])
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(expos_weights_long, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%', labels=names)
plt.axis('equal')
plt.tight_layout()
plt.title('Long Portfolio Exposures Relative to Asset Classes')
plt.show()

# --------
# Short Portfolio Exposure
# --------
tot_expos_short = tot_port_short.get_exposure(mkt_env)
equity_expos_short = equity_port_short.get_exposure(mkt_env)
FI_expos_short = FI_port_short.get_exposure(mkt_env)
eo_expos_short = eo_port_short.get_exposure(mkt_env)
CDS_expos_short = CDS_port_short.get_exposure(mkt_env)

# Determine the weight of exposure of each sub-portfolio
equity_expos_weight_short = equity_expos_short / tot_expos_short
FI_expos_weight_short = FI_expos_short / tot_expos_short
eo_expos_weight_short = eo_expos_short / tot_expos_short
CDS_expos_weight_short = CDS_expos_short / tot_expos_short

# Plot the sub-portfolio percetages of exposure
expos_weights_short = np.array([FI_expos_weight_short, CDS_expos_weight_short])
colors = ['lightskyblue', 'yellowgreen']
plt.pie(expos_weights_short, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%',
        labels=['Fixed Income Portfolio', 'CDS Portfolio'])
plt.axis('equal')
plt.tight_layout()
plt.title('Short Portfolio Exposures Relative to Asset Classes Converted to CAD')
plt.show()

# --------
# Total Currency Portfolio Net Exposure
# --------
CAD_expos = CAD_port.get_exposure(mkt_env)
USD_expos = USD_port.get_exposure(mkt_env)
EUR_expos = EUR_port.get_exposure(mkt_env)

# Determine the weight of exposure of each sub-portfolio
CAD_expos_weight = CAD_expos / tot_expos
USD_expos_weight = USD_expos / tot_expos
EUR_expos_weight = EUR_expos / tot_expos

# Plot the sub-portfolio percetages of exposure
expos_weights_curr = np.array([CAD_expos_weight, USD_expos_weight, EUR_expos_weight])
colors = ['gold', 'lightskyblue', 'lightcoral']
plt.pie(expos_weights_curr, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%', labels=currency_names)
plt.axis('equal')
plt.tight_layout()
plt.title('Total Portfolio Exposures Relative to Currencies Converted to CAD')
plt.show()

# --------
# Long Currency Portfolio Exposure
# --------
CAD_expos_long = CAD_port_long.get_exposure(mkt_env)
USD_expos_long = USD_port_long.get_exposure(mkt_env)
EUR_expos_long = EUR_port_long.get_exposure(mkt_env)

# Determine the weight of exposure of each sub-portfolio
CAD_expos_weight_long = CAD_expos_long / tot_expos_long
USD_expos_weight_long = USD_expos_long / tot_expos_long
EUR_expos_weight_long = EUR_expos_long / tot_expos_long

# Plot the sub-portfolio percetages of exposure
expos_weights_curr_long = np.array([CAD_expos_weight_long, USD_expos_weight_long, EUR_expos_weight_long])
colors = ['gold', 'lightskyblue', 'lightcoral']
plt.pie(expos_weights_curr_long, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%', labels=currency_names)
plt.axis('equal')
plt.tight_layout()
plt.title('Long Portfolio Exposures Relative to Currencies Converted to CAD')
plt.show()

# --------
# Short Currency Portfolio Exposure
# --------
CAD_expos_short = CAD_port_short.get_exposure(mkt_env)
USD_expos_short = USD_port_short.get_exposure(mkt_env)
EUR_expos_short = EUR_port_short.get_exposure(mkt_env)

# Determine the weight of exposure of each sub-portfolio
CAD_expos_weight_short = CAD_expos_short / tot_expos_short
USD_expos_weight_short = USD_expos_short / tot_expos_short
EUR_expos_weight_short = EUR_expos_short / tot_expos_short

# Plot the sub-portfolio percetages of exposure
expos_weights_curr_short = np.array([CAD_expos_weight_short, USD_expos_weight_short, EUR_expos_weight_short])
colors = ['gold', 'lightskyblue', 'lightcoral']
plt.pie(expos_weights_curr_short, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%', labels=currency_names)
plt.axis('equal')
plt.tight_layout()
plt.title('Short Portfolio Exposures Relative to Currencies')
plt.show()

# Calculate the amount of leverage in the portfolio
tot_val = tot_port.value_product(mkt_env)
tot_val_long = tot_port_long.value_product(mkt_env)
tot_val_short = tot_port_short.value_product(mkt_env)
leverage_expos = (tot_expos_long - tot_expos_short) / (tot_expos_long + tot_expos_short)
leverage_val = (tot_val_long - tot_val_short) / (tot_val_long + tot_val_short)

# -----------------------------------------------------------------------------
# Market VaR Calculation for all Sub-portfolios
# -----------------------------------------------------------------------------

# Generate Scenarios
print('Generating Market Risk Scenarios..')
scenarios = finRisk.SimulationEngine(corr_mat, factor_vol, num_sims_mkt, sim_delta_t)

# Convert Scenarios to Market Environment
print('Converting Scenarios to Market Environments..')
mkt_env_dist = finRisk.generate_mkt_env_distribution(scenarios, mkt_env)

# Generate PnL Distributions and Calculate Market VaR and ES
print('Generating Market Risk Total Portfolio Distribution..')
tot_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(tot_port, mkt_env_dist, mkt_env)
tot_mkt_VaR, tot_mkt_ES = finRisk.calculate_VaR_from_PnL(tot_mkt_PnL_dist, alpha_mkt)

tot_mkt_mean = np.mean(tot_mkt_PnL_dist)
tot_mkt_vol = np.std(tot_mkt_PnL_dist)

print('Generating Market Risk Equity Portfolio Distribution..')
equity_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(equity_port, mkt_env_dist, mkt_env)
equity_mkt_VaR, equity_mkt_ES = finRisk.calculate_VaR_from_PnL(equity_mkt_PnL_dist, alpha_mkt)

print('Generating Market Risk Fixed Income Portfolio Distribution..')
FI_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(FI_port, mkt_env_dist, mkt_env)
FI_mkt_VaR, FI_mkt_ES = finRisk.calculate_VaR_from_PnL(FI_mkt_PnL_dist, alpha_mkt)

print('Generating Market Risk Equity Option Portfolio Distribution..')
eo_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(eo_port, mkt_env_dist, mkt_env)
eo_mkt_VaR, eo_mkt_ES = finRisk.calculate_VaR_from_PnL(eo_mkt_PnL_dist, alpha_mkt)

print('Generating Market Risk CDS Portfolio Distribution..')
CDS_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(CDS_port, mkt_env_dist, mkt_env)
CDS_mkt_VaR, CDS_mkt_ES = finRisk.calculate_VaR_from_PnL(CDS_mkt_PnL_dist, alpha_mkt)

print('Generating Market Risk CAD Portfolio Distribution..')
CAD_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(CAD_port, mkt_env_dist, mkt_env)
CAD_mkt_VaR, CAD_mkt_ES = finRisk.calculate_VaR_from_PnL(CAD_mkt_PnL_dist, alpha_mkt)

print('Generating Market Risk USD Portfolio Distribution..')
USD_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(USD_port, mkt_env_dist, mkt_env)
USD_mkt_VaR, USD_mkt_ES = finRisk.calculate_VaR_from_PnL(USD_mkt_PnL_dist, alpha_mkt)

print('Generating Market Risk EUR Portfolio Distribution..')
EUR_mkt_PnL_dist = finRisk.generate_PnL_distribution_from_mkt_envs(EUR_port, mkt_env_dist, mkt_env)
EUR_mkt_VaR, EUR_mkt_ES = finRisk.calculate_VaR_from_PnL(EUR_mkt_PnL_dist, alpha_mkt)

# -----------------------------------------------------------------------------
# Marginal Market VaR of the portfolio and sub-portfolios
# -----------------------------------------------------------------------------

print('Calculating Marginal VaR and Risk Contribution..')

# Determine the weights of the sub-portfolios and create a matrix of the
# returns of the sub-portfolios
tot_val = tot_port.value_product(mkt_env)
equity_val = equity_port.value_product(mkt_env)
FI_val = FI_port.value_product(mkt_env)
eo_val = eo_port.value_product(mkt_env)
CDS_val = CDS_port.value_product(mkt_env)

weights_assets = np.array([equity_val / tot_val, FI_val / tot_val, eo_val / tot_val, CDS_val / tot_val])
combined_dist_assets = np.matrix([equity_mkt_PnL_dist, FI_mkt_PnL_dist, eo_mkt_PnL_dist, CDS_mkt_PnL_dist])

CAD_val = CAD_port.value_product(mkt_env)
USD_val = USD_port.value_product(mkt_env)
EUR_val = EUR_port.value_product(mkt_env)

weights_currency = np.array([CAD_val / tot_val, USD_val / tot_val, EUR_val / tot_val])
combined_dist_currency = np.matrix([CAD_mkt_PnL_dist, USD_mkt_PnL_dist, EUR_mkt_PnL_dist])

# Calculate Marginal VaR with respect the the sub portfolios
print('Total Portfolio Marginal VaR with respect to asset classes..')
tot_RC, tot_MVaR = finRisk.marginal_VaR_from_sub_dists(combined_dist_assets, weights_assets, alpha_mkt, names)

print('Total Portfolio Marginal VaR with respect to currencies..')
tot_RC_curr, tot_MVaR_curr = finRisk.marginal_VaR_from_sub_dists(combined_dist_currency, weights_currency, alpha_mkt,
                                                                 currency_names)

# Calculate Marginal VaR of each sub portfolio with respect to the underlying
# assets
print('Equity Portfolio Marginal VaR..')
equity_RC, equity_MVaR = finRisk.marginal_VaR_from_total_port(equity_port, mkt_env, scenarios, alpha_mkt)
print('Fixed Income Portfolio Marginal VaR..')
FI_RC, FI_MVaR = finRisk.marginal_VaR_from_total_port(FI_port, mkt_env, scenarios, alpha_mkt)
print('Equity Option Portfolio Marginal VaR..')
eo_RC, eo_MVaR = finRisk.marginal_VaR_from_total_port(eo_port, mkt_env, scenarios, alpha_mkt)
print('CDS Portfolio Marginal VaR..')
CDS_RC, CDS_MVaR = finRisk.marginal_VaR_from_total_port(CDS_port, mkt_env, scenarios, alpha_mkt)

# -----------------------------------------------------------------------------
# Plot the Market VaR Distribution of the Portfolios
# -----------------------------------------------------------------------------
print('Plotting the Market VaR Distribution of the Portfolios..')
finRisk.plot_market_VaR_dist(tot_mkt_PnL_dist, tot_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'Total')

finRisk.plot_market_VaR_dist(equity_mkt_PnL_dist, equity_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt,
                             alpha_mkt, num_bins, 'Equity')

finRisk.plot_market_VaR_dist(FI_mkt_PnL_dist, FI_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'Fixed Income')

finRisk.plot_market_VaR_dist(eo_mkt_PnL_dist, eo_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'Equity Option')

finRisk.plot_market_VaR_dist(CDS_mkt_PnL_dist, CDS_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'CDS')

finRisk.plot_market_VaR_dist(CAD_mkt_PnL_dist, CAD_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'CAD')

finRisk.plot_market_VaR_dist(USD_mkt_PnL_dist, USD_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'USD')

finRisk.plot_market_VaR_dist(EUR_mkt_PnL_dist, EUR_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'EUR')

# -----------------------------------------------------------------------------
# Credit VaR Calculation for all Sub-portfolios
# -----------------------------------------------------------------------------

# Generate PnL Distributions and Calculate Credit VaR and ES
print('Generating Credit Risk Total Portfolio Distribution..')
tot_cred_PnL_dists = finRisk.generate_credit_VaR_distrubtion(tot_port, mkt_env, num_sims_crd, rho)
tot_cred_PnL_dist = tot_cred_PnL_dists[0]
tot_mig_PnL_dist = tot_cred_PnL_dists[1]
tot_dflt_PnL_dist = tot_cred_PnL_dists[2]

tot_cred_VaR, tot_cred_ES = finRisk.calculate_VaR_from_PnL(tot_cred_PnL_dist, alpha_crd)
tot_mig_VaR, tot_mig_ES = finRisk.calculate_VaR_from_PnL(tot_mig_PnL_dist, alpha_crd)
tot_dflt_VaR, tot_dflt_ES = finRisk.calculate_VaR_from_PnL(tot_dflt_PnL_dist, alpha_crd)

tot_cred_mean = np.mean(tot_cred_PnL_dist)
tot_cred_vol = np.std(tot_cred_PnL_dist)

# calculate the expected loss and economic capital for credit risk
expected_credit_loss = np.mean(tot_cred_PnL_dist)
credit_economic_capital = -1.0 * (tot_cred_VaR - expected_credit_loss)

# Generate PnL Distributions and Calculate Credit VaR and ES under stressed
# pairwise correlation
print('Generating Stressed Credit Risk Total Portfolio Distribution..')
tot_stressed_cred_PnL_dists = finRisk.generate_credit_VaR_distrubtion(tot_port, mkt_env, num_sims_crd, stressed_rho)
tot_stressed_cred_PnL_dist = tot_stressed_cred_PnL_dists[0]
tot_stressed_mig_PnL_dist = tot_stressed_cred_PnL_dists[1]
tot_stressed_dflt_PnL_dist = tot_stressed_cred_PnL_dists[2]

tot_stressed_cred_VaR, tot_stressed_cred_ES = finRisk.calculate_VaR_from_PnL(tot_stressed_cred_PnL_dist, alpha_crd)
tot_stressed_mig_VaR, tot_stressed_mig_ES = finRisk.calculate_VaR_from_PnL(tot_stressed_mig_PnL_dist, alpha_crd)
tot_stressed_dflt_VaR, tot_stressed_dflt_ES = finRisk.calculate_VaR_from_PnL(tot_stressed_dflt_PnL_dist, alpha_crd)

tot_cred_mean = np.mean(tot_stressed_cred_PnL_dist)
tot_cred_vol = np.std(tot_stressed_cred_PnL_dist)

# -----------------------------------------------------------------------------
# Plot the Credit VaR Distribution of the Portfolios
# -----------------------------------------------------------------------------

# Regular Correlation
finRisk.plot_credit_VaR_dist(tot_cred_PnL_dist, tot_port, mkt_env, scenario_horizon_crd, VaR_horizon_crd, alpha_crd,
                             num_bins, 'Total')
finRisk.plot_credit_VaR_dist(tot_mig_PnL_dist, tot_port, mkt_env, scenario_horizon_crd, VaR_horizon_crd, alpha_crd,
                             num_bins, 'Total Migration')
finRisk.plot_credit_VaR_dist(tot_dflt_PnL_dist, tot_port, mkt_env, scenario_horizon_crd, VaR_horizon_crd, alpha_crd,
                             num_bins, 'Total Defaults')

# Stressed Correlation
finRisk.plot_credit_VaR_dist(tot_cred_PnL_dist, tot_port, mkt_env, scenario_horizon_crd, VaR_horizon_crd, alpha_crd,
                             num_bins, 'Stressed Total')
finRisk.plot_credit_VaR_dist(tot_mig_PnL_dist, tot_port, mkt_env, scenario_horizon_crd, VaR_horizon_crd, alpha_crd,
                             num_bins, 'Stressed Total Migration')
finRisk.plot_credit_VaR_dist(tot_dflt_PnL_dist, tot_port, mkt_env, scenario_horizon_crd, VaR_horizon_crd, alpha_crd,
                             num_bins, 'Stressed Total Defaults')

# -----------------------------------------------------------------------------
# Generate Portfolio Sensitivities
# -----------------------------------------------------------------------------
print('Generating Total Portfolio Sensitivities..')
sensitivities_tot = finScenarios.calculate_portfolio_sensitivities(mkt_env, tot_port)
sensitivities_tot = pd.DataFrame.from_dict(sensitivities_tot)

# -----------------------------------------------------------------------------
# Historic Stressed VaR
# -----------------------------------------------------------------------------
print('Generating Distribution for Market Stressed VaR..')
stressed_scenarios = finScenarios.housing_bubble_scenerios()
stressed_tot_PnL_dist = finRisk.generate_PnL_distribution(tot_port, stressed_scenarios, mkt_env)
tot_SVaR, tot_SES = finRisk.calculate_VaR_from_PnL(stressed_tot_PnL_dist, alpha_mkt)
finRisk.plot_market_VaR_dist(stressed_tot_PnL_dist, tot_port, mkt_env, scenario_horizon_mkt, VaR_horizon_mkt, alpha_mkt,
                             num_bins, 'Total Stressed')

# -----------------------------------------------------------------------------
# Scenario Analysis
# -----------------------------------------------------------------------------
print('Generating Stress Scenarios..')
# Adverse Scenario
mkt_env_Adverse_Scenario = finScenarios.generate_adverse_scenario(mkt_env)
SVaR_Adverse_Scenario = tot_port.value_product(mkt_env_Adverse_Scenario) - tot_port.value_product(mkt_env)

# FS_Vulnerability Scenario
mkt_env_FS_Vulnerability_Scenario = finScenarios.generate_vulnerability_stress_scenario(mkt_env)
SVaR_FS_Vulnerability_Scenario = tot_port.value_product(mkt_env_FS_Vulnerability_Scenario) - tot_port.value_product(
    mkt_env)

# -----------------------------------------------------------------------------
# Regulatory Capital
# -----------------------------------------------------------------------------
print('Calculating Total Regulatory Capital..')
tot_val = tot_port.value_product(mkt_env)
breachs = finRisk.backtest_VaR_from_historic(tot_port, mkt_env, tot_mkt_VaR, 252, val_date)
adj_factor = finRisk.calculate_capital_factor(breachs)
MarketRiskCapital = finRisk.calculate_market_risk_capital(tot_mkt_VaR, SVaR_Adverse_Scenario, tot_cred_VaR, adj_factor)
CounterpartyCreditRiskCapital_SA = finRisk.calculate_counterparty_credit_risk_capital(tot_port, mkt_env)
tot_reg_Capital = finRisk.calculate_regulatory_capital(MarketRiskCapital, CounterpartyCreditRiskCapital_SA)

# -----------------------------------------------------------------------------
# Economic Capital
# -----------------------------------------------------------------------------
print('Calculating Total Economic Capital..')
tot_economic_capital = credit_economic_capital + adj_factor * (-1.0 * tot_mkt_VaR)

# ------------------------------------------------------------------------------
# Capital Allocation
# ------------------------------------------------------------------------------
print('Calculating Capital Allocation..')
Capital_Allocation = np.zeros(len(tot_RC))
idx = 0
for n in names:
    val = tot_RC.loc[n]
    wgt = val / tot_mkt_VaR
    Capital_Allocation[idx] = wgt * tot_reg_Capital
    idx += 1

Capital_Allocation = pd.DataFrame(Capital_Allocation, index=names)

# ------------------------------------------------------------------------------
# Historic Portfolio Risk/Return metrics
# ------------------------------------------------------------------------------

print('Populating Market Environment for yesterday..')
val_date_yester = dt.datetime(2017, 5, 31)
mkt_env_yester = finDB.populate_mkt_env_from_repository(val_date_yester)
tot_val_yester = tot_port.value_product(mkt_env_yester)

# Generate a historic PnL distribution
historic_scenarios = finScenarios.historic_specified_amt(253, val_date_yester)
PnL_dist_hist = finRisk.generate_PnL_distribution(tot_port, historic_scenarios, mkt_env)

# Calculate Returns
tot_val_yester = tot_port.value_product(mkt_env_yester)
returns = np.zeros(len(PnL_dist_hist) - 1)
idx = 0
for val in PnL_dist_hist:
    returns[idx] = val / tot_val_yester

# Provide some risk/return statistics
risk_free_CAD = mkt_env.get_curve('RiskFree-Gov-CAD')
rf = risk_free_CAD['0.25'][0]
port_return = np.mean(returns) * 252
port_vol = np.std(returns) * math.sqrt(252)
sharpe_ratio = (port_return - rf) / port_vol

# -----------------------------------------------------------------------------
# Plot the market environment for today and yesterday
# -----------------------------------------------------------------------------

print('Plotting Market Environments..')

# Valuation Date
key_rates = [0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30]

risk_free_CAD = mkt_env.get_curve('RiskFree-Gov-CAD')
risk_free_USD = mkt_env.get_curve('RiskFree-Gov-USD')
risk_free_EUR = mkt_env.get_curve('RiskFree-Gov-EUR')
risk_free_CAD = finModels.interpolated_yield_curve(risk_free_CAD, key_rates)
risk_free_USD = finModels.interpolated_yield_curve(risk_free_USD, key_rates)
risk_free_EUR = finModels.interpolated_yield_curve(risk_free_EUR, key_rates)

plt.plot(key_rates, risk_free_CAD)
plt.plot(key_rates, risk_free_USD)
plt.plot(key_rates, risk_free_EUR)
plt.legend(currency_names)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('Bootstrapped Government Risk Free Curves ' + str(val_date));
plt.show();

credit_spread_CAD = mkt_env.get_matrix('CreditSpreads-Ratings-CAD')
time_strs = credit_spread_CAD.columns
ratings = credit_spread_CAD.index
times = np.zeros((len(ratings), len(time_strs)))
idx = 0
for s in time_strs:
    for ii in range(len(ratings)):
        times[ii, idx] = float(s)
    idx += 1
plt.plot(np.transpose(times), np.transpose(credit_spread_CAD.as_matrix()))
plt.legend(ratings, loc=2)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('CAD Credit Spreads ' + str(val_date));
plt.show();

credit_spread_USD = mkt_env.get_matrix('CreditSpreads-Ratings-USD')
time_strs = credit_spread_USD.columns
ratings = credit_spread_USD.index
times = np.zeros((len(ratings), len(time_strs)))
idx = 0
for s in time_strs:
    for ii in range(len(ratings)):
        times[ii, idx] = float(s)
    idx += 1
plt.plot(np.transpose(times), np.transpose(credit_spread_USD.as_matrix()))
plt.legend(ratings, loc=2)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('USD Credit Spreads ' + str(val_date));
plt.show();

credit_spread_EUR = mkt_env.get_matrix('CreditSpreads-Ratings-EUR')
time_strs = credit_spread_EUR.columns
ratings = credit_spread_EUR.index
times = np.zeros((len(ratings), len(time_strs)))
idx = 0
for s in time_strs:
    for ii in range(len(ratings)):
        times[ii, idx] = float(s)
    idx += 1
plt.plot(np.transpose(times), np.transpose(credit_spread_EUR.as_matrix()))
plt.legend(ratings, loc=2)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('EUR Credit Spreads ' + str(val_date));
plt.show();

# Yesterday
risk_free_CAD = mkt_env_yester.get_curve('RiskFree-Gov-CAD')
risk_free_USD = mkt_env_yester.get_curve('RiskFree-Gov-USD')
risk_free_EUR = mkt_env_yester.get_curve('RiskFree-Gov-EUR')
risk_free_CAD = finModels.interpolated_yield_curve(risk_free_CAD, key_rates)
risk_free_USD = finModels.interpolated_yield_curve(risk_free_USD, key_rates)
risk_free_EUR = finModels.interpolated_yield_curve(risk_free_EUR, key_rates)

plt.plot(key_rates, risk_free_CAD)
plt.plot(key_rates, risk_free_USD)
plt.plot(key_rates, risk_free_EUR)
plt.legend(currency_names)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('Bootstrapped Government Risk Free Curves ' + str(val_date_yester));
plt.show();

credit_spread_CAD = mkt_env.get_matrix('CreditSpreads-Ratings-CAD')
time_strs = credit_spread_CAD.columns
ratings = credit_spread_CAD.index
times = np.zeros((len(ratings), len(time_strs)))
idx = 0
for s in time_strs:
    for ii in range(len(ratings)):
        times[ii, idx] = float(s)
    idx += 1
plt.plot(np.transpose(times), np.transpose(credit_spread_CAD.as_matrix()))
plt.legend(ratings, loc=2)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('CAD Credit Spreads ' + str(val_date_yester));
plt.show();

credit_spread_USD = mkt_env.get_matrix('CreditSpreads-Ratings-USD')
time_strs = credit_spread_USD.columns
ratings = credit_spread_USD.index
times = np.zeros((len(ratings), len(time_strs)))
idx = 0
for s in time_strs:
    for ii in range(len(ratings)):
        times[ii, idx] = float(s)
    idx += 1
plt.plot(np.transpose(times), np.transpose(credit_spread_USD.as_matrix()))
plt.legend(ratings, loc=2)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('USD Credit Spreads ' + str(val_date_yester));
plt.show();

credit_spread_EUR = mkt_env.get_matrix('CreditSpreads-Ratings-EUR')
time_strs = credit_spread_EUR.columns
ratings = credit_spread_EUR.index
times = np.zeros((len(ratings), len(time_strs)))
idx = 0
for s in time_strs:
    for ii in range(len(ratings)):
        times[ii, idx] = float(s)
    idx += 1
plt.plot(np.transpose(times), np.transpose(credit_spread_EUR.as_matrix()))
plt.legend(ratings, loc=2)
plt.xlabel('Time (years)');
plt.ylabel('Rate');
plt.title('EUR Credit Spreads ' + str(val_date_yester));
plt.show();
