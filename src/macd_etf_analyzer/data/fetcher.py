import yfinance as yf
import pandas as pd

def download_data(symbol, start_date, end_date):
    """Download price and VIX data for a symbol"""
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)
    
    # Download VIX data only once if needed
    if symbol not in ['VIX', '^VIX']:
        vix = yf.Ticker('^VIX')
        vix_df = vix.history(start=start_date, end=end_date)
        return df, vix_df
    return df, None 