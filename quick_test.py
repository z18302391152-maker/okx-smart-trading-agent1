# -*- coding: utf-8 -*-
"""
Quick test script
"""

import sys
import os

# Add project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("OKX Smart Trading Agent - Quick Test")
    print("=" * 60)
    
    try:
        print("\n[1/5] Testing config import...")
        from config import config
        print("      PASS: config imported successfully")
        
        print("\n[2/5] Testing skills imports...")
        from skills.market_monitor import MarketMonitor
        from skills.smart_trading import SmartTrading
        from skills.risk_manager import RiskManager
        from skills.portfolio_manager import PortfolioManager
        print("      PASS: All skills imported successfully")
        
        print("\n[3/5] Testing utils imports...")
        from utils.api_client import OKXAPIClient
        from utils.helpers import format_usd, format_percentage
        print("      PASS: All utils imported successfully")
        
        print("\n[4/5] Testing helper functions...")
        result = format_usd(1234.56)
        assert result == "$1,234.56"
        result = format_percentage(12.34)
        assert result == "12.34%"
        print("      PASS: Helper functions work correctly")
        
        print("\n[5/5] Testing main module...")
        from main import OKXSmartTradingAgent
        print("      PASS: Main module imported successfully")
        
        print("\n" + "=" * 60)
        print("SUCCESS: All tests passed!")
        print("=" * 60)
        print("\nProject is ready to use!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OKX API credentials to .env")
        print("3. Run: python main.py")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
