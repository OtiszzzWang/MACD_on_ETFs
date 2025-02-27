import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def plot_strategy_distribution(summary_df, output_dir='data/summary'):
    """
    Plot the distribution of best strategies across ETFs
    
    Parameters:
    -----------
    summary_df : pandas.DataFrame
        DataFrame with summary statistics for all ETFs
    output_dir : str
        Directory to save the plot
    """
    plt.figure(figsize=(10, 6))
    strategy_counts = summary_df['Best Strategy'].value_counts()
    
    # Create pie chart
    plt.pie(strategy_counts, labels=strategy_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette('viridis', len(strategy_counts)))
    plt.axis('equal')
    plt.title('Distribution of Best Strategies Across ETFs', fontsize=16)
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'strategy_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_performance_comparison(summary_df, output_dir='data/summary'):
    """
    Plot performance comparison of ETFs
    
    Parameters:
    -----------
    summary_df : pandas.DataFrame
        DataFrame with summary statistics for all ETFs
    output_dir : str
        Directory to save the plot
    """
    plt.figure(figsize=(12, 8))
    
    # Sort by Sharpe ratio
    df_sorted = summary_df.sort_values('Sharpe Ratio', ascending=False)
    
    # Create color mapping for strategies
    strategies = df_sorted['Best Strategy'].unique()
    color_map = dict(zip(strategies, sns.color_palette('viridis', len(strategies))))
    colors = [color_map[strategy] for strategy in df_sorted['Best Strategy']]
    
    # Create bar chart
    bars = plt.bar(df_sorted['ETF'], df_sorted['Sharpe Ratio'], color=colors)
    
    # Add a horizontal line for average Sharpe ratio
    plt.axhline(y=df_sorted['Sharpe Ratio'].mean(), color='red', linestyle='--', 
                label=f'Average Sharpe Ratio: {df_sorted["Sharpe Ratio"].mean():.2f}')
    
    # Add labels and title
    plt.xlabel('ETF', fontsize=12)
    plt.ylabel('Sharpe Ratio', fontsize=12)
    plt.title('ETF Performance Comparison by Sharpe Ratio', fontsize=16)
    plt.xticks(rotation=45)
    
    # Add legend for strategies
    legend_handles = [plt.Rectangle((0,0),1,1, color=color_map[strategy]) for strategy in strategies]
    plt.legend(legend_handles, strategies, title='Best Strategy')
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'performance_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_returns_vs_drawdown(summary_df, output_dir='data/summary'):
    """
    Plot returns vs drawdown scatter plot
    
    Parameters:
    -----------
    summary_df : pandas.DataFrame
        DataFrame with summary statistics for all ETFs
    output_dir : str
        Directory to save the plot
    """
    plt.figure(figsize=(12, 8))
    
    # Create color mapping for strategies
    strategies = summary_df['Best Strategy'].unique()
    color_map = dict(zip(strategies, sns.color_palette('viridis', len(strategies))))
    colors = [color_map[strategy] for strategy in summary_df['Best Strategy']]
    
    # Create scatter plot
    plt.scatter(summary_df['Annual Return (%)'], summary_df['Max Drawdown (%)'], 
                c=colors, s=100, alpha=0.7)
    
    # Add labels for each point
    for i, row in summary_df.iterrows():
        plt.annotate(row['ETF'], 
                    (row['Annual Return (%)'], row['Max Drawdown (%)']),
                    xytext=(5, 5), textcoords='offset points')
    
    # Add labels and title
    plt.xlabel('Annual Return (%)', fontsize=12)
    plt.ylabel('Maximum Drawdown (%)', fontsize=12)
    plt.title('Risk-Return Profile: Annual Return vs Maximum Drawdown', fontsize=16)
    
    # Add legend for strategies
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[strategy], 
                                markersize=10) for strategy in strategies]
    plt.legend(legend_handles, strategies, title='Best Strategy')
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'returns_vs_drawdown.png'), dpi=300, bbox_inches='tight')
    plt.close()

def plot_win_ratio_vs_trades(summary_df, output_dir='data/summary'):
    """
    Plot win ratio vs number of trades
    
    Parameters:
    -----------
    summary_df : pandas.DataFrame
        DataFrame with summary statistics for all ETFs
    output_dir : str
        Directory to save the plot
    """
    plt.figure(figsize=(12, 8))
    
    # Create color mapping for strategies
    strategies = summary_df['Best Strategy'].unique()
    color_map = dict(zip(strategies, sns.color_palette('viridis', len(strategies))))
    colors = [color_map[strategy] for strategy in summary_df['Best Strategy']]
    
    # Create scatter plot with size proportional to Sharpe ratio
    sizes = summary_df['Sharpe Ratio'] * 100
    plt.scatter(summary_df['Number of Trades'], summary_df['Win Ratio (%)'], 
                c=colors, s=sizes, alpha=0.7)
    
    # Add labels for each point
    for i, row in summary_df.iterrows():
        plt.annotate(row['ETF'], 
                    (row['Number of Trades'], row['Win Ratio (%)']),
                    xytext=(5, 5), textcoords='offset points')
    
    # Add labels and title
    plt.xlabel('Number of Trades', fontsize=12)
    plt.ylabel('Win Ratio (%)', fontsize=12)
    plt.title('Trading Efficiency: Win Ratio vs Number of Trades', fontsize=16)
    
    # Add legend for strategies
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[strategy], 
                                markersize=10) for strategy in strategies]
    plt.legend(legend_handles, strategies, title='Best Strategy')
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'win_ratio_vs_trades.png'), dpi=300, bbox_inches='tight')
    plt.close()

def generate_summary_visualizations(summary_csv='data/summary/etf_strategy_summary.csv', output_dir='data/summary'):
    """
    Generate all summary visualizations
    
    Parameters:
    -----------
    summary_csv : str
        Path to the summary CSV file
    output_dir : str
        Directory to save the plots
    """
    # Load summary data
    summary_df = pd.read_csv(summary_csv)
    
    # Generate plots
    plot_strategy_distribution(summary_df, output_dir)
    plot_performance_comparison(summary_df, output_dir)
    plot_returns_vs_drawdown(summary_df, output_dir)
    plot_win_ratio_vs_trades(summary_df, output_dir)
    
    print(f"Summary visualizations saved to {output_dir}")

if __name__ == "__main__":
    generate_summary_visualizations() 