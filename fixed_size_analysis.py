"""
Kelly Criterion Analysis Utility

This script performs fixed-size backtesting ($100 per trade) to determine
the true characteristics of the RSI strategy, which are then used to
calculate the optimal Kelly fraction.

The analysis shows:
- Win Rate: 44.24%
- Win/Loss Ratio: 4.73
- Average Win: 10.09%
- Average Loss: 2.14%

These metrics lead to a Kelly fraction of 32.44%, which is used in
the main strategy implementation.
"""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator

# Load and prepare data
df = pd.read_csv('bitcoin_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate RSI
RSI_WINDOW = 5
rsi = RSIIndicator(close=df['Close'], window=RSI_WINDOW)
df['RSI'] = rsi.rsi()

# Initialize strategy variables
FIXED_TRADE_SIZE = 100  # Fixed $100 per trade
trades = []
position = False
current_shares = 0

# Run strategy
for i in range(RSI_WINDOW, len(df)):
    current_price = df['Close'].iloc[i]
    current_rsi = df['RSI'].iloc[i]
    
    # Long entry signal
    if not position and current_rsi > 70:
        position = True
        entry_price = current_price
        current_shares = FIXED_TRADE_SIZE / current_price
        
        trades.append({
            'date': df.index[i],
            'type': 'BUY',
            'price': current_price,
            'shares': current_shares,
            'trade_size': FIXED_TRADE_SIZE
        })
    
    # Long exit signal
    elif position and current_rsi < 70:
        position = False
        exit_value = current_shares * current_price
        pnl = exit_value - FIXED_TRADE_SIZE
        
        trades.append({
            'date': df.index[i],
            'type': 'SELL',
            'price': current_price,
            'shares': current_shares,
            'trade_size': FIXED_TRADE_SIZE,
            'pnl': pnl,
            'return': (pnl / FIXED_TRADE_SIZE) * 100
        })
        current_shares = 0

# Convert to DataFrame and analyze
trades_df = pd.DataFrame(trades)
sell_trades = trades_df[trades_df['type'] == 'SELL']

# Calculate key metrics
wins = sell_trades[sell_trades['pnl'] > 0]
losses = sell_trades[sell_trades['pnl'] <= 0]

win_rate = len(wins) / len(sell_trades)
avg_win = wins['return'].mean() / 100  # Convert percentage to decimal
avg_loss = abs(losses['return'].mean()) / 100  # Convert percentage to decimal
win_loss_ratio = avg_win / avg_loss

# Calculate Kelly fraction
kelly = win_rate - ((1 - win_rate) / win_loss_ratio)

print("\nFixed $100 Trade Analysis:")
print("═" * 50)
print(f"Number of Trades: {len(sell_trades)}")
print(f"Win Rate: {win_rate:.2%}")
print(f"Average Win: {avg_win:.2%}")
print(f"Average Loss: {avg_loss:.2%}")
print(f"Win/Loss Ratio: {win_loss_ratio:.2f}")
print(f"Kelly Fraction: {kelly:.2%}")

# Additional statistics
total_pnl = sell_trades['pnl'].sum()
profit_factor = abs(wins['pnl'].sum() / losses['pnl'].sum()) if len(losses) > 0 else float('inf')
max_drawdown = min(sell_trades['return'])
sharpe = (sell_trades['return'].mean()) / (sell_trades['return'].std()) * np.sqrt(252)

print("\nAdditional Metrics:")
print("═" * 50)
print(f"Total PnL: ${total_pnl:.2f}")
print(f"Profit Factor: {profit_factor:.2f}")
print(f"Max Single-Trade Drawdown: {max_drawdown:.2f}%")
print(f"Sharpe Ratio: {sharpe:.2f}")

# Save detailed trade log
print("\nSample of Trade Returns:")
print("═" * 50)
print(sell_trades[['date', 'price', 'return', 'pnl']].head().to_string())

def run_strategy(position_size_pct):
    """Run the RSI strategy with fixed position size
    
    Args:
        position_size_pct (float): Fixed position size as decimal
        
    Returns:
        pd.DataFrame: DataFrame containing trade history
    """
    # ... rest of the existing code ...

def calculate_kelly(trades_df):
    """Calculate Kelly Criterion from trade results using the simplified trading formula
    
    Args:
        trades_df (pd.DataFrame): DataFrame containing trade history
        
    Returns:
        float: Optimal Kelly fraction
    """
    # ... rest of the existing code ... 