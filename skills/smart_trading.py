# -*- coding: utf-8 -*-
"""
OKX Smart Trading Agent - Smart Trading Skill
鏅鸿兘浜ゆ槗鎶鑳斤細鏈浼樿矾寰勬煡鎵俱佹粦鐐规帶鍒躲佽法閾句氦鏄
"""

import asyncio
import aiohttp
from loguru import logger
from typing import Dict, Optional
from datetime import datetime


class SmartTrading:
    """鏅鸿兘浜ゆ槗鎶鑳"""
    
    def __init__(self):
        """鍒濆嬪寲鏅鸿兘浜ゆ槗"""
        self.base_url = 'https://www.okx.com'
        self.session = None
        logger.info('Smart Trading 鍒濆嬪寲鎴愬姛')
    
    async def __aenter__(self):
        """寮傛ヤ笂涓嬫枃绠＄悊鍣ㄥ叆鍙"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """寮傛ヤ笂涓嬫枃绠＄悊鍣ㄥ嚭鍙"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None, method: str = 'GET') -> Dict:
        """鍙戦 API 璇锋眰"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f'{self.base_url}{endpoint}'
            
            if method == 'GET':
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f'API 璇锋眰澶辫触: {response.status}')
                        return {'error': f'HTTP {response.status}'}
            elif method == 'POST':
                async with self.session.post(url, json=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f'API 璇锋眰澶辫触: {response.status}')
                        return {'error': f'HTTP {response.status}'}
                    
        except Exception as e:
            logger.error(f'璇锋眰寮傚父: {str(e)}')
            return {'error': str(e)}
    
    async def get_swap_quote(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum',
        slippage: float = 0.5
    ) -> Optional[Dict]:
        """
        鑾峰彇浜ゆ崲鎶ヤ环
        
        Args:
            from_token: 婧愪唬甯佺﹀彿
            to_token: 鐩鏍囦唬甯佺﹀彿
            amount: 浜ゆ崲鏁伴噺
            chain: 鍖哄潡閾剧綉缁
            slippage: 婊戠偣鐧惧垎姣
        
        Returns:
            浜ゆ崲鎶ヤ环淇℃伅
        """
        try:
            logger.info(f'鑾峰彇浜ゆ崲鎶ヤ环: {amount} {from_token} -> {to_token}')
            
            endpoint = '/api/v5/dex/aggregator/quote'
            
            params = {
                'chainId': chain,
                'fromTokenAddress': self._get_token_address(from_token, chain),
                'toTokenAddress': self._get_token_address(to_token, chain),
                'amount': str(amount),
                'slippage': str(slippage / 100)
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                quote = response['data'][0]
                logger.info(f'鎶ヤ环: {quote["toAmount"]} {to_token}')
                return {
                    'from_amount': amount,
                    'to_amount': float(quote['toAmount']),
                    'from_token': from_token,
                    'to_token': to_token,
                    'chain': chain,
                    'slippage': slippage,
                    'price_impact': float(quote.get('priceImpact', 0)),
                    'gas_price': quote.get('gasPrice', '0'),
                    'routes': quote.get('routes', [])
                }
            else:
                logger.warning(f'鑾峰彇鎶ヤ环澶辫触: {response}')
                return None
                
        except Exception as e:
            logger.error(f'鑾峰彇浜ゆ崲鎶ヤ环澶辫触: {str(e)}')
            return None
    
    async def swap_tokens(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum',
        slippage: float = 0.5,
        user_address: str = None
    ) -> Dict:
        """
        鎵ц屼唬甯佷氦鎹
        
        Args:
            from_token: 婧愪唬甯佺﹀彿
            to_token: 鐩鏍囦唬甯佺﹀彿
            amount: 浜ゆ崲鏁伴噺
            chain: 鍖哄潡閾剧綉缁
            slippage: 婊戠偣鐧惧垎姣
            user_address: 鐢ㄦ埛閽卞寘鍦板潃
        
        Returns:
            浜ゆ崲缁撴灉
        """
        try:
            logger.info(f'鎵ц屼氦鎹: {amount} {from_token} -> {to_token}')
            
            # 1. 鑾峰彇鎶ヤ环
            quote = await self.get_swap_quote(from_token, to_token, amount, chain, slippage)
            
            if not quote:
                return {
                    'success': False,
                    'reason': '鑾峰彇鎶ヤ环澶辫触'
                }
            
            # 2. 鏋勫缓浜ゆ槗
            endpoint = '/api/v5/dex/aggregator/buildTx'
            
            params = {
                'chainId': chain,
                'fromTokenAddress': self._get_token_address(from_token, chain),
                'toTokenAddress': self._get_token_address(to_token, chain),
                'amount': str(amount),
                'slippage': str(slippage / 100),
                'userAddress': user_address
            }
            
            response = await self._make_request(endpoint, params, 'POST')
            
            if 'error' not in response and 'data' in response:
                tx_data = response['data'][0]
                
                logger.info(f'浜ゆ槗宸叉瀯寤猴紝绛夊緟绛惧悕鍜屽箍鎾')
                
                return {
                    'success': True,
                    'quote': quote,
                    'tx_data': tx_data,
                    'message': '浜ゆ槗宸叉瀯寤猴紝闇瑕佺敤鎴风惧悕鍜屽箍鎾',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.warning(f'鏋勫缓浜ゆ槗澶辫触: {response}')
                return {
                    'success': False,
                    'reason': '鏋勫缓浜ゆ槗澶辫触',
                    'error': response
                }
                
        except Exception as e:
            logger.error(f'鎵ц屼氦鎹㈠け璐: {str(e)}')
            return {
                'success': False,
                'reason': str(e)
            }
    
    async def find_best_route(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum'
    ) -> Optional[Dict]:
        """
        鏌ユ壘鏈浼樹氦鏄撹矾寰
        
        Args:
            from_token: 婧愪唬甯佺﹀彿
            to_token: 鐩鏍囦唬甯佺﹀彿
            amount: 浜ゆ崲鏁伴噺
            chain: 鍖哄潡閾剧綉缁
        
        Returns:
            鏈浼樿矾寰勪俊鎭
        """
        try:
            logger.info(f'鏌ユ壘鏈浼樿矾寰: {from_token} -> {to_token}')
            
            endpoint = '/api/v5/dex/aggregator/allRoutes'
            
            params = {
                'chainId': chain,
                'fromTokenAddress': self._get_token_address(from_token, chain),
                'toTokenAddress': self._get_token_address(to_token, chain),
                'amount': str(amount)
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                routes = response['data']
                
                # 鎵惧埌鏈浼樿矾寰勶紙杈撳嚭閲戦濇渶澶э級
                best_route = max(routes, key=lambda x: float(x['toAmount']))
                
                logger.info(f'鏈浼樿矾寰: {best_route}')
                return {
                    'best_route': best_route,
                    'all_routes': routes,
                    'from_token': from_token,
                    'to_token': to_token,
                    'amount': amount
                }
            else:
                logger.warning(f'鏌ユ壘璺寰勫け璐: {response}')
                return None
                
        except Exception as e:
            logger.error(f'鏌ユ壘鏈浼樿矾寰勫け璐: {str(e)}')
            return None
    
    async def estimate_gas(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum'
    ) -> Optional[Dict]:
        """
        浼扮畻 Gas 璐圭敤
        
        Args:
            from_token: 婧愪唬甯佺﹀彿
            to_token: 鐩鏍囦唬甯佺﹀彿
            amount: 浜ゆ崲鏁伴噺
            chain: 鍖哄潡閾剧綉缁
        
        Returns:
            Gas 璐圭敤淇℃伅
        """
        try:
            logger.info(f'浼扮畻 Gas 璐圭敤: {from_token} -> {to_token}')
            
            # 鑾峰彇鎶ヤ环淇℃伅
            quote = await self.get_swap_quote(from_token, to_token, amount, chain)
            
            if quote and 'gas_price' in quote:
                gas_price = float(quote['gas_price'])
                gas_limit = 210000  # 榛樿 gas limit
                
                gas_fee = gas_price * gas_limit / 10**18  # 杞鎹涓 ETH
                
                return {
                    'gas_price': gas_price,
                    'gas_limit': gas_limit,
                    'gas_fee': gas_fee,
                    'gas_fee_usd': gas_fee * 2000  # 鍋囪 ETH 浠锋牸涓 $2000
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f'浼扮畻 Gas 璐圭敤澶辫触: {str(e)}')
            return None
    
    def _get_token_address(self, token_symbol: str, chain: str) -> str:
        """
        鑾峰彇浠ｅ竵鍦板潃
        
        Args:
            token_symbol: 浠ｅ竵绗﹀彿
            chain: 鍖哄潡閾剧綉缁
        
        Returns:
            浠ｅ竵鍦板潃
        """
        # 甯歌佷唬甯佸湴鍧鏄犲皠
        token_addresses = {
            'ethereum': {
                'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                'ETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                'OKB': '0x85Ea30cC7B3204042f291A4DfF4B911075845F9e'
            },
            'solana': {
                'USDC': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
                'USDT': 'Es9vMFrzaCERmJfrF4HfFYq4RxuNEb6KnsT2RQB7CYsh',
                'SOL': 'So11111111111111111111111111111111111111112'
            },
            'base': {
                'USDC': '0x833589fCD6eDb6E08f4c34C3F5e5d753940C3fBc',
                'ETH': '0x4200000000000000000000000000000000000006'
            }
        }
        
        return token_addresses.get(chain, {}).get(token_symbol, token_symbol)
    
    async def close(self):
        """鍏抽棴杩炴帴"""
        if self.session:
            await self.session.close()
            logger.info('Smart Trading 杩炴帴宸插叧闂')
