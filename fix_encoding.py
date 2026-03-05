# -*- coding: utf-8 -*-
import os
import sys

def fix_file_encoding(file_path):
    """修复文件编码为 UTF-8"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 写入文件，确保使用 UTF-8 编码
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'已修复: {file_path}')
        return True
    except Exception as e:
        print(f'修复失败: {file_path} - {str(e)}')
        return False

# 需要修复的文件列表
files_to_fix = [
    'skills/smart_trading.py',
    'skills/risk_manager.py',
    'skills/market_monitor.py',
    'skills/portfolio_manager.py',
    'utils/api_client.py',
    'utils/helpers.py',
    'main.py',
    'config.py',
    'tests/test_agent.py'
]

# 修复所有文件
base_path = r'F:\软件\科学家脚本\clawbot\okxsmarttradingagent'
success_count = 0

for file_path in files_to_fix:
    full_path = os.path.join(base_path, file_path)
    if fix_file_encoding(full_path):
        success_count += 1

print(f'\n修复完成: {success_count}/{len(files_to_fix)} 个文件')
