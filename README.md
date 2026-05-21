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

# Strategic Demand Forecasting: Volatile SKU Analysis

This repository contains a forecasting pipeline for low-volume SKUs with stochastic demand profiles. It utilizes Simple Exponential Smoothing (SES) to extract the true baseline Run Rate, bypassing classical models (Holt-Winters, SBA) that mathematically fail and overfit to noise on intermittent data.

## Directory Structure

The source data file is not included in this repository. To run the scripts, you must manually place the dataset in the root directory and name it exactly `Case_Study.xlsx`.

├── Case_Study.xlsx                 # Source dataset containing 'Database Permanent' (add manually)
├── acf_permanent_pr...py           # Autocorrelation (ACF) testing script to prove white noise
├── exs.py                          # Core SES forecasting and imputation script (Primary Model)
├── main.py                         # General execution and data processing
├── permanent_produc...py           # Legacy Holt-Winters testing (Dismissed due to overfitting)
├── requirements.txt                # Python dependencies
└── README.md                       # This documentation

==================================================
EXECUTIVE SUMMARY: ADAPTIVE FORECASTING FOR NOISE
==================================================

--- MACRO LEVEL (Data & Architecture) ---
Historical Window:  2022-2024 (156 weeks)
Data Cleansing:     COVID-19 period (2020-2021) was surgically removed to prevent extreme macroeconomic anomalies from poisoning the model weights. Technical NaN gaps were imputed via a 5-week centered rolling median to prevent false geometric trends.
Model Selection:    Simple Exponential Smoothing (SES) - Trend and Seasonality disabled. ACF testing proved the demand is stochastic "white noise".

--- MICRO LEVEL (Forecast Metrics for Target SKU) ---
Historical Mean (3yr):    5.34 units/week
Current Run Rate (SES):   7.58 units/week (Actual market velocity)
Alpha (Smoothing Factor): 0.13 (Filters 87% of historical noise, trusts 13% of recent shifts)
MAE (Absolute Error):     2.12 units
RMSE (Deviation):         3.00 units (Baseline for Safety Stock calculation)

--- BUSINESS CONCLUSION ---
Procurement based on the standard 3-year historical average (5.34 units) will result in a ~30% stockout deficit. The market demand has shifted. The SES model identifies a stable expected value (Run Rate) of 7.58 units/week. 

Classical models fail here by overfitting to random weekly spikes. Supply Chain operations must plan Cycle Stock against the flat 7.58 rate, using RMSE (3.00) for Safety Stock, and apply manual "Event Overrides" (multipliers) only for known seasonal anomalies like December holidays.
==================================================