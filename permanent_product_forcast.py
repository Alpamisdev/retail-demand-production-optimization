import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from statsmodels.tsa.forecasting.stl import STLForecast
from statsmodels.tsa.arima.model import ARIMA

# Loading data
df = pd.read_excel('Case_Study.xlsx', 'Database Permanent', header=1)

products = df[['SKU_SIZE', 'Week', 'Year', 'TIME', 'ID time', 'SALES ACTUAL']].copy()
products = products[products['Year'] > 21].copy()
products = products[products['Year'] < 25].copy()

# Convert Week and Year to numeric
products['Week'] = pd.to_numeric(products['Week'], errors='coerce').astype('Int64')
products['Year'] = pd.to_numeric(products['Year'], errors='coerce').astype('Int64')

date_time = products['Year'].astype('str') + products['Week'].astype('str').str.zfill(2) + '1'
products['Date'] = pd.to_datetime(date_time, format='%y%W%w')

# Build master calendar anchored on Monday
master_calendar = pd.date_range(
    start=products['Date'].min(),
    end=products['Date'].max(),
    freq='W-MON',
    name='Date'
)

# Find missing weeks
missing_weeks = master_calendar.difference(products['Date'])
print(f"Missing weeks: {len(missing_weeks)}")
print(missing_weeks)

# Reindex to full calendar
products_full = (
    products
    .set_index('Date')
    .reindex(master_calendar)
)

missing = products_full[products_full['SALES ACTUAL'].isna()]
print(missing[['SKU_SIZE', 'SALES ACTUAL']])

# Fill missing weeks with linear interpolation rounded to integers
products_full['SALES ACTUAL'] = products_full['SALES ACTUAL'].interpolate(method='linear').round().astype(int)
products_full['SKU_SIZE'] = products_full['SKU_SIZE'].ffill()

print(products_full[products_full.index.isin(missing_weeks)])

ts = products_full['SALES ACTUAL'].astype(float)

# Build Holt-Winters model with additive trend and seasonality
# model = ExponentialSmoothing(
#     ts,
#     trend='add',
#     damped_trend=True,
#     seasonal='mul',
#     seasonal_periods=52
# )

# Вариант A — только damped
# model = ExponentialSmoothing(
#     ts,
#     trend='add',
#     damped_trend=True,
#     seasonal='add',
#     seasonal_periods=52
# )

# Вариант B — только mul seasonal
# model = ExponentialSmoothing(
#     ts,
#     trend='add',
#     damped_trend=False,
#     seasonal='mul',
#     seasonal_periods=52
# )

model = ExponentialSmoothing(
    ts,
    trend=None, 
    seasonal=None 
)

fit = model.fit(
    # smoothing_level=0.2,    # alpha
    # smoothing_trend=0.4,   # beta
    # smoothing_seasonal=0.5, # gamma
    # optimized=True
)
fitted = fit.fittedvalues

# Forecast next 10 weeks
forecast = fit.forecast(10)
print(forecast)

bias = ts.mean() - fitted.mean()
forecast_corrected = forecast + bias
print(f"Bias correction: +{bias:.2f} units")
print(forecast_corrected)




# === Model quality metrics ===
mae = mean_absolute_error(ts, fitted)
rmse = np.sqrt(mean_squared_error(ts, fitted))
mape = np.mean(np.abs((ts - fitted) / ts.replace(0, np.nan))) * 100

print("=== Model Quality ===")
print(f"MAE  (mean absolute error):       {mae:.2f} units")
print(f"RMSE (root mean squared error):   {rmse:.2f} units")
print(f"MAPE (mean absolute % error):     {mape:.1f}%")
print(f"SSE  (sum of squared errors):     {fit.sse:.2f}")

print("\n=== Model Parameters ===")
print(f"Alpha (level):      {fit.params['smoothing_level']:.4f}  — how fast the model forgets the past")
print(f"Beta  (trend):      {fit.params['smoothing_trend']:.4f}  — how strongly trend is weighted")
print(f"Gamma (seasonal):   {fit.params['smoothing_seasonal']:.4f}  — how strongly seasonality is weighted")

print("\n=== Forecast Summary ===")
print(f"Mean actual sales:   {ts.mean():.2f}")
print(f"Mean forecast:       {forecast.mean():.2f}")
print(f"Forecast direction:  {'↑ growing' if forecast.iloc[-1] > forecast.iloc[0] else '↓ declining'}")

print(f"\nLast date in training data: {ts.index[-1]}")
print(f"Total weeks in training:    {len(ts)}")

# Visualization
plt.figure(figsize=(14, 5))
plt.plot(ts, label='Actual')
plt.plot(fitted, label='Fitted')
plt.plot(forecast, label='Forecast', linestyle='--')
plt.legend()
plt.show()