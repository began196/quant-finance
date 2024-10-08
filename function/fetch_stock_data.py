import yfinance as yf

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker.
    Parameters:
        ticker (String): Ticker Symbol for a given company.
        start_date: Start date of window.
        end_date: End date of window.

    Returns: (Pandas dataframe) dataframe of stock related data. 
        Function throws an error if ticker not found.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if len(data) == 0:
            print(f"No data for {ticker}")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None