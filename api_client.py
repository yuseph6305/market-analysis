import yfinance as yf
import pandas as pd

def fetch_market_data(ticker: str, period="1y", interval="1d") -> pd.DataFrame:
    """Fetch historical OHLCV data using yfinance."""
    df = yf.download(ticker, period=period, interval=interval)
    df.reset_index(inplace=True)
    return df
