"""
Main script to run stock analysis.
"""

import sys
import os
from pathlib import Path
from stock_analysis import StockAnalyzer

def main():
    """Main function to run stock analysis."""
    # Check if ticker is provided as command line argument
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        # Prompt user for ticker input
        ticker = input("Enter stock ticker symbol: ").strip()
    
    if not ticker:
        print("Error: No ticker symbol provided.")
        return 1
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Define sheet mapping for Excel file
    sheet_mapping = {
        'income': 'Income-Annual',
        'balance_sheet': 'Balance-Sheet-Annual',
        'cash_flow': 'Cash-Flow-Annual',
        'ratios': 'Ratios-Annual'
    }
    
    # Initialize analyzer
    analyzer = StockAnalyzer(data_directory="data")
    
    try:
        # Load data for the specified ticker
        print(f"Loading financial data for {ticker.upper()}...")
        analyzer.load_data(ticker, sheet_mapping)
        
        # Perform analysis
        print("\nPerforming stock analysis...")
        results = analyzer.analyze_stock()
        
        # Print results to console
        print("\n")
        analyzer.print_analysis()
        
        # Export results to Excel in output folder
        print("\nExporting results to Excel...")
        output_file = output_dir / f"{ticker.lower()}-result.xlsx"
        analyzer.export_to_excel(str(output_file))
        
        print(f"\nAnalysis complete for {ticker.upper()}!")
        print(f"Results saved to: {output_file}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Make sure the file '{ticker.lower()}-financials.xlsx' exists in the data folder.")
        return 1
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1
    
    return 0

def analyze_multiple_tickers(tickers: list):
    """
    Analyze multiple tickers in batch and export to single Excel file.
    
    Args:
        tickers: List of ticker symbols to analyze
    """
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    sheet_mapping = {
        'income': 'Income-Annual',
        'balance_sheet': 'Balance-Sheet-Annual',
        'cash_flow': 'Cash-Flow-Annual',
        'ratios': 'Ratios-Annual'
    }
    
    analyzer = StockAnalyzer(data_directory="data")
    
    successful_analyses = []
    failed_analyses = []
    batch_results = []  # Store all results for batch export
    
    for ticker in tickers:
        print(f"\n{'='*60}")
        print(f"Analyzing {ticker.upper()}...")
        print('='*60)
        
        try:
            # Load data for the current ticker
            analyzer.load_data(ticker, sheet_mapping)
            
            # Perform analysis
            results = analyzer.analyze_stock()
            
            # Print results to console
            analyzer.print_analysis()
            
            # Store results for batch export (make a copy)
            batch_results.append(analyzer.results.copy())
            
            successful_analyses.append(ticker.upper())
            print(f"✓ Analysis complete for {ticker.upper()}!")
            
        except Exception as e:
            failed_analyses.append(ticker.upper())
            batch_results.append(None)  # Add None for failed analysis
            print(f"✗ Error analyzing {ticker.upper()}: {e}")
    
    # Export all results to a single Excel file
    if batch_results and any(result is not None for result in batch_results):
        print(f"\n{'='*60}")
        print("EXPORTING BATCH RESULTS TO EXCEL...")
        print('='*60)
        
        try:
            # Create batch filename in output directory
            batch_filename = f"stock-analysis.xlsx"
            batch_filepath = output_dir / batch_filename
            
            # Export all results to single Excel file
            analyzer.export_to_excel(str(batch_filepath), batch_results)
            
            print(f"✓ Batch results exported to: {batch_filepath}")
            
        except Exception as e:
            print(f"✗ Error exporting batch results: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("BATCH ANALYSIS SUMMARY")
    print('='*60)
    print(f"Successfully analyzed: {len(successful_analyses)} tickers")
    if successful_analyses:
        print(f"Success: {', '.join(successful_analyses)}")
    
    print(f"Failed to analyze: {len(failed_analyses)} tickers")
    if failed_analyses:
        print(f"Failed: {', '.join(failed_analyses)}")
    
    print(f"\nAll output files saved to: {output_dir.absolute()}")
def analyze_from_file(filename: str):
    """
    Analyze tickers from a text file (one ticker per line).
    
    Args:
        filename: Path to file containing ticker symbols
    """
    try:
        with open(filename, 'r') as f:
            tickers = [line.strip().upper() for line in f if line.strip()]
        
        if not tickers:
            print(f"No tickers found in {filename}")
            return
        
        print(f"Found {len(tickers)} tickers in {filename}: {', '.join(tickers)}")
        analyze_multiple_tickers(tickers)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")

def create_output_directory_structure():
    """Create organized output directory structure."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create subdirectories for better organization
    (output_dir / "individual").mkdir(exist_ok=True)
    (output_dir / "batch").mkdir(exist_ok=True)
    (output_dir / "reports").mkdir(exist_ok=True)
    
    return output_dir

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Batch mode - analyze multiple tickers
        tickers = sys.argv[1:]
        analyze_multiple_tickers(tickers)
    elif len(sys.argv) == 2:
        # Check if it's a file with .txt extension
        if sys.argv[1].endswith('.txt'):
            analyze_from_file(sys.argv[1])
        else:
            # Single ticker mode
            exit(main())
    else:
        # Interactive mode
        print("Stock Analysis Tool")
        print("==================")
        print("1. Single ticker analysis")
        print("2. Multiple ticker analysis")
        print("3. Analyze from file")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            exit(main())
        elif choice == "2":
            ticker_input = input("Enter tickers separated by spaces: ").strip()
            if ticker_input:
                tickers = ticker_input.split()
                analyze_multiple_tickers(tickers)
            else:
                print("No tickers provided.")
        elif choice == "3":
            filename = input("Enter filename: ").strip()
            if filename:
                analyze_from_file(filename)
            else:
                print("No filename provided.")
        else:
            print("Invalid choice.")