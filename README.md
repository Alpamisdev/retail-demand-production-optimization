# Retail Diagnostic: Stockout Analysis

This script analyzes distribution efficiency by calculating potential lost sales caused by out-of-stock events (`On Hand Qty = 0`), leveraging historical demand data.

## Directory Structure

The source data file is not included in this repository. To run the script, you must manually place the dataset in the root directory and name it exactly `Case_Study.xlsx`.
```text
├── Case_Study.xlsx   # Source dataset containing the 'Database Seasonal' sheet (add manually)
├── main.py           # Core analysis script
├── requirements.txt  # libraries to install
└── README.md         # This documentation