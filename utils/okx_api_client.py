# -*- coding: utf-8 -*-
"""
OKX OnchainOS API Client
Standard OKX API client following official documentation
"""

import hmac
import base64
import json
import time
import aiohttp
from loguru import logger
from typing import Dict, Optional
from config import config


class OKXOnchainOSClient:
    """OKX OnchainOS API Client"""
    
    def __init__(self):
        """Initialize OKX API client"""
        self.api_key = config.OKX_API_KEY
        self.api_secret = config.OKX_API_SECRET
        self.api_passphrase = config.OKX_API_PASSPHRASE
        self.base_url = config.OKX_API_BASE_URL
        self.session = None
        
        logger.info('OKX OnchainOS API Client initialized')
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _generate_signature(self, timestamp: str, method: str, request_path: str, body: str = '') -> str:
        """
        Generate API signature
        
        Args:
            timestamp: ISO format timestamp
            method: HTTP method (GET, POST, etc.)
            request_path: API endpoint path
            body: Request body (empty for GET requests)
        
        Returns:
            Base64 encoded signature
        """
        try:
            message = timestamp + method + request_path + body
            mac = hmac.new(
                bytes(self.api_secret, encoding='utf-8'),
                bytes(message, encoding='utf-8'),
                digestmod='sha256'
            )
            d = mac.digest()
            return base64.b64encode(d).decode()
        except Exception as e:
            logger.error(f'Failed to generate signature: {str(e)}')
            raise
    
    def _get_headers(self, method: str, request_path: str, body: str = '') -> Dict:
        """
        Get request headers
        
        Args:
            method: HTTP method
            request_path: API endpoint path
            body: Request body
        
        Returns:
            Headers dictionary
        """
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        signature = self._generate_signature(timestamp, method, request_path, body)
        
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.api_passphrase,
            'Content-Type': 'application/json'
        }
        
        return headers
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None
    ) -> Dict:
        """
        Send API request
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: URL parameters
            data: Request body data
        
        Returns:
            API response data
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f'{self.base_url}{endpoint}'
            
            # Build request body
            body = ''
            if data:
                body = json.dumps(data)
            
            # Get headers
            headers = self._get_headers(method, endpoint, body)
            
            # Send request
            if method == 'GET':
                async with self.session.get(url, params=params, headers=headers) as response:
                    return await self._handle_response(response)
            elif method == 'POST':
                async with self.session.post(url, params=params, data=body, headers=headers) as response:
                    return await self._handle_response(response)
            elif method == 'PUT':
                async with self.session.put(url, params=params, data=body, headers=headers) as response:
                    return await self._handle_response(response)
            elif method == 'DELETE':
                async with self.session.delete(url, params=params, data=body, headers=headers) as response:
                    return await self._handle_response(response)
            else:
                raise ValueError(f'Unsupported HTTP method: {method}')
                
        except Exception as e:
            logger.error(f'Request failed: {str(e)}')
            return {
                'code': '-1',
                'msg': str(e),
                'data': []
            }
    
    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """
        Handle API response
        
        Args:
            response: aiohttp response object
        
        Returns:
            Parsed response data
        """
        try:
            if response.status == 200:
                data = await response.json()
                
                # Check OKX API response code
                if data.get('code') == '0':
                    return {
                        'code': '0',
                        'msg': data.get('msg', ''),
                        'data': data.get('data', [])
                    }
                else:
                    logger.warning(f'API returned error: {data.get("msg", "Unknown error")}')
                    return {
                        'code': data.get('code', '-1'),
                        'msg': data.get('msg', 'Unknown error'),
                        'data': data.get('data', [])
                    }
            else:
                error_text = await response.text()
                logger.error(f'HTTP error: {response.status} - {error_text}')
                return {
                    'code': str(response.status),
                    'msg': f'HTTP {response.status}',
                    'data': []
                }
                
        except Exception as e:
            logger.error(f'Failed to handle response: {str(e)}')
            return {
                'code': '-1',
                'msg': str(e),
                'data': []
            }
    
    # OKX DEX Aggregator API methods
    
    async def get_swap_quote(
        self,
        chain_id: str,
        from_token_address: str,
        to_token_address: str,
        amount: str,
        slippage: str = '0.005'
    ) -> Optional[Dict]:
        """
        Get swap quote
        
        Args:
            chain_id: Chain ID (e.g., '1' for Ethereum, '56' for BSC)
            from_token_address: Source token address
            to_token_address: Target token address
            amount: Amount to swap
            slippage: (Optional) Slippage percentage (default 0.5%)
        
        Returns:
            Quote data
        """
        try:
            logger.info(f'Getting swap quote: {amount} tokens')
            
            endpoint = '/api/v5/dex/aggregator/quote'
            
            params = {
                'chainId': chain_id,
                'fromTokenAddress': from_token_address,
                'toTokenAddress': to_token_address,
                'amount': amount,
                'slippage': slippage
            }
            
            response = await self._request('GET', endpoint, params=params)
            
            if response['code'] == '0' and response['data']:
                return response['data'][0]
            else:
                logger.warning(f'Failed to get quote: {response["msg"]}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to get swap quote: {str(e)}')
            return None
    
    async def get_swap_routes(
        self,
        chain_id: str,
        from_token_address: str,
        to_token_address: str,
        amount: str
    ) -> Optional[Dict]:
        """
        Get all swap routes
        
        Args:
            chain_id: Chain ID
            from_token_address: Source token address
            to_token_address: Target token address
            amount: Amount to swap
        
        Returns:
            Routes data
        """
        try:
            logger.info('Getting swap routes')
            
            endpoint = '/api/v5/dex/aggregator/allRoutes'
            
            params = {
                'chainId': chain_id,
                'fromTokenAddress': from_token_address,
                'toTokenAddress': to_token_address,
                'amount': amount
            }
            
            response = await self._request('GET', endpoint, params=params)
            
            if response['code'] == '0' and response['data']:
                return response['data']
            else:
                logger.warning(f'Failed to get routes: {response["msg"]}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to get swap routes: {str(e)}')
            return None
    
    async def build_swap_transaction(
        self,
        chain_id: str,
        from_token_address: str,
        to_token_address: str,
        amount: str,
        slippage: str = '0.005',
        user_address: str = None
    ) -> Optional[Dict]:
        """
        Build swap transaction
        
        Args:
            chain_id: Chain ID
            from_token_address: Source token address
            to_token_address: Target token address
            amount: Amount to swap
            slippage: Slippage percentage
            user_address: User wallet address
        
        Returns:
            Transaction data
        """
        try:
            logger.info('Building swap transaction')
            
            endpoint = '/api/v5/dex/aggregator/buildTx'
            
            params = {
                'chainId': chain_id,
                'fromTokenAddress': from_token_address,
                'toTokenAddress': to_token_address,
                'amount': amount,
                'slippage': slippage
            }
            
            if user_address:
                params['userAddress'] = user_address
            
            response = await self._request('GET', endpoint, params=params)
            
            if response['code'] == '0' and response['data']:
                return response['data'][0]
            else:
                logger.warning(f'Failed to build transaction: {response["msg"]}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to build transaction: {str(e)}')
            return None
    
    # OKX Market API methods
    
    async def get_ticker(self, inst_id: str) -> Optional[Dict]:
        """
        Get ticker data
        
        Args:
            inst_id: Instrument ID (e.g., 'BTC-USDT')
        
        Returns:
            Ticker data
        """
        try:
            logger.info(f'Getting ticker: {inst_id}')
            
            endpoint = '/api/v5/market/ticker'
            
            params = {'instId': inst_id}
            
            response = await self._request('GET', endpoint, params=params)
            
            if response['code'] == '0' and response['data']:
                return response['data'][0]
            else:
                logger.warning(f'Failed to get ticker: {response["msg"]}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to get ticker: {str(e)}')
            return None
    
    async def get_candles(
        self,
        inst_id: str,
        bar: str = '1H',
        limit: str = '100'
    ) -> Optional[list]:
        """
        Get candle data
        
        Args:
            inst_id: Instrument ID
            bar: Time bar (1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 12H, 1D, 1W, 1M)
            limit: Number of candles (max 300)
        
        Returns:
            Candle data
        """
        try:
            logger.info(f'Getting candles: {inst_id}')
            
            endpoint = '/api/v5/market/candles'
            
            params = {
                'instId': inst_id,
                'bar': bar,
                'limit': limit
            }
            
            response = await self._request('GET', endpoint, params=params)
            
            if response['code'] == '0' and response['data']:
                return response['data']
            else:
                logger.warning(f'Failed to get candles: {response["msg"]}')
                return None
                
        except Exception as e:
            logger.error(f'Failed to get candles: {str(e)}')
            return None
    
    async def close(self):
        """Close connection"""
        if self.session:
            await self.session.close()
            logger.info('OKX OnchainOS API Client connection closed')


# Create global API client instance
okx_api_client = OKXOnchainOSClient()
