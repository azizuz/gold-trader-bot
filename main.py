# main.py - Main entry point for the Gold Trading Bot
import asyncio
import schedule
import time
from datetime import datetime
from data_collector import collect_gold_data
from signal_generator import generate_signals
from alert_system import send_alert

def run_bot():
    """Main function to run the trading bot"""
    print(f"\n{'='*50}")
    print(f"Gold Trading Bot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        # Step 1: Collect data
        print("📊 Collecting market data...")
        market_data = collect_gold_data()
        
        if not market_data:
            print("❌ Failed to collect data")
            return
        
        # Step 2: Generate signals
        print("🤖 Analyzing signals...")
        signals = generate_signals(market_data)
        
        # Step 3: Display results
        print(f"\n📈 Current XAUUSD Price: ${market_data['gold_price']:.2f}")
        print(f"📊 USD Index (DXY): {market_data['dxy']:.2f}")
        
        if signals:
            print(f"\n🎯 Trading Signal: {signals['action']}")
            print(f"💪 Confidence: {signals['confidence']:.2%}")
            print(f"📝 Reason: {signals['reason']}")
            
            # Step 4: Send alert if strong signal
            if abs(signals['confidence']) > 0.7:
                print("🔔 Sending alert for strong signal...")
                send_alert(signals)
        else:
            print("\n⏸️ No clear signal at this time")
            
        print(f"\n✅ Bot run completed at {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")

def main():
    """Setup and run the bot"""
    print("🚀 Starting Gold Trading Bot")
    print("⚠️ Remember: This is for educational purposes only!")
    
    # Run immediately once
    run_bot()
    
    # Schedule to run every 15 minutes
    schedule.every(15).minutes.do(run_bot)
    
    print("\n⏰ Bot scheduled to run every 15 minutes")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
