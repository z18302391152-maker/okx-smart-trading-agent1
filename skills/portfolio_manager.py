# -*- coding: utf-8 -*-
"""
OKX Smart Trading Agent - Portfolio Manager Skill
璧勪骇绠＄悊鎶鑳斤細澶氶摼璧勪骇鏌ヨ銆佹姇璧勬剧粍鍚堝垎鏋愩佽祫浜т环鍊艰＄畻
"""

import asyncio
import aiohttp
from loguru import logger
from typing import Dict, List, Optional
from datetime import datetime


class PortfolioManager:
    """璧勪骇绠＄悊鎶鑳"""
    
    def __init__(self):
        """鍒濆嬪寲璧勪骇绠＄悊"""
        self.base_url = 'https://www.okx.com'
        self.session = None
        logger.info('Portfolio Manager 鍒濆嬪寲鎴愬姛')
    
    async def __aenter__(self):
        """寮傛ヤ笂涓嬫枃绠＄悊鍣ㄥ叆鍙"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """寮傛ヤ笂涓嬫枃绠＄悊鍣ㄥ嚭鍙"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """鍙戦 API 璇锋眰"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f'{self.base_url}{endpoint}'
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f'API 璇锋眰澶辫触: {response.status}')
                    return {'error': f'HTTP {response.status}'}
                    
        except Exception as e:
            logger.error(f'璇锋眰寮傚父: {str(e)}')
            return {'error': str(e)}
    
    async def get_portfolio_value(
        self,
        wallet_address: str = None,
        chains: List[str] = None
    ) -> Dict:
        """
        鑾峰彇璧勪骇缁勫悎鎬讳环鍊
        
        Args:
            wallet_address: 閽卞寘鍦板潃
            chains: 瑕佹煡璇㈢殑鍖哄潡閾惧垪琛
        
        Returns:
            璧勪骇缁勫悎淇℃伅娆
        """
        try:
            logger.info('鏌ヨ㈣祫浜х粍鍚堟讳环鍊')
            
            if not chains:
                chains = ['ethereum', 'solana', 'base', 'bsc', 'arbitrum', 'polygon']
            
            total_value = 0.0
            assets_by_chain = {}
            
            for chain in chains:
                chain_assets = await self.get_chain_assets(wallet_address, chain)
                chain_value = chain_assets.get('total_value', 0.0)
                
                total_value += chain_value
                assets_by_chain[chain] = chain_assets
            
            result = {
                'total_value': total_value,
                'assets_by_chain': assets_by_chain,
                'chains_analyzed': chains,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f'璧勪骇缁勫悎鎬讳环鍊: ${total_value:.2f}')
            return result
            
        except Exception as e:
            logger.error(f'鏌ヨ㈣祫浜х粍鍚堝け璐: {str(e)}')
            return {
                'total_value': 0.0,
                'error': str(e)
            }
    
    async def get_chain_assets(
        self,
        wallet_address: str = None,
        chain: str = 'ethereum'
    ) -> Dict:
        """
        鑾峰彇鐗瑰畾閾句笂鐨勮祫浜
        
        Args:
            wallet_address: 閽卞寘鍦板潃
            chain: 鍖哄潡閾剧綉缁
        
        Returns:
            閾句笂璧勪骇淇℃伅
        """
        try:
            logger.info(f'鏌ヨ {chain} 閾句笂鐨勮祫浜')
            
            # 鑾峰彇閾句笂璧勪骇
            endpoint = '/api/v5/wallet/account/balance'
            
            params = {
                'chainId': chain
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                assets = []
                total_value = 0.0
                
                for item in response['data']:
                    token_symbol = item['ccy']
                    balance = float(item['bal'])
                    usd_value = float(item.get('usdVal', 0))
                    
                    if balance > 0:
                        assets.append({
                            'token': token_symbol,
                            'balance': balance,
                            'usd_value': usd_value,
                            'chain': chain
                        })
                        total_value += usd_value
                
                result = {
                    'chain': chain,
                    'assets': assets,
                    'total_value': total_value,
                    'asset_count': len(assets)
                }
                
                logger.info(f'{chain} 閾捐祫浜т环鍊: ${total_value:.2f}')
                return result
            else:
                logger.warning(f'鑾峰彇 {chain} 閾捐祫浜уけ璐: {response}')
                return {
                    'chain': chain,
                    'assets': [],
                    'total_value': 0.0
                }
                
        except Exception as e:
            logger.error(f'鏌ヨ㈤摼涓婅祫浜уけ璐: {str(e)}')
            return {
                'chain': chain,
                'assets': [],
                'total_value': 0.0,
                'error': str(e)
            }
    
    async def get_token_balance(
        self,
        token_symbol: str,
        wallet_address: str = None,
        chain: str = 'ethereum'
    ) -> Dict:
        """
        鑾峰彇鐗瑰畾浠ｅ竵浣欓
        
        Args:
            token_symbol: 浠ｅ竵绗﹀彿
            wallet_address: 閽卞寘鍦板潃
            chain: 鍖哄潡閾剧綉缁
        
        Returns:
            浠ｅ竵浣欓濅俊鎭
        """
        try:
            logger.info(f'鏌ヨ {token_symbol} 浣欓')
            
            # 鑾峰彇浠ｅ竵浣欓
            endpoint = '/api/v5/wallet/account/balance'
            
            params = {
                'chainId': chain,
                'ccy': token_symbol
            }
            
            response = await self._make_request(endpoint, params)
            
            if 'error' not in response and 'data' in response:
                for item in response['data']:
                    if item['ccy'] == token_symbol:
                        balance = float(item['bal'])
                        usd_value = float(item.get('usdVal', 0))
                        
                        result = {
                            'token': token_symbol,
                            'balance': balance,
                            'usd_value': usd_value,
                            'chain': chain
                        }
                        
                        logger.info(f'{token_symbol} 浣欓: {balance} (${usd_value:.2f})')
                        return result
                
                return {
                    'token': token_symbol,
                    'balance': 0.0,
                    'usd_value': 0.0
                }
            else:
                logger.warning(f'鑾峰彇 {token_symbol} 浣欓濆け璐: {response}')
                return {
                    'token': token_symbol,
                    'balance': 0.0,
                    'usd_value': 0.0
                }
                
        except Exception as e:
            logger.error(f'鏌ヨ浠ｅ竵浣欓濆け璐: {str(e)}')
            return {
                'token': token_symbol,
                'balance': 0.0,
                'usd_value': 0.0,
                'error': str(e)
            }
    
    async def analyze_portfolio_distribution(
        self,
        wallet_address: str = None,
        chains: List[str] = None
    ) -> Dict:
        """
        鍒嗘瀽璧勪骇缁勫悎鍒嗗竷
        
        Args:
            wallet_address: 閽卞寘鍦板潃
            chains: 瑕佹煡璇㈢殑鍖哄潡閾惧垪琛
        
        Returns:
            璧勪骇缁勫悎鍒嗗竷鍒嗘瀽
        """
        try:
            logger.info('鍒嗘瀽璧勪骇缁勫悎鍒嗗竷')
            
            # 鑾峰彇璧勪骇缁勫悎
            portfolio = await self.get_portfolio_value(wallet_address, chains)
            
            total_value = portfolio.get('total_value', 0.0)
            
            if total_value == 0:
                return {
                    'total_value': 0.0,
                    'distribution': {},
                    'message': '鏃犺祫浜'
                }
            
            # 鎸変唬甯佺粺璁
            token_distribution = {}
            chain_distribution = {}
            
            for chain, chain_data in portfolio.get('assets_by_chain', {}).items():
                chain_value = chain_data.get('total_value', 0.0)
                chain_distribution[chain] = {
                    'value': chain_value,
                    'percentage': (chain_value / total_value) * 100
                }
                
                for asset in chain_data.get('assets', []):
                    token = asset['token']
                    token_value = asset['usd_value']
                    
                    if token not in token_distribution:
                        token_distribution[token] = {
                            'value': 0.0,
                            'chains': []
                        }
                    
                    token_distribution[token]['value'] += token_value
                    token_distribution[token]['chains'].append(chain)
            
            # 璁＄畻浠ｅ竵鐧惧垎姣
            for token, data in token_distribution.items():
                data['percentage'] = (data['value'] / total_value) * 100
            
            result = {
                'total_value': total_value,
                'token_distribution': token_distribution,
                'chain_distribution': chain_distribution,
                'top_tokens': sorted(
                    token_distribution.items(),
                    key=lambda x: x[1]['value'],
                    reverse=True
                )[:10],
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info('璧勪骇缁勫悎鍒嗗竷鍒嗘瀽瀹屾垚')
            return result
            
        except Exception as e:
            logger.error(f'鍒嗘瀽璧勪骇缁勫悎鍒嗗竷澶辫触: {str(e)}')
            return {
                'error': str(e)
            }
    
    async def get_portfolio_performance(
        self,
        wallet_address: str = None,
        days: int = 7
    ) -> Dict:
        """
        鑾峰彇璧勪骇缁勫悎琛ㄧ幇
        
        Args:
            wallet_address: 閽卞寘鍦板潃
            days: 鏌ヨ㈠ぉ鏁
        
        Returns:
            璧勪骇缁勫悎琛ㄧ幇鏁版嵁
        """
        try:
            logger.info(f'鏌ヨ㈣祫浜х粍鍚堣〃鐜帮紙鏈杩 {days} 澶╋級')
            
            # 鑾峰彇褰撳墠璧勪骇缁勫悎
            current_portfolio = await self.get_portfolio_value(wallet_address)
            current_value = current_portfolio.get('total_value', 0.0)
            
            # 妯℃嫙鍘嗗彶鏁版嵁锛堝疄闄呭簲鐢ㄤ腑搴斾粠鏁版嵁搴撴垨 API 鑾峰彇锛
            # 杩欓噷浣跨敤妯℃嫙鏁版嵁婕旂ず
            import random
            
            historical_values = []
            base_value = current_value * 0.9  # 鍋囪 7 澶╁墠浠峰间负褰撳墠鐨 90%
            
            for i in range(days):
                change = random.uniform(-0.02, 0.03)  # 姣忓ぉ鍙樺寲 -2% 鍒 +3%
                base_value = base_value * (1 + change)
                historical_values.append({
                    'day': i + 1,
                    'value': base_value,
                    'date': (datetime.now()).strftime('%Y-%m-%d')
                })
            
            # 璁＄畻鏀剁泭鐜
            if len(historical_values) > 0:
                start_value = historical_values[0]['value']
                total_return = ((current_value - start_value) / start_value) * 100
            else:
                total_return = 0.0
            
            result = {
                'current_value': current_value,
                'start_value': historical_values[0]['value'] if historical_values else 0.0,
                'total_return': total_return,
                'period_days': days,
                'historical_values': historical_values,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f'璧勪骇缁勫悎琛ㄧ幇: {total_return:.2f}% ({days} 澶)')
            return result
            
        except Exception as e:
            logger.error(f'鏌ヨ㈣祫浜х粍鍚堣〃鐜板け璐: {str(e)}')
            return {
                'error': str(e)
            }
    
    async def close(self):
        """鍏抽棴杩炴帴"""
        if self.session:
            await self.session.close()
            logger.info('Portfolio Manager 杩炴帴宸插叧闂')
