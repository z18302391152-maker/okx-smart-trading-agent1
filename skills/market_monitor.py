# -*- coding: utf-8 -*-
"""
OKX Smart Trading Agent - Market Monitor Skill
Market monitoring: real-time price tracking, K-line data analysis, trade history
"""

import asyncio
import aiohttp
from loguru import logger
from typing import Dict, List, Optional
from datetime import datetime


class MarketMonitor:
    """Market monitoring skill"""
    
    def __init__(self):
        """Initialize market monitor"""
        self.base_url = 'https://www.okx.com'
        self.session = None
        logger.info('Market Monitor initialized successfully')
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Send API request"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f'{self.base_url}{endpoint}'
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f'API request failed: {response.status}')
                    return {'error': f'HTTP {response.status}'}
                    
        except Exception as e:
            logger.error(f'Request exception: {str(e)}')
            return {'error': str(e)}
    
    async def get_token_price(
        self, 
        token_symbol: str, 
        chain: str = 'ethereum',
        quote_token: str = 'USDC'
    ) -> Optional[float]:
        """
        Get token price
        
        Args:
            token_symbol: Token symbol (e.g., 'OKB', 'SOL')
            chain: Blockchain network
            quote_token: Quote token (default USDC)
        
        Returns:
            Token price
        """
        try:
            logger.info(f'Querying {token_symbol} price on {chain}')
            
            # OKX DEX Market API
            endpoint = '/api/v5/dex/aggregator/quote'
            
            params = {
                'chainId': chain,
                'fromTokenAddress': self._get_token_address(token_symbol, chain),
                'toTokenAddress': self._get_token_address(quote_token, chain),
                'amount': '1'
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                price = float(response['data'][0]['toAmount'])
                logger.info(f'{token_symbol} price: ${price:.6f}')
                return price
            else:
                logger.warning(f'Failed to get price: {response}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to get token price: {str(e)}')
            return None
    
    async def get_kline_data(
        self,
        token_symbol: str,
        chain: str = 'ethereum',
        interval: str = '1H',
        limit: int = 100
    ) -> List[Dict]:
        """
        Get K-line data
        
        Args:
            token_symbol: Token symbol
            chain: Blockchain network
            interval: Time interval (1m, 5m, 15m, 1H, 4H, 1D)
            limit: Number of data points
        
        Returns:
            K-line data list
        """
        try:
            logger.info(f'Getting {token_symbol} K-line data, interval: {interval}')
            
            endpoint = '/api/v5/market/candles'
            
            params = {
                'instId': f'{token_symbol}-USDC',
                'bar': interval,
                'limit': str(limit)
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                klines = []
                for item in response['data']:
                    klines.append({
                        'timestamp': int(item[0]),
                        'open': float(item[1]),
                        'high': float(item[2]),
                        'low': float(item[3]),
                        'close': float(item[4]),
                        'volume': float(item[5]),
                        'datetime': datetime.fromtimestamp(int(item[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                logger.info(f'Got {len(klines)} K-line data points')
                return klines
            else:
                logger.warning(f'Failed to get K-line data: {response}')
                return []
                
        except Exception as e:
            logger.error(f'Failed to get K-line data: {str(e)}')
            return []
    
    async def get_trade_history(
        self,
        token_symbol: str,
        chain: str = 'ethereum',
        limit: int = 50
    ) -> List[Dict]:
        """
        Get trade history
        
        Args:
            token_symbol: Token symbol
            chain: Blockchain network
            limit: Number of trades
        
        Returns:
            Trade history list
        """
        try:
            logger.info(f'Getting {token_symbol} trade history')
            
            endpoint = '/api/v5/market/trades'
            
            params = {
                'instId': f'{token_symbol}-USDC',
                'limit': str(limit)
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                trades = []
                for item in response['data']:
                    trades.append({
                        'trade_id': item[0],
                        'price': float(item[1]),
                        'size': float(item[2]),
                        'side': item[3],
                        'timestamp': int(item[4]),
                        'datetime': datetime.fromtimestamp(int(item[4]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                logger.info(f'Got {len(trades)} trade records')
                return trades
            else:
                logger.warning(f'Failed to get trade history: {response}')
                return []
                
        except Exception as e:
            logger.error(f'Failed to get trade history: {str(e)}')
            return []
    
    async def get_ticker_24h(self, token_symbol: str) -> Dict:
        """
        Get 24-hour ticker data
        
        Args:
            token_symbol: Token symbol
        
        Returns:
            24-hour ticker data
        """
        try:
            logger.info(f'Getting {token_symbol} 24-hour ticker')
            
            endpoint = '/api/v5/market/ticker'
            
            params = {
                'instId': f'{token_symbol}-USDC'
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                data = response['data'][0]
                return {
                    'last_price': float(data['last']),
                    '24h_high': float(data['high24h']),
                    '24h_low': float(data['low24h']),
                    '24h_volume': float(data['vol24h']),
                    '24h_change': float(data['sodUtc8'])
                }
            else:
                logger.warning(f'Failed to get 24-hour ticker: {response}')
                return {}
                
        except Exception as e:
            logger.error(f'Failed to get 24-hour ticker: {str(e)}')
            return {}
    
    def _get_token_address(self, token_symbol: str, chain: str) -> str:
        """
        Get token address
        
        Args:
            token_symbol: Token symbol
            chain: Blockchain network
        
        Returns:
            Token address
        """
        # Common token address mapping
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
        """Close connection"""
        if self.session:
            await self.session.close()
            logger.info('Market Monitor connection closed')
