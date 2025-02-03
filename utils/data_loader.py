import yfinance as yf
from datetime import datetime
import time

def data_loader(start_date, end_date, ticker):
    """
    Load NASDAQ financial data between start and end date, inclusive.
    """

    # format dates to yyyy-mm-dd as yfinance expects
    start_date = datetime.strptime(start_date, "%d%m%Y").strftime("%Y-%m-%d")
    end_date   = datetime.strptime(end_date, "%d%m%Y").strftime("%Y-%m-%d")

    # try download a few times to deal with possible connection issues
    n_tries   = 0
    max_tries = 10
    while n_tries < max_tries:

        try:
            data = yf.download(f"{ticker}", start = start_date, end = end_date)
            
            # count and return the number of nans
            print(f"Found NaNs:\n{data.isna().sum()}\n")
            return data # success

        except (ConnectionError, ProtocolError):
            n_tries += 1
            if n_tries == max_tries:
                print("Download error: max retries reached. Aborting.")
                return None
            print("Download error. Resubmitting ...")
            time.sleep(2)
