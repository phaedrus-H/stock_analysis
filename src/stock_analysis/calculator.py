"""
Module for financial calculations and metrics.
"""

import pandas as pd
import numpy as np
from typing import Union, Dict, Any


class FinancialCalculator:
    """Performs various financial calculations on stock data."""
    
    def __init__(self, data: Dict[str, pd.DataFrame]):
        """
        Initialize calculator with financial data.
        
        Args:
            data: Dictionary containing financial DataFrames
        """
        self.income_data = data.get('income')
        self.balance_sheet_data = data.get('balance_sheet')
        self.cash_flow_data = data.get('cash_flow')
        self.ratios_data = data.get('ratios')
    
    def calculate_growth_rate(self, start_year: str, end_year: str, 
                            data_type: str, metric: str) -> Union[float, str]:
        """
        Calculate growth rate between two years for a specific metric.
        
        Args:
            start_year: Starting year (e.g., '2019-12-31')
            end_year: Ending year (e.g., '2024-12-31')
            data_type: Type of data ('income', 'balance_sheet', 'cash_flow', 'ratios')
            metric: Metric name to calculate growth for
            
        Returns:
            Growth rate as percentage or 'N/A' if calculation not possible
        """
        data_map = {
            'income': self.income_data,
            'balance_sheet': self.balance_sheet_data,
            'cash_flow': self.cash_flow_data,
            'ratios': self.ratios_data
        }
        
        df = data_map.get(data_type)
        if df is None:
            return 'N/A'
        
        try:
            start_value = df.loc[start_year, metric]
            end_value = df.loc[end_year, metric]
            
            # Check for invalid values
            if (pd.isna(start_value) or pd.isna(end_value) or 
                start_value == 0 or np.isinf(start_value) or np.isinf(end_value)):
                return 'N/A'
            
            # Calculate growth rate
            growth_rate = ((end_value - start_value) / abs(start_value)) * 100
            
            # Check if result is valid
            if np.isnan(growth_rate) or np.isinf(growth_rate):
                return 'N/A'
            
            return growth_rate
            
        except (KeyError, IndexError, TypeError):
            return 'N/A'
    
    def calculate_enterprise_value(self, year: str) -> Union[float, str]:
        """
        Calculate Enterprise Value = Market Cap + Total Debt - Cash and Equivalents
        
        Args:
            year: Year for calculation (e.g., '2024-12-31')
            
        Returns:
            Enterprise value or 'N/A' if calculation not possible
        """
        try:
            market_cap = self.ratios_data.loc[year, 'Market Capitalization']
            total_debt = self.balance_sheet_data.loc[year, 'Total Debt']
            cash_and_equivalents = self.balance_sheet_data.loc[year, 'Cash & Equivalents']
            
            # Check for invalid values
            if (pd.isna(market_cap) or pd.isna(total_debt) or pd.isna(cash_and_equivalents) or
                np.isinf(market_cap) or np.isinf(total_debt) or np.isinf(cash_and_equivalents)):
                return 'N/A'
            
            enterprise_value = market_cap + total_debt - cash_and_equivalents
            
            # Check if result is valid
            if np.isnan(enterprise_value) or np.isinf(enterprise_value):
                return 'N/A'
            
            return enterprise_value
            
        except (KeyError, IndexError, TypeError):
            return 'N/A'
    
    def get_metric_value(self, year: str, data_type: str, metric: str) -> Union[float, str]:
        """
        Get a specific metric value for a given year.
        
        Args:
            year: Year (e.g., '2024-12-31')
            data_type: Type of data ('income', 'balance_sheet', 'cash_flow', 'ratios')
            metric: Metric name
            
        Returns:
            Metric value or 'N/A' if not available
        """
        data_map = {
            'income': self.income_data,
            'balance_sheet': self.balance_sheet_data,
            'cash_flow': self.cash_flow_data,
            'ratios': self.ratios_data
        }
        
        df = data_map.get(data_type)
        if df is None:
            return 'N/A'
        
        try:
            value = df.loc[year, metric]
            
            # Check for invalid values
            if pd.isna(value) or np.isinf(value):
                return 'N/A'
            
            return value
            
        except (KeyError, IndexError, TypeError):
            return 'N/A'
    
    def get_available_years(self, data_type: str) -> list:
        """
        Get list of available years for a specific data type.
        
        Args:
            data_type: Type of data ('income', 'balance_sheet', 'cash_flow', 'ratios')
            
        Returns:
            List of available years as strings
        """
        data_map = {
            'income': self.income_data,
            'balance_sheet': self.balance_sheet_data,
            'cash_flow': self.cash_flow_data,
            'ratios': self.ratios_data
        }
        
        df = data_map.get(data_type)
        if df is None:
            return []
        
        return sorted(df.index.strftime('%Y-%m-%d').tolist())
    
    def validate_data_availability(self, year: str, data_type: str, metric: str) -> bool:
        """
        Check if data is available for a specific year, data type, and metric.
        
        Args:
            year: Year to check
            data_type: Type of data
            metric: Metric name
            
        Returns:
            True if data is available and valid, False otherwise
        """
        value = self.get_metric_value(year, data_type, metric)
        return value != 'N/A' and value is not None