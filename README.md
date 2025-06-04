
# Crypto Trading Bot 🤖📈

This project is a cryptocurrency trading bot using real-time market data and custom strategies. It's designed to interact with crypto exchanges via API and run basic automated strategies.

## Features
- Real-time trading via Binance API
- Strategy modularization (easy to test and plug in new logic)
- Configurable parameters (risk, amount, pairs)

## Quick Start

```bash
git clone https://github.com/RCATENACCI/crypto-bot.git
cd crypto-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


```
## 📊 2025 Strategy Results (Jan 1 – May 31)

- **Backtest period:** 2025-01-01 to 2025-05-31
- **Data frequency:** 15-minute candles
- **Number of trades:** 1,992
- **Cumulative return on the period** 20%
- **Sharpe ratio (on trades only):** 2.06 ✅
- **Total Sharpe ratio :** 2,12 ✅
- **Mean return per trade:** 0.0095%
- **Standard deviation per trade:** 0.259%
- **Strategy type:** Weighted combination of technical indicators + ML predictions
- **Positioning logic:**
  - **Buy** when signal > 0.65
  - **Sell** when signal < 0.35
  - **No trade** otherwise

📌 *Note: This performance is theoretical and does not include slippage, fees, or real market frictions.*
