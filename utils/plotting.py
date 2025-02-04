import matplotlib.pyplot as plt
from scipy.stats import norm, kstest, kurtosis
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

    def check_name(name):
        if name != "Return" and name != "Log Return":
            print("ERROR: name '{name}' not valid for plotting functions.")
            return 0
        else:
            return 1

    def fit_gaussian(data, bins, ax):
        # fit a gaussian across the domain
        x_min, x_max = ax.get_xlim()
        x            = np.linspace(x_min *0.9, x_max * 1.1, 1000)
        mu, std      = norm.fit(data)
        pdf          = norm.pdf(x, mu, std)
        n            = len(data)
        scaled_pdf   = pdf * n * np.diff(bins)[0] # scale PDF to counts in histogram
        ax.plot(x, scaled_pdf, label = "Gaussian Fit")
        
        # KS test (compare distribution to normal)
        ks_stat, pval = kstest(data, 'norm', args=(mu, std))
        ax.plot([], [], linestyle = "", label = f"KS test p-val = {pval:.3f}")

    def create_return_series(name):
        flag = check_name(name)

        if flag == 1:
            # create either return or log(return) over time plot.
            plt.figure(figsize = (6, 4))
            ax = plt.gca()
            data.plot(ax = ax, y = f"{name}", color = "black", linewidth = 2)
            plt.ylabel(f"{name}")
            plt.xlabel("Date (YYYY-MM-DD)")
            plt.savefig(f"outputs/{analysis_method}/{name}.pdf")
            plt.close()
    
    def create_individual_histos(name):
        flag = check_name(name)
        
        if flag == 1:
            # create histograms of returns with fitted gaussian
            plt.figure(figsize = (6, 4))
            counts, bins, _  = plt.hist(data[f"{name}"], bins = "auto", alpha = 0.7, density = False, label = "Data")
            mids             = bins[:-1] + np.diff(bins)[0] / 2
            fit_gaussian(data[f"{name}"].iloc[1:], bins, plt.gca())
            plt.xlabel("Return")
            plt.ylabel("Counts")
            plt.legend()
            plt.savefig(f"outputs/{analysis_method}/{name}_hist.pdf")
            plt.close()

    def create_aggregational_plots(name):
        flag = check_name(name)
        
        if flag == 1:
            # sample returns into 3 new data frames: daily, weekly and monthly
            daily   = data[f"{name}"].iloc[1:] 
            if name == "Return":
                # product of returns needed across period
                ### much more computationally intensive than using log returns! ###
                print("Resampling RETURNS --> large products needed. Are you sure you want to do this?")
                weekly = daily.resample("W").prod()
                monthly = daily.resample("M").prod()
            else:
                # sum of log returns needed within each period
                weekly = daily.resample("W").sum()
                monthly = daily.resample("M").sum()
            plot_data = [daily, weekly, monthly]
            
            # create 3 plots showing return histos + fit results for each grouping
            fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (12, 4))
            for iplot in range(3):
                counts, bins, _ = axes[iplot].hist(plot_data[iplot], bins = "auto", density = False, alpha = 0.7, label = "Data")
                axes[iplot].set_title(f"Counts: {np.sum(counts)}")
                axes[iplot].set_xlabel(f"{name}")
                axes[iplot].set_ylabel("Counts")

                # add gaussian fit and KS-test p-values
                fit_gaussian(plot_data[iplot], bins, axes[iplot])

                # calculate and add kurtosis of data to plot
                axes[iplot].plot([], [], linestyle = "", label = f"Kurtosis: {kurtosis(plot_data[iplot]):.3f}")
                axes[iplot].legend()
            plt.savefig(f"outputs/{analysis_method}/{name}_aggregation.pdf")
            plt.close()
    
    # create plots of arithmetic return and log ratio of returns
    create_return_series("Return")
    create_return_series("Log Return")

    # create histograms + gaussian fits of arithmetic return and log ratio return
    create_individual_histos("Return")
    create_individual_histos("Log Return")
    create_aggregational_plots("Log Return")

def plot_clusters(data, change_point_idx):
    """
    Plot log returns and identified change points between high / low volatility regimes.
    """

    # find the dates at which to plot cluster start/ends
    cluster_dates = data["Log Return"].iloc[change_point_idx].index
    plt.figure(figsize = (6, 4))
    ax = plt.gca()
    data.plot(ax = ax, y = "Log Return", color = "black", linewidth = 2)
    plt.ylabel("Log Return")
    plt.xlabel("Date (YYYY-MM-DD)")
    y_min, y_max = ax.get_ylim()
    ax.vlines(cluster_dates, ymin = y_min, ymax = y_max, color = "red", linestyle = "dotted")
    plt.savefig(f"outputs/stylised_facts/clustering.pdf")
    plt.close()
