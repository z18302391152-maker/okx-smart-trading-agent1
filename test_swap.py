# -*- coding: utf-8 -*-
"""
Test swap functionality: Swap 80% BNB to USDT on BSC
"""

import asyncio
import sys
import os

# Add project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills.smart_trading import SmartTrading
from skills.risk_manager import RiskManager
from skills.market_monitor import MarketMonitor


async def test_swap_bnb_to_usdt():
    """Test swapping BNB to USDT on BSC"""
    
    print("=" * 60)
    print("Testing Swap: 80% BNB -> USDT on BSC")
    print("=" * 60)
    
    try:
        # Initialize modules
        print("\n[1/5] Initializing modules...")
        smart_trading = SmartTrading()
        risk_manager = RiskManager()
        market_monitor = MarketMonitor()
        print("      Modules initialized successfully")
        
        # Get BNB balance
        print("\n[2/5] Getting BNB balance...")
        bnb_price = await market_monitor.get_token_price('BNB', 'bsc', 'USDT')
        if bnb_price:
            print(f"      BNB price: ${bnb_price:.2f}")
        else:
            print("      Failed to get BNB price")
            return False
        
        # Calculate swap amount (80% of balance)
        print("\n[3/5] Calculating swap amount...")
        # For testing, use a fixed amount (you can change this)
        bnb_amount = 0.1  # 0.1 BNB for testing
        print(f"      Swap amount: {bnb_amount} BNB")
        print(f"      Estimated value: ${bnb_amount * bnb_price:.2f}")
        
        # Check swap risk
        print("\n[4/5] Checking swap risk...")
        risk_check = await risk_manager.check_swap_risk(
            from_token='BNB',
            to_token='USDT',
            amount=bnb_amount,
            chain='bsc',
            slippage=0.5
        )
        
        if risk_check['safe']:
            print("      Risk check: PASSED")
            print(f"      Liquidity: ${risk_check['liquidity']:.2f}")
            print(f"      Price impact: {risk_check['price_impact']:.2f}%")
        else:
            print("      Risk check: FAILED")
            print(f"      Reason: {risk_check.get('reason', 'Unknown')}")
            print(f"      Risk factors: {risk_check.get('risk_factors', [])}")
            return False
        
        # Get swap quote
        print("\n[5/5] Getting swap quote...")
        quote = await smart_trading.get_swap_quote(
            from_token='BNB',
            to_token='USDT',
            amount=bnb_amount,
            chain='bsc',
            slippage=0.5
        )
        
        if quote:
            print("      Quote received successfully")
            print(f"      From: {quote['from_amount']} {quote['from_token']}")
            print(f"      To: {quote['to_amount']:.6f} {quote['to_token']}")
            print(f"      Chain: {quote['chain']}")
            print(f"      Slippage: {quote['slippage']}%")
            print(f"      Price impact: {quote['price_impact']:.2f}%")
            
            # Calculate expected output
            expected_usdt = quote['to_amount']
            print(f"\n      Expected output: {expected_usdt:.6f} USDT")
            
            return True
        else:
            print("      Failed to get quote")
            return False
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("OKX Smart Trading Agent - Swap Test")
    print("=" * 60)
    
    # Run test
    success = await test_swap_bnb_to_usdt()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if success:
        print("SUCCESS: Swap test passed!")
        print("\nNote: This test only gets the quote.")
        print("To execute the actual swap, you need to:")
        print("1. Configure your wallet private key in .env")
        print("2. Implement transaction signing and broadcasting")
        print("3. Call the swap_tokens function with user_address")
    else:
        print("FAILED: Swap test failed")
        print("\nPlease check:")
        print("1. Your OKX API credentials in .env")
        print("2. Your internet connection")
        print("3. OKX API availability")
    
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
