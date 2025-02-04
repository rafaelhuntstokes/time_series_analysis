import argparse
import importlib
from datetime import datetime

"""
Entry point of analysis scripts. User calls this script, inputs a start and end
date for the analysis, along with an analysis type to perform.
"""

def check_date_format(arg):
    try:
        datetime.strptime(arg, "%d%m%Y")
    except:
        print(f"Start date '{arg}' is incorrectly formatted.")
        return 0
    return 1

def main():
    parser = argparse.ArgumentParser(description="Run specified analysis on NASDAQ data.")
    parser.add_argument("analysis", type=str, help="Analysis name. Must match those in /scripts.")
    parser.add_argument("start_date", type=str, help="Start date for analysis in ddmmyyyy format.")
    parser.add_argument("end_date", type=str, help="End date for analysis in ddmmyyyy format.")
    parser.add_argument("--ticker", type=str, default="^IXIC", help="Specify stock / index ticker",)
    args = parser.parse_args()

    # verify inputs
    if check_date_format(args.start_date) == 0 or check_date_format(args.end_date) == 0:
        return
    try:
        analysis_module = importlib.import_module(f"scripts.{args.analysis}")
    except:
        print(f"Analysis module '{args.analysis}' not found.")

    print(f"Running {args.analysis} between {args.start_date} to {args.end_date} inclusive.")
    analysis_module.run_analysis(args.start_date, args.end_date, args.ticker)

if __name__ == "__main__":
    main()