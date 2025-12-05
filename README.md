# 🏆 XAUUSD Gold Trading Bot

An AI-powered trading signal bot for gold (XAUUSD) built with Python, GitHub, and Render.

## ✨ Features

- **Real-time Data**: Fetches gold prices from MetalPriceAPI
- **Smart Signals**: Generates BUY/SELL/HOLD signals using multiple indicators
- **Risk Management**: Includes confidence scoring and risk parameters
- **Multiple Alerts**: Console, Telegram, and email notifications
- **Scheduled Runs**: Automatically runs every 15 minutes
- **Database Storage**: Saves all signals for analysis

## 🚀 Quick Start

### 1. Get Your API Key
1. Sign up at [MetalPriceAPI](https://metalpriceapi.com)
2. Get your API key from the dashboard
3. (Optional) Create a Telegram bot via @BotFather

### 2. Deploy on Render (Free)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Connect your GitHub repository
3. Add environment variables:
   - `METALPRICEAPI_KEY`: Your MetalPriceAPI key
   - `TELEGRAM_BOT_TOKEN`: (Optional) Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: (Optional) Your Telegram chat ID

### 3. Run the Bot

The bot will automatically:
- Run every 15 minutes
- Fetch gold prices and market data
- Generate trading signals
- Send alerts for strong signals

## 📊 How It Works

### Signal Generation Logic
1. **RSI Analysis**: Oversold (<30) = BUY, Overbought (>70) = SELL
2. **Moving Averages**: Bullish crossover = BUY, Bearish crossover = SELL
3. **Market Regime**: Considers real yields and USD strength
4. **Confidence Scoring**: Signals rated 0-100% confidence

### Data Sources
- **Gold Prices**: MetalPriceAPI (real-time)
- **USD Index**: Yahoo Finance (DXY)
- **Treasury Yields**: Yahoo Finance (^TNX)
- **Historical Data**: Gold futures (GC=F)

## ⚙️ Configuration

Edit `config.py` to customize:
- RSI thresholds
- Moving average periods
- Risk parameters
- Alert methods

## 📈 Example Output

==================================================
Gold Trading Bot - 2024-01-15 10:30:00
==================================================
📊 Collecting market data...
✅ Gold price: $1950.50
✅ DXY: 104.52
✅ 10-Year Yield: 4.25%
✅ Real Yield: -0.75%
✅ Historical data: 7 days

🤖 Analyzing signals...

╔══════════════════════════════════════╗
║ GOLD TRADING SIGNAL ║
╠══════════════════════════════════════╣
║ Action: BUY ║
║ Confidence: 75.0% ║
║ Price: $1950.50 ║
║ RSI: 28.5 ║
╚══════════════════════════════════════╝

Reasons:
• Oversold (RSI: 28.5)
• Bullish MA crossover
• Negative real yields support gold

🔔 Sending alert for strong signal...
✅ Bot run completed at 10:30:00

text

## 🛡️ Risk Warning

⚠️ **IMPORTANT DISCLAIMER**

This bot is for **EDUCATIONAL PURPOSES ONLY**.

- **NEVER** trade with real money based solely on these signals
- **ALWAYS** do your own research
- **START** with paper trading
- **UNDERSTAND** that all trading involves risk
- **CONSULT** a financial advisor before real trading

## 🔧 Technical Details

### Project Structure
xauusd-trading-bot/
├── main.py # Main bot runner
├── data_collector.py # Market data collection
├── signal_generator.py # Signal generation logic
├── alert_system.py # Alert/notification system
├── database.py # Database operations (optional)
├── config.py # Configuration settings
├── requirements.txt # Python dependencies
└── README.md # This file

text

### Dependencies
See `requirements.txt` for full list.

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ❓ Getting Help

- Open an Issue for bug reports
- Check the code comments for documentation
- Review the config.py file for customization options

---
**Remember**: Trading bots are tools, not magic. Always use proper risk management!
