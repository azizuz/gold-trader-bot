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
