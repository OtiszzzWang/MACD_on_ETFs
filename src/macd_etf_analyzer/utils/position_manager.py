import pandas as pd

def apply_stop_loss(df, stop_loss_pct=0.03):
    """
    Apply stop loss to positions immediately when threshold is breached
    Uses intraweek high/low prices to check for stop loss triggers
    Returns a new DataFrame with stop loss applied
    """
    # Create a copy of the input DataFrame
    result_df = df.copy()
    
    position = 0
    entry_price = 0
    portfolio_value = result_df['Portfolio_Value'].iloc[0]
    
    for i in range(len(result_df)):
        if result_df['Position'].iloc[i] != 0 and position == 0:
            # Enter new position
            position = result_df['Position'].iloc[i]
            entry_price = result_df['Close'].iloc[i]
            portfolio_value = result_df['Portfolio_Value'].iloc[i]
        elif position != 0:
            # Check for stop loss using High and Low prices
            if position == 1:  # Long position
                lowest_price = result_df['Low'].iloc[i]
                loss_pct = (lowest_price - entry_price) / entry_price
                if loss_pct < -stop_loss_pct:
                    # Stop loss triggered - use the stop loss price for return calculation
                    stop_price = entry_price * (1 - stop_loss_pct)
                    result_df.loc[result_df.index[i], 'Close'] = stop_price  # Assume execution at stop price
                    result_df.loc[result_df.index[i], 'Position'] = 0
                    position = 0
                    entry_price = 0
                    
            else:  # Short position
                highest_price = result_df['High'].iloc[i]
                loss_pct = (entry_price - highest_price) / entry_price
                if loss_pct < -stop_loss_pct:
                    # Stop loss triggered - use the stop loss price for return calculation
                    stop_price = entry_price * (1 + stop_loss_pct)
                    result_df.loc[result_df.index[i], 'Close'] = stop_price  # Assume execution at stop price
                    result_df.loc[result_df.index[i], 'Position'] = 0
                    position = 0
                    entry_price = 0
            
            # Check for regular position change
            if result_df['Position'].iloc[i] != position and position != 0:
                position = result_df['Position'].iloc[i]
                entry_price = result_df['Close'].iloc[i] if position != 0 else 0
                portfolio_value = result_df['Portfolio_Value'].iloc[i]
    
    return result_df

def calculate_strategy_returns(df):
    """Calculate strategy returns with position changes"""
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    df['Strategy_Returns'] = df['Strategy_Returns'].fillna(0)
    df['Portfolio_Returns'] = df['Strategy_Returns']
    df['Portfolio_Value'] = df['Portfolio_Value'].iloc[0] * (1 + df['Portfolio_Returns']).cumprod()
    df['Position_Change'] = df['Position'].diff()
    return df 