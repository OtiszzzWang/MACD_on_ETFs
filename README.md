# MACD ETF Analyzer

A Python package for analyzing ETFs using MACD and VPVMA strategies.

## Project Structure

```
macd_etf_analyzer/
├── src/
│   └── macd_etf_analyzer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── data/
│       │   ├── __init__.py
│       │   └── fetcher.py
│       ├── strategies/
│       │   ├── __init__.py
│       │   ├── macd.py
│       │   └── vpvma.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── performance.py
│       │   └── position_manager.py
│       └── visualization/
│           ├── __init__.py
│           └── plots.py
├── setup.py
└── README.md
```

## Features

- MACD (Moving Average Convergence Divergence) strategy implementation
- VPVMA (Volume Price Volume Moving Average) strategy implementation
- Zero-crossing variants for both strategies
- Stop-loss implementation
- Performance analysis and visualization
- Parallel processing of multiple ETFs
- VIX-adjusted calculations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MACD_on_ETFs.git
cd MACD_on_ETFs
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Usage

You can run the analysis in two ways:

1. As a module:
```bash
python -m macd_etf_analyzer
```

2. Using the installed command:
```bash
macd-etf-analyzer
```

## Supported ETFs

The package currently supports analysis of the following ETFs:

### Country/Region ETFs
- EEM (Emerging Markets)
- VWO (Emerging Markets)
- FXI (China Large-Cap)
- AAXJ (Asia ex-Japan)
- EWJ (Japan)
- ACWX (All Country World ex-US)
- CHIX (China Technology)
- CQQQ (China Technology)
- EWZ (Brazil)
- ERUS (Russia)
- EWC (Canada)
- EWU (United Kingdom)
- VGK (Europe)
- VPL (Pacific)

### Sector ETFs
- XLF (Financial Sector)
- XLE (Energy Sector)
- XLK (Technology Sector)
- XLV (Healthcare Sector)
- XLI (Industrial Sector)
- XLP (Consumer Staples Sector)
- XLY (Consumer Discretionary Sector)
- XLB (Materials Sector)
- XLU (Utilities Sector)
- XLRE (Real Estate Sector)

### Bond ETFs
- AGG (US Aggregate Bond)
- BND (Total Bond Market)
- TLT (20+ Year Treasury Bond)
- IEF (7-10 Year Treasury Bond)
- SHY (1-3 Year Treasury Bond)
- LQD (Investment Grade Corporate Bond)
- HYG (High Yield Corporate Bond)
- MUB (Municipal Bond)
- EMB (Emerging Markets Bond)
- BNDX (Total International Bond)

## Output

The analysis results are saved in a `data` directory, with each ETF having its own subdirectory containing:
- Strategy comparison results
- Trade information for each strategy
- Performance metrics
- Visualization plots

Additionally, comprehensive summary reports are generated in the `data/summary` directory:
- `etf_strategy_summary.csv`: CSV file with summary statistics for all ETFs
- `etf_strategy_report.txt`: Detailed text report with performance metrics for all ETFs
- `all_trades_summary.csv`: CSV file with all trades across all ETFs
- `trade_statistics_report.txt`: Detailed text report with trade statistics

### Summary Reports

The program generates comprehensive summary reports in the `data/summary` directory:

- `etf_strategy_summary.csv`: CSV file with summary statistics for all ETFs
- `etf_strategy_report.txt`: Detailed text report with performance metrics for all ETFs
- `all_trades_summary.csv`: CSV file containing all trades across all ETFs
- `trade_statistics_report.txt`: Detailed text report with trade statistics

### ETF Strategy Report

The ETF Strategy Report provides insights into the performance of different strategies across all ETFs, including:

- Top performing ETFs by Sharpe ratio
- Strategy distribution (percentage of ETFs using each strategy)
- Performance statistics (average Sharpe ratio, annual return, max drawdown, win ratio)
- Detailed performance metrics for each ETF

### Trade Statistics Report

The Trade Statistics Report provides detailed information about trading performance:

- Overall trade statistics (total trades, winning trades, average PnL, average duration)
- Trade statistics by ETF (total trades, winning trades, average PnL, best/worst trades)
- Trade statistics by strategy (total trades, winning trades, average PnL, average duration)

## Visualizations

The program generates visual representations of the analysis results in the `data/summary` directory:

- `strategy_distribution.png`: Pie chart showing the distribution of best strategies across ETFs
- `performance_comparison.png`: Bar chart comparing ETF performance by Sharpe ratio
- `returns_vs_drawdown.png`: Scatter plot showing the risk-return profile (annual return vs maximum drawdown)
- `win_ratio_vs_trades.png`: Scatter plot showing trading efficiency (win ratio vs number of trades)
- `category_performance.png`: Multi-panel chart comparing performance metrics across ETF categories (Country/Region, Sector, Bond)
- `strategy_by_category.png`: Stacked bar chart showing strategy distribution by ETF category

These visualizations provide a quick and intuitive way to understand the performance characteristics of different ETFs and strategies, as well as how performance varies across different asset classes.

## Dependencies

- pandas
- numpy
- yfinance
- matplotlib
- seaborn
- scipy

## License

This project is licensed under the MIT License - see the LICENSE file for details.