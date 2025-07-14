# Stock Analysis Tool

A Python package for analyzing financial data from CSV files extracted from Excel spreadsheets.

## Features

- Load and preprocess financial data from multiple CSV files
- Calculate growth rates for various financial metrics
- Compute enterprise value and other key financial ratios
- Generate comprehensive financial analysis reports

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage

### Basic Usage

```python
from stock_analysis import StockAnalyzer

# Initialize the analyzer
analyzer = StockAnalyzer(data_directory="data")

# Define your CSV files
file_mapping = {
    'income': 'reax-financials.xlsx - Income-Annual.csv',
    'balance_sheet': 'reax-financials.xlsx - Balance-Sheet-Annual.csv',
    'cash_flow': 'reax-financials.xlsx - Cash-Flow-Annual.csv',
    'ratios': 'reax-financials.xlsx - Ratios-Annual.csv'
}

# Load data and perform analysis
analyzer.load_data(file_mapping)
results = analyzer.analyze_stock(start_year="2019-12-31", end_year="2024-12-31")
analyzer.print_analysis()
```

### Command Line Usage

```bash
# Make sure you're in the project directory and virtual environment is activated
python -m stock_analysis.main
```

## Data Structure

Place your CSV files in the `data/` directory. The expected file structure is:

```
data/
├── reax-financials.xlsx - Income-Annual.csv
├── reax-financials.xlsx - Balance-Sheet-Annual.csv
├── reax-financials.xlsx - Cash-Flow-Annual.csv
└── reax-financials.xlsx - Ratios-Annual.csv
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
```

### Linting

```bash
flake8 src/
```

## Project Structure

```
stock_analysis/
├── src/
│   └── stock_analysis/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── calculator.py
│       ├── data_loader.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_calculator.py
│   └── test_data_loader.py
├── data/
│   └── (your CSV files here)
├── requirements.txt
├── setup.py
└── README.md
```


# Stock Analysis Tool - Usage Guide

## Overview
The updated stock analysis tool now supports multiple tickers, automatic file detection, Excel output, and intelligent start year selection.

## Key Features

### 1. Ticker-based File Detection
- The tool automatically looks for Excel files with the pattern: `{ticker}-financials.xlsx`
- Supports multiple case variations (lowercase, uppercase, mixed case)
- Example: For ticker "AAPL", it looks for:
  - `aapl-financials.xlsx`
  - `AAPL-financials.xlsx`
  - `AAPL-financials.xlsx`

### 2. Intelligent Start Year Selection
- Default preference order: 2019 → 2020 → 2021 → 2022
- Automatically selects the earliest year with available revenue data
- Displays the selected start year in the output

### 3. Excel Output
- Results are automatically exported to `{TICKER}-result.xlsx`
- Formatted output with clear sections and proper value formatting
- Includes analysis period information

## Usage Methods

### Method 1: Single Ticker Analysis
```bash
# Interactive mode (prompts for ticker)
python main.py

# Command line argument
python main.py AAPL
```

### Method 2: Batch Analysis (Multiple Tickers)
```bash
# Analyze multiple tickers at once
python main.py AAPL MSFT GOOGL TSLA
```

## File Structure Requirements

```
project/
├── data/
│   ├── aapl-financials.xlsx
│   ├── msft-financials.xlsx
│   ├── googl-financials.xlsx
│   └── tsla-financials.xlsx
├── stock_analysis/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── calculator.py
│   └── data_loader.py
└── main.py
```

## Expected Excel File Format
Each ticker's Excel file should contain these sheets:
- `Income-Annual`
- `Balance-Sheet-Annual`
- `Cash-Flow-Annual`
- `Ratios-Annual`

## Output Files
For each analyzed ticker, the tool creates:
- `{TICKER}-result.xlsx` - Detailed analysis results in Excel format
- Console output with formatted results

## Error Handling
- **File not found**: Clear error message with expected filename
- **Missing data**: Graceful handling with 'N/A' values
- **Invalid calculations**: Robust error checking for edge cases
- **Batch mode**: Continues processing other tickers if one fails

## Example Output Structure

### Console Output
```
Financial Analysis Results for AAPL:
Analysis Period: 2019-12-31 to 2024-12-31
============================================================
Revenue (Start): $260,174.00
Revenue (End): $383,285.00
Revenue Growth: 47.35%
...
```

### Excel Output
The Excel file contains a structured table with:
- Ticker symbol
- Analysis period
- Revenue analysis (start, end, growth)
- Net income analysis
- Free cash flow analysis
- Financial ratios
- Other key metrics

## Customization Options

### Modify Sheet Names
Edit the `sheet_mapping` dictionary in `main.py`:
```python
sheet_mapping = {
    'income': 'Your-Income-Sheet-Name',
    'balance_sheet': 'Your-Balance-Sheet-Name',
    'cash_flow': 'Your-Cash-Flow-Sheet-Name',
    'ratios': 'Your-Ratios-Sheet-Name'
}
```

### Change Analysis Period
Modify the `end_year` parameter in the `analyze_stock()` call:
```python
results = analyzer.analyze_stock(end_year="2023-12-31")
```

### Adjust Start Year Preferences
Edit the `preferred_years` list in the `find_best_start_year()` method:
```python
preferred_years = ["2018-12-31", "2019-12-31", "2020-12-31"]
```

## Dependencies
Make sure you have the required packages installed:
```bash
pip install pandas openpyxl
```

## Troubleshooting

### Common Issues
1. **"No financial data file found"**: Ensure the Excel file follows the naming convention
2. **"Data must be loaded first"**: The system automatically loads data, this shouldn't occur
3. **Sheet not found**: Check that your Excel file contains the expected sheet names
4. **Invalid calculations**: Usually due to missing or corrupted data in the source Excel file

### Tips
- Use consistent ticker symbols (preferably uppercase)
- Ensure