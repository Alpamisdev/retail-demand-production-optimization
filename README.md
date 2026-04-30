# Retail Diagnostic: Stockout Analysis

This script analyzes distribution efficiency by calculating potential lost sales caused by out-of-stock events (`On Hand Qty = 0`), leveraging historical demand data.

## Directory Structure

The source data file is not included in this repository. To run the script, you must manually place the dataset in the root directory and name it exactly `Case_Study.xlsx`.
```text
├── Case_Study.xlsx   # Source dataset containing the 'Database Seasonal' sheet (add manually)
├── main.py           # Core analysis script
├── requirements.txt  # libraries to install
└── README.md         # This documentation

==================================================
EXECUTIVE SUMMARY: THE STOCKOUT PARADOX
==================================================

--- MACRO LEVEL (Global Network) ---
Total Produced/Bought: 12,407 units
Total Actually Sold:   5,080 units
Total Unsold Stock:    7,327 units (Massive Overstock)
Total Loses:           83,835.79 euros

--- MICRO LEVEL (Root Cause of Stockouts) ---
Total Stockout Events:    360
1. Buyer/Planning Errors: 337 cases (Bought wrong items for wrong stores)
2. Distribution Errors:   23 cases (Bought enough, but didn't deliver to shelf)

--- BUSINESS CONCLUSION ---
The company has a massive OVERSTOCK globally (>7,300 unsold units),
but still loses sales because buyers allocate the WRONG sizes/models to the WRONG stores.
==================================================