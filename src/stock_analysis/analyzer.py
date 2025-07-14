"""
Main analyzer class that orchestrates the stock analysis process.
"""

import pandas as pd
from typing import Dict, Any, Optional
from pathlib import Path
from .data_loader import FinancialDataLoader
from .calculator import FinancialCalculator


class StockAnalyzer:
    """Main class for performing comprehensive stock analysis."""
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize the stock analyzer.
        
        Args:
            data_directory: Path to directory containing Excel files
        """
        self.data_directory = Path(data_directory)
        self.data_loader = FinancialDataLoader(data_directory)
        self.calculator = None
        self.results = {}
        self.ticker = None
    
    def find_ticker_file(self, ticker: str) -> Optional[str]:
        """
        Find the Excel file for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Filename if found, None otherwise
        """
        # Look for files with pattern: ticker-financials.xlsx
        possible_files = [
            f"{ticker.lower()}-financials.xlsx",
            f"{ticker.upper()}-financials.xlsx",
            f"{ticker}-financials.xlsx"
        ]
        
        for filename in possible_files:
            file_path = self.data_directory / filename
            if file_path.exists():
                return filename
        
        return None
    
    def load_data(self, ticker: str, sheet_mapping: Dict[str, str]) -> None:
        """
        Load financial data files for a specific ticker.
        
        Args:
            ticker: Stock ticker symbol
            sheet_mapping: Dictionary mapping data types to sheet names
        """
        self.ticker = ticker.upper()
        excel_file = self.find_ticker_file(ticker)
        
        if excel_file is None:
            raise FileNotFoundError(f"No financial data file found for ticker {ticker}")
        
        print(f"Found data file: {excel_file}")
        data = self.data_loader.load_financial_data(sheet_mapping, excel_file)
        self.calculator = FinancialCalculator(data)
    
    def find_best_start_year(self, preferred_years: list = None) -> str:
        """
        Find the best available start year based on data availability.
        Ensures the start year has all required metrics: Revenue, Income, and FCF.
        Searches by year (2019, 2020, 2021, etc.) regardless of month/day.
        
        Args:
            preferred_years: List of preferred years in order of preference
            
        Returns:
            Best available start year (2019 or later)
        """
        if preferred_years is None:
            preferred_years = [2019, 2020, 2021, 2022, 2023, 2024]
        
        def find_date_for_year(year: int) -> str:
            """Find any date entry for the given year in the data."""
            if self.calculator.income_data is not None:
                available_dates = self.calculator.income_data.index.strftime('%Y-%m-%d')
                for date in available_dates:
                    if date.startswith(str(year)):
                        return date
            return None
        
        # Check data availability for each preferred year
        for year in preferred_years:
            date_for_year = find_date_for_year(year)
            
            if date_for_year:
                revenue_value = self.calculator.get_metric_value(date_for_year, 'income', 'Revenue')
                income_value = self.calculator.get_metric_value(date_for_year, 'income', 'Net Income')
                fcf_value = self.calculator.get_metric_value(date_for_year, 'cash_flow', 'Free Cash Flow')
                
                # Check if all three required values are available
                if (revenue_value != 'N/A' and revenue_value is not None and
                    income_value != 'N/A' and income_value is not None and
                    fcf_value != 'N/A' and fcf_value is not None):
                    print(f"Using start year: {year} (date: {date_for_year})")
                    return date_for_year
        
        # If no preferred year works, find the earliest available year from 2019 onwards
        # that has all three required metrics
        if self.calculator.income_data is not None:
            available_dates = sorted(self.calculator.income_data.index.strftime('%Y-%m-%d'))
            
            for date in available_dates:
                year = int(date[:4])
                
                # Skip years before 2019 and after 2024
                if year < 2019 or year > 2024:
                    continue
                    
                revenue_value = self.calculator.get_metric_value(date, 'income', 'Revenue')
                income_value = self.calculator.get_metric_value(date, 'income', 'Net Income')
                fcf_value = self.calculator.get_metric_value(date, 'cash_flow', 'Free Cash Flow')
                
                # Check if all three required values are available
                if (revenue_value != 'N/A' and revenue_value is not None and
                    income_value != 'N/A' and income_value is not None and
                    fcf_value != 'N/A' and fcf_value is not None):
                    print(f"Using earliest available year with all metrics: {year} (date: {date})")
                    return date
        
        # Default fallback - try to find any 2019 date, or create one
        fallback_date = find_date_for_year(2019)
        if fallback_date:
            print(f"Warning: No year found with all required metrics. Using fallback: {fallback_date}")
            return fallback_date
        
        # Absolute fallback
        print("Warning: No suitable date found. Using default 2019-12-31")
        return "2019-12-31"

    def find_best_end_year(self) -> str:
        """
        Find the best available end year from 2024 based on data availability.
        Ensures the end year has all required metrics: Revenue, Income, and FCF.
        
        Returns:
            Best available end year date from 2024
        """
        
        def has_all_metrics(date: str) -> bool:
            """Check if a date has all three required metrics."""
            revenue_value = self.calculator.get_metric_value(date, 'income', 'Revenue')
            income_value = self.calculator.get_metric_value(date, 'income', 'Net Income')
            fcf_value = self.calculator.get_metric_value(date, 'cash_flow', 'Free Cash Flow')
            
            return (revenue_value != 'N/A' and revenue_value is not None and
                    income_value != 'N/A' and income_value is not None and
                    fcf_value != 'N/A' and fcf_value is not None)
        
        # Find all available 2024 dates
        if self.calculator.income_data is not None:
            available_dates = sorted(self.calculator.income_data.index.strftime('%Y-%m-%d'))
            
            # Look for 2024 dates with all required metrics
            for date in reversed(available_dates):  # Start from latest date
                if date.startswith('2024') and has_all_metrics(date):
                    print(f"Using end year: 2024 (date: {date})")
                    return date
            
            # If no 2024 date has all metrics, just pick any 2024 date
            for date in reversed(available_dates):
                if date.startswith('2024'):
                    print(f"Warning: Using 2024 date without all metrics: {date}")
                    return date
        
        # Fallback if no 2024 data exists
        print("Warning: No 2024 data found. Using default 2024-12-31")
        return "2024-12-31"
    
    def analyze_stock(self) -> Dict[str, Any]:
        """
        Perform comprehensive stock analysis.
        
        Args:
            end_year: Ending year for analysis
            
        Returns:
            Dictionary containing analysis results
        """
        if self.calculator is None:
            raise ValueError("Data must be loaded first using load_data()")
        
        # Find the best start year
        start_year = self.find_best_start_year()
        end_year = self.find_best_end_year()
        
        # Revenue analysis
        revenue_start = self.calculator.get_metric_value(start_year, 'income', 'Revenue')
        revenue_end = self.calculator.get_metric_value(end_year, 'income', 'Revenue')
        revenue_growth = self.calculator.calculate_growth_rate(start_year, end_year, 'income', 'Revenue')
        
        # Net Income analysis
        net_income_start = self.calculator.get_metric_value(start_year, 'income', 'Net Income')
        net_income_end = self.calculator.get_metric_value(end_year, 'income', 'Net Income')
        net_income_growth = self.calculator.calculate_growth_rate(start_year, end_year, 'income', 'Net Income')
        
        # Free Cash Flow per Share analysis
        fcf_start = self.calculator.get_metric_value(start_year, 'cash_flow', 'Free Cash Flow Per Share')
        fcf_end = self.calculator.get_metric_value(end_year, 'cash_flow', 'Free Cash Flow Per Share')
        fcf_growth = self.calculator.calculate_growth_rate(start_year, end_year, 'cash_flow', 'Free Cash Flow Per Share')
        
        # Ratios
        pe_ratio = self.calculator.get_metric_value(end_year, 'ratios', 'PE Ratio')
        
        #EPS Growth
        eps_growth_direct = self.calculator.get_metric_value(end_year, 'ratios', 'EPS Growth')
        eps_basic_start = self.calculator.get_metric_value(start_year, 'income', 'EPS (Basic)')
        eps_basic_end = self.calculator.get_metric_value(end_year, 'income', 'EPS (Basic)')
        eps_growth_calculated = self.calculator.calculate_growth_rate(start_year, end_year, 'income', 'EPS (Basic)')

        
        # Calculate PEG ratio
        if pe_ratio != 'N/A' and eps_growth_direct != 'N/A' and eps_growth_direct != 0:
            peg_ratio = pe_ratio / eps_growth_direct
        elif pe_ratio != 'N/A' and eps_growth_calculated != 'N/A' and eps_growth_calculated != 0:
            peg_ratio = pe_ratio / eps_growth_calculated
        else:
            peg_ratio = 'N/A'
        
        # Enterprise Value and Gross Profit
        market_cap = self.calculator.get_metric_value(end_year, 'ratios', 'Market Capitalization')
        total_debt = self.calculator.get_metric_value(end_year, 'balance_sheet', 'Total Debt')
        cash_and_equivalents = self.calculator.get_metric_value(end_year, 'balance_sheet', 'Cash & Equivalents')
        enterprise_value = self.calculator.calculate_enterprise_value(end_year)
        gross_profit = self.calculator.get_metric_value(end_year, 'income', 'Gross Profit')
        
        self.results = {
            'ticker': self.ticker,
            'analysis_period': {
                'start_year': start_year,
                'end_year': end_year
            },
            'revenue': {
                'start_value': revenue_start,
                'end_value': revenue_end,
                'growth_rate': revenue_growth
            },
            'net_income': {
                'start_value': net_income_start,
                'end_value': net_income_end,
                'growth_rate': net_income_growth
            },
            'free_cash_flow_per_share': {
                'start_value': fcf_start,
                'end_value': fcf_end,
                'growth_rate': fcf_growth
            },
            'ratios': {
                'pe_ratio': pe_ratio,
                'peg_ratio': peg_ratio
            },
            'values': {
                'market_cap': market_cap,
                'total_debt': total_debt,
                'cash_and_equivalents': cash_and_equivalents,
                'enterprise_value': enterprise_value,
                'gross_profit': gross_profit
            }
        }
        
        return self.results
    
    def export_to_excel(self, output_filename: str = None, batch_results: list = None) -> None:
        """
        Export analysis results to Excel file.
        
        Args:
            output_filename: Output filename (optional)
            batch_results: List of results from multiple tickers (optional)
        """
        if batch_results is None:
            # Single ticker mode
            if not self.results:
                raise ValueError("No analysis results available. Run analyze_stock() first.")
            results_to_process = [self.results]
        else:
            # Batch mode
            results_to_process = batch_results
        
        if output_filename is None:
            if batch_results is None:
                output_filename = f"{self.ticker}-result.xlsx"
            else:
                output_filename = "batch-analysis-results.xlsx"
        
        # Create output directory if it doesn't exist
        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare data for Excel export
        data_rows = []
        
        # Define column headers
        headers = [
            'Ticker', 'Start Year', 'Revenue (Start)', 'Revenue (End)', 'Revenue Growth',
            'Income (Start)', 'Income (End)', 'Income Growth', 'FCF (Start)', 'FCF (End)',
            'FCF Growth', 'PE Ratio', 'PEG Ratio', 'Market Cap', 'Total Debt',
            'Cash & Equivalents', 'Enterprise Value', 'Gross Profit'
        ]
        
        # Process each ticker result
        for result in results_to_process:
            if not result:  # Skip empty results
                continue
                
            row_data = []
            
            # Basic info
            row_data.append(result['ticker'])
            row_data.append(result['analysis_period']['start_year'])
            
            # Revenue metrics
            rev = result['revenue']
            row_data.append(self._format_value(rev['start_value']))
            row_data.append(self._format_value(rev['end_value']))
            row_data.append(self._format_percentage(rev['growth_rate']))
            
            # Net Income metrics
            ni = result['net_income']
            row_data.append(self._format_value(ni['start_value']))
            row_data.append(self._format_value(ni['end_value']))
            row_data.append(self._format_percentage(ni['growth_rate']))
            
            # Free Cash Flow metrics
            fcf = result['free_cash_flow_per_share']
            row_data.append(self._format_value(fcf['start_value']))
            row_data.append(self._format_value(fcf['end_value']))
            row_data.append(self._format_percentage(fcf['growth_rate']))
            
            # Ratios
            ratios = result['ratios']
            row_data.append(self._format_value(ratios['pe_ratio']))
            row_data.append(self._format_value(ratios['peg_ratio']))
            
            # Other metrics
            values = result['values']
            row_data.append(self._format_value(values['market_cap']))
            row_data.append(self._format_value(values['total_debt']))
            row_data.append(self._format_value(values['cash_and_equivalents']))
            row_data.append(self._format_value(values['enterprise_value']))
            row_data.append(self._format_value(values['gross_profit']))
            
            data_rows.append(row_data)
        
        # Create DataFrame and export
        df = pd.DataFrame(data_rows, columns=headers)
        
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Analysis Results', index=False)
        
        print(f"Analysis results exported to: {output_filename}")


    # Example usage for batch processing:
    def batch_analyze_and_export(self, tickers: list, output_filename: str = None) -> None:
        """
        Analyze multiple tickers and export results to Excel.
        
        Args:
            tickers: List of ticker symbols
            output_filename: Output filename (optional)
        """
        batch_results = []
        
        for ticker in tickers:
            try:
                # Assuming you have a method to set ticker and analyze
                original_ticker = self.ticker
                self.ticker = ticker
                self.analyze_stock()  # Your existing analyze method
                batch_results.append(self.results.copy())
                self.ticker = original_ticker
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                batch_results.append(None)  # Add None for failed analysis
        
        # Export all results
        self.export_to_excel(output_filename, batch_results)
    
    def _format_value(self, value):
        """Format numeric values for display."""
        if value == 'N/A' or value is None:
            return 'N/A'
        try:
            return f"${value:,.2f}"
        except:
            return str(value)
    
    def _format_percentage(self, value):
        """Format percentage values for display."""
        if value == 'N/A' or value is None:
            return 'N/A'
        try:
            return f"{value:.2f}%"
        except:
            return str(value)
    
    def print_analysis(self) -> None:
        """Print formatted analysis results."""
        if not self.results:
            print("No analysis results available. Run analyze_stock() first.")
            return
        
        print(f"Financial Analysis Results for {self.results['ticker']}:")
        print(f"Analysis Period: {self.results['analysis_period']['start_year']} to {self.results['analysis_period']['end_year']}")
        print("=" * 60)
        
        # Revenue
        rev = self.results['revenue']
        print(f"Revenue (Start): {self._format_value(rev['start_value'])}")
        print(f"Revenue (End): {self._format_value(rev['end_value'])}")
        print(f"Revenue Growth: {self._format_percentage(rev['growth_rate'])}")
        print("-" * 40)
        
        # Net Income
        ni = self.results['net_income']
        print(f"Net Income (Start): {self._format_value(ni['start_value'])}")
        print(f"Net Income (End): {self._format_value(ni['end_value'])}")
        print(f"Net Income Growth: {self._format_percentage(ni['growth_rate'])}")
        print("-" * 40)
        
        # Free Cash Flow
        fcf = self.results['free_cash_flow_per_share']
        print(f"FCF per Share (Start): {self._format_value(fcf['start_value'])}")
        print(f"FCF per Share (End): {self._format_value(fcf['end_value'])}")
        print(f"FCF per Share Growth: {self._format_percentage(fcf['growth_rate'])}")
        print("-" * 40)
        
        # Ratios
        ratios = self.results['ratios']
        print(f"PE Ratio: {self._format_value(ratios['pe_ratio'])}")
        print(f"PEG Ratio: {self._format_value(ratios['peg_ratio'])}")
        print("-" * 40)
        
        # Enterprise Value and Gross Profit
        values = self.results['values']
        print(f"Market Cap: {self._format_value(values['market_cap'])}")
        print(f"Total Debt: {self._format_value(values['total_debt'])}")
        print(f"Cash & Equivalents: {self._format_value(values['cash_and_equivalents'])}")
        print(f"Enterprise Value: {self._format_value(values['enterprise_value'])}")
        print(f"Gross Profit: {self._format_value(values['gross_profit'])}")
        print("=" * 60)