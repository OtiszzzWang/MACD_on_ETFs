import pandas as pd
from ..utils.position_manager import apply_stop_loss, calculate_strategy_returns

def get_macd_signals(df=None, symbol='^GSPC', start_date='2005-01-01', end_date='2023-12-31', initial_capital=1_000_000):
    """MACD strategy with pre-downloaded data option"""
    if df is None:
        return None
    
    # Convert timezone from UTC to US/Eastern
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_convert('US/Eastern')
    
    # Resample to weekly data (last trading day of the week)
    weekly_df = df.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    
    # Calculate weekly MACD
    exp1 = weekly_df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = weekly_df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    
    # Create signals on weekly data
    weekly_df['MACD'] = macd
    weekly_df['Signal_Line'] = signal
    weekly_df['MACD_Histogram'] = macd - signal
    
    # Generate buy/sell signals
    weekly_df['Position'] = 0
    weekly_df['Position'] = weekly_df['Position'].mask(macd > signal, 1)
    weekly_df['Position'] = weekly_df['Position'].mask(macd < signal, -1)
    
    # Shift positions by 1 week to implement signal lag
    weekly_df['Position'] = weekly_df['Position'].shift(1)
    
    # Initialize Portfolio Value
    weekly_df['Portfolio_Value'] = initial_capital
    
    # Apply stop loss with 5%
    weekly_df = apply_stop_loss(weekly_df, stop_loss_pct=0.05)
    
    # Recalculate returns after stop loss
    weekly_df = calculate_strategy_returns(weekly_df)
    
    return weekly_df

def get_macd_signals_zero_cross(df, symbol):
    """MACD zero-crossing strategy implementation"""
    # Convert timezone from UTC to US/Eastern
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_convert('US/Eastern')
    
    # Resample to weekly data (last trading day of the week)
    weekly_df = df.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    
    # Calculate weekly MACD
    exp1 = weekly_df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = weekly_df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    
    # Create signals on weekly data
    weekly_df['MACD'] = macd
    weekly_df['Signal_Line'] = signal
    weekly_df['MACD_Histogram'] = macd - signal
    
    # Generate buy/sell signals with zero-line condition
    weekly_df['Position'] = 0
    
    # Previous position to maintain when no new signal
    prev_position = 0
    
    for i in range(len(weekly_df)):
        # Buy signal: MACD crosses above signal line AND MACD is above zero
        if (macd.iloc[i] > signal.iloc[i]) and (macd.iloc[i] > 0):
            weekly_df.iloc[i, weekly_df.columns.get_loc('Position')] = 1
            prev_position = 1
        # Sell signal: MACD crosses below signal line AND MACD crosses below zero
        elif (macd.iloc[i] < signal.iloc[i]) and (macd.iloc[i] < 0):
            weekly_df.iloc[i, weekly_df.columns.get_loc('Position')] = -1
            prev_position = -1
        else:
            # Maintain previous position when no new signal
            weekly_df.iloc[i, weekly_df.columns.get_loc('Position')] = prev_position
    
    # Shift positions by 1 week to implement signal lag
    weekly_df['Position'] = weekly_df['Position'].shift(1)
    
    # Initialize Portfolio Value
    weekly_df['Portfolio_Value'] = 1_000_000
    
    # Apply stop loss with 5%
    weekly_df = apply_stop_loss(weekly_df, stop_loss_pct=0.05)
    
    # Recalculate returns after stop loss
    weekly_df = calculate_strategy_returns(weekly_df)
    
    return weekly_df 