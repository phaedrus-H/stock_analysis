"""
Module for loading and preprocessing financial data from CSV files.
"""

import pandas as pd
from typing import Dict, List
from pathlib import Path


class FinancialDataLoader:
    """Handles loading and preprocessing of financial data from Excel files."""
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize the data loader.
        
        Args:
            data_directory: Path to directory containing Excel files
        """
        self.data_directory = Path(data_directory)
        self.data: Dict[str, pd.DataFrame] = {}
    
    def load_financial_data(self, sheet_mapping: Dict[str, str], excel_file: str) -> Dict[str, pd.DataFrame]:
        """
        Load financial data from Excel file sheets.
        
        Args:
            sheet_mapping: Dictionary mapping data types to sheet names
            excel_file: Name of the Excel file to read from
            
        Returns:
            Dictionary of loaded and processed DataFrames
        """
        file_path = self.data_directory / excel_file
        
        try:
            # Load all sheets at once for efficiency
            all_sheets = pd.read_excel(file_path, sheet_name=list(sheet_mapping.values()))
            
            for data_type, sheet_name in sheet_mapping.items():
                df = all_sheets[sheet_name]
                self.data[data_type] = self._preprocess_dataframe(df)
                print(f"✓ Loaded {data_type} data from sheet '{sheet_name}'")
                
        except FileNotFoundError:
            print(f"✗ Error: File {excel_file} not found in {self.data_directory}")
            raise
        except ValueError as e:
            if "Worksheet" in str(e):
                print(f"✗ Error: One or more sheets not found in {excel_file}. Available sheets: {pd.ExcelFile(file_path).sheet_names}")
            else:
                print(f"✗ Error reading {excel_file}: {e}")
            raise
        except Exception as e:
            print(f"✗ Error loading {excel_file}: {e}")
            raise
        
        return self.data
    
    def _preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess DataFrame by transposing and converting to numeric.
        
        Args:
            df: Raw DataFrame from Excel sheet
            
        Returns:
            Processed DataFrame with datetime index
        """
        # Transpose so years are columns and metrics are rows
        df = df.transpose()
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    
        #Convert columns to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set datetime index
        df.index = pd.to_datetime(df.index)
        
        return df
    
    def get_data(self, data_type: str) -> pd.DataFrame:
        """Get specific financial data type."""
        if data_type not in self.data:
            raise ValueError(f"Data type '{data_type}' not loaded")
        return self.data[data_type]
