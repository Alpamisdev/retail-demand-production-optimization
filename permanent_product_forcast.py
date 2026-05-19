import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

# Loading data
df = pd.read_excel('Case_Study.xlsx', 'Database Permanent', header=1)

products = df[['SKU_SIZE', 'Week', 'Year', 'TIME', 'ID time', 'SALES ACTUAL']].copy()
products = products[products['Year'] > 21].copy()


# getting date format from week and year columns
products['Week'] = pd.to_numeric(products['Week'], errors='coerce').astype('Int64')
products['Year'] = pd.to_numeric(products['Year'], errors='coerce').astype('Int64')

date_time = products['Year'].astype('str') + products['Week'].astype('str').str.zfill(2) + '1'

products['Date'] = pd.to_datetime(date_time, format='%y%W%w')



# Исправляем якорь
master_calendar = pd.date_range(
    start=products['Date'].min(),
    end=products['Date'].max(),
    freq='W-MON',
    name='Date'
)

# Находим пропущенные недели
missing_weeks = master_calendar.difference(products['Date'])
print(f"Пропущено недель: {len(missing_weeks)}")
print(missing_weeks)

products_full = (
    products
    .set_index('Date')
    .reindex(master_calendar)
)

missing = products_full[products_full['SALES ACTUAL'].isna()]
print(missing[['SKU_SIZE', 'SALES ACTUAL']])