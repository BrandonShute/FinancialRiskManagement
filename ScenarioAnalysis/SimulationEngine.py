import pandas as pd
import numpy as np
import math
from scipy.linalg import cholesky


def SimulationEngine(corr_matrix, std_dev_vector, numSim, sim_delta_t, vol_delta_t=None):
    # corr_matrix is correlation matrix of risk factor time series; format will be pandas DataFrame matrix
    # std_dev_vector is vector of standard deviations of risk factor time series; format will be pandas DataFrame matrix
    # numSim is number of simulations
    # sim_delta_t is the time horizon for the simulation in years
    # vol_delta_t will be the time horizon of the vol data in years (defaulted to sim horizon)
    # The scaling factor is with the intent to do a 1-Day Market Risk VaR calculation.
    # Aside: corr_matrix is invariant of time-scale.

    # Step 0: Convert Pandas DataFrames to Matrices and Vectors
    col_names = list(corr_matrix)
    corr_matrix = corr_matrix.as_matrix()
    std_dev_vector = std_dev_vector.as_matrix()
    std_dev_vector = np.squeeze(np.asarray(std_dev_vector))

    # Step 1: Create Covariance Matrix
    std_dev_diag_matrix = np.diag(std_dev_vector)
    temp1 = np.dot(std_dev_diag_matrix, corr_matrix)
    cov_matrix = np.dot(temp1, std_dev_diag_matrix)

    # Step 2: Calculate Cholesky Decomposition of Covariance Matrix
    try:
        lower_cholesky = cholesky(cov_matrix, lower=True)
    except:
        # If the covariance matrix is not PSD, find the closest possible PSD matrix
        _, sin_val, sin_vect = np.linalg.svd(cov_matrix, full_matrices=True)
        sym_polar = np.dot(np.dot(sin_vect, sin_val), np.transpose(sin_vect))
        cov_matrix_adj = (sym_polar + cov_matrix) / 2.0
        cov_matrix = (cov_matrix_adj + np.transpose(cov_matrix_adj)) / 2.0
        lower_cholesky = cholesky(cov_matrix, lower=True)

    # Step 3: Simulate Vector of Standard Normal Random Variables
    std_normal_matrix = np.random.normal(0, 1, (len(corr_matrix), numSim))

    # Step 4: Calculate the time scaling factor
    if vol_delta_t == None:
        vol_delta_t = sim_delta_t
    scaling_factor = 1.0 * sim_delta_t / vol_delta_t

    # Step 5: Calculate Diffusion Term
    diffusion_term_matrix = (math.sqrt(scaling_factor)) * np.dot(lower_cholesky, std_normal_matrix)
    # Output the diffusion term matrix with rows representing different simulations and columns representing each risk factor:
    diffusion_term_matrix = np.transpose(diffusion_term_matrix)

    scenarios = pd.DataFrame(diffusion_term_matrix, columns=col_names)
    return scenarios
