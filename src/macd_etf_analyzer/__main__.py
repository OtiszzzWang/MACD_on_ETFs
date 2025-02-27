import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from .data.fetcher import download_data
from .strategies.macd import get_macd_signals, get_macd_signals_zero_cross
from .strategies.vpvma import get_vpvma_signals, get_vpvma_signals_zero_cross
from .utils.performance import calculate_performance_metrics, get_trade_info
from .utils.summary import generate_etf_summary, save_summary_report, generate_trade_logs_summary
from .visualization.summary_plots import generate_summary_visualizations

def analyze_strategy_performance(results, symbol):
    """Analyze and compare strategy performance for a ticker"""
    strategy_metrics = {
        'MACD': results[0],
        'MACD Zero-Cross': results[1],
        'VPVMA': results[2],
        'VPVMA Zero-Cross': results[3]
    }
    
    # Calculate Sharpe ratio for each strategy
    sharpe_ratios = {}
    for strategy_name, df in strategy_metrics.items():
        returns = df['Strategy_Returns']
        sharpe = np.sqrt(52) * returns.mean() / returns.std() if returns.std() != 0 else 0
        sharpe_ratios[strategy_name] = sharpe
    
    # Find best strategy
    best_strategy = max(sharpe_ratios.items(), key=lambda x: x[1])
    
    # Save performance comparison to ticker directory
    ticker_dir = os.path.join('data', symbol.replace('^', ''))
    performance_file = os.path.join(ticker_dir, 'strategy_comparison.txt')
    
    with open(performance_file, 'w') as f:
        f.write(f"Strategy Performance Comparison for {symbol}\n")
        f.write("=" * 50 + "\n\n")
        f.write("Sharpe Ratios:\n")
        for strategy, sharpe in sharpe_ratios.items():
            f.write(f"{strategy}: {sharpe:.2f}\n")
        f.write(f"\nBest Strategy: {best_strategy[0]} (Sharpe: {best_strategy[1]:.2f})")
    
    return best_strategy[0], sharpe_ratios

def process_etf(symbol, start_date='2005-01-01', end_date='2023-12-31', initial_capital=1_000_000):
    """Process all strategies for a single ETF"""
    try:
        # Create ETF-specific directory
        ticker_dir = os.path.join('data', symbol.replace('^', ''))
        os.makedirs(ticker_dir, exist_ok=True)
        
        # Download data once and reuse
        df, vix_df = download_data(symbol, start_date, end_date)
        
        # Process all strategies in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            futures.append(executor.submit(get_macd_signals, df=df.copy(), symbol=symbol))
            futures.append(executor.submit(get_macd_signals_zero_cross, df=df.copy(), symbol=symbol))
            futures.append(executor.submit(get_vpvma_signals, df=df.copy(), vix_df=vix_df.copy(), symbol=symbol))
            futures.append(executor.submit(get_vpvma_signals_zero_cross, df=df.copy(), vix_df=vix_df.copy(), symbol=symbol))
            
            results = [f.result() for f in as_completed(futures)]
            
            # Analyze strategy performance
            best_strategy, sharpe_ratios = analyze_strategy_performance(results, symbol)
            print(f"\n{symbol} Best Strategy: {best_strategy}")
            
            # Generate trade logs for each strategy
            strategy_names = ['MACD', 'MACD Zero-Cross', 'VPVMA', 'VPVMA Zero-Cross']
            for i, strategy_name in enumerate(strategy_names):
                get_trade_info(results[i], strategy_name, symbol)
            
            return results, best_strategy, sharpe_ratios
            
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")
        return None

def main():
    # List of ETFs to analyze
    etfs = [
        # Country/Region ETFs
        'EEM',  # Emerging Markets
        'VWO',  # Emerging Markets
        'FXI',  # China Large-Cap
        'AAXJ', # Asia ex-Japan
        'EWJ',  # Japan
        'ACWX', # All Country World ex-US
        'CHIX', # China Technology
        'CQQQ', # China Technology
        'EWZ',  # Brazil
        'ERUS', # Russia
        'EWC',  # Canada
        'EWU',  # United Kingdom
        'VGK',  # Europe
        'VPL',  # Pacific
        
        # Sector ETFs
        'XLF',  # Financial Sector
        'XLE',  # Energy Sector
        'XLK',  # Technology Sector
        'XLV',  # Healthcare Sector
        'XLI',  # Industrial Sector
        'XLP',  # Consumer Staples Sector
        'XLY',  # Consumer Discretionary Sector
        'XLB',  # Materials Sector
        'XLU',  # Utilities Sector
        'XLRE', # Real Estate Sector
        
        # Bond ETFs
        'AGG',  # US Aggregate Bond
        'BND',  # Total Bond Market
        'TLT',  # 20+ Year Treasury Bond
        'IEF',  # 7-10 Year Treasury Bond
        'SHY',  # 1-3 Year Treasury Bond
        'LQD',  # Investment Grade Corporate Bond
        'HYG',  # High Yield Corporate Bond
        'MUB',  # Municipal Bond
        'EMB',  # Emerging Markets Bond
        'BNDX'  # Total International Bond
    ]
    
    # Dictionary to store results for all ETFs
    etf_results = {}
    
    # Process ETFs in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_etf, etf): etf for etf in etfs}
        for future in as_completed(futures):
            etf = futures[future]
            try:
                results = future.result()
                if results:
                    etf_results[etf] = results
                    _, best_strategy, sharpe_ratios = results
                    print(f"\nResults for {etf}:")
                    print(f"Best Strategy: {best_strategy}")
                    print("Sharpe Ratios:")
                    for strategy, sharpe in sharpe_ratios.items():
                        print(f"{strategy}: {sharpe:.2f}")
            except Exception as e:
                print(f"Error processing {etf}: {str(e)}")
    
    # Generate summary reports if we have results
    if etf_results:
        print("\nGenerating summary reports...")
        summary_df = generate_etf_summary(etf_results)
        save_summary_report(summary_df)
        generate_trade_logs_summary(etf_results)
        
        # Generate summary visualizations
        print("\nGenerating summary visualizations...")
        generate_summary_visualizations()
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main() 