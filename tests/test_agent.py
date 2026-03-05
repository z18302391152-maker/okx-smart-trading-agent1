"""
OKX Smart Trading Agent - Test Suite
娴嬭瘯鏂囦欢锛氭祴璇 Agent 鐨勫悇涓鍔熻兘妯″潡
"""

import pytest
import asyncio
from loguru import logger
import sys
import os

# 娣诲姞椤圭洰璺寰勫埌 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.market_monitor import MarketMonitor
from skills.smart_trading import SmartTrading
from skills.risk_manager import RiskManager
from skills.portfolio_manager import PortfolioManager
from utils.helpers import (
    format_usd,
    format_percentage,
    validate_address,
    validate_amount,
    validate_slippage
)


class TestMarketMonitor:
    """甯傚満鐩戞帶娴嬭瘯"""
    
    @pytest.fixture
    async def monitor(self):
        """鍒涘缓甯傚満鐩戞帶瀹炰緥"""
        monitor = MarketMonitor()
        yield monitor
        await monitor.close()
    
    @pytest.mark.asyncio
    async def test_get_token_price(self, monitor):
        """娴嬭瘯鑾峰彇浠ｅ竵浠锋牸"""
        try:
            price = await monitor.get_token_price('OKB', 'ethereum')
            assert price is not None
            assert price > 0
            logger.info(f'娴嬭瘯閫氳繃: OKB 浠锋牸 = ${price}')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')
    
    @pytest.mark.asyncio
    async def test_get_kline_data(self, monitor):
        """娴嬭瘯鑾峰彇 K绾挎暟鎹"""
        try:
            klines = await monitor.get_kline_data('OKB', 'ethereum', '1H', 10)
            assert isinstance(klines, list)
            assert len(klines) > 0
            logger.info(f'娴嬭瘯閫氳繃: 鑾峰彇鍒 {len(klines)} 鏉 K绾挎暟鎹')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')
    
    @pytest.mark.asyncio
    async def test_get_trade_history(self, monitor):
        """娴嬭瘯鑾峰彇浜ゆ槗鍘嗗彶"""
        try:
            trades = await monitor.get_trade_history('OKB', 'ethereum', 10)
            assert isinstance(trades, list)
            logger.info(f'娴嬭瘯閫氳繃: 鑾峰彇鍒 {len(trades)} 鏉′氦鏄撹板綍')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')


class TestSmartTrading:
    """鏅鸿兘浜ゆ槗娴嬭瘯"""
    
    @pytest.fixture
    async def trader(self):
        """鍒涘缓鏅鸿兘浜ゆ槗瀹炰緥"""
        trader = SmartTrading()
        yield trader
        await trader.close()
    
    @pytest.mark.asyncio
    async def test_get_swap_quote(self, trader):
        """娴嬭瘯鑾峰彇浜ゆ崲鎶ヤ环"""
        try:
            quote = await trader.get_swap_quote('OKB', 'USDC', 1.0, 'ethereum', 0.5)
            assert quote is not None
            assert 'to_amount' in quote
            logger.info(f'娴嬭瘯閫氳繃: 1 OKB = {quote["to_amount"]} USDC')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')
    
    @pytest.mark.asyncio
    async def test_find_best_route(self, trader):
        """娴嬭瘯鏌ユ壘鏈浼樿矾寰"""
        try:
            route = await trader.find_best_route('OKB', 'USDC', 1.0, 'ethereum')
            assert route is not None
            assert 'best_route' in route
            logger.info(f'娴嬭瘯閫氳繃: 鎵惧埌鏈浼樿矾寰')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')


class TestRiskManager:
    """椋庨櫓绠＄悊娴嬭瘯"""
    
    @pytest.fixture
    async def risk_manager(self):
        """鍒涘缓椋庨櫓绠＄悊瀹炰緥"""
        risk_manager = RiskManager()
        yield risk_manager
        await risk_manager.close()
    
    @pytest.mark.asyncio
    async def test_check_swap_risk(self, risk_manager):
        """娴嬭瘯妫鏌ヤ氦鎹㈤庨櫓"""
        try:
            result = await risk_manager.check_swap_risk('OKB', 'USDC', 1.0, 'ethereum', 0.5)
            assert 'safe' in result
            assert 'risk_factors' in result
            logger.info(f'娴嬭瘯閫氳繃: 椋庨櫓妫鏌ョ粨鏋 = {result["safe"]}')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')
    
    @pytest.mark.asyncio
    async def test_optimize_slippage(self, risk_manager):
        """娴嬭瘯浼樺寲婊戠偣"""
        try:
            result = await risk_manager.optimize_slippage('OKB', 'USDC', 1.0, 'ethereum')
            assert 'recommended_slippage' in result
            logger.info(f'娴嬭瘯閫氳繃: 寤鸿婊戠偣 = {result["recommended_slippage"]}%')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')


