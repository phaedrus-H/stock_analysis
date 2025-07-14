# Stock Analysis Tool

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

### 2. Intelligent Start Date & End Date Selection
- Default preference order: 2019 → 2020 → 2021 → 2022
- Automatically selects the earliest year with available revenue, net income and free cash flow data
- Displays the selected start year in the output
- Automatically selects any 2024 date as the end date with available revenue, net income and free cash flow data

### 3. Excel Output
- Results are automatically exported to `{TICKER}-result.xlsx`
- Formatted output with clear sections and proper value formatting
- Includes analysis start year information
- The Excel file contains a structured table with following columns:
    |--------|------------|-----------------|---------------|----------------|----------------|--------------|---------------|-------------|-----------|------------|----------|-----------|------------|------------|--------------------|------------------|--------------|
    | Ticker | Start Year | Revenue (Start) | Revenue (End) | Revenue Growth | Income (Start) | Income (End) | Income Growth | FCF (Start) | FCF (End) | FCF Growth | PE Ratio | PEG Ratio | Market Cap | Total Debt | Cash & Equivalents | Enterprise Value | Gross Profit |
    |--------|------------|-----------------|---------------|----------------|----------------|--------------|---------------|-------------|-----------|------------|----------|-----------|------------|------------|--------------------|------------------|--------------|

## Installation

1. Clone the repository using `git clone git@github.com:phaedrus-H/stock_analysis.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`. Or run `pip install -e .`

## Usage

### Command Line Usage

```bash
# Make sure you're in the project directory and virtual environment is activated
python -m stock_analysis.main
```


## Usage Methods

### Method 1: Interactive mode - Prompts for Ticker
```bash
# Make sure you're in the project directory and virtual environment is activated
# Interactive mode (prompts for ticker)
python -m stock_analysis.main
```

### Method 2: Single Ticker Analysis
```bash
# Make sure you're in the project directory and virtual environment is activated
# Command line argument
python -m stock_analysis.main AAPL
```

### Method 2: Batch Analysis (Multiple Tickers)
```bash
# Make sure you're in the project directory and virtual environment is activated
# Analyze multiple tickers at once
python -m stock_analysis.main AAPL MSFT GOOGL TSLA
```

## Data File Structure Requirements

```
stock_analysis/
├── data/
│   ├── aapl-financials.xlsx
│   ├── msft-financials.xlsx
│   ├── googl-financials.xlsx
│   └── tsla-financials.xlsx
├── src/
│   └──   stock_analysis/
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
│   └── (your XLSX files here)
├── output/
│   └── (output XLSX files get written here)
├── requirements.txt
├── setup.py
└── README.md
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

#### Adjust End Year Preferences
Modify the `end_year` parameter in the `find_best_end_year()` method in `analyzer.py`:
```python
end_year = '2024'
```

#### Adjust Start Year Preferences
Edit the `preferred_years` list in the `find_best_start_year()` method in `analyzer.py`:
```python
preferred_years = [2019, 2020, 2021, 2022, 2023, 2024]
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