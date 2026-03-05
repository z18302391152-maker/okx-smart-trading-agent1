# -*- coding: utf-8 -*-
"""
简单的项目测试脚本
"""

import sys
import os

# 添加项目路径到 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块是否可以正常导入"""
    print("=" * 60)
    print("开始测试模块导入...")
    print("=" * 60)
    
    try:
        print("\n1. 测试导入 config...")
        from config import config
        print("   ✓ config 导入成功")
        
        print("\n2. 测试导入 skills.market_monitor...")
        from skills.market_monitor import MarketMonitor
        print("   ✓ MarketMonitor 导入成功")
        
        print("\n3. 测试导入 skills.smart_trading...")
        from skills.smart_trading import SmartTrading
        print("   ✓ SmartTrading 导入成功")
        
        print("\n4. 测试导入 skills.risk_manager...")
        from skills.risk_manager import RiskManager
        print("   ✓ RiskManager 导入成功")
        
        print("\n5. 测试导入 skills.portfolio_manager...")
        from skills.portfolio_manager import PortfolioManager
        print("   ✓ PortfolioManager 导入成功")
        
        print("\n6. 测试导入 utils.api_client...")
        from utils.api_client import OKXAPIClient
        print("   ✓ OKXAPIClient 导入成功")
        
        print("\n7. 测试导入 utils.helpers...")
        from utils.helpers import format_usd, format_percentage
        print("   ✓ helpers 导入成功")
        
        print("\n8. 测试导入 main...")
        from main import OKXSmartTradingAgent
        print("   ✓ OKXSmartTradingAgent 导入成功")
        
        print("\n" + "=" * 60)
        print("所有模块导入测试通过！")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_helpers():
    """测试辅助函数"""
    print("\n" + "=" * 60)
    print("开始测试辅助函数...")
    print("=" * 60)
    
    try:
        from utils.helpers import format_usd, format_percentage, validate_address
        
        print("\n1. 测试 format_usd...")
        result = format_usd(1234.56)
        print(f"   format_usd(1234.56) = {result}")
        assert result == "$1,234.56"
        print("   ✓ format_usd 测试通过")
        
        print("\n2. 测试 format_percentage...")
        result = format_percentage(12.34)
        print(f"   format_percentage(12.34) = {result}")
        assert result == "12.34%"
        print("   ✓ format_percentage 测试通过")
        
        print("\n3. 测试 validate_address...")
        result = validate_address("0x742d35Cc6634C0532925a3b844Bc9e7595f8bEdb")
        print(f"   validate_address(ethereum_address) = {result}")
        assert result == True
        print("   ✓ validate_address 测试通过")
        
        print("\n" + "=" * 60)
        print("所有辅助函数测试通过！")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """测试配置"""
    print("\n" + "=" * 60)
    print("开始测试配置...")
    print("=" * 60)
    
    try:
        from config import config
        
        print("\n1. 检查配置属性...")
        print(f"   OKX_API_BASE_URL: {config.OKX_API_BASE_URL}")
        print(f"   DEFAULT_CHAIN: {config.DEFAULT_CHAIN}")
        print(f"   DEFAULT_SLIPPAGE: {config.DEFAULT_SLIPPAGE}")
        print(f"   MAX_SLIPPAGE: {config.MAX_SLIPPAGE}")
        print(f"   MIN_LIQUIDITY: ${config.MIN_LIQUIDITY}")
        
        print("\n2. 检查支持的区块链...")
        print(f"   支持的区块链数量: {len(config.SUPPORTED_CHAINS)}")
        print(f"   前 5 个链: {config.SUPPORTED_CHAINS[:5]}")
        
        print("\n3. 检查链配置...")
        eth_config = config.get_chain_config('ethereum')
        print(f"   Ethereum 配置: {eth_config}")
        
        print("\n" + "=" * 60)
        print("配置测试通过！")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("OKX Smart Trading Agent - 项目测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("模块导入测试", test_imports()))
    results.append(("辅助函数测试", test_helpers()))
    results.append(("配置测试", test_config()))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    # 统计结果
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed}/{total} 通过")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 所有测试通过！项目可以正常运行！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查错误信息。")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
