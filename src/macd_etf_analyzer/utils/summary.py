import os
import pandas as pd
import numpy as np
from datetime import datetime

def generate_etf_summary(etf_results):
    """
    Generate a summary of results across all ETFs
    
    Parameters:
    -----------
    etf_results : dict
        Dictionary with ETF symbols as keys and (results, best_strategy, sharpe_ratios) as values
    
    Returns:
    --------
    summary_df : pandas.DataFrame
        DataFrame with summary statistics for all ETFs
    """
    summary_data = []
    
    for etf, (results, best_strategy, sharpe_ratios) in etf_results.items():
        # Extract data for each strategy
        strategy_metrics = {
            'MACD': results[0],
            'MACD Zero-Cross': results[1],
            'VPVMA': results[2],
            'VPVMA Zero-Cross': results[3]
        }
        
        # Get metrics for the best strategy
        best_df = strategy_metrics[best_strategy]
        
        # Calculate key metrics
        total_return = (best_df['Portfolio_Value'].iloc[-1] / best_df['Portfolio_Value'].iloc[0] - 1) * 100
        annual_return = ((best_df['Portfolio_Value'].iloc[-1] / best_df['Portfolio_Value'].iloc[0]) ** 
                         (1 / ((best_df.index[-1] - best_df.index[0]).days / 365.25)) - 1) * 100
        
        # Calculate max drawdown
        portfolio_value = best_df['Portfolio_Value']
        peak = portfolio_value.expanding(min_periods=1).max()
        drawdown = (portfolio_value - peak) / peak
        max_drawdown = drawdown.min() * 100
        
        # Count trades
        position_changes = best_df['Position_Change'].fillna(0)
        num_trades = len(position_changes[position_changes != 0])
        
        # Win ratio
        position_change_indices = best_df[best_df['Position_Change'] != 0].index
        winning_trades = len(best_df.loc[position_change_indices][best_df.loc[position_change_indices, 'Strategy_Returns'] > 0])
        win_ratio = winning_trades / num_trades if num_trades > 0 else 0
        
        # Add to summary data
        summary_data.append({
            'ETF': etf,
            'Best Strategy': best_strategy,
            'Sharpe Ratio': sharpe_ratios[best_strategy],
            'Total Return (%)': total_return,
            'Annual Return (%)': annual_return,
            'Max Drawdown (%)': max_drawdown,
            'Number of Trades': num_trades,
            'Win Ratio (%)': win_ratio * 100,
            'Start Date': best_df.index[0].strftime('%Y-%m-%d'),
            'End Date': best_df.index[-1].strftime('%Y-%m-%d')
        })
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary_data)
    
    # Sort by Sharpe Ratio
    summary_df = summary_df.sort_values('Sharpe Ratio', ascending=False)
    
    return summary_df

