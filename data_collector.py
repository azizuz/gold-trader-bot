# data_collector.py - Collect market data from various APIs
import requests
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from config import METALPRICEAPI_KEY, SYMBOL
import time

class GoldDataCollector:
    def __init__(self):
        self.metalpriceapi_key = METALPRICEAPI_KEY
        self.base_url = "https://api.metalpriceapi.com/v1/"
        
    def get_gold_price(self):
        """Get current gold price from MetalPriceAPI"""
        try:
            url = f"{self.base_url}latest"
            params = {
                "api_key": self.metalpriceapi_key,
                "base": "XAU",
                "currencies": "USD"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                return data["rates"]["USD"]
            else:
                print(f"API Error: {data.get('error', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Network error getting gold price: {e}")
            return None
        except Exception as e:
            print(f"Error getting gold price: {e}")
            return None
    
    def get_dxy_price(self):
        """Get US Dollar Index (DXY) price"""
        try:
            # Get DXY from Yahoo Finance
            dxy = yf.Ticker("DX-Y.NYB")
            hist = dxy.history(period="1d", interval="1m")
            
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
            else:
                # Fallback to fixed value if data unavailable
                return 105.0
                
        except Exception as e:
            print(f"Error getting DXY: {e}")
            return 105.0  # Fallback value
    
    def get_treasury_yields(self):
        """Get US Treasury yields"""
        try:
            # 10-year yield
            ten_year = yf.Ticker("^TNX")
            hist = ten_year.history(period="1d")
            
            yields = {
                "us10y": float(hist['Close'].iloc[-1]) if not hist.empty else 4.5,
                "us2y": 4.8,  # Placeholder - you can add real data source
                "tips": 2.1   # Placeholder for TIPS yield
            }
            return yields
            
        except Exception as e:
            print(f"Error getting yields: {e}")
            return {"us10y": 4.5, "us2y": 4.8, "tips": 2.1}
    
    def get_historical_data(self, days=30):
        """Get historical gold data"""
        try:
            # Using yfinance as fallback for historical data
            gold = yf.Ticker("GC=F")  # Gold futures
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            hist = gold.history(start=start_date, end=end_date)
            
            if not hist.empty:
                return {
                    "prices": hist['Close'].tolist(),
                    "dates": hist.index.strftime('%Y-%m-%d').tolist(),
                    "highs": hist['High'].tolist(),
                    "lows": hist['Low'].tolist(),
                    "volumes": hist['Volume'].tolist()
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error getting historical data: {e}")
            return None
    
    def collect_all_data(self):
        """Collect all market data"""
        print("Collecting market data...")
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "gold_price": None,
            "dxy": None,
            "yields": None,
            "historical": None
        }
        
        # Get gold price
        gold_price = self.get_gold_price()
        if gold_price:
            data["gold_price"] = gold_price
            print(f"✅ Gold price: ${gold_price:.2f}")
        else:
            print("❌ Failed to get gold price")
            return None
        
        # Get DXY
        data["dxy"] = self.get_dxy_price()
        print(f"✅ DXY: {data['dxy']:.2f}")
        
        # Get yields
        data["yields"] = self.get_treasury_yields()
        print(f"✅ 10-Year Yield: {data['yields']['us10y']:.2f}%")
        
        # Calculate real yield (simplified)
        if data["yields"] and gold_price:
            inflation_rate = 3.2  # Placeholder - get from API if available
            real_yield = data["yields"]["us10y"] - inflation_rate
            data["real_yield"] = real_yield
            print(f"✅ Real Yield: {real_yield:.2f}%")
        
        # Get historical data (last 7 days)
        data["historical"] = self.get_historical_data(days=7)
        if data["historical"]:
            print(f"✅ Historical data: {len(data['historical']['prices'])} days")
        
        return data

# Convenience function
def collect_gold_data():
    """Simple function to collect all gold data"""
    collector = GoldDataCollector()
    return collector.collect_all_data()

# Test function
if __name__ == "__main__":
    data = collect_gold_data()
    if data:
        print("\n📊 Data Collection Complete:")
        for key, value in data.items():
            if key != "historical":
                print(f"{key}: {value}")
    else:
        print("Failed to collect data")
