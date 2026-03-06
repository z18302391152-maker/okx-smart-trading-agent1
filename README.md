# OKX Smart Trading Agent - 智能交易助手

## 🎯 项目简介

这是一个基于 OKX OnchainOS 的智能交易 AI Agent，整合了市场监控、智能交易、风险管理和资产管理四大核心功能，为用户提供安全、高效的 DeFi 交易体验。

## ✨ 核心特性

### 1. 市场监控 (Market Monitor)
- 实时价格追踪
- K线数据分析
- 交易历史查询
- 市场趋势分析

### 2. 智能交易 (Smart Trading)
- 最优路径查找
- 滑点控制
- 价格影响保护
- 跨链交易支持

### 3. 风险管理 (Risk Manager)
- 流动性评估
- 滑点优化
- 交易风险预警
- 资金安全检查

### 4. 资产管理 (Portfolio Manager)
- 多链资产查询
- 投资组合分析
- 资产价值计算
- 持仓分布统计

## 🌐 支持的区块链

- XLayer
- Solana
- Ethereum
- Base
- BSC
- Arbitrum
- Polygon
- 以及 20+ 其他链

## 📋 系统要求

- Python 3.11.9
- pip 包管理器
- OKX API 密钥

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并添加：

```env
OKX_API_KEY=your_api_key
OKX_API_SECRET=your_api_secret
OKX_API_PASSPHRASE=your_api_passphrase
```

### 3. 运行程序

```bash
python main.py
```

## 📁 项目结构

```
okx-smart-trading-agent/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python 依赖
├── config.py                   # 配置文件
├── main.py                     # 主程序入口
├── skills/                     # 技能模块
│   ├── market_monitor.py      # 市场监控
│   ├── smart_trading.py       # 智能交易
│   ├── risk_manager.py        # 风险管理
│   └── portfolio_manager.py    # 资产管理
├── utils/                     # 工具模块
│   ├── api_client.py         # OKX API 客户端
│   └── helpers.py            # 辅助函数
└── tests/                      # 测试文件
    └── test_agent.py          # Agent 测试
```

## 💡 使用示例

### 查询代币价格

```python
from skills.market_monitor import MarketMonitor

monitor = MarketMonitor()
price = monitor.get_token_price('SOL', 'USDC', 'solana')
print(f'SOL 价格: ${price}')
```

### 执行交易

```python
from skills.smart_trading import SmartTrading

trader = SmartTrading()
result = trader.swap_tokens(
    from_token='SOL',
    to_token='USDC',
    amount=1.0,
    chain='solana',
    slippage=0.5
)
print(f'交易结果: {result}')
```

### 查询资产组合

```python
from skills.portfolio_manager import PortfolioManager

portfolio = PortfolioManager()
assets = portfolio.get_portfolio_value()
print(f'总资产价值: ${assets}')
```

## 🔒 安全特性

- API 密钥加密存储
- 交易前风险检查
- 滑点保护机制
- 流动性验证
- 交易模拟功能

## 📊 技术架构

```
┌─────────────────────────────────────┐
│         Main Application            │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼────┐ ┌──▼─────┐ ┌──▼▼──────┐
│ Market │ │ Smart  │ │  Risk    │
│Monitor │ │Trading │ │ Manager  │
└───┬────┘ └──┬─────┘ └──┬───────┘
    │          │          │
    └──────────┼──────────┘
               │
        ┌──────▼──────┐
        │  API Client │
        └─────────────┘
```

## 🧪 测试

运行测试：

```bash
python -m pytest tests/
```

## 📝 参赛提交指南

### 必需文件
- ✅ 项目源代码（完整实现）
- ✅ 项目文档（README.md）
- ✅ requirements.txt
- ✅ 配置文件示例

### 可选材料
- 项目演示视频
- 技术架构图
- 部署文档
- API 测试报告
- 用户使用指南

### 参赛渠道
1. **官方渠道**: 访问 OKX 开发者门户提交项目
   - https://web3.okx.com/onchain-os/dev-portal

2. **GitHub 提交**: 将项目推送到 GitHub 并提交链接
   - Fork 项目并提交 PR

3. **社区参与**: 在相关技术社区分享项目

## 🎓 项目亮点

### 核心亮点
- **完整技能集成**: 展示如何将 5 个 OKX 技能整合成完整 Agent
- **智能决策引擎**: 基于市场数据的自动交易决策
- **风险管理系统**: 内置风险管理和滑点控制
- **多链支持**: 支持 20+ 条区块链网络
- **实用场景**: 提供真实 DeFi 交易场景

### 技术亮点
- **模块化架构**: 清晰的代码结构
- **Python 3.11.9**: 使用最新 Python 版本
- **OKX API 集成**: 完整的 API 客户端实现
- **环境变量配置**: 安全的 API 密钥管理
- **可测试性**: 包含测试文件

### 创新特性
- **自动化交易策略**: 基于技术指标的自动买入/卖出
- **跨链套利机会**: 自动发现不同链上的价格差异
- **智能提醒系统**: 价格异常提醒和交易机会通知
- **风险预警**: 流动性评估和滑点优化建议

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- 项目地址: https://github.com/yourusername/okx-smart-trading-agent
- OKX 开发者文档: https://web3.okx.com/zh-hans/onchainos/dev-docs/home/what-is-onchainos

---
OKX项目id:03512cdc920abbde9dadf07e3da97b36  钱包地址：0x2004fdf4f6233cba5f2762bde36ba9857ef96ff4
**注意**: 本项目仅供学习和研究使用，实际交易请谨慎操作，风险自负。
