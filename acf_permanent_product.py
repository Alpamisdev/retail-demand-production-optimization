import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

df = pd.read_excel('Case_Study.xlsx', 'Database Permanent', header=1)

products = df[['SKU_SIZE', 'Week', 'Year', 'TIME', 'ID time', 'SALES ACTUAL']].copy()

products_sales = products['SALES ACTUAL']

plot_acf(products_sales, lags=204)

plt.title('(ACF)')
plt.xlabel('Лаг (Сдвиг во времени)')
plt.ylabel('Коэффициент автокорреляции')
plt.grid(True)
plt.show()