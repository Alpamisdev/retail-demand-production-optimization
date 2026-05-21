import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

df = pd.read_excel('Case_Study.xlsx', 'Database Permanent', header=1)

products = df[['SKU_SIZE', 'Week', 'Year', 'TIME', 'ID time', 'SALES ACTUAL']].copy()

products_sales = products['SALES ACTUAL']

products = products[products['Year'] > 21].copy()
products['Week'] = pd.to_numeric(products['Week'], errors='coerce').astype('Int64')
products['Year'] = pd.to_numeric(products['Year'], errors='coerce').astype('Int64')
date_time = products['Year'].astype('str') + products['Week'].astype('str').str.zfill(2) + '1'
products['Date'] = pd.to_datetime(date_time, format='%y%W%w')
products = products.set_index('Date').sort_index()

master_calendar = pd.date_range(
    start=products.index.min(),
    end=products.index.max(),
    freq='W-MON'
)
products = products.reindex(master_calendar)
products['SALES ACTUAL'] = products['SALES ACTUAL'].interpolate(method='linear').round()

plot_acf(products['SALES ACTUAL'], lags=104)

# plot_acf(products_sales, lags=204)

plt.title('(ACF)')
plt.xlabel('Лаг (Сдвиг во времени)')
plt.ylabel('Коэффициент автокорреляции')
plt.grid(True)
plt.show()