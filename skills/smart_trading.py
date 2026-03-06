# -*- coding: utf-8 -*-
"""
OKX Smart Trading Agent - Smart Trading Skill
Smart trading: optimal route finding, slippage control, cross-chain trading
"""

import asyncio
import aiohttp
from loguru import logger
from typing import Dict, Optional
from datetime import datetime


class SmartTrading:
    """Smart trading skill"""
    
    def __init__(self):
        """Initialize smart trading"""
        self.base_url = 'https://www.okx.com'
        self.session = None
        logger.info('Smart Trading initialized successfully')
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None, method: str = 'GET') -> Dict:
        """Send API request"""
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
                        logger.error(f'API request failed: {response.status}')
                        return {'error': f'HTTP {response.status}'}
            elif method == 'POST':
                async with self.session.post(url, json=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.error(f'API request failed: {response.status}')
                        return {'error': f'HTTP {response.status}'}
                    
        except Exception as e:
            logger.error(f'Request exception: {str(e)}')
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
        Get swap quote
        
        Args:
            from_token: Source token symbol
            to_token: Target token symbol
            amount: Swap amount
            chain: Blockchain network
            slippage: Slippage percentage
        
        Returns:
            Swap quote information
        """
        try:
            logger.info(f'Getting swap quote: {amount} {from_token} -> {to_token}')
            
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
                logger.info(f'Quote: {quote["toAmount"]} {to_token}')
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
                logger.warning(f'Failed to get quote: {response}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to get swap quote: {str(e)}')
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
        Execute token swap
        
        Args:
            from_token: Source token symbol
            to_token: Target token symbol
            amount: Swap amount
            chain: Blockchain network
            slippage: Slippage percentage
            user_address: User wallet address
        
        Returns:
            Swap result
        """
        try:
            logger.info(f'Executing swap: {amount} {from_token} -> {to_token}')
            
            # 1. Get quote
            quote = await self.get_swap_quote(from_token, to_token, amount, chain, slippage)
            
            if not quote:
                return {
                    'success': False,
                    'reason': 'Failed to get quote'
                }
            
            # 2. Build transaction
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
                
                logger.info(f'Transaction built, waiting for signature and broadcast')
                
                return {
                    'success': True,
                    'quote': quote,
                    'tx_data': tx_data,
                    'message': 'Transaction built, needs user signature and broadcast',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.warning(f'Failed to build transaction: {response}')
                return {
                    'success': False,
                    'reason': 'Failed to build transaction',
                    'error': response
                }
                
        except Exception as e:
            logger.error(f'Failed to execute swap: {str(e)}')
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
        Find best trading route
        
        Args:
            from_token: Source token symbol
            to_token: Target token symbol
            amount: Swap amount
            chain: Blockchain network
        
        Returns:
            Best route information
        """
        try:
            logger.info(f'Finding best route: {from_token} -> {to_token}')
            
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
                
                # Find best route (maximum output amount)
                best_route = max(routes, key=lambda x: float(x['toAmount']))
                
                logger.info(f'Best route: {best_route}')
                return {
                    'best_route': best_route,
                    'all_routes': routes,
                    'from_token': from_token,
                    'to_token': to_token,
                    'amount': amount
                }
            else:
                logger.warning(f'Failed to find routes: {response}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to find best route: {str(e)}')
            return None
    
    async def estimate_gas(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum'
    ) -> Optional[Dict]:
        """
        Estimate gas fee
        
        Args:
            from_token: Source token symbol
            to_token: Target token symbol
            amount: Swap amount
            chain: Blockchain network
        
        Returns:
            Gas fee information
        """
        try:
            logger.info(f'Estimating gas fee: {from_token} -> {to_token}')
            
            # Get quote information

            quote = await self.get_swap_quote(from_token, to_token, amount, chain)
            
            if quote and 'gas_price' in quote:
                gas_price = float(quote['gas_price'])
                gas_limit = 210000  # Default gas limit
                
                gas_fee = gas_price * gas_limit / 10**18  # Convert to ETH
                
                return {
                    'gas_price': gas_price,
                    'gas_limit': gas_limit,
                    'gas_fee': gas_fee,
                    'gas_fee_usd': gas_fee * 2000  # Assume ETH price is $2000
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f'Failed to estimate gas fee: {str(e)}')
            return None
    
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
            'bsc': {
                'USDT': '0x55d398326b9b594e4fb1e36dc3b0e4f976b0fab',
                'BNB': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d01794C9d4',
                'BUSD': '0xe9e7CEA3Ded6914Ad9badcFdD84924298Ae8D741'
            },
            'solana': {
                'USDC': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
                'USDT': 'Es9vMFrzaCERmJfrF4HfFYq4RxuNEb6KnsT2RQB7CYsh',
                'SOL': 'So11111111111111111111111111111111111111111112'
            },
            'base': {
                'USDC': '0x833589fCD6eDb6E08f4c34C3F5e5d753940C3fBc',
                'ETH': '0x4200000000000000000000000000000000000000006'
            }
        }
        
        return token_addresses.get(chain, {}).get(token_symbol, token_symbol)
    
    async def close(self):
        """Close connection"""
        if self.session:
            await self.session.close()
            logger.info('Smart Trading connection closed')
