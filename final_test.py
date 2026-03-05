# -*- coding: utf-8 -*-
"""
Final test script - Check if all files exist and can be imported
"""
import os
import sys

# Add project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_files_exist():
    """Check if all required files exist"""
    print("=" * 60)
    print("Checking if all files exist...")
    print("=" * 60)
    
    required_files = [
        'config.py',
        'main.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        'skills/__init__.py',
        'skills/market_monitor.py',
        'skills/smart_trading.py',
        'skills/risk_manager.py',
        'skills/portfolio_manager.py',
        'utils/__init__.py',
        'utils/api_client.py',
        'utils/helpers.py',
        'tests/__init__.py',
        'tests/test_agent.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[MISSING] {file_path}")
            missing_files.append(file_path)
    
    print("\n" + "=" * 60)
    if missing_files:
        print(f"Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("All required files exist!")
        return True

def test_imports():
    """Test if all modules can be imported"""
    print("\n" + "=" * 60)
    print("Testing module imports...")
    print("=" * 60)
    
    try:
        print("\n[1/7] Importing config...")
        from config import config
        print("      PASS")
        
        print("\n[2/7] Importing skills.market_monitor...")
        from skills.market_monitor import MarketMonitor
        print("      PASS")
        
        print("\n[3/7] Importing skills.smart_trading...")
        from skills.smart_trading import SmartTrading
        print("      PASS")
        
        print("\n[4/7] Importing skills.risk_manager...")
        from skills.risk_manager import RiskManager
        print("      PASS")
        
        print("\n[5/7] Importing skills.portfolio_manager...")
        from skills.portfolio_manager import PortfolioManager
        print("      PASS")
        
        print("\n[6/7] Importing utils.api_client...")
        from utils.api_client import OKXAPIClient
        print("      PASS")
        
        print("\n[7/7] Importing main...")
        from main import OKXSmartTradingAgent
        print("      PASS")
        
        print("\n" + "=" * 60)
        print("All modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("OKX Smart Trading Agent - Final Test")
    print("=" * 60)
    
    # Check files
    files_ok = check_files_exist()
    
    # Test imports
    imports_ok = test_imports()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Files check: {'PASS' if files_ok else 'FAIL'}")
    print(f"Imports test: { 'PASS' if imports_ok else 'FAIL'}")
    
    if files_ok and imports_ok:
        print("\n" + "=" * 60)
        print("SUCCESS: Project is ready!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OKX API credentials to .env")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Run the agent: python main.py")
        print("\nFor competition submission:")
        print("1. Create a GitHub repository")
        print("2. Push all files to GitHub")
        print("3. Submit via OKX Developer Portal")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("FAILED: Some tests did not pass")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
