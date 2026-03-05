"""
OKX Smart Trading Agent - Helper Functions
杈呭姪鍑芥暟锛氶氱敤宸ュ叿鍑芥暟銆佹暟鎹鏍煎紡鍖栥侀獙璇佺瓑
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from loguru import logger


def format_usd(value: float, decimals: int = 2) -> str:
    """
    鏍煎紡鍖栫編鍏冮噾棰
    
    Args:
        value: 鏁板
        decimals: 灏忔暟浣嶆暟
    
    Returns:
        鏍煎紡鍖栧悗鐨勫瓧绗︿覆
    """
    try:
        return f'${value:,.{decimals}f}'
    except Exception as e:
        logger.error(f'鏍煎紡鍖栫編鍏冮噾棰濆け璐: {str(e)}')
        return f'${value}'


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    鏍煎紡鍖栫櫨鍒嗘瘮
    
    Args:
        value: 鏁板
        decimals: 灏忔暟浣嶆暟
    
    Returns:
        鏍煎紡鍖栧悗鐨勫瓧绗︿覆
    """
    try:
        return f'{value:.{decimals}f}%'
    except Exception as e:
        logger.error(f'鏍煎紡鍖栫櫨鍒嗘瘮澶辫触: {str(e)}')
        return f'{value}%'


def format_number(value: float, decimals: int = 4) -> str:
    """
    鏍煎紡鍖栨暟瀛
    
    Args:
        value: 鏁板
        decimals: 灏忔暟浣嶆暟
    
    Returns:
        鏍煎紡鍖栧悗鐨勫瓧绗︿覆
    """
    try:
        return f'{value:,.{decimals}f}'
    except Exception as e:
        logger.error(f'鏍煎紡鍖栨暟瀛楀け璐: {str(e)}')
        return str(value)


def validate_address(address: str) -> bool:
    """
    楠岃瘉鍖哄潡閾惧湴鍧鏍煎紡
    
    Args:
        address: 鍖哄潡閾惧湴鍧
    
    Returns:
        鏄鍚︽湁鏁
    """
    try:
        # Ethereum 鍦板潃鏍煎紡
        if re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return True
        
        # Solana 鍦板潃鏍煎紡
        if re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address):
            return True
        
        return False
    except Exception as e:
        logger.error(f'楠岃瘉鍦板潃澶辫触: {str(e)}')
        return False


def validate_amount(amount: float) -> bool:
    """
    楠岃瘉閲戦
    
    Args:
        amount: 閲戦
    
    Returns:
        鏄鍚︽湁鏁
    """
    try:
        return amount > 0
    except Exception as e:
        logger.error(f'楠岃瘉閲戦濆け璐: {str(e)}')
        return False


def validate_slippage(slippage: float) -> bool:
    """
    楠岃瘉婊戠偣
    
    Args:
        slippage: 婊戠偣鐧惧垎姣
    
    Returns:
        鏄鍚︽湁鏁
    """
    try:
        return 0 <= slippage <= 100
    except Exception as e:
        logger.error(f'楠岃瘉婊戠偣澶辫触: {str(e)}')
        return False


def validate_chain(chain: str, supported_chains: List[str]) -> bool:
    """
    楠岃瘉鍖哄潡閾剧綉缁
    
    Args:
        chain: 鍖哄潡閾剧綉缁
        supported_chains: 鏀鎸佺殑鍖哄潡閾惧垪琛
    
    Returns:
        鏄鍚︽湁鏁
    """
    try:
        return chain.lower() in [c.lower() for c in supported_chains]
    except Exception as e:
        logger.error(f'楠岃瘉鍖哄潡閾剧綉缁滃け璐: {str(e)}')
        return False


def calculate_price_impact(
    input_amount: float,
    output_amount: float,
    input_price: float,
    output_price: float
) -> float:
    """
    璁＄畻浠锋牸褰卞搷
    
    Args:
        input_amount: 杈撳叆鏁伴噺
        output_amount: 杈撳嚭鏁伴噺
        input_price: 杈撳叆浠ｅ竵浠锋牸
        output_price: 杈撳嚭浠ｅ竵浠锋牸
    
    Returns:
        浠锋牸褰卞搷鐧惧垎姣
    """
    try:
        expected_output = (input_amount * input_price) / output_price
        price_impact = ((expected_output - output_amount) / expected_output) * 100
        return price_impact
    except Exception as e:
        logger.error(f'璁＄畻浠锋牸褰卞搷澶辫触: {str(e)}')
        return 0.0


def calculate_gas_fee(gas_price: float, gas_limit: int, eth_price: float = 2000.0) -> Dict:
    """
    璁＄畻 Gas 璐圭敤
    
    Args:
        gas_price: Gas 浠锋牸锛圙wei锛
        gas_limit: Gas 闄愬埗
        eth_price: ETH 浠锋牸锛堢編鍏冿級
    
    Returns:
        Gas 璐圭敤淇℃伅
    """
    try:
        gas_fee_eth = (gas_price * gas_limit) / 10**18
        gas_fee_usd = gas_fee_eth * eth_price
        
        return {
            'gas_price': gas_price,
            'gas_limit': gas_limit,
            'gas_fee_eth': gas_fee_eth,
            'gas_fee_usd': gas_fee_usd,
            'eth_price': eth_price
        }
    except Exception as e:
        logger.error(f'璁＄畻 Gas 璐圭敤澶辫触: {str(e)}')
        return {
            'gas_fee_eth': 0.0,
            'gas_fee_usd': 0.0
        }


