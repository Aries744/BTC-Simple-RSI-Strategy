"""
Bitcoin RSI Trading Strategy with Kelly-Optimal Position Sizing

This strategy combines a 5-period RSI indicator with mathematically optimal
position sizing based on the Kelly Criterion. The position sizing (32.44%)
was derived from fixed-size backtesting analysis that showed:
- Win Rate: 44.24%
- Win/Loss Ratio: 4.73
- Average Win: 10.09%
- Average Loss: 2.14%

Kelly Formula: K% = W - [(1-W)/R]
            = 0.4424 - [(1-0.4424)/4.73]
            = 32.44%
"""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set visualization style
sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Load and prepare data
df = pd.read_csv('bitcoin_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Strategy Parameters
RSI_WINDOW = 5
RSI_OVERBOUGHT = 70
KELLY_FRACTION = 0.3244  # Derived from fixed-size analysis
INITIAL_CAPITAL = 100000

# Calculate RSI
rsi = RSIIndicator(close=df['Close'], window=RSI_WINDOW)
df['RSI'] = rsi.rsi()

# Initialize strategy variables
capital = INITIAL_CAPITAL
position = False
trades = []
portfolio_values = [capital]
dates = [df.index[0]]
current_shares = 0

# Run strategy
for i in range(RSI_WINDOW, len(df)):
    current_price = df['Close'].iloc[i]
    current_rsi = df['RSI'].iloc[i]
    
    # Calculate current portfolio value
    current_portfolio_value = capital
    if position:
        current_portfolio_value += (current_shares * current_price)
    
    # Calculate trade size using Kelly-optimal fraction
    trade_size = current_portfolio_value * KELLY_FRACTION
    
    # Long entry signal (RSI overbought)
    if not position and current_rsi > RSI_OVERBOUGHT:
        position = True
        current_shares = trade_size / current_price
        capital -= trade_size
        
        trades.append({
            'date': df.index[i],
            'type': 'BUY',
            'price': current_price,
            'shares': current_shares,
            'trade_size': trade_size
        })
    
    # Long exit signal (RSI no longer overbought)
    elif position and current_rsi < RSI_OVERBOUGHT:
        position = False
        exit_value = current_shares * current_price
        pnl = exit_value - trade_size
        capital += exit_value  # Add the exit value back to capital
        
        trades.append({
            'date': df.index[i],
            'type': 'SELL',
            'price': current_price,
            'shares': current_shares,
            'trade_size': trade_size,
            'pnl': pnl,
            'return': (pnl / trade_size) * 100
        })
        current_shares = 0
    
    # Track portfolio value
    portfolio_value = capital + (current_shares * current_price if position else 0)
    portfolio_values.append(portfolio_value)
    dates.append(df.index[i])

# Convert to DataFrame for analysis
portfolio_df = pd.DataFrame({
    'Date': dates,
    'Portfolio_Value': portfolio_values
}).set_index('Date')

trades_df = pd.DataFrame(trades)

# Calculate performance metrics
if not trades_df.empty:
    sell_trades = trades_df[trades_df['type'] == 'SELL'].copy()
    total_pnl = sell_trades['pnl'].sum()
    win_rate = (sell_trades['pnl'] > 0).mean() * 100
    total_return = (portfolio_df['Portfolio_Value'].iloc[-1] / INITIAL_CAPITAL - 1) * 100

# Calculate risk metrics
portfolio_df['Daily_Return'] = portfolio_df['Portfolio_Value'].pct_change()
portfolio_df['Cummax'] = portfolio_df['Portfolio_Value'].cummax()
portfolio_df['Drawdown'] = (portfolio_df['Portfolio_Value'] - portfolio_df['Cummax']) / portfolio_df['Cummax'] * 100

# Calculate Sharpe Ratio (assuming risk-free rate of 2%)
risk_free_rate = 0.02
excess_returns = portfolio_df['Daily_Return'] - risk_free_rate/252
sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# Calculate drawdown metrics
max_drawdown = portfolio_df['Drawdown'].min()
current_drawdown = portfolio_df['Drawdown'].iloc[-1]

# Create visualization
fig = plt.figure(figsize=(15, 15))
gs = plt.GridSpec(4, 1, figure=fig, height_ratios=[1.5, 1, 1, 1.5])

# Bitcoin Price Chart
ax1 = fig.add_subplot(gs[0])
ax1.plot(df.index, df['Close'], color='blue', alpha=0.3, label='BTC Price')
ax1.set_ylabel('BTC Price ($)')
ax1.legend()

# RSI Indicator
ax2 = fig.add_subplot(gs[1])
ax2.plot(df.index, df['RSI'], color='purple')
ax2.axhline(y=RSI_OVERBOUGHT, color='red', linestyle='--')
ax2.fill_between(df.index, RSI_OVERBOUGHT, 100, color='red', alpha=0.1)
ax2.set_ylabel(f'{RSI_WINDOW}-Day RSI')
ax2.set_ylim(0, 100)

# Drawdown
ax3 = fig.add_subplot(gs[2])
ax3.fill_between(portfolio_df.index, portfolio_df['Drawdown'], 0, color='red', alpha=0.3)
ax3.set_ylabel('Drawdown %')
ax3.set_title('Portfolio Drawdown')

# Portfolio Value
ax4 = fig.add_subplot(gs[3])
ax4.plot(portfolio_df.index, portfolio_df['Portfolio_Value'], color='#2ecc71', linewidth=2)
ax4.set_ylabel('Portfolio Value ($)')
ax4.set_title('Equity Curve')

# Add title with metrics
title = f"Bitcoin RSI Strategy with Kelly-Optimal Position Sizing ({KELLY_FRACTION:.2%})\n"
title += f"Total Return: {total_return:.2f}% | Win Rate: {win_rate:.1f}% | Sharpe: {sharpe_ratio:.2f}\n"
title += f"Max Drawdown: {max_drawdown:.2f}% | Total PnL: ${total_pnl:.2f} | Trades: {len(sell_trades)}"
plt.suptitle(title, y=0.95)

plt.tight_layout()
plt.savefig('rsi_strategy.png', dpi=300, bbox_inches='tight')

# Print key statistics
print("\nStrategy Results:")
print("═" * 50)
print(f"Total Return:     {total_return:.2f}%")
print(f"Win Rate:        {win_rate:.1f}%")
print(f"Total PnL:       ${total_pnl:.2f}")
print(f"Total Trades:    {len(sell_trades)}")
print(f"Sharpe Ratio:    {sharpe_ratio:.2f}")
print(f"Max Drawdown:    {max_drawdown:.2f}%")
print(f"Current Drawdown: {current_drawdown:.2f}%") 