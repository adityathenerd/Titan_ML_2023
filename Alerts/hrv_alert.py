import numpy as np
import pandas as pd

# Generate example HRV data for a week (in milliseconds)
np.random.seed(42)
days = 7
hours_per_day = 24
data = np.random.normal(loc=1000, scale=50, size=days * hours_per_day)

# Create a DataFrame with timestamps and HRV values
date_rng = pd.date_range(start='2023-08-01', periods=days * hours_per_day, freq='H')
hrv_df = pd.DataFrame(data, columns=['HRV'], index=date_rng)

# Calculate the mean and standard deviation of HRV
mean_hrv = hrv_df['HRV'].mean()
std_hrv = hrv_df['HRV'].std()

# Define the normal range based on mean +/- 2 * standard deviation
lower_limit = mean_hrv - 2 * std_hrv
upper_limit = mean_hrv + 2 * std_hrv

# Check HRV values and deploy an alerting system if out of range
for index, row in hrv_df.iterrows():
    if row['HRV'] < lower_limit or row['HRV'] > upper_limit:
        print(f"ALERT: HRV value ({row['HRV']:.2f} ms) on {index} is out of normal range!")
print(f"Normal Range: {lower_limit:.2f} ms to {upper_limit:.2f} ms")
