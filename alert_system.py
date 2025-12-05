# alert_system.py - Send alerts via various channels
import telebot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import logging

class AlertSystem:
    def __init__(self):
        self.telegram_bot = None
        
        # Initialize Telegram bot if token provided
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            try:
                self.telegram_bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
                print("✅ Telegram bot initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Telegram bot: {e}")
        
        # Setup logging
        logging.basicConfig(
            filename='bot_alerts.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def format_alert_message(self, signal):
        """Format signal into alert message"""
        emoji = "🟢" if signal["action"] == "BUY" else "🔴" if signal["action"] == "SELL" else "🟡"
        
        message = f"""
{emoji} *Gold Trading Alert* {emoji}

*Action:* {signal['action']}
*Confidence:* {signal['confidence']:.1%}
*Price:* ${signal['price']:.2f}

*Indicators:*
• RSI: {signal['indicators']['rsi']:.1f}
• Short MA: ${signal['indicators']['ma_short']:.2f}
• Long MA: ${signal['indicators']['ma_long']:.2f}

*Reasons:*
"""
        
        for reason in signal.get('reasons', []):
            message += f"• {reason}\n"
        
        message += f"\n_Time: {signal['timestamp'][11:16]} UTC_"
        
        return message
    
    def send_telegram_alert(self, signal):
        """Send alert via Telegram"""
        if not self.telegram_bot:
            print("⚠️ Telegram bot not configured")
            return False
        
        try:
            message = self.format_alert_message(signal)
            self.telegram_bot.send_message(
                TELEGRAM_CHAT_ID,
                message,
                parse_mode='Markdown'
            )
            print("✅ Telegram alert sent")
            logging.info(f"Telegram alert sent: {signal['action']} at {signal['price']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send Telegram alert: {e}")
            logging.error(f"Telegram alert failed: {e}")
            return False
    
    def send_console_alert(self, signal):
        """Display alert in console"""
        message = self.format_alert_message(signal)
        print("\n" + "="*50)
        print("🔔 TRADING ALERT 🔔")
        print("="*50)
        print(message)
        print("="*50)
        
        logging.info(f"Console alert: {signal['action']} at {signal['price']}")
        return True
    
    def send_alert(self, signal, methods=['console']):
        """Send alert through specified methods"""
        if not signal or signal['action'] == 'HOLD':
            return False
        
        results = []
        
        for method in methods:
            if method == 'telegram':
                if self.telegram_bot:
                    results.append(self.send_telegram_alert(signal))
            elif method == 'console':
                results.append(self.send_console_alert(signal))
            elif method == 'all':
                results.append(self.send_console_alert(signal))
                if self.telegram_bot:
                    results.append(self.send_telegram_alert(signal))
        
        return any(results)

# Global instance
alert_system = AlertSystem()

# Convenience function
def send_alert(signal, methods=['console']):
    """Send alert using the global alert system"""
    return alert_system.send_alert(signal, methods)

# Test function
if __name__ == "__main__":
    # Test alert
    test_signal = {
        "timestamp": "2024-01-15T10:30:00",
        "price": 1950.50,
        "action": "BUY",
        "confidence": 0.85,
        "reasons": ["Oversold (RSI: 28.5)", "Bullish MA crossover"],
        "indicators": {
            "rsi": 28.5,
            "ma_short": 1945.20,
            "ma_long": 1938.75
        }
    }
    
    print("Testing alert system...")
    success = send_alert(test_signal, methods=['console'])
    print(f"Alert sent: {success}")
