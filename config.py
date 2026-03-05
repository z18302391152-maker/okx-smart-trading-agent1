"""
OKX Smart Trading Agent - Configuration File
閰嶇疆鏂囦欢锛氱＄悊 API 瀵嗛挜銆佺綉缁滆剧疆鍜屽叾浠栭厤缃鍙傛暟
"""

import os
from dotenv import load_dotenv

# 鍔犺浇鐜澧冨彉閲
load_dotenv()

class Config:
    """閰嶇疆绫"""
    
    # OKX API 閰嶇疆
    OKX_API_KEY = os.getenv('OKX_API_KEY', '')
    OKX_API_SECRET = os.getenv('OKX_API_SECRET', '')
    OKX_API_PASSPHRASE = os.getenv('OKX_API_PASSPHRASE', '')
    
    # API 绔鐐
    OKX_API_BASE_URL = 'https://www.okx.com'
    OKX_API_PUBLIC_URL = 'https://www.okx.com'
    
    # 鏀鎸佺殑鍖哄潡閾剧綉缁
    SUPPORTED_CHAINS = [
        'xlayer',
        'solana',
        'ethereum',
        'base',
        'bsc',
        'arbitrum',
        'polygon',
        'optimism',
        'avalanche',
        'fantom',
        'aurora',
        'harmony',
        'cronos',
        'moonbeam',
        'celo',
        'heco',
        'kcc',
        'okc',
        'metis',
        'boba',
        'canto'
    ]
    
    # 榛樿ら厤缃
    DEFAULT_CHAIN = 'ethereum'
    DEFAULT_SLIPPAGE = 0.5  # 榛樿ゆ粦鐐 0.5%
    DEFAULT_GAS_PRICE = 'medium'  # low, medium, high
    
    # 椋庨櫓绠＄悊閰嶇疆
    MAX_SLIPPAGE = 5.0  # 鏈澶ф粦鐐 5%
    MIN_LIQUIDITY = 10000  # 鏈灏忔祦鍔ㄦ $10,000
    MAX_TRADE_AMOUNT = 10000  # 鍗曠瑪鏈澶т氦鏄撻噾棰 $10,000
    
    # 浜ゆ槗閰嶇疆
    TRANSACTION_TIMEOUT = 300  # 浜ゆ槗瓒呮椂鏃堕棿锛堢掞級
    CONFIRMATION_BLOCKS = 2  # 纭璁ゅ尯鍧楁暟
    
    # 鏃ュ織閰嶇疆
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'trading_agent.log'
    
    # 缂撳瓨閰嶇疆
    CACHE_ENABLED = True
    CACHE_TTL = 60  # 缂撳瓨杩囨湡鏃堕棿锛堢掞級
    
    @classmethod
    def validate_config(cls):
        """楠岃瘉閰嶇疆"""
        if not cls.OKX_API_KEY:
            raise ValueError('OKX_API_KEY 鏈璁剧疆')
        if not cls.OKX_API_SECRET:
            raise ValueError('OKX_API_SECRET 鏈璁剧疆')
        if not cls.OKX_API_PASSPHRASE:
            raise ValueError('OKX_API_PASSPHRASE 鏈璁剧疆')
        return True
    
    @classmethod
    def get_chain_config(cls, chain):
        """鑾峰彇鐗瑰畾閾剧殑閰嶇疆"""
        chain_configs = {
            'ethereum': {
                'chain_id': 1,
                'native_token': 'ETH',
                'rpc_url': 'https://mainnet.infura.io/v3/YOUR_INFURA_KEY'
            },
            'solana': {
                'chain_id': 'solana',
                'native_token': 'SOL',
                'rpc_url': 'https://api.mainnet-beta.solana.com'
            },
            'base': {
                'chain_id': 8453,
                'native_token': 'ETH',
                'rpc_url': 'https://mainnet.base.org'
            },
            'bsc': {
                'chain_id': 56,
                'native_token': 'BNB',
                'rpc_url': 'https://bsc-dataseed.binance.org'
            },
            'arbitrum': {
                'chain_id': 42161,
                'native_token': 'ETH',
                'rpc_url': 'https://arb1.arbitrum.io/rpc'
            },
            'polygon': {
                'chain_id': 137,
                'native_token': 'MATIC',
                'rpc_url': 'https://polygon-rpc.com'
            }
        }
        return chain_configs.get(chain.lower(), {})

# 鍒涘缓閰嶇疆瀹炰緥
config = Config()
