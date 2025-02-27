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

## Output

The analysis results are saved in a `data` directory, with each ETF having its own subdirectory containing:
- Strategy comparison results
- Trade information for each strategy
- Performance metrics
- Visualization plots

## Dependencies

- pandas
- numpy
- yfinance
- matplotlib
- seaborn
- scipy

## License

This project is licensed under the MIT License - see the LICENSE file for details.


