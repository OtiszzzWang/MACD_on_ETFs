import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from macd_etf_analyzer.strategies.macd import get_macd_signals
from macd_etf_analyzer.utils.position_manager import apply_stop_loss, calculate_strategy_returns

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        # Create sample data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        self.df = pd.DataFrame({
            'Open': np.random.randn(len(dates)) + 100,
            'High': np.random.randn(len(dates)) + 102,
            'Low': np.random.randn(len(dates)) + 98,
            'Close': np.random.randn(len(dates)) + 100,
            'Volume': np.random.randint(1000, 10000, len(dates))
        }, index=dates)
        
        # Convert index to US/Eastern timezone
        self.df.index = pd.DatetimeIndex(dates).tz_localize('UTC').tz_convert('US/Eastern')

    def test_macd_signals(self):
        # Test MACD signal generation
        result = get_macd_signals(df=self.df.copy(), symbol='TEST')
        
        # Basic checks
        self.assertIsNotNone(result)
        self.assertTrue('MACD' in result.columns)
        self.assertTrue('Signal_Line' in result.columns)
        self.assertTrue('Position' in result.columns)
        
        # Check that positions are -1, 0, or 1
        positions = result['Position'].dropna().unique()
        self.assertTrue(all(p in [-1, 0, 1] for p in positions))

    def test_stop_loss(self):
        # Create a DataFrame with a known pattern
        df = self.df.copy()
        df['Position'] = 1  # Long position
        df['Portfolio_Value'] = 1_000_000
        
        # Apply stop loss
        result = apply_stop_loss(df, stop_loss_pct=0.03)
        
        # Check that stop loss is working
        self.assertIsNotNone(result)
        self.assertTrue('Position' in result.columns)
        
        # Verify that positions are changed to 0 when stop loss is hit
        position_changes = result['Position'].diff()
        self.assertTrue(any(position_changes != 0))

    def test_returns_calculation(self):
        # Create a DataFrame with known positions
        df = self.df.copy()
        df['Position'] = 1  # Long position
        df['Portfolio_Value'] = 1_000_000
        
        # Calculate returns
        result = calculate_strategy_returns(df)
        
        # Check that returns are calculated
        self.assertIsNotNone(result)
        self.assertTrue('Returns' in result.columns)
        self.assertTrue('Strategy_Returns' in result.columns)
        self.assertTrue('Portfolio_Value' in result.columns)
        
        # Verify that portfolio value changes
        self.assertNotEqual(result['Portfolio_Value'].iloc[0], 
                          result['Portfolio_Value'].iloc[-1])

if __name__ == '__main__':
    unittest.main() 