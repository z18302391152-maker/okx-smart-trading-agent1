# -*- coding: utf-8 -*-
"""
OKX Smart Trading Agent - Risk Manager Skill
Risk management: liquidity assessment, slippage optimization, trading risk alerts
"""

import asyncio
import aiohttp
from loguru import logger
from typing import Dict, Optional
from datetime import datetime


class RiskManager:
    """Risk management skill"""
    
    def __init__(self):
        """Initialize risk manager"""
        self.base_url = 'https://www.okx.com'
        self.session = None
        
        # Risk threshold configuration
        self.max_slippage = 5.0  # Maximum slippage 5%
        self.min_liquidity = 10000  # Minimum liquidity $10,000
        self.max_price_impact = 1.0  # Maximum price impact 1%
        
        logger.info('Risk Manager initialized successfully')
    
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
    
    async def check_swap_risk(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum',
        slippage: float = 0.5
    ) -> Dict:
        """
        Check swap risk
        
        Args:
            from_token: Source token symbol
            to: Target token symbol
            amount: Swap amount
            chain: Blockchain network
            slippage: Slippage percentage
        
        Returns:
            Risk check result
        """
        try:
            logger.info(f'Checking swap risk: {amount} {from_token} -> {to_token}')
            
            risk_factors = []
            is_safe = True
            
            # 1. Check slippage
            if slippage > self.max_slippage:
                risk_factors.append(f'Slippage too high: {slippage}% > {self.max_slippage}%')
                is_safe = False
            
            # 2. Check liquidity
            liquidity = await self.check_liquidity(from_token, chain)
            if liquidity < self.min_liquidity:
                risk_factors.append(f'Insufficient liquidity: ${liquidity} < ${self.min_liquidity}')
                is_safe = False
            
            # 3. Check price impact
            price_impact = await self.check_price_impact(from_token, to_token, amount, chain)
            if price_impact > self.max_price_impact:
                risk_factors.append(f'Price impact too high: {price_impact}% > {self.max_price_impact}%')
                is_safe = False
            
            # 4. Check token safety
            token_safe = await self.check_token_safety(to_token, chain)
            if not token_safe['safe']:
                risk_factors.append(f'Token safety warning: {token_safe["reason"]}')
                is_safe = False
            
            result = {
                'safe': is_safe,
                'risk_factors': risk_factors,
                'liquidity': liquidity,
                'price_impact': price_impact,
                'token_safe': token_safe,
                'timestamp': datetime.now().isoformat()
            }
            
            if is_safe:
                logger.info('Risk check passed')
            else:
                logger.warning(f'Risk check failed: {risk_factors}')
            
            return result
            
        except Exception as e:
            logger.error(f'Risk check failed: {str(e)}')
            return {
                'safe': False,
                'reason': str(e)
            }
    
    async def check_liquidity(self, token_symbol: str, chain: str = 'ethereum') -> float:
        """
        Check token liquidity
        
        Args:
            token_symbol: Token symbol
            chain: Blockchain network
        
        Returns:
            Liquidity amount in USD
        """
        try:
            logger.info(f'Checking {token_symbol} liquidity')
            
            # Get token information
            endpoint = '/api/v5/dex/aggregator/token'
            
            params = {
                'chainId': chain,
                'tokenAddress': self._get_token_address(token_symbol, chain)
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                token_data = response['data'][0]
                liquidity = float(token_data.get('liquidity', 0))
                logger.info(f'{token_symbol} liquidity: ${liquidity:.2f}')
                return liquidity
            else:
                logger.warning(f'Failed to get liquidity: {response}')
                return 0.0
                
        except Exception as e:
            logger.error(f'Failed to check liquidity: {str(e)}')
            return 0.0
    
    async def check_price_impact(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum'
    ) -> float:
        """
        Check price impact
        
        Args:
            from_token: Source token symbol
            to_token: Target token symbol
            amount: Swap amount
            chain: Blockchain network
        
        Returns:
            Price impact percentage
        """
        try:
            logger.info(f'Checking price impact: {amount} {from_token} -> {to_token}')
            
            # Get quote
            endpoint = '/api/v5/dex/aggregator/quote'
            
            params = {
                'chainId': chain,
                'fromTokenAddress': self._get_token_address(from_token, chain),
                'toTokenAddress': self._get_token_address(to_token, chain),
                'amount': str(amount),
                'slippage': '0.01'
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                quote = response['data'][0]
                price_impact = float(quote.get('priceImpact', 0)) * 100
                logger.info(f'Price impact: {price_impact:.2f}%')
                return price_impact
            else:
                logger.warning(f'Failed to get price impact: {response}')
                return 0.0
                
        except Exception as e:
            logger.error(f'Failed to check price impact: {str(e)}')
            return 0.0
    
    async def check_token_safety(self, token_symbol: str, chain: str = 'ethereum') -> Dict:
        """
        Check token safety
        
        Args:
            token_symbol: Token symbol
            chain: Blockchain network
        
        Returns:
            Token safety information
        """
        try:
            logger.info(f'Checking {token_symbol} safety')
            
            # Get token information
            endpoint = '/api/v5/dex/aggregator/token'
            
            params = {
                'chainId': chain,
                'tokenAddress': self._get_token_address(token_symbol, chain)
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                token_data = response['data'][0]
                
                # Check if token is verified
                is_verified = token_data.get('verified', False)
                has_liquidity = float(token_data.get('liquidity', 0)) > 0
                
                safety_issues = []
                
                if not is_verified:
                    safety_issues.append('Token not verified')
                
                if not has_liquidity:
                    safety_issues.append('Token has no liquidity')
                
                result = {
                    'safe': len(safety_issues) == 0,
                    'verified': is_verified,
                    'has_liquidity': has_liquidity,
                    'issues': safety_issues,
                    'token_info': token_data
                }
                
                if result['safe']:
                    logger.info(f'{token_symbol} safety check passed')
                else:
                    logger.warning(f'{token_symbol} safety warning: {safety_issues}')
                
                return result
            else:
                logger.warning(f'Failed to get token information: {response}')
                return {
                    'safe': False,
                    'reason': 'Unable to get token information'
                }
                
        except Exception as e:
            logger.error(f'Failed to check token safety: {str(e)}')
            return {
                'safe': False,
                'reason': str(e)
            }
    
    async def optimize_slippage(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        chain: str = 'ethereum'
    ) -> Dict:
        """
        Optimize slippage settings
        
        Args:
            from_token: Source token symbol
            to_token: Target token symbol
            amount: Swap amount
            chain: Blockchain network
        
        Returns:
            Optimized slippage recommendation
        """
        try:
            logger.info(f'Optimizing slippage: {amount} {from_token} -> {to_token}')
            
            # Check liquidity
            liquidity = await self.check_liquidity(from_token, chain)
            
            # Recommend slippage based on liquidity
            if liquidity > 1000000:  # High liquidity
                recommended_slippage = 0.3
            elif liquidity > 100000:  # Medium liquidity
                recommended_slippage = 0.5
            elif liquidity > 10000:  # Low liquidity
                recommended_slippage = 1.0
            else:  # Very low liquidity
                recommended_slippage = 2.0
            
            result = {
                'recommended_slippage': recommended_slippage,
                'liquidity': liquidity,
                'reason': f'Based on ${liquidity:.2f} liquidity, recommend {recommended_slippage}% slippage'
            }
            
            logger.info(f'Recommended slippage: {recommended_slippage}%')
            return result
            
        except Exception as e:
            logger.error(f'Failed to optimize slippage: {str(e)}')
            return {
                'recommended_slippage': 0.5,
                'reason': 'Using default slippage'
            }
    
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
            logger.info('Risk Manager connection closed')
