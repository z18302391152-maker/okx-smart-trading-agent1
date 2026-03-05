# -*- coding: utf-8 -*-
"""
OKX Smart Trading Agent - Main Entry Point
涓荤▼搴忓叆鍙ｏ細鏅鸿兘浜ゆ槗鍔╂墜鐨勪富绋嬪簭
"""

import sys
import asyncio
from loguru import logger
from config import config

# 娣诲姞椤圭洰璺寰勫埌 sys.path
sys.path.append('.')

# 瀵煎叆鎶鑳芥ā鍧
from skills.market_monitor import MarketMonitor
from skills.smart_trading import SmartTrading
from skills.risk_manager import RiskManager
from skills.portfolio_manager import PortfolioManager


class OKXSmartTradingAgent:
    """OKX 鏅鸿兘浜ゆ槗鍔╂墜"""
    
    def __init__(self):
        """鍒濆嬪寲 Agent"""
        try:
            # 楠岃瘉閰嶇疆
            config.validate_config()
            
            # 鍒濆嬪寲鎶鑳芥ā鍧
            self.market_monitor = MarketMonitor()
            self.smart_trading = SmartTrading()
            self.risk_manager = RiskManager()
            self.portfolio_manager = PortfolioManager()
            
            logger.info('OKX Smart Trading Agent 鍒濆嬪寲鎴愬姛')
            
        except Exception as e:
            logger.error(f'鍒濆嬪寲澶辫触: {str(e)}')
            raise
    
    async def check_token_price(self, token_symbol, chain='ethereum'):
        """鏌ヨ浠ｅ竵浠锋牸"""
        try:
            logger.info(f'鏌ヨ {token_symbol} 鍦 {chain} 涓婄殑浠锋牸')
            price = await self.market_monitor.get_token_price(token_symbol, chain)
            logger.info(f'{token_symbol} 浠锋牸: ${price}')
            return price
        except Exception as e:
            logger.error(f'鏌ヨ浠锋牸澶辫触: {str(e)}')
            return None
    
    async def execute_swap(self, from_token, to_token, amount, chain='ethereum', slippage=0.5):
        """鎵ц屼唬甯佷氦鎹"""
        try:
            logger.info(f'鍑嗗囦氦鎹: {amount} {from_token} -> {to_token} 鍦 {chain}')
            
            # 椋庨櫓妫鏌
            risk_check = await self.risk_manager.check_swap_risk(
                from_token, to_token, amount, chain, slippage
            )
            
            if not risk_check['safe']:
                logger.warning(f'椋庨櫓妫鏌ユ湭閫氳繃: {risk_check["reason"]}')
                return {'success': False, 'reason': risk_check['reason']}
            
            # 鎵ц屼氦鎹
            result = await self.smart_trading.swap_tokens(
                from_token, to_token, amount, chain, slippage
            )
            
            if result['success']:
                logger.info(f'浜ゆ崲鎴愬姛: {result}')
            else:
                logger.error(f'浜ゆ崲澶辫触: {result}')
            
            return result
            
        except Exception as e:
            logger.error(f'鎵ц屼氦鎹㈠け璐: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    async def get_portfolio(self):
        """鑾峰彇璧勪骇缁勫悎"""
        try:
            logger.info('鏌ヨ㈣祫浜х粍鍚')
            portfolio = await self.portfolio_manager.get_portfolio_value()
            logger.info(f'鎬昏祫浜т环鍊: ${portfolio}')
            return portfolio
        except Exception as e:
            logger.error(f'鏌ヨ㈣祫浜х粍鍚堝け璐: {str(e)}')
            return None
    
    async def monitor_market(self, token_symbol, chain='ethereum'):
        """鐩戞帶甯傚満"""
        try:
            logger.info(f'寮濮嬬洃鎺 {token_symbol} 甯傚満')
            
            # 鑾峰彇浠锋牸
            price = await self.market_monitor.get_token_price(token_symbol, chain)
            
            # 鑾峰彇 K绾挎暟鎹
            klines = await self.market_monitor.get_kline_data(token_symbol, chain)
            
            # 鑾峰彇浜ゆ槗鍘嗗彶
            trades = await self.market_monitor.get_trade_history(token_symbol, chain)
            
            return {
                'price': price,
                'klines': klines,
                'trades': trades
            }
            
        except Exception as e:
            logger.error(f'鐩戞帶甯傚満澶辫触: {str(e)}')
            return None


async def main():
    """涓诲嚱鏁"""
    try:
        # 鍒濆嬪寲 Agent
        agent = OKXSmartTradingAgent()
        
        # 绀轰緥锛氭煡璇浠ｅ竵浠锋牸
        print('\n=== 鏌ヨ浠ｅ竵浠锋牸 ===')
        price = await agent.check_token_price('OKB', 'ethereum')
        
        # 绀轰緥锛氭煡璇㈣祫浜х粍鍚
        print('\n=== 鏌ヨ㈣祫浜х粍鍚 ===')
        portfolio = await agent.get_portfolio()
        
        # 绀轰緥锛氱洃鎺у競鍦
        print('\n=== 鐩戞帶甯傚満 ===')
        market_data = await agent.monitor_market('OKB', 'ethereum')
        
        # 绀轰緥锛氭墽琛屼氦鎹锛堥渶瑕佺敤鎴风‘璁わ級
        print('\n=== 鎵ц屼唬甯佷氦鎹 ===')
        print('娉ㄦ剰锛氬疄闄呬氦鏄撻渶瑕佺敤鎴风‘璁ゅ拰绉侀挜绛惧悕')
        # swap_result = await agent.execute_swap('OKB', 'USDC', 1.0, 'ethereum', 0.5)
        
        logger.info('绋嬪簭鎵ц屽畬鎴')
        
    except KeyboardInterrupt:
        logger.info('绋嬪簭琚鐢ㄦ埛涓鏂')
    except Exception as e:
        logger.error(f'绋嬪簭鎵ц屽け璐: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    # 閰嶇疆鏃ュ織
    logger.add(
        config.LOG_FILE,
        rotation='10 MB',
        retention='7 days',
        level=config.LOG_LEVEL
    )
    
    # 杩愯屼富绋嬪簭
    asyncio.run(main())
