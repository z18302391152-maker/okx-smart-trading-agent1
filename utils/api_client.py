"""
OKX Smart Trading Agent - API Client
OKX API 瀹㈡埛绔锛氱粺涓鐨 API 璇锋眰澶勭悊銆佺惧悕鐢熸垚銆侀敊璇澶勭悊
"""

import asyncio
import aiohttp
import hmac
import base64
import json
from datetime import datetime
from loguru import logger
from typing import Dict, Optional, List
from config import config


class OKXAPIClient:
    """OKX API 瀹㈡埛绔"""
    
    def __init__(self):
        """鍒濆嬪寲 API 瀹㈡埛绔"""
        self.api_key = config.OKX_API_KEY
        self.api_secret = config.OKX_API_SECRET
        self.api_passphrase = config.OKX_API_PASSPHRASE
        self.base_url = config.OKX_API_BASE_URL
        self.session = None
        

        
        logger.info('OKX API Client 鍒濆嬪寲鎴愬姛')
    
    async def __aenter__(self):
        """寮傛ヤ笂涓嬫枃绠＄悊鍣ㄥ叆鍙"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """寮傛ヤ笂涓嬫枃绠＄悊鍣ㄥ嚭鍙"""
        if self.session:
            await self.session.close()
    
    def _generate_signature(self, timestamp: str, method: str, request_path: str, body: str = '') -> str:
        """
        鐢熸垚 API 绛惧悕
        
        Args:
            timestamp: 鏃堕棿鎴
            method: HTTP 鏂规硶
            request_path: 璇锋眰璺寰
            body: 璇锋眰浣
        
        Returns:
            Base64 缂栫爜鐨勭惧悕
        """
        try:
            message = timestamp + method + request_path + body
            mac = hmac.new(
                bytes(self.api_secret, encoding='utf8'),
                bytes(message, encoding='utf-8'),
                digestmod='sha256'
            )
            d = mac.digest()
            return base64.b64encode(d).decode()
        except Exception as e:
            logger.error(f'鐢熸垚绛惧悕澶辫触: {str(e)}')
            raise
    
    def _get_headers(self, method: str, request_path: str, body: str = '') -> Dict:
        """
        鑾峰彇璇锋眰澶
        
        Args:
            method: HTTP 鏂规硶
            request_path: 璇锋眰璺寰
            body: 璇锋眰浣
        
        Returns:
            璇锋眰澶村瓧鍏
        """
        timestamp = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
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
        鍙戦 API 璇锋眰
        
        Args:
            method: HTTP 鏂规硶锛圙ET, POST, PUT, DELETE锛
            endpoint: API 绔鐐
            params: URL 鍙傛暟
            data: 璇锋眰浣撴暟鎹
        
        Returns:
            API 鍝嶅簲鏁版嵁
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f'{self.base_url}{endpoint}'
            
            # 鏋勫缓璇锋眰浣
            body = ''
            if data:
                body = json.dumps(data)
            
            # 鑾峰彇璇锋眰澶
            headers = self._get_headers(method, endpoint, body)
            
            # 鍙戦佽锋眰
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
                raise ValueError(f'涓嶆敮鎸佺殑 HTTP 鏂规硶: {method}')
                
        except Exception as e:
            logger.error(f'API 璇锋眰澶辫触: {str(e)}')
            return {
                'error': str(e),
                'success': False
            }
    
    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """
        澶勭悊 API 鍝嶅簲
        
        Args:
            response: aiohttp 鍝嶅簲瀵硅薄
        
        Returns:
            瑙ｆ瀽鍚庣殑鍝嶅簲鏁版嵁
        """
        try:
            if response.status == 200:
                data = await response.json()
                
                # 妫鏌 OKX API 鍝嶅簲鐮
                if data.get('code') == '0':
                    return {
                        'success': True,
                        'data': data.get('data', []),
                        'message': data.get('msg', '')
                    }
                else:
                    logger.warning(f'API 杩斿洖閿欒: {data.get("msg", "鏈鐭ラ敊璇")}')
                    return {
                        'success': False,
                        'error': data.get('msg', '鏈鐭ラ敊璇'),
                        'code': data.get('code')
                    }
            else:
                error_text = await response.text()
                logger.error(f'HTTP 閿欒: {response.status} - {error_text}')
                return {
                    'success': False,
                    'error': f'HTTP {response.status}',
                    'details': error_text
                }
                
        except Exception as e:
            logger.error(f'澶勭悊鍝嶅簲澶辫触: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get(self, endpoint: str, params: Dict = None) -> Dict:
        """
        GET 璇锋眰
        
        Args:
            endpoint: API 绔鐐
            params: URL 鍙傛暟
        
        Returns:
            API 鍝嶅簲鏁版嵁
        """
        return await self._request('GET', endpoint, params=params)
    
    async def post(self, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """
        POST 璇锋眰
        
        Args:
            endpoint: API 绔鐐
            data: 璇锋眰浣撴暟鎹
            params: URL 鍙傛暟
        
        Returns:
            API 鍝嶅簲鏁版嵁
        """
        return await self._request('POST', endpoint, params=params, data=data)
    
    async def put(self, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """
        PUT 璇锋眰
        
        Args:
            endpoint: API 绔鐐
            data: 璇锋眰浣撴暟鎹
            params: URL 鍙傛暟
        
        Returns:
            API 鍝嶅簲鏁版嵁
        """
        return await self._request('PUT', endpoint, params=params, data=data)
    
    async def delete(self, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """
        DELETE 璇锋眰
        
        Args:
            endpoint: API 绔鐐
            data: 璇锋眰浣撴暟鎹
            params: URL 鍙傛暟
        
        Returns:
            API 鍝嶅簲鏁版嵁
        """
        return await self._request('DELETE', endpoint, params=params, data=data)
    
    async def get_account_balance(self) -> Dict:
        """
        鑾峰彇璐︽埛浣欓
        
        Returns:
            璐︽埛浣欓濅俊鎭
        """
        try:
            logger.info('鑾峰彇璐︽埛浣欓')
            response = await self.get('/api/v5/account/balance')
            
            if response['success']:
                logger.info('璐︽埛浣欓濊幏鍙栨垚鍔')
                return response['data']
            else:
                logger.error(f'鑾峰彇璐︽埛浣欓濆け璐: {response.get("error")}')
                return []
                
        except Exception as e:
            logger.error(f'鑾峰彇璐︽埛浣欓濆紓甯: {str(e)}')
            return []
    
    async def get_wallet_balance(self, chain: str = None) -> Dict:
        """
        鑾峰彇閽卞寘浣欓
        
        Args:
            chain: 鍖哄潡閾剧綉缁
        
        Returns:
            閽卞寘浣欓濅俊鎭
        """
        try:
            logger.info(f'鑾峰彇閽卞寘浣欓濓紙閾: {chain}锛')
            
            params = {}
            if chain:
                params['chainId'] = chain
            
            response = await self.get('/api/v5/wallet/account/balance', params=params)
            
            if response['success']:
                logger.info('閽卞寘浣欓濊幏鍙栨垚鍔')
                return response['data']
            else:
                logger.error(f'鑾峰彇閽卞寘浣欓濆け璐: {response.get("error")}')
                return []
                
        except Exception as e:
            logger.error(f'鑾峰彇閽卞寘浣欓濆紓甯: {str(e)}')
            return []
    
    async def close(self):
        """鍏抽棴杩炴帴"""
        if self.session:
            await self.session.close()
            logger.info('OKX API Client 杩炴帴宸插叧闂')


# 鍒涘缓鍏ㄥ眬 API 瀹㈡埛绔瀹炰緥
api_client = OKXAPIClient()
