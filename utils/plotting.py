import matplotlib.pyplot as plt
from scipy.stats import norm, kstest
import numpy as np
"""
Contains all the plotting scripts for each analysis method.
"""

def plot_returns(data, analysis_method):
    """
    Function creates plots of: 

    a) returns vs time
    b) log returns vs time
    c) histogram of returns fit the Gaussian
    """

    def fit_gaussian(name, bins):
        # fit a gaussian across the domain
        x_min, x_max = plt.xlim()
        x            = np.linspace(x_min - 0.02, x_max + 0.02, 1000)
        mu, std      = norm.fit(data[f"{name}"].iloc[1:])
        pdf          = norm.pdf(x, mu, std)
        scaled_pdf   = pdf * len(data[1:]) * np.diff(bins)[0] # scale PDF to counts in histogram
        plt.plot(x, scaled_pdf, label = "Gaussian Fit")
        
        # KS test (compare distribution to normal)
        ks_stat, pval = kstest(data[f"{name}"].iloc[1:], 'norm', args=(mu, std))
        plt.plot([], [], linestyle = "", label = f"KS test p-val = {pval:.2f}")

    def create_return_series(name):
        # create either return or log(return) over time plot.
        plt.figure(figsize = (6, 4))
        ax = plt.gca()
        data.plot(ax = ax, y = f"{name}", color = "black", linewidth = 2)
        plt.ylabel(f"{name}")
        plt.xlabel("Date (YYYY-MM-DD)")
        plt.savefig(f"outputs/{analysis_method}/{name}.pdf")
        plt.close()
    
    def create_individual_histos(name):
        # create histograms of returns with fitted gaussian
        plt.figure(figsize = (6, 4))
        counts, bins, _  = plt.hist(data[f"{name}"], bins = 10, alpha = 0.7, density = False, label = "Data")
        mids             = bins[:-1] + np.diff(bins)[0] / 2
        fit_gaussian(name, bins)
        plt.xlabel("Return")
        plt.ylabel("Counts")
        plt.legend()
        plt.savefig(f"outputs/{analysis_method}/{name}_hist.pdf")
        plt.close()

    # create plots of arithmetic return and log ratio of returns
    create_return_series("Return")
    create_return_series("Log Return")

    # create histograms + gaussian fits of arithmetic return and log ratio return
    create_individual_histos("Return")
    create_individual_histos("Log Return")