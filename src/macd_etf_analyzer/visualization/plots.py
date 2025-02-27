import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_macd_signals(df):
    """Plot MACD signals and price movements"""
    # Create figure with secondary y-axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[2, 1])
    
    # Plot price
    ax1.plot(df.index, df['Close'], label='Price', color='blue', alpha=0.6)
    
    # Plot buy/sell signals
    buy_signals = df[df['Position_Change'] == 1].index
    sell_signals = df[df['Position_Change'] == -2].index  # From 1 to -1
    ax1.scatter(buy_signals, df.loc[buy_signals, 'Close'], marker='^', color='green', label='Buy Signal')
    ax1.scatter(sell_signals, df.loc[sell_signals, 'Close'], marker='v', color='red', label='Sell Signal')
    
    ax1.set_title('Price Movement and Trading Signals')
    ax1.set_ylabel('Price')
    ax1.legend()
    
    # Plot MACD
    ax2.plot(df.index, df['MACD'], label='MACD', color='blue')
    ax2.plot(df.index, df['Signal_Line'], label='Signal Line', color='orange')
    ax2.bar(df.index, df['MACD_Histogram'], label='MACD Histogram', color='gray', alpha=0.3)
    ax2.set_title('MACD Indicator')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def plot_performance(df):
    """Plot strategy performance metrics"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Cumulative returns comparison
    strategy_cum_returns = (1 + df['Strategy_Returns']).cumprod()
    market_cum_returns = (1 + df['Returns']).cumprod()
    ax1.plot(df.index, strategy_cum_returns, label='Strategy Returns', color='blue')
    ax1.plot(df.index, market_cum_returns, label='Market Returns', color='gray', alpha=0.6)
    ax1.set_title('Cumulative Returns')
    ax1.legend()
    
    # Monthly returns heatmap
    monthly_returns = df['Strategy_Returns'].groupby([df.index.year, df.index.month]).sum().unstack()
    sns.heatmap(monthly_returns, ax=ax2, cmap='RdYlGn', center=0, annot=True, fmt='.2%')
    ax2.set_title('Monthly Returns Heatmap')
    
    # Rolling Sharpe ratio (252-day)
    rolling_sharpe = (df['Strategy_Returns'].rolling(252).mean() / 
                     df['Strategy_Returns'].rolling(252).std() * np.sqrt(252))
    ax3.plot(df.index, rolling_sharpe)
    ax3.axhline(y=0, color='r', linestyle='--')
    ax3.set_title('Rolling Sharpe Ratio (252-day)')
    
    # Drawdown analysis
    strategy_cum_returns = (1 + df['Strategy_Returns']).cumprod()
    rolling_max = strategy_cum_returns.expanding().max()
    drawdowns = (strategy_cum_returns - rolling_max) / rolling_max
    ax4.fill_between(df.index, drawdowns, 0, color='red', alpha=0.3)
    ax4.set_title('Drawdown Analysis')
    
    plt.tight_layout()
    plt.show() 