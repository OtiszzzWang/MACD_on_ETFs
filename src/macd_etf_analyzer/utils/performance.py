import pandas as pd
import numpy as np
import os

def calculate_performance_metrics(df):
    """Calculate various trading performance metrics"""
    
    # Number of Trades
    trades = df['Position_Change'].fillna(0)
    num_trades = len(trades[trades != 0])
    
    # Win Ratio - only count returns when position changes
    position_changes = df[df['Position_Change'] != 0]
    winning_trades = len(position_changes[position_changes['Strategy_Returns'] > 0])
    win_ratio = winning_trades / num_trades if num_trades > 0 else 0
    
    # Profit & Loss
    cumulative_returns = (1 + df['Strategy_Returns']).cumprod()
    total_return = (cumulative_returns.iloc[-1] - 1) * 100
    
    # Calculate annual return
    years = (df.index[-1] - df.index[0]).days / 365.25
    annual_return = (cumulative_returns.iloc[-1] ** (1/years)) - 1
    
    # Sharpe Ratio (assuming 0% risk-free rate)
    mean_returns = df['Strategy_Returns'].mean()
    std_returns = df['Strategy_Returns'].std()
    sharpe_ratio = np.sqrt(52) * mean_returns / std_returns if std_returns != 0 else 0
    
    # Maximum Drawdown calculation
    portfolio_value = df['Portfolio_Value']
    peak = portfolio_value.expanding(min_periods=1).max()
    drawdown = (portfolio_value - peak) / peak
    max_drawdown = drawdown.min() * 100
    
    # Portfolio Value metrics
    initial_value = df['Portfolio_Value'].iloc[0]
    final_value = df['Portfolio_Value'].iloc[-1]
    portfolio_return = ((final_value - initial_value) / initial_value) * 100
    
    return {
        'Number of Trades': num_trades,
        'Win Ratio': f"{win_ratio:.2%}",
        'Total Return': f"{total_return:.2f}%",
        'Annual Return': f"{annual_return*100:.2f}%",
        'Sharpe Ratio': f"{sharpe_ratio:.2f}",
        'Maximum Drawdown': f"{max_drawdown:.2f}%",
        'Initial Portfolio Value': f"${initial_value:,.2f}",
        'Final Portfolio Value': f"${final_value:,.2f}",
        'Portfolio Return': f"{portfolio_return:.2f}%"
    }

def get_trade_info(df, strategy_name, ticker):
    """Extract trade information from the signals DataFrame"""
    trades = []
    position = 0
    entry_price = 0
    entry_date = None
    
    for date, row in df.iterrows():
        if row['Position_Change'] != 0:
            # Case 1: Opening a new position from neutral
            if position == 0:
                position = row['Position']
                entry_price = row['Close']
                entry_date = date
            # Case 2: Direct switch between long and short positions
            elif (position == 1 and row['Position'] == -1) or (position == -1 and row['Position'] == 1):
                # Close current position
                exit_price = row['Close']
                pnl = position * (exit_price - entry_price) / entry_price * 100
                trades.append({
                    'Entry Date': entry_date,
                    'Exit Date': date,
                    'Position': 'Long' if position == 1 else 'Short',
                    'Entry Price': entry_price,
                    'Exit Price': exit_price,
                    'PnL %': pnl
                })
                # Open new position
                position = row['Position']
                entry_price = row['Close']
                entry_date = date
            # Case 3: Closing a position to neutral
            elif row['Position'] == 0:
                exit_price = row['Close']
                pnl = position * (exit_price - entry_price) / entry_price * 100
                trades.append({
                    'Entry Date': entry_date,
                    'Exit Date': date,
                    'Position': 'Long' if position == 1 else 'Short',
                    'Entry Price': entry_price,
                    'Exit Price': exit_price,
                    'PnL %': pnl
                })
                position = 0
    
    trades_df = pd.DataFrame(trades)
    
    # Create ticker-specific directory
    ticker_dir = os.path.join('data', ticker)
    os.makedirs(ticker_dir, exist_ok=True)
    
    # Save trade information to CSV in ticker directory
    output_file = os.path.join(ticker_dir, f'trade_info_{strategy_name}.csv')
    trades_df.to_csv(output_file, index=False)
    
    return trades_df 