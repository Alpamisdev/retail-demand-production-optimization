import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. Load and filter data
df = pd.read_excel('Case_Study.xlsx', 'Database Permanent', header=1)
products = df[['SKU_SIZE', 'Week', 'Year', 'TIME', 'ID time', 'SALES ACTUAL']].copy()

# Apply strict year filter
products = products[products['Year'] > 21].copy()

# 2. Date conversion
products['Week'] = pd.to_numeric(products['Week'], errors='coerce').astype('Int64')
products['Year'] = pd.to_numeric(products['Year'], errors='coerce').astype('Int64')
date_time = products['Year'].astype('str') + products['Week'].astype('str').str.zfill(2) + '1'
products['Date'] = pd.to_datetime(date_time, format='%y%W%w')

# 3. Build master calendar anchored on Monday
master_calendar = pd.date_range(
    start=products['Date'].min(),
    end=products['Date'].max(),
    freq='W-MON',
    name='Date'
)

# Reindex to full calendar to identify gaps
products_full = products.set_index('Date').reindex(master_calendar)
missing_weeks = master_calendar.difference(products['Date'])
missing_data = products_full[products_full['SALES ACTUAL'].isna()]

print("=== Missing Data Identified ===")
print(missing_data[['SKU_SIZE', 'SALES ACTUAL']])

# 4. Impute missing values
# Step A: 5-week centered rolling median
rolling_median = products_full['SALES ACTUAL'].rolling(window=5, min_periods=1, center=True).median()
products_full['SALES ACTUAL'] = products_full['SALES ACTUAL'].fillna(rolling_median)

# Step B: Fallback to global median for edge cases
global_median = products_full['SALES ACTUAL'].median()
products_full['SALES ACTUAL'] = products_full['SALES ACTUAL'].fillna(global_median)

# Step C: Round to integers
products_full['SALES ACTUAL'] = products_full['SALES ACTUAL'].round().astype(int)

print("\n=== Imputed Values for Missing Weeks ===")
print(products_full[products_full.index.isin(missing_weeks)][['SKU_SIZE', 'SALES ACTUAL']])

# 5. Build Simple Exponential Smoothing (SES) Model
ts = products_full['SALES ACTUAL'].astype(float)
model = ExponentialSmoothing(ts, trend=None, seasonal=None)
fit = model.fit()
fitted = fit.fittedvalues

# 6. Forecasting
forecast_horizon = 53
forecast = fit.forecast(forecast_horizon)

# 7. Model quality metrics
mae = mean_absolute_error(ts, fitted)
rmse = np.sqrt(mean_squared_error(ts, fitted))
mape = np.mean(np.abs((ts - fitted) / ts.replace(0, np.nan))) * 100

print("\n=== Model Quality ===")
print(f"MAE  (Mean Absolute Error):       {mae:.2f} units")
print(f"RMSE (Root Mean Squared Error):   {rmse:.2f} units")
print(f"MAPE (Mean Absolute % Error):     {mape:.1f}%")
print(f"SSE  (Sum of Squared Errors):     {fit.sse:.2f}")

print("\n=== Model Parameters ===")
print(f"Alpha (Smoothing Level): {fit.params['smoothing_level']:.4f}")

print("\n=== Forecast Summary ===")
print(f"Historical Mean (Actuals):   {ts.mean():.2f}")
print(f"Current Run Rate (Forecast): {forecast.mean():.2f}")

# Forecast direction logic
if forecast.iloc[-1] > forecast.iloc[0]:
    direction = '↑ Growing'
elif forecast.iloc[-1] < forecast.iloc[0]:
    direction = '↓ Declining'
else:
    direction = '→ Flat (Expected Value)'
print(f"Forecast Direction:          {direction}")

print(f"\n=== Next {forecast_horizon} Weeks Forecast ===")
print(forecast.round(2))

# 8. Visualization
plt.figure(figsize=(14, 5))
plt.plot(ts, label='Actual Sales', color='black')
plt.plot(fitted, label='Fitted (SES)', alpha=0.7, color='blue')
plt.plot(forecast, label='Forecast (SES)', linestyle='--', color='red', linewidth=2)

plt.legend()
plt.title('Simple Exponential Smoothing (SES) - Run Rate Forecast')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()