import pandas as pd
import math

df = pd.read_excel('Case_Study.xlsx', 'Database Seasonal', header=2)

sales = df[['Week', 'Year', 'STORE', 'SKU', 'SKU_SIZE', 'Sales Qty', 'On Hand Qty']]

buying = df[['SKU.1', 'SKU_SIZE.1', 'STORE.1', 'Buying Qty']]

prices = df[['SKU.2', 'STORE.2', 'Average Price']]

# print(sales.head(5))
# print(buying.head(5))
# print(prices.head(5))

sales = sales.dropna(subset=['Week', 'STORE', 'SKU_SIZE'])
# print(sales.shape)

sales_with_stock = sales[sales['On Hand Qty'] > 0]

avg_sales = sales_with_stock.groupby(['STORE', 'SKU_SIZE'])['Sales Qty'].mean().reset_index()
avg_sales.columns = ['STORE', 'SKU_SIZE', 'Avg_Sales']

# print(avg_sales.head(10))
# print('rows:', avg_sales.shape[0])

sales_stock_out = sales[sales['On Hand Qty'] == 0]

# print(sales_stock_out.head(10))
# print('rows: ', sales_stock_out.shape[0])


missed_sales = sales_stock_out.merge(avg_sales, how='left')
# print(missed_sales.head(10))
# print('rows: ', missed_sales.shape[0])

missed_sales = missed_sales.dropna()
missed_sales = missed_sales[missed_sales['Avg_Sales'] > 0]

# print(missed_sales.head(10))
# print('rows: ', missed_sales.shape[0])

missed_sales_sum_qty = math.ceil(missed_sales['Avg_Sales'].sum())
missed_sales_sum_qty_not_round_up = missed_sales['Avg_Sales'].sum()
print('round up: ', missed_sales_sum_qty)
print('not rounded: ', missed_sales_sum_qty_not_round_up)