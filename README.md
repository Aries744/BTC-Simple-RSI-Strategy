# Bitcoin RSI Trading Strategy

A sophisticated cryptocurrency trading strategy that uses RSI (Relative Strength Index) to identify overbought conditions in Bitcoin, combined with dynamic position sizing for enhanced returns.

## Strategy Overview

The strategy implements a simple yet effective approach:
- Uses 5-period RSI to identify overbought conditions (RSI > 70)
- Implements dynamic position sizing (20% of portfolio)
- Maintains a long-only approach with clear entry/exit rules
- Achieved 294.34% return in backtesting

## Key Features

- **RSI-based Signals**: Short-term (5-period) RSI for quick signal generation
- **Dynamic Position Sizing**: Starts with 20% of portfolio ($20,000) and grows with equity
- **Risk Management**: Integrated drawdown monitoring and position size adjustment
- **Performance Analytics**: Comprehensive visualization of trades, equity, and risk metrics

## Requirements

```bash
pandas==2.0.0
numpy==1.24.0
ta==0.10.2
matplotlib==3.7.1
seaborn==0.12.2
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bitcoin-rsi-strategy.git
cd bitcoin-rsi-strategy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the strategy:
```bash
python plot_simple_rsi.py
```

This will:
- Load Bitcoin price data
- Calculate RSI signals
- Execute the trading strategy
- Generate performance visualizations
- Output key metrics

## Strategy Performance

- **Total Return**: 294.34%
- **Win Rate**: 44.2%
- **Total PnL**: $235,471.13
- **Sharpe Ratio**: 1.14
- **Maximum Drawdown**: -8.02%

## Visualization Components

The strategy generates a comprehensive visualization including:
1. Bitcoin price with buy/sell signals
2. RSI indicator with overbought threshold
3. Portfolio drawdown analysis
4. Returns distribution
5. Equity curve

## Project Structure

```
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── plot_simple_rsi.py    # Main strategy implementation
├── strategy_analysis.md  # Detailed strategy analysis
└── bitcoin_data.csv      # Historical price data
```

## Risk Warning

This strategy involves trading cryptocurrency with significant position sizes (20% of portfolio). While the backtesting results are promising, past performance does not guarantee future results. Use appropriate risk management and consider your risk tolerance before implementing.

## Future Improvements

1. **Risk Management**
   - Implement stop-loss levels
   - Add trailing stops
   - Maximum position size caps

2. **Position Management**
   - Partial profit taking
   - Scaled entries and exits
   - Time-based exit rules

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 