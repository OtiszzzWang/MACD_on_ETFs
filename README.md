# Trading Strategy Analysis Framework

## Overview
This project implements and analyzes multiple trading strategies including MACD and VPVMA (Volume-Price-Volatility Moving Average) across various ETFs. The framework includes standard and zero-crossing variants of each strategy, with integrated stop-loss mechanisms and comprehensive performance metrics.

## Features
- Multiple trading strategies:
  - Standard MACD
  - MACD Zero-Cross
  - VPVMA (Volume-Price-Volatility Moving Average)
  - VPVMA Zero-Cross
- Automated data collection using yfinance
- Stop-loss implementation
- Performance metrics including:
  - Sharpe Ratio
  - Win Ratio
  - Maximum Drawdown
  - Total/Annual Returns
- Parallel processing for efficient analysis
- Comprehensive visualization tools
- Detailed trade logging and analysis

## Installation
1. Clone the repository
2. Install required packages:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Usage
Run the script:
```bash
python MACD_Based_Signals.py
```

The script will:
1. Download historical data for specified ETFs
2. Apply multiple trading strategies
3. Generate performance metrics
4. Save results in the `data` directory

## Project Structure

├── data/
│   ├── summary/
│   │   ├── best_strategies.txt
│   │   ├── sharpe_ratios.csv
│   │   └── strategy_statistics.csv
│   └── {ETF_SYMBOL}/
│       ├── weekly_macd_signals.csv
│       ├── weekly_macd_zero_cross.csv
│       ├── weekly_vpvma_signals.csv
│       └── weekly_vpvma_zero_cross.csv
├── Signals.py
├── MACD_Based_Signals.py
├── requirements.txt
└── README.md

## Output
The analysis generates several output files:
- Strategy comparison metrics
- Trade logs for each strategy
- Performance visualizations
- Summary statistics across all ETFs

## Performance Metrics
- Number of Trades
- Win Ratio
- Total Return
- Annual Return
- Sharpe Ratio
- Maximum Drawdown
- Portfolio Value Changes

## Contributing
Feel free to submit issues and enhancement requests.

## License
MIT License


