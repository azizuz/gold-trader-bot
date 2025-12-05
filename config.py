# config.py - Configuration for Gold Trading Bot
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (will be set as environment variables)
METALPRICEAPI_KEY = os.getenv("METALPRICEAPI_KEY", "your_api_key_here")

# Trading Settings
SYMBOL = "XAUUSD"
TIMEZONE = "UTC"

# Signal Parameters
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MA_SHORT_PERIOD = 20
MA_LONG_PERIOD = 50

# Risk Management
MAX_POSITION_SIZE = 0.02  # 2% of capital per trade
STOP_LOSS_ATR_MULTIPLIER = 2.0
TAKE_PROFIT_RATIO = 2.0  # 1:2 risk-reward

# Database Settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trading_bot.db")

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
