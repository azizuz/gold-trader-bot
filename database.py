# database.py - Database operations for storing signals
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL
import json

Base = declarative_base()

class TradingSignal(Base):
    __tablename__ = 'trading_signals'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String(10))  # BUY, SELL, HOLD
    confidence = Column(Float)
    price = Column(Float)
    reasons = Column(String(500))  # JSON string of reasons
    indicators = Column(String(500))  # JSON string of indicators
    
    def __repr__(self):
        return f"<Signal {self.timestamp}: {self.action} at ${self.price}>"

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def save_signal(self, signal):
        """Save a trading signal to database"""
        try:
            # Convert lists to JSON strings
            reasons_json = json.dumps(signal.get('reasons', []))
            indicators_json = json.dumps(signal.get('indicators', {}))
            
            # Create signal record
            signal_record = TradingSignal(
                action=signal.get('action', 'HOLD'),
                confidence=signal.get('confidence', 0.0),
                price=signal.get('price', 0.0),
                reasons=reasons_json,
                indicators=indicators_json
            )
            
            # Save to database
            self.session.add(signal_record)
            self.session.commit()
            
            print(f"✅ Signal saved to database (ID: {signal_record.id})")
            return True
            
        except Exception as e:
            print(f"❌ Error saving signal to database: {e}")
            self.session.rollback()
            return False
    
    def get_recent_signals(self, limit=10):
        """Get recent trading signals"""
        try:
            signals = self.session.query(TradingSignal)\
                .order_by(TradingSignal.timestamp.desc())\
                .limit(limit)\
                .all()
            
            return signals
            
        except Exception as e:
            print(f"Error getting signals: {e}")
            return []
    
    def get_performance_stats(self):
        """Get trading performance statistics"""
        try:
            # Count signals by type
            total = self.session.query(TradingSignal).count()
            buys = self.session.query(TradingSignal)\
                .filter(TradingSignal.action == 'BUY').count()
            sells = self.session.query(TradingSignal)\
                .filter(TradingSignal.action == 'SELL').count()
            
            # Get average confidence
            avg_confidence = self.session.query(
                func.avg(TradingSignal.confidence)
            ).scalar() or 0
            
            return {
                'total_signals': total,
                'buy_signals': buys,
                'sell_signals': sells,
                'avg_confidence': round(avg_confidence, 2)
            }
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}

# Global instance
db_manager = DatabaseManager()

# Convenience functions
def save_signal(signal):
    """Save signal to database"""
    return db_manager.save_signal(signal)

def get_recent_signals(limit=10):
    """Get recent signals"""
    return db_manager.get_recent_signals(limit)

# Test function
if __name__ == "__main__":
    print("Testing database...")
    
    # Test signal
    test_signal = {
        "action": "BUY",
        "confidence": 0.75,
        "price": 1950.50,
        "reasons": ["Test reason 1", "Test reason 2"],
        "indicators": {"rsi": 30.5, "ma_short": 1945.20}
    }
    
    # Save test signal
    success = save_signal(test_signal)
    print(f"Save successful: {success}")
    
    # Get recent signals
    signals = get_recent_signals(5)
    print(f"Recent signals: {len(signals)}")
    for s in signals:
        print(f"  {s.timestamp}: {s.action} at ${s.price}")
