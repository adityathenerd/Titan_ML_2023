import numpy as np
import pandas as pd

# Generate example sleep duration data for a week (in hours)
np.random.seed(42)
days = 7
hours_per_day = 24
data = np.random.normal(loc=7, scale=1, size=days * hours_per_day)

# Create a DataFrame with timestamps and sleep duration values
date_rng = pd.date_range(start='2023-08-01', periods=days * hours_per_day, freq='H')
sleep_df = pd.DataFrame(data, columns=['SleepDuration'], index=date_rng)

# Set the sleep duration threshold (in hours)
sleep_threshold = 6

# Check sleep duration and deploy an alerting system if below the threshold
for index, row in sleep_df.iterrows():
    if row['SleepDuration'] < sleep_threshold:
        print(f"ALERT: Sleep duration ({row['SleepDuration']:.2f} hours) on {index.date()} is below the threshold!")

# Display sleep duration threshold information
print(f"Sleep Duration Threshold: {sleep_threshold} hours")