def format_timestamp(timestamp: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    鏍煎紡鍖栨椂闂存埑
    
    Args:
        timestamp: Unix 鏃堕棿鎴筹紙姣绉掞級
        format: 鏍煎紡鍖栧瓧绗︿覆
    
    Returns:
        鏍煎紡鍖栧悗鐨勬椂闂村瓧绗︿覆
    """
    try:
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime(format)
    except Exception as e:
        logger.error(f'鏍煎紡鍖栨椂闂存埑澶辫触: {str(e)}')
        return str(timestamp)


def truncate_address(address: str, start: int = 6, end: int = 4) -> str:
    """
    鎴鏂鍦板潃鏄剧ず
    
    Args:
        address: 鍦板潃
        start: 淇濈暀寮澶村瓧绗︽暟
        end: 淇濈暀缁撳熬瀛楃︽暟
    
    Returns:
        鎴鏂鍚庣殑鍦板潃
    """
    try:
        if len(address) <= start + end:
            return address
        return f'{address[:start]}...{address[-end:]}'
    except Exception as e:
        logger.error(f'鎴鏂鍦板潃澶辫触: {str(e)}')
        return address


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    瀹夊叏闄ゆ硶
    
    Args:
        numerator: 鍒嗗瓙
        denominator: 鍒嗘瘝
        default: 榛樿ゅ
    
    Returns:
        闄ゆ硶缁撴灉
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except Exception as e:
        logger.error(f'瀹夊叏闄ゆ硶澶辫触: {str(e)}')
        return default


def parse_json_string(json_string: str) -> Optional[Dict]:
    """
    瑙ｆ瀽 JSON 瀛楃︿覆
    
    Args:
        json_string: JSON 瀛楃︿覆
    
    Returns:
        瑙ｆ瀽鍚庣殑瀛楀吀
    """
    try:
        return json.loads(json_string)
    except Exception as e:
        logger.error(f'瑙ｆ瀽 JSON 瀛楃︿覆澶辫触: {str(e)}')
        return None


def to_json_string(data: Any, indent: int = 2) -> str:
    """
    杞鎹涓 JSON 瀛楃︿覆
    
    Args:
        data: 鏁版嵁
        indent: 缂╄繘
    
    Returns:
        JSON 瀛楃︿覆
    """
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except Exception as e:
        logger.error(f'杞鎹涓 JSON 瀛楃︿覆澶辫触: {str(e)}')
        return str(data)


def retry_async(func, max_retries: int = 3, delay: float = 1.0):
    """
    寮傛ラ噸璇曡呴グ鍣
    
    Args:
        func: 寮傛ュ嚱鏁
        max_retries: 鏈澶ч噸璇曟℃暟
        delay: 閲嶈瘯寤惰繜锛堢掞級
    
    Returns:
        鍖呰呭悗鐨勫嚱鏁
    """
    import asyncio
    
    async def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f'閲嶈瘯 {max_retries} 娆″悗浠嶇劧澶辫触: {str(e)}')
                    raise
                logger.warning(f'绗 {attempt + 1} 娆″皾璇曞け璐ワ紝{delay} 绉掑悗閲嶈瘯: {str(e)}')
                await asyncio.sleep(delay)
    
    return wrapper


def log_execution_time(func):
    """
    璁板綍鎵ц屾椂闂磋呴グ鍣
    
    Args:
        func: 鍑芥暟
    
    Returns:
        鍖呰呭悗鐨勫嚱鏁
    """
    import time
    from functools import wraps
    
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f'{func.__name__} 鎵ц屾椂闂: {execution_time:.2f} 绉')
        return result
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f'{func.__name__} 鎵ц屾椂闂: {execution_time:.2f} 绉')
        return result
    
    # 鍒ゆ柇鏄鍚︿负寮傛ュ嚱鏁
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    灏嗗垪琛ㄥ垎鍧
    
    Args:
        lst: 鍒楄〃
        chunk_size: 鍧楀ぇ灏
    
    Returns:
        鍒嗗潡鍚庣殑鍒楄〃
    """
    try:
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    except Exception as e:
        logger.error(f'鍒楄〃鍒嗗潡澶辫触: {str(e)}')
        return [lst]


def flatten_list(nested_list: List) -> List:
    """
    灞曞钩宓屽楀垪琛
    
    Args:
        nested_list: 宓屽楀垪琛
    
    Returns:
        灞曞钩鍚庣殑鍒楄〃
    """
    try:
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(flatten_list(item))
            else:
                result.append(item)
        return result
    except Exception as e:
        logger.error(f'灞曞钩鍒楄〃澶辫触: {str(e)}')
        return nested_list


def get_nested_value(data: Dict, keys: List[str], default: Any = None) -> Any:
    """
    鑾峰彇宓屽楀瓧鍏哥殑鍊
    
    Args:
        data: 瀛楀吀
        keys: 閿鍒楄〃
        default: 榛樿ゅ
    
    Returns:
        宓屽楀
    """
    try:
        value = data
        for key in keys:
            value = value.get(key, {})
        return value if value != {} else default
    except Exception as e:
        logger.error(f'鑾峰彇宓屽楀煎け璐: {str(e)}')
        return default
