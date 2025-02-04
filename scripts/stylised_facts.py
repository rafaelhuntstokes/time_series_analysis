from utils import data_loader
from utils import plotting
import pandas as pd
import numpy as np
from scipy.stats import mood

def calc_returns(data):
    """
    Calculate daily return and log(return) of adjusted close price.
    """

    data["Return"]     = data["Adj Close"].pct_change()
    data["Log Return"] = np.log( data["Adj Close"] / data["Adj Close"].shift(1) )

def volatility_clustering(data):
    """
    Perform a Mood test statistic on input returns data stream.
    Non parameteric rank-based test to decide if given sample is drawn
    from the same probability distribution as the previous batch.

    Discontinuities signal new volatility cluster regimes.

    Index locs of discontinuities are returned for analysis.
    """

    # loop through each day's returns and save idx locs of discontinuities
    current_regime    = [] # track current cluster return values
    discontinuity_idx = [] # row idx of detected discontinuities

    # first row return is NaN so start from idx 1
    for iday in range(1, len(data)):

        input_data = [data["Log Return"].iloc[iday]]
        if len(current_regime) < 2:
            # need at least 2 samples in current regime before applying test
            current_regime.append(input_data[0])
        else:
            # compare new sample to previous regime
            pval = mood(current_regime, input_data).pvalue

            if pval < 0.05:
                # REJECT null: the samples are different!
                discontinuity_idx.append(iday)
                current_regime.clear()
            
            # add to current regime whether null accepted or rejected
            current_regime.append(input_data[0])

    return discontinuity_idx

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

    # return volatility cluster indicies
    cluster_idx = volatility_clustering(data)

    # create a plot of the volatility clusters
    plotting.plot_clusters(data, cluster_idx)


    