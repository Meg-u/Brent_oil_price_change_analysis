import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.makedirs("outputs", exist_ok=True)
# Load data
df = pd.read_csv("data/BrentOilPrices.csv")  

# Convert date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows with invalid dates
df = df.dropna(subset=['Date'])

# Sort by date
df = df.sort_values('Date')

# Plot raw prices
plt.figure(figsize=(12, 5))
plt.plot(df['Date'], df['Price'], label='Brent Oil Price')
plt.title('Brent Oil Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("outputs/plot_price_over_time.png")
plt.close()

# Calculate log returns
df['LogReturn'] = np.log(df['Price']) - np.log(df['Price'].shift(1))

# Plot log returns
plt.figure(figsize=(12, 5))
sns.lineplot(x=df['Date'], y=df['LogReturn'])
plt.title('Daily Log Returns of Brent Oil Price')
plt.xlabel('Date')
plt.ylabel('Log Return')
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/plot_log_returns.png")
plt.close()

# Save cleaned data
df.dropna().to_csv("data/brent_oil_cleaned.csv", index=False)
