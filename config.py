"""
OKX Smart Trading Agent - Configuration File
配置文件：管理 API 密钥、网络设置和其他配置参数
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # OKX API 配置
    OKX_API_KEY = os.getenv('OKX_API_KEY', '')
    OKX_API_SECRET = os.getenv('OKX_API_SECRET', '')
    OKX_API_PASSPHRASE = os.getenv('OKX_API_PASSPHRASE', '')
    
    # 钱包私钥配置
    WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY', '')
    
    # API 端点
    OKX_API_BASE_URL = 'https://www.okx.com'
    OKX_API_PUBLIC_URL = 'https://www.okx.com'
    
    # 支持的区块链网络
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
    
    # 默认配置
    DEFAULT_CHAIN = 'ethereum'
    DEFAULT_SLIPPAGE = 0.5  # 默认滑点 0.5%
    DEFAULT_GAS_PRICE = 'medium'  # low, medium, high
    
    # 风险管理配置
    MAX_SLIPPAGE = 5.0  # 最大滑点 5%
    MIN_LIQUIDITY = 10000  # 最小流动性 $10,000
    MAX_TRADE_AMOUNT = 10000  # 单笔最大交易金额 $10,000
    
    # 交易配置
    TRANSACTION_TIMEOUT = 300  # 交易超时时间（秒）
    CONFIRMATION_BLOCKS = 2  # 确认区块数
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'trading_agent.log'
    
    # 缓存配置
    CACHE_ENABLED = True
    CACHE_TTL = 60  # 缓存过期时间（秒）
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        if not cls.OKX_API_KEY:
            raise ValueError('OKX_API_KEY 未设置')
        if not cls.OKX_API_SECRET:
            raise ValueError('OKX_API_SECRET 未设置')
        if not cls.OKX_API_PASSPHRASE:
            raise ValueError('OKX_API_PASSPHRASE 未设置')
        return True
    
    @classmethod
    def get_chain_config(cls, chain):
        """获取特定链的配置"""
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

# 创建配置实例
config = Config()
