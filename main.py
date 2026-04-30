import pandas as pd
import math

# --- Loading Data ---
df = pd.read_excel('Case_Study.xlsx', 'Database Seasonal', header=2)

sales = df[['Week', 'Year', 'STORE', 'SKU', 'SKU_SIZE', 'Sales Qty', 'On Hand Qty']]
buying = df[['SKU.1', 'SKU_SIZE.1', 'STORE.1', 'Buying Qty']]
prices = df[['SKU.2', 'STORE.2', 'Average Price']]

# --- Cleaning Data ---
sales = sales.dropna(subset=['Week', 'STORE', 'SKU_SIZE'])
prices.columns = ['SKU', 'STORE', 'Average Price']


# ==========================================
# 1st Question
# ==========================================
# Filter sales where item is in stock
sales_with_stock = sales[sales['On Hand Qty'] > 0]

# Calculate average sales per store and SKU
avg_sales = sales_with_stock.groupby(['STORE', 'SKU_SIZE'])['Sales Qty'].mean().reset_index()
avg_sales.columns = ['STORE', 'SKU_SIZE', 'Avg_Sales']

# Filter sales where item is out of stock
sales_stock_out = sales[sales['On Hand Qty'] == 0]

# Merge stockouts with average sales to find potential sales
missed_sales = sales_stock_out.merge(avg_sales, how='left')

# --- Cleaning from nan and zero sales ---
missed_sales = missed_sales.dropna() 
missed_sales = missed_sales[missed_sales['Avg_Sales'] > 0]

# --- Total Missed sales ---
missed_sales_sum_qty = math.ceil(missed_sales['Avg_Sales'].sum()) 
missed_sales_sum_qty_not_round_up = missed_sales['Avg_Sales'].sum()

# --- Missed Sales grouped by STORE and SKU_SIZE ---
missed_sales_by_sku_store = missed_sales.groupby(['STORE', 'SKU_SIZE'])['Avg_Sales'].sum().reset_index() 


# ==========================================
# 2nd Question 
# ==========================================
# Calculate global totals
total_sold_products = sales['Sales Qty'].sum()
total_buied_products = buying['Buying Qty'].sum()

# Standardize column names for buying table
buying.columns = ['SKU', 'SKU_SIZE', 'STORE', 'Buying Qty']

# Merge grouped missed sales with buying data
buying_vs_potential = missed_sales_by_sku_store.merge(buying, how='left')

# Calculate actual sales grouped by STORE and SKU_SIZE
actual_sales_by_store_sku = sales.groupby(['STORE', 'SKU_SIZE'])['Sales Qty'].sum().reset_index()

# Consolidate all data (Potential, Buying, Actual Sales)
coverage_analysis = buying_vs_potential.merge(actual_sales_by_store_sku, how='left')

# Calculate leftover stock based strictly on actual sales
coverage_analysis['Covered'] = coverage_analysis['Buying Qty'] - coverage_analysis['Sales Qty']

# --- Final calculations to answer Question 2 ---
# 1. Total Demand = Actual Sales + Potential Lost Sales
coverage_analysis['Total_Demand'] = coverage_analysis['Sales Qty'] + coverage_analysis['Avg_Sales']

# 2. Buying Gap = Initial Buying Target - Total Demand
coverage_analysis['Buying_Gap'] = coverage_analysis['Buying Qty'] - coverage_analysis['Total_Demand']

# 3. Verdict: Was buying sufficient? (True = Yes, False = No)
coverage_analysis['Enough_Buying'] = coverage_analysis['Buying_Gap'] >= 0

# print("Root Cause Analysis for Stockouts:")
# print(coverage_analysis['Enough_Buying'].value_counts())

# print('Total sold products: ', total_sold_products, '\nTotal buied products: ', total_buied_products)

# ==========================================
# 3rd Question - What would be the increase in value if the company were able to record potential sales?
# ==========================================

price_of_miss = missed_sales.merge(prices, how='left')
price_of_miss['Missed_sales_euro'] = price_of_miss['Avg_Sales'] * price_of_miss['Average Price']
price_of_miss_groupped = price_of_miss.groupby(['SKU', 'STORE'])['Missed_sales_euro'].sum().reset_index()
total_loases = price_of_miss_groupped['Missed_sales_euro'].sum()

# ==========================================
# EXECUTIVE SUMMARY: THE STOCKOUT PARADOX
# ==========================================
def executive_summary_q1_q2_q3():
    print("\n" + "="*50)
    print("EXECUTIVE SUMMARY: THE STOCKOUT PARADOX")
    print("="*50)

    # 1. Macro Level (Global Inefficiency)
    total_leftover = total_buied_products - total_sold_products
    print("\n--- MACRO LEVEL (Global Network) ---")
    print(f"Total Produced/Bought: {total_buied_products:,.0f} units")
    print(f"Total Actually Sold:   {total_sold_products:,.0f} units")
    print(f"Total Unsold Stock:    {total_leftover:,.0f} units (Massive Overstock)")
    print(f"Total Loses:           {total_loases:,.2f} euros")

    # print('Total loses:          ',round(total_loases, 2),'euros')


    # 2. Micro Level (Local Failures)
    buyer_errors = (coverage_analysis['Enough_Buying'] == False).sum()
    dist_errors = (coverage_analysis['Enough_Buying'] == True).sum()

    print("\n--- MICRO LEVEL (Root Cause of Stockouts) ---")
    print(f"Total Stockout Events:    {len(coverage_analysis)}")
    print(f"1. Buyer/Planning Errors: {buyer_errors} cases (Bought wrong items for wrong stores)")
    print(f"2. Distribution Errors:   {dist_errors} cases (Bought enough, but didn't deliver to shelf)")

    # 3. Business Conclusion
    print("\n--- BUSINESS CONCLUSION ---")
    print("The company has a massive OVERSTOCK globally (>7,300 unsold units),")
    print("but still loses sales because buyers allocate the WRONG sizes/models to the WRONG stores.")
    print("="*50 + "\n")


executive_summary_q1_q2_q3()