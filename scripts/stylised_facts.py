from utils import data_loader
from utils import plotting
import pandas as pd
import numpy as np

def calc_returns(data):
    """
    Calculate daily return and log(return) of adjusted close price.
    """

    data["Return"]     = data["Adj Close"].pct_change()
    data["Log Return"] = np.log( data["Adj Close"] / data["Adj Close"].shift(1) )

def run_analysis(start_date, end_date, ticker):
    """
    Called by run_analysis entry script. Generates the following plots to verify
    observed 'stylized facts' of financial data, between the start and end dates:

    1. Autocorrelation of returns and magnitude of returns (normal and log)
    2. Leptokurtosis plots & aggregational Gaussianity - histograms of returns for
        different length periods fit to Gaussian
    3. Volatility Clustering plots - returns classified into high and low volatility
        clusters using Mood test statistic
    """

    data = data_loader.data_loader(start_date, end_date, ticker)
    if isinstance(data, pd.DataFrame) == False:
        return

    # calculate returns and log returns and add respective cols to data
    calc_returns(data)

    # create an output plot of the returns & aggregational gaussianity
    plotting.plot_returns(data, "stylised_facts")

    