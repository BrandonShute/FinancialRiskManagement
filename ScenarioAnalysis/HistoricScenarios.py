###
# Most of these functions are used for generating sets of historic scenerios
# to use for risk analytics
###

import datetime as dt
import pandas as pd
import os


def historic_between_dates(start_date, end_date=None):
    '''
    historic_between_dates(start_date, end_date=None)

    Functionality
    =============
    This returns a matrix of scenerios between two dates where the columns
    correspond to the new values of the risk factors and the rows correspond to
    the scenerio

    Parameters
    ==========
    start_date : datetime
         the start date for the historic scenerios
    end_date : datetime
        the end date for the historic scenerios
    factors : set of strings
        a set of strings specifing the unique identifiers of the risk factors

    Returns
    =======
    scenarios : pandas dataframe
        a pandas matrix of historic scenerios
    '''

    # Paths where the portfolio repository is stored
    SEARCH_STR = 'Dropbox'
    REPOSITORY_PATH = 'Risk Management Project!!/Repositories/'
    REPOSITORY_NAME = 'HistoricRiskScenerioRepository'
    REPOSITORY_FILETYPE = '.xlsx'

    # Find the path on the local machine where dropbox is located
    curr_dir = os.getcwd()
    search_str_idx = curr_dir.find(SEARCH_STR) + len(SEARCH_STR) + 1
    user_path = curr_dir[:search_str_idx]

    # Specify the string of the path with file name and sheet names list
    path_w_file = user_path + REPOSITORY_PATH + REPOSITORY_NAME + REPOSITORY_FILETYPE

    # if the end date is not given, generate from scenerios until today
    if end_date == None:
        end_date = dt.datetime.today()

    # import the historic data from excel
    hist_data = pd.read_excel(path_w_file, header=0)

    # Filter the rows and columns
    mask = (hist_data['Date'] > start_date) & (hist_data['Date'] <= end_date)
    hist_data = hist_data.loc[mask]
    del hist_data['Date']

    scenarios = hist_data

    return scenarios


def historic_specified_amt(num_scenarios, end_date=None):
    '''
    historic_specified_amt(num_scenerios, end_date=None)

    Functionality
    =============
    This returns a specified number of scenerios ending on end_date where the
    columns correspond to the new values of the risk factors and the rows
    correspond to the scenerio

    Parameters
    ==========
    num_scenerios : int
         tthe number of scenerios to return
    end_date : datetime
        the end date for the historic scenerios

    Returns
    =======
    scenarios : pandas dataframe
        a pandas matrix of historic scenerios
    '''

    # Paths where the portfolio repository is stored
    SEARCH_STR = 'Dropbox'
    REPOSITORY_PATH = 'Risk Management Project!!/Repositories/'
    REPOSITORY_NAME = 'HistoricRiskScenerioRepository'
    REPOSITORY_FILETYPE = '.xlsx'

    # Find the path on the local machine where dropbox is located
    curr_dir = os.getcwd()
    search_str_idx = curr_dir.find(SEARCH_STR) + len(SEARCH_STR) + 1
    user_path = curr_dir[:search_str_idx]

    # Specify the string of the path with file name and sheet names list
    path_w_file = user_path + REPOSITORY_PATH + REPOSITORY_NAME + REPOSITORY_FILETYPE

    # if the end date is not given, generate from scenerios until today
    if end_date == None:
        end_date = dt.datetime.today()

    # import the historic data from excel
    hist_data = pd.read_excel(path_w_file, header=0)

    # Filter the rows and columns
    mask = (hist_data['Date'] <= end_date)
    hist_data = hist_data.loc[mask]
    del hist_data['Date']

    # Filter the rows and columns
    scenarios = hist_data.tail(num_scenarios)

    return scenarios


def dotcom_bubble_scenerios():
    '''
    dotcom_bubble_scenerios()

    Functionality
    =============
    This returns a set of scenerios corresponding to the dot com bubble. The
    dates selected to represent this crisis are specified in the top of the
    script

    Parameters
    ==========

    Returns
    =======
    scenarios : pandas dataframe
        a pandas matrix of historic scenerios
    '''

    # Specify specific dates for stressed VaR
    DOTCOM_START = dt.datetime(2000, 1, 1)
    DOTCOM_END = dt.datetime(2003, 1, 1)

    return historic_between_dates(DOTCOM_START, DOTCOM_END)


def housing_bubble_scenerios():
    '''
    dotcom_bubble_scenerios(market_env, factors=None)

    Functionality
    =============
    This returns a set of scenerios corresponding to the housing bubble. The
    dates selected to represent this crisis are specified in the top of the
    script

    Parameters
    ==========

    Returns
    =======
    scenarios : pandas dataframe
        a pandas matrix of historic scenerios
    '''

    # Specify specific dates for stressed VaR
    HOUSING_START = dt.datetime(2007, 9, 1)
    HOUSING_END = dt.datetime(2009, 9, 1)
    return historic_between_dates(HOUSING_START, HOUSING_END)


# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print
    '\nHistoric Generation Testing...'