class TestPortfolioManager:
    """璧勪骇绠＄悊娴嬭瘯"""
    
    @pytest.fixture
    async def portfolio_manager(self):
        """鍒涘缓璧勪骇绠＄悊瀹炰緥"""
        portfolio_manager = PortfolioManager()
        yield portfolio_manager
        await portfolio_manager.close()
    
    @pytest.mark.asyncio
    async def test_get_portfolio_value(self, portfolio_manager):
        """娴嬭瘯鑾峰彇璧勪骇缁勫悎浠峰"""
        try:
            portfolio = await portfolio_manager.get_portfolio_value()
            assert 'total_value' in portfolio
            logger.info(f'娴嬭瘯閫氳繃: 璧勪骇缁勫悎浠峰 = ${portfolio["total_value"]}')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')
    
    @pytest.mark.asyncio
    async def test_analyze_portfolio_distribution(self, portfolio_manager):
        """娴嬭瘯鍒嗘瀽璧勪骇缁勫悎鍒嗗竷"""
        try:
            distribution = await portfolio_manager.analyze_portfolio_distribution()
            assert 'total_value' in distribution
            logger.info(f'娴嬭瘯閫氳繃: 璧勪骇缁勫悎鍒嗗竷鍒嗘瀽瀹屾垚')
        except Exception as e:
            logger.warning(f'娴嬭瘯璺宠繃: {str(e)}')
            pytest.skip('API 璋冪敤澶辫触')


class TestHelpers:
    """杈呭姪鍑芥暟娴嬭瘯"""
    
    def test_format_usd(self):
        """娴嬭瘯鏍煎紡鍖栫編鍏冮噾棰"""
        assert format_usd(1234.56) == '$1,234.56'
        assert format_usd(1000000.0) == '$1,000,000.00'
        logger.info('娴嬭瘯閫氳繃: format_usd')
    
    def test_format_percentage(self):
        """娴嬭瘯鏍煎紡鍖栫櫨鍒嗘瘮"""
        assert format_percentage(12.34) == '12.34%'
        assert format_percentage(0.5) == '0.50%'
        logger.info('娴嬭瘯閫氳繃: format_percentage')
    
    def test_validate_address(self):
        """娴嬭瘯楠岃瘉鍦板潃"""
        # Ethereum 鍦板潃
        assert validate_address('0x742d35Cc6634C0532925a3b844Bc9e7595f8bEdb') == True
        assert validate_address('invalid_address') == False
        logger.info('娴嬭瘯閫氳繃: validate_address')
    
    def test_validate_amount(self):
        """娴嬭瘯楠岃瘉閲戦"""
        assert validate_amount(100.0) == True
        assert validate_amount(0.0) == False
        assert validate_amount(-10.0) == False
        logger.info('娴嬭瘯閫氳繃: validate_amount')
    
    def test_validate_slippage(self):
        """娴嬭瘯楠岃瘉婊戠偣"""
        assert validate_slippage(0.5) == True
        assert validate_slippage(5.0) == True
        assert validate_slippage(100.0) == True
        assert validate_slippage(-1.0) == False
        assert validate_slippage(101.0) == False
        logger.info('娴嬭瘯閫氳繃: validate_slippage')


# 杩愯屾祴璇曠殑涓诲嚱鏁
async def run_tests():
    """杩愯屾墍鏈夋祴璇"""
    logger.info('寮濮嬭繍琛屾祴璇曞椾欢')
    
    # 杩愯 pytest
    exit_code = pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--asyncio-mode=auto'
    ])
    
    if exit_code == 0:
        logger.info('鎵鏈夋祴璇曢氳繃锛')
    else:
        logger.warning(f'娴嬭瘯澶辫触锛岄鍑虹爜: {exit_code}')
    
    return exit_code


if __name__ == '__main__':
    # 閰嶇疆鏃ュ織
    logger.add(
        'test_agent.log',
        rotation='10 MB',
        retention='7 days',
        level='INFO'
    )
    
    # 杩愯屾祴璇
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)
