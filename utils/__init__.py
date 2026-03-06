# -*- coding: utf-8 -*-
"""
Utils module initialization
"""

from .api_client import OKXAPIClient
from .okx_api_client import OKXOnchainOSClient
from .helpers import (
    format_usd,
    format_percentage,
    format_number,
    validate_address,
    validate_amount,
    validate_slippage,
    validate_chain,
    calculate_price_impact,
    calculate_gas_fee,
    format_timestamp,
    truncate_address,
    safe_divide,
    parse_json_string,
    to_json_string,
    retry_async,
    log_execution_time,
    chunk_list,
    flatten_list,
    get_nested_value
)

__all__ = [
    'OKXAPIClient',
    'OKXOnchainOSClient',
    'format_usd',
    'format_percentage',
    'format_number',
    'validate_address',
    'validate_amount',
    'validate_slippage',
    'validate_chain',
    'calculate_price_impact',
    'calculate_gas_fee',
    'format_timestamp',
    'truncate_address',
    'safe_divide',
    'parse_json_string',
    'to_json_string',
    'retry_async',
    'log_execution_time',
    'chunk_list',
    'flatten_list',
    'get_nested_value'
]
