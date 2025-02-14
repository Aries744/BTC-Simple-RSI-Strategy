# Bitcoin RSI Strategy Documentation

## Strategy Overview
A simple RSI-based trading strategy for Bitcoin that aims to capture overbought conditions. The strategy uses a short-term RSI (5-period) to identify potential reversal points in the market, combined with dynamic position sizing for enhanced returns.

## Core Components

### Strategy Parameters
- **RSI Window**: 5 periods (short-term for faster signals)
- **Entry Signal**: RSI > 70 (overbought condition)
- **Exit Signal**: RSI < 70 (exit when overbought condition ends)
- **Position Size**: 20% of current portfolio value
- **Initial Capital**: $100,000
- **Initial Trade Size**: $20,000 (20% of initial capital)
- **Trading Style**: Long-only, fully automated

### Technical Indicators
1. **RSI (Relative Strength Index)**
   - 5-period window for rapid signal generation
   - Primary signal generator for entries and exits
   - Overbought threshold at 70

## Performance Metrics

### Overall Results
- **Total Return**: 294.34% (nearly quadrupled initial capital)
- **Total PnL**: $235,471.13
- **Number of Trades**: 217
- **Win Rate**: 44.2%
- **Average Trade PnL**: $1,085.12
- **Sharpe Ratio**: 1.14
- **Maximum Drawdown**: -8.02%
- **Current Drawdown**: -2.82%

### Risk-Adjusted Performance
- **Sharpe Ratio Details**:
  - Calculation: Using 2% risk-free rate
  - Daily returns annualized
  - Value of 1.14 indicates moderate risk-adjusted returns
  - Shows strategy generates returns above risk-free rate with notable volatility

### Drawdown Analysis
- **Maximum Drawdown**: -8.02%
  - Relatively contained given aggressive position sizing
  - Indicates effective risk management despite high exposure
- **Current Drawdown**: -2.82%
  - Strategy currently near historical peaks
  - Shows strong recovery capability

## Risk Management Framework

### Position Sizing
- Dynamic sizing at 20% of portfolio value
- Initial trade size: $20,000
- Position size grows with portfolio value
- Aggressive approach that amplifies both gains and risks

### Risk Controls
1. **Entry Conditions**
   - RSI must exceed 70 (strong momentum)
   - No existing position requirement
   - Clear entry price execution

2. **Exit Conditions**
   - RSI drops below 70
   - Full position exit
   - No partial profit taking

### Risk Considerations
1. Aggressive 20% position sizing requires careful monitoring
2. No implemented stop-loss mechanism
3. Relies on RSI signal for risk management
4. High exposure during trades

## Visualization Components

### Main Chart Elements
1. **Price and Trades Plot**
   - Bitcoin price line
   - Buy signals (green triangles)
   - Sell signals (red triangles)
   - Shows trade timing and frequency

2. **RSI Indicator**
   - 5-period RSI line
   - 70 threshold line
   - Overbought zone highlighting
   - Signal generation visualization

3. **Portfolio Analysis**
   - Drawdown chart showing risk exposure
   - Returns distribution showing performance characteristics
   - Equity curve displaying portfolio growth

## Technical Implementation

### Dependencies
```
pandas==2.0.0
numpy==1.24.0
ta==0.10.2
matplotlib==3.7.1
seaborn==0.12.2
```

### Data Requirements
- Daily Bitcoin OHLCV data
- Clean and adjusted prices
- Datetime-indexed data

## Future Improvements

### Strategy Enhancements
1. **Risk Management**
   - Implement stop-loss levels
   - Add trailing stops
   - Consider volatility-based position sizing
   - Maximum position size caps

2. **Position Management**
   - Partial profit taking
   - Scaled entries and exits
   - Time-based exit rules

## Conclusion
The strategy demonstrates exceptional performance with a 294.34% return, nearly quadrupling the initial capital. While the win rate of 44.2% is moderate, the aggressive position sizing amplifies returns significantly. The strategy maintains reasonable risk control with a maximum drawdown of 8.02% despite the large position sizes.

The combination of short-term RSI signals and dynamic position sizing creates a powerful trading system, though it requires careful risk management due to the aggressive exposure. The moderate Sharpe ratio suggests opportunities for further optimization while maintaining the strategy's core strengths in capturing overbought conditions in the Bitcoin market. 