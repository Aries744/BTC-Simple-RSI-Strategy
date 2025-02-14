import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set Seaborn style
sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Load and prepare data
df = pd.read_csv('bitcoin_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate RSI
RSI_WINDOW = 5
rsi = RSIIndicator(close=df['Close'], window=RSI_WINDOW)
df['RSI'] = rsi.rsi()

# Initialize strategy variables
INITIAL_TRADE_SIZE = 20000  # Starting with 20% of 100k
POSITION_SIZE_PCT = 0.20    # 20% of portfolio per trade
capital = 100000
position = False
trades = []
portfolio_values = [capital]
dates = [df.index[0]]
current_shares = 0

# Run strategy
for i in range(RSI_WINDOW, len(df)):
    current_price = df['Close'].iloc[i]
    current_rsi = df['RSI'].iloc[i]
    
    # Calculate current portfolio value for position sizing
    current_portfolio_value = capital
    if position:
        current_portfolio_value += (current_shares * current_price)
    
    # Calculate trade size (20% of portfolio)
    if len(portfolio_values) <= 1:
        trade_size = INITIAL_TRADE_SIZE
    else:
        trade_size = current_portfolio_value * POSITION_SIZE_PCT
    
    # Long entry signal
    if not position and current_rsi > 70:
        position = True
        entry_price = current_price
        entry_date = df.index[i]
        current_shares = trade_size / current_price
        capital -= trade_size
        
        trades.append({
            'date': df.index[i],
            'type': 'BUY',
            'price': current_price,
            'shares': current_shares,
            'trade_size': trade_size
        })
    
    # Long exit signal
    elif position and current_rsi < 70:
        position = False
        exit_value = current_shares * current_price
        capital += exit_value
        pnl = exit_value - trade_size
        
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
    
    # Calculate current portfolio value
    if position:
        portfolio_value = capital + (current_shares * current_price)
    else:
        portfolio_value = capital
    
    portfolio_values.append(portfolio_value)
    dates.append(df.index[i])

# Convert to DataFrame
portfolio_df = pd.DataFrame({
    'Date': dates,
    'Portfolio_Value': portfolio_values
}).set_index('Date')

trades_df = pd.DataFrame(trades)

# Calculate metrics
if not trades_df.empty:
    sell_trades = trades_df[trades_df['type'] == 'SELL'].copy()
    total_pnl = sell_trades['pnl'].sum()
    win_rate = (sell_trades['pnl'] > 0).mean() * 100
    total_return = (portfolio_df['Portfolio_Value'].iloc[-1] / 100000 - 1) * 100

# Calculate drawdown and Sharpe ratio
portfolio_df['Daily_Return'] = portfolio_df['Portfolio_Value'].pct_change()
portfolio_df['Cummax'] = portfolio_df['Portfolio_Value'].cummax()
portfolio_df['Drawdown'] = (portfolio_df['Portfolio_Value'] - portfolio_df['Cummax']) / portfolio_df['Cummax'] * 100

# Calculate Sharpe Ratio (assuming risk-free rate of 2%)
risk_free_rate = 0.02
excess_returns = portfolio_df['Daily_Return'] - risk_free_rate/252
sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# Calculate max drawdown
max_drawdown = portfolio_df['Drawdown'].min()
current_drawdown = portfolio_df['Drawdown'].iloc[-1]

# Create visualization
fig = plt.figure(figsize=(15, 15))
gs = plt.GridSpec(5, 2, figure=fig, height_ratios=[1, 1, 0.8, 0.8, 1])

# Price and trades (spanning both columns)
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(df.index, df['Close'], color='blue', alpha=0.3, label='BTC Price')
ax1.set_ylabel('BTC Price ($)')
ax1.legend()

# RSI (spanning both columns)
ax2 = fig.add_subplot(gs[1, :])
ax2.plot(df.index, df['RSI'], color='purple')
ax2.axhline(y=70, color='red', linestyle='--')
ax2.fill_between(df.index, 70, 100, color='red', alpha=0.1)
ax2.set_ylabel('5-Day RSI')
ax2.set_ylim(0, 100)

# Drawdown (left column)
ax3 = fig.add_subplot(gs[2, 0])
ax3.fill_between(portfolio_df.index, portfolio_df['Drawdown'], 0, color='red', alpha=0.3)
ax3.plot(portfolio_df.index, portfolio_df['Drawdown'], color='red', alpha=0.8)
ax3.set_ylabel('Drawdown %')
ax3.set_title('Portfolio Drawdown')

# Returns Distribution (right column)
ax4 = fig.add_subplot(gs[2, 1])
daily_returns = portfolio_df['Daily_Return'].dropna() * 100
sns.histplot(data=daily_returns, bins=50, kde=True, ax=ax4)
ax4.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax4.set_title('Daily Returns Distribution')
ax4.set_xlabel('Daily Return (%)')
ax4.set_ylabel('Frequency')

# Portfolio Value (spanning both columns, at bottom)
ax5 = fig.add_subplot(gs[3:, :])
ax5.plot(portfolio_df.index, portfolio_df['Portfolio_Value'], color='#2ecc71', linewidth=2)
ax5.set_ylabel('Portfolio Value ($)')
ax5.set_title('Equity Curve')

# Format
for ax in fig.axes:
    ax.grid(True, alpha=0.2)

# Add title with metrics
title = f"Simple RSI Long-Only Strategy (>70) - 20% Portfolio Risk\n"
title += f"Total Return: {total_return:.2f}% | Win Rate: {win_rate:.1f}% | Sharpe: {sharpe_ratio:.2f}\n"
title += f"Max Drawdown: {max_drawdown:.2f}% | Total PnL: ${total_pnl:.2f} | Trades: {len(sell_trades)}"
plt.suptitle(title, y=0.95)

plt.tight_layout()
plt.savefig('simple_rsi_strategy.png', dpi=300, bbox_inches='tight')

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