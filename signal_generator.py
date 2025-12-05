# signal_generator.py - Generate trading signals based on market data
import numpy as np
from datetime import datetime
from config import (
    RSI_OVERBOUGHT, 
    RSI_OVERSOLD, 
    MA_SHORT_PERIOD, 
    MA_LONG_PERIOD
)

class SignalGenerator:
    def __init__(self):
        self.signals_history = []
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50  # Neutral if not enough data
        
        deltas = np.diff(prices)
        seed = deltas[:period]
        
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        if down == 0:
            return 100 if up > 0 else 50
        
        rs = up / down
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_moving_average(self, prices, period):
        """Calculate simple moving average"""
        if len(prices) >= period:
            return sum(prices[-period:]) / period
        return sum(prices) / len(prices) if prices else 0
    
    def analyze_market_regime(self, data):
        """Determine current market regime"""
        gold_price = data.get("gold_price", 0)
        dxy = data.get("dxy", 100)
        real_yield = data.get("real_yield", 0)
        
        regime = "neutral"
        reasons = []
        
        # Check real yield regime
        if real_yield < -0.5:
            regime = "bullish"
            reasons.append("Negative real yields support gold")
        elif real_yield > 1.5:
            regime = "bearish"
            reasons.append("High real yields pressure gold")
        
        # Check DXY strength
        if dxy > 106:
            regime = "bearish" if regime == "neutral" else regime
            reasons.append("Strong USD pressures gold")
        elif dxy < 102:
            regime = "bullish" if regime == "neutral" else regime
            reasons.append("Weak USD supports gold")
        
        return regime, reasons
    
    def generate_signal(self, data):
        """Generate trading signal based on market data"""
        if not data or "gold_price" not in data:
            return None
        
        gold_price = data["gold_price"]
        historical = data.get("historical", {})
        prices = historical.get("prices", [gold_price])
        
        # Calculate indicators
        rsi = self.calculate_rsi(prices)
        ma_short = self.calculate_moving_average(prices, MA_SHORT_PERIOD)
        ma_long = self.calculate_moving_average(prices, MA_LONG_PERIOD)
        
        # Get market regime
        regime, regime_reasons = self.analyze_market_regime(data)
        
        # Initialize signal
        signal = {
            "timestamp": datetime.now().isoformat(),
            "price": gold_price,
            "action": "HOLD",
            "confidence": 0.0,
            "reasons": [],
            "indicators": {
                "rsi": round(rsi, 2),
                "ma_short": round(ma_short, 2),
                "ma_long": round(ma_long, 2)
            }
        }
        
        confidence = 0.0
        reasons = []
        
        # Rule 1: RSI based signals
        if rsi < RSI_OVERSOLD:
            confidence += 0.3
            reasons.append(f"Oversold (RSI: {rsi:.1f})")
            signal["action"] = "BUY"
        elif rsi > RSI_OVERBOUGHT:
            confidence += 0.3
            reasons.append(f"Overbought (RSI: {rsi:.1f})")
            signal["action"] = "SELL"
        
        # Rule 2: Moving average crossover
        if ma_short > ma_long and gold_price > ma_short:
            confidence += 0.2
            reasons.append("Bullish MA crossover")
            if signal["action"] == "HOLD":
                signal["action"] = "BUY"
        elif ma_short < ma_long and gold_price < ma_short:
            confidence += 0.2
            reasons.append("Bearish MA crossover")
            if signal["action"] == "HOLD":
                signal["action"] = "SELL"
        
        # Rule 3: Market regime alignment
        if regime == "bullish" and signal["action"] == "BUY":
            confidence += 0.2
            reasons.extend(regime_reasons)
        elif regime == "bearish" and signal["action"] == "SELL":
            confidence += 0.2
            reasons.extend(regime_reasons)
        elif regime != "neutral" and signal["action"] == "HOLD":
            # If market has strong regime but no technical signal
            signal["action"] = "BUY" if regime == "bullish" else "SELL"
            confidence += 0.1
            reasons.append(f"Market regime: {regime}")
        
        # Rule 4: Price relative to moving averages
        if gold_price > ma_long * 1.05:  # 5% above long MA
            confidence += 0.1
            reasons.append("Price well above long-term average")
        elif gold_price < ma_long * 0.95:  # 5% below long MA
            confidence += 0.1
            reasons.append("Price well below long-term average")
        
        # Cap confidence at 1.0
        signal["confidence"] = min(confidence, 1.0)
        
        # If confidence too low, revert to HOLD
        if signal["confidence"] < 0.3:
            signal["action"] = "HOLD"
            signal["confidence"] = 0.0
            reasons = ["Insufficient confidence for clear signal"]
        
        signal["reasons"] = reasons
        
        # Add to history
        self.signals_history.append(signal)
        
        return signal
    
    def get_signal_summary(self, signal):
        """Format signal for display"""
        if not signal:
            return "No signal generated"
        
        summary = f"""
        ╔══════════════════════════════════════╗
        ║         GOLD TRADING SIGNAL          ║
        ╠══════════════════════════════════════╣
        ║ Action:    {signal['action']:<10}            ║
        ║ Confidence:{signal['confidence']:>7.1%}                ║
        ║ Price:     ${signal['price']:>8.2f}              ║
        ║ RSI:       {signal['indicators']['rsi']:>8.1f}              ║
        ╚══════════════════════════════════════╝
        
        Reasons:
        """
        
        for reason in signal['reasons']:
            summary += f"• {reason}\n"
        
        return summary

# Convenience function
def generate_signals(data):
    """Generate signals from market data"""
    generator = SignalGenerator()
    signal = generator.generate_signal(data)
    
    if signal:
        print(generator.get_signal_summary(signal))
    
    return signal

# Test function
if __name__ == "__main__":
    # Test with sample data
    test_data = {
        "gold_price": 1950.50,
        "dxy": 104.5,
        "real_yield": -0.3,
        "historical": {
            "prices": [1930, 1940, 1945, 1950, 1950.50, 1948, 1952, 1955, 1953, 1950],
            "dates": []
        }
    }
    
    signal = generate_signals(test_data)
    print(f"Signal: {signal}")
