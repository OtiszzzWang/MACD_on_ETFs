#!/usr/bin/env python3
"""
Script to view the generated visualizations.
This script opens the visualization images in the default image viewer.
"""

import os
import sys
import platform
import subprocess

def open_file(filepath):
    """
    Open a file with the default application based on the operating system.
    
    Parameters:
    -----------
    filepath : str
        Path to the file to open
    """
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # Linux variants
        subprocess.call(('xdg-open', filepath))

def main():
    """
    Main function to open visualization files.
    """
    # Define the directory containing the visualizations
    summary_dir = 'data/summary'
    
    # List of visualization files to open
    visualization_files = [
        'strategy_distribution.png',
        'performance_comparison.png',
        'returns_vs_drawdown.png',
        'win_ratio_vs_trades.png'
    ]
    
    # Check if the directory exists
    if not os.path.exists(summary_dir):
        print(f"Error: Directory '{summary_dir}' does not exist.")
        print("Please run the MACD ETF analyzer first to generate visualizations.")
        sys.exit(1)
    
    # Open each visualization file
    for filename in visualization_files:
        filepath = os.path.join(summary_dir, filename)
        
        if os.path.exists(filepath):
            print(f"Opening {filename}...")
            open_file(filepath)
        else:
            print(f"Warning: File '{filepath}' does not exist.")
    
    print("\nVisualization files opened in your default image viewer.")
    print("Close the image viewer windows when you're done viewing the visualizations.")

if __name__ == "__main__":
    main() 