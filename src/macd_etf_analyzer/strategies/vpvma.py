import pandas as pd
from ..utils.position_manager import apply_stop_loss, calculate_strategy_returns

def get_vpvma_signals(df=None, vix_df=None, symbol='^GSPC', start_date='2005-01-01', end_date='2023-12-31', initial_capital=1_000_000):
    """VPVMA strategy with pre-downloaded data option"""
    if df is None or vix_df is None:
        return None
    
    # Convert timezone from UTC to US/Eastern
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_convert('US/Eastern')
    vix_df.index = pd.to_datetime(vix_df.index)
    vix_df.index = vix_df.index.tz_convert('US/Eastern')
    
    # Resample to weekly data
    weekly_df = df.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    
    weekly_vix = vix_df.resample('W').agg({
        'Close': 'last'
    })
    
    # Calculate VIX-adjusted Price Volume Moving Average (VPVMA)
    vix_weight = 1 / weekly_vix['Close']
    volume_price = weekly_df['Close'] * weekly_df['Volume'] * vix_weight
    vpvma = volume_price.rolling(window=12).mean() / weekly_df['Volume'].rolling(window=12).mean()
    signal = vpvma.rolling(window=26).mean()
    
    # Create signals on weekly data
    weekly_df['VPVMA'] = vpvma
    weekly_df['Signal_Line'] = signal
    weekly_df['VPVMA_Histogram'] = vpvma - signal
    
    # Generate buy/sell signals
    weekly_df['Position'] = 0
    weekly_df['Position'] = weekly_df['Position'].mask(vpvma > signal, 1)
    weekly_df['Position'] = weekly_df['Position'].mask(vpvma < signal, -1)
    
    # Shift positions by 1 week to implement signal lag
    weekly_df['Position'] = weekly_df['Position'].shift(1)
    
    # Initialize Portfolio Value
    weekly_df['Portfolio_Value'] = initial_capital
    
    # Apply stop loss with 5%
    weekly_df = apply_stop_loss(weekly_df, stop_loss_pct=0.05)
    
    # Recalculate returns after stop loss
    weekly_df = calculate_strategy_returns(weekly_df)
    
    return weekly_df

def get_vpvma_signals_zero_cross(df, vix_df, symbol):
    """VPVMA zero-crossing strategy implementation"""
    # Convert timezone from UTC to US/Eastern
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_convert('US/Eastern')
    vix_df.index = pd.to_datetime(vix_df.index)
    vix_df.index = vix_df.index.tz_convert('US/Eastern')
    
    # Resample to weekly data
    weekly_df = df.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    
    weekly_vix = vix_df.resample('W').agg({
        'Close': 'last'
    })
    
    # Calculate VIX-adjusted Price Volume Moving Average (VPVMA)
    vix_weight = 1 / weekly_vix['Close']
    volume_price = weekly_df['Close'] * weekly_df['Volume'] * vix_weight
    vpvma = volume_price.rolling(window=12).mean() / weekly_df['Volume'].rolling(window=12).mean()
    signal = vpvma.rolling(window=26).mean()
    
    # Create signals on weekly data
    weekly_df['VPVMA'] = vpvma
    weekly_df['Signal_Line'] = signal
    weekly_df['VPVMA_Histogram'] = vpvma - signal
    
    # Generate buy/sell signals with zero-line condition
    weekly_df['Position'] = 0
    
    # Previous position to maintain when no new signal
    prev_position = 0
    
    for i in range(len(weekly_df)):
        # Buy signal: VPVMA crosses above signal line AND VPVMA is above zero
        if (vpvma.iloc[i] > signal.iloc[i]) and (vpvma.iloc[i] > weekly_df['Close'].iloc[i]):
            weekly_df.iloc[i, weekly_df.columns.get_loc('Position')] = 1
            prev_position = 1
        # Sell signal: VPVMA crosses below signal line AND VPVMA crosses below zero
        elif (vpvma.iloc[i] < signal.iloc[i]) and (vpvma.iloc[i] < weekly_df['Close'].iloc[i]):
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