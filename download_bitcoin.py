import yfinance as yf
import pandas as pd
from datetime import datetime

# Calculate dates
end_date = datetime(2024, 12, 31)  # End at December 31, 2024
start_date = datetime(2014, 1, 1)  # Start from January 1, 2014

# Download Bitcoin data
print(f"Downloading Bitcoin data from {start_date.date()} to {end_date.date()}")
bitcoin = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Clean and format data
bitcoin = bitcoin.reset_index()
bitcoin.columns = [col[0] if isinstance(col, tuple) else col for col in bitcoin.columns]  # Flatten MultiIndex columns
bitcoin = bitcoin[['Date', 'Close', 'High', 'Low', 'Open', 'Volume']]  # Reorder columns
bitcoin = bitcoin.dropna()  # Remove any NA rows

# Save to CSV
bitcoin.to_csv('bitcoin_data.csv', index=False)

print(f"Data saved to bitcoin_data.csv")
print(f"Number of records: {len(bitcoin)}")
print(f"\nDate range: {bitcoin['Date'].min().date()} to {bitcoin['Date'].max().date()}") 