def save_summary_report(summary_df, output_dir='data/summary'):
    """
    Save summary report to CSV and generate a text report
    
    Parameters:
    -----------
    summary_df : pandas.DataFrame
        DataFrame with summary statistics for all ETFs
    output_dir : str
        Directory to save the summary report
    """
    # Create summary directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    csv_file = os.path.join(output_dir, 'etf_strategy_summary.csv')
    summary_df.to_csv(csv_file, index=False)
    
    # Generate text report
    report_file = os.path.join(output_dir, 'etf_strategy_report.txt')
    
    with open(report_file, 'w') as f:
        f.write("ETF Strategy Analysis Summary Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("Top Performing ETFs by Sharpe Ratio:\n")
        f.write("-" * 50 + "\n")
        for i, row in summary_df.head(5).iterrows():
            f.write(f"{row['ETF']}: {row['Best Strategy']} (Sharpe: {row['Sharpe Ratio']:.2f})\n")
        
        f.write("\nStrategy Distribution:\n")
        f.write("-" * 50 + "\n")
        strategy_counts = summary_df['Best Strategy'].value_counts()
        for strategy, count in strategy_counts.items():
            f.write(f"{strategy}: {count} ETFs ({count/len(summary_df)*100:.1f}%)\n")
        
        f.write("\nPerformance Statistics:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Average Sharpe Ratio: {summary_df['Sharpe Ratio'].mean():.2f}\n")
        f.write(f"Average Annual Return: {summary_df['Annual Return (%)'].mean():.2f}%\n")
        f.write(f"Average Max Drawdown: {summary_df['Max Drawdown (%)'].mean():.2f}%\n")
        f.write(f"Average Win Ratio: {summary_df['Win Ratio (%)'].mean():.2f}%\n")
        
        f.write("\nDetailed ETF Performance:\n")
        f.write("-" * 50 + "\n")
        for i, row in summary_df.iterrows():
            f.write(f"\n{row['ETF']} - {row['Best Strategy']}:\n")
            f.write(f"  Sharpe Ratio: {row['Sharpe Ratio']:.2f}\n")
            f.write(f"  Total Return: {row['Total Return (%)']:.2f}%\n")
            f.write(f"  Annual Return: {row['Annual Return (%)']:.2f}%\n")
            f.write(f"  Max Drawdown: {row['Max Drawdown (%)']:.2f}%\n")
            f.write(f"  Trades: {row['Number of Trades']} (Win Ratio: {row['Win Ratio (%)']:.2f}%)\n")
    
    print(f"Summary report saved to {report_file}")
    print(f"Summary CSV saved to {csv_file}")
    
    return report_file, csv_file

def generate_trade_logs_summary(etf_results, output_dir='data/summary'):
    """
    Generate a summary of trade logs across all ETFs
    
    Parameters:
    -----------
    etf_results : dict
        Dictionary with ETF symbols as keys and (results, best_strategy, sharpe_ratios) as values
    output_dir : str
        Directory to save the trade logs summary
    """
    # Create summary directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Collect all trade logs
    all_trades = []
    
    for etf, (results, best_strategy, _) in etf_results.items():
        # Get the index of the best strategy
        strategy_index = {
            'MACD': 0,
            'MACD Zero-Cross': 1,
            'VPVMA': 2,
            'VPVMA Zero-Cross': 3
        }[best_strategy]
        
        # Get the DataFrame for the best strategy
        best_df = results[strategy_index]
        
        # Extract trade information
        trades = []
        position = 0
        entry_price = 0
        entry_date = None
        
        for date, row in best_df.iterrows():
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
                        'ETF': etf,
                        'Strategy': best_strategy,
                        'Entry Date': entry_date,
                        'Exit Date': date,
                        'Position': 'Long' if position == 1 else 'Short',
                        'Entry Price': entry_price,
                        'Exit Price': exit_price,
                        'PnL %': pnl,
                        'Duration (days)': (date - entry_date).days
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
                        'ETF': etf,
                        'Strategy': best_strategy,
                        'Entry Date': entry_date,
                        'Exit Date': date,
                        'Position': 'Long' if position == 1 else 'Short',
                        'Entry Price': entry_price,
                        'Exit Price': exit_price,
                        'PnL %': pnl,
                        'Duration (days)': (date - entry_date).days
                    })
                    position = 0
        
        all_trades.extend(trades)
    
    # Create DataFrame with all trades
    trades_df = pd.DataFrame(all_trades)
    
    # Save to CSV
    csv_file = os.path.join(output_dir, 'all_trades_summary.csv')
    trades_df.to_csv(csv_file, index=False)
    
    # Generate trade statistics report
    report_file = os.path.join(output_dir, 'trade_statistics_report.txt')
    
    with open(report_file, 'w') as f:
        f.write("Trade Statistics Summary Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("Overall Trade Statistics:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Trades: {len(trades_df)}\n")
        f.write(f"Winning Trades: {len(trades_df[trades_df['PnL %'] > 0])} ({len(trades_df[trades_df['PnL %'] > 0])/len(trades_df)*100:.2f}%)\n")
        f.write(f"Losing Trades: {len(trades_df[trades_df['PnL %'] <= 0])} ({len(trades_df[trades_df['PnL %'] <= 0])/len(trades_df)*100:.2f}%)\n")
        f.write(f"Average PnL: {trades_df['PnL %'].mean():.2f}%\n")
        f.write(f"Average Duration: {trades_df['Duration (days)'].mean():.2f} days\n")
        
        f.write("\nTrade Statistics by ETF:\n")
        f.write("-" * 50 + "\n")
        for etf in trades_df['ETF'].unique():
            etf_trades = trades_df[trades_df['ETF'] == etf]
            f.write(f"\n{etf}:\n")
            f.write(f"  Total Trades: {len(etf_trades)}\n")
            f.write(f"  Winning Trades: {len(etf_trades[etf_trades['PnL %'] > 0])} ({len(etf_trades[etf_trades['PnL %'] > 0])/len(etf_trades)*100:.2f}%)\n")
            f.write(f"  Average PnL: {etf_trades['PnL %'].mean():.2f}%\n")
            f.write(f"  Best Trade: {etf_trades['PnL %'].max():.2f}%\n")
            f.write(f"  Worst Trade: {etf_trades['PnL %'].min():.2f}%\n")
        
        f.write("\nTrade Statistics by Strategy:\n")
        f.write("-" * 50 + "\n")
        for strategy in trades_df['Strategy'].unique():
            strategy_trades = trades_df[trades_df['Strategy'] == strategy]
            f.write(f"\n{strategy}:\n")
            f.write(f"  Total Trades: {len(strategy_trades)}\n")
            f.write(f"  Winning Trades: {len(strategy_trades[strategy_trades['PnL %'] > 0])} ({len(strategy_trades[strategy_trades['PnL %'] > 0])/len(strategy_trades)*100:.2f}%)\n")
            f.write(f"  Average PnL: {strategy_trades['PnL %'].mean():.2f}%\n")
            f.write(f"  Average Duration: {strategy_trades['Duration (days)'].mean():.2f} days\n")
    
    print(f"Trade statistics report saved to {report_file}")
    print(f"All trades summary saved to {csv_file}")
    
    return report_file, csv_file 