# 港股数据集成指南

本项目已成功集成富途API，支持获取港股数据。以下是详细的使用说明。

## 功能概述

### 新增功能
- ✅ 支持港股价格数据获取
- ✅ 支持港股财务指标获取
- ✅ 支持港股市值数据获取
- ✅ 支持港股新闻数据获取
- ✅ 自动识别港股代码格式
- ✅ 与原有美股数据API无缝集成

### 支持的港股代码格式
- `00700` - 5位数字格式
- `700` - 4位数字格式
- `00700.HK` - 带.HK后缀格式

## 安装依赖

### 1. 安装富途API依赖
```bash
cd /Users/zhaxu/Work/Personal/ai-hedge-fund
poetry add futu-api
```

### 2. 安装富途客户端
1. 下载并安装富途客户端：https://www.futunn.com/
2. 注册富途账户
3. 在富途客户端中开启API权限

## 使用方法

### 基本用法

```python
from src.tools.api import get_prices, get_price_data

# 获取港股价格数据
prices = get_prices("00700", "2024-01-01", "2024-01-31")
print(f"获取到 {len(prices)} 条价格数据")

# 获取港股DataFrame格式数据
df = get_price_data("00700", "2024-01-01", "2024-01-31")
print(df.head())
```

### 高级用法

```python
from src.tools.futu_api import (
    get_hk_prices,
    get_hk_financial_metrics,
    get_hk_market_cap,
    get_hk_company_news
)

# 获取港股价格数据
prices = get_hk_prices("00700", "2024-01-01", "2024-01-31")

# 获取港股财务指标
metrics = get_hk_financial_metrics("00700", "2024-01-31")

# 获取港股市值
market_cap = get_hk_market_cap("00700", "2024-01-31")

# 获取港股新闻
news = get_hk_company_news("00700", "2024-01-31", limit=10)
```

## 测试功能

运行测试脚本验证功能：

```bash
cd /Users/zhaxu/Work/Personal/ai-hedge-fund
poetry run python test_hk_data.py
```

## 数据格式

### 价格数据格式
```python
class Price:
    open: float      # 开盘价
    close: float     # 收盘价
    high: float      # 最高价
    low: float       # 最低价
    volume: int      # 成交量
    time: str        # 时间戳
```

### 财务指标格式
```python
class FinancialMetrics:
    ticker: str                    # 股票代码
    report_period: str            # 报告期
    period: str                   # 期间类型
    currency: str                 # 货币（HKD）
    market_cap: float | None      # 市值
    # ... 其他财务指标
```

## 配置说明

### 富途API配置
```python
# 默认配置
host = '127.0.0.1'  # 富途客户端IP
port = 11111        # 富途客户端端口

# 自定义配置
from src.tools.futu_api import FutuAPIClient
client = FutuAPIClient(host='your_host', port=your_port)
```

### 环境变量
```bash
# .env 文件
FINANCIAL_DATASETS_API_KEY=your_api_key  # 美股数据API密钥
```

## 常见问题

### Q: 连接富途API失败
A: 请确保：
1. 富途客户端已安装并运行
2. API权限已开启
3. 网络连接正常
4. 端口11111未被占用

### Q: 获取港股数据为空
A: 请检查：
1. 股票代码格式是否正确
2. 日期范围是否有效
3. 是否为交易日
4. 富途API连接是否正常

### Q: 美股数据获取失败
A: 请确保：
1. 已设置FINANCIAL_DATASETS_API_KEY环境变量
2. API密钥有效
3. 网络连接正常

## 性能优化

### 缓存机制
- 所有数据都会自动缓存
- 相同参数的请求会直接返回缓存数据
- 缓存键包含所有参数，确保数据准确性

### 错误处理
- 自动重试机制
- 详细的错误信息
- 优雅的降级处理

## 扩展功能

### 添加新的港股数据源
1. 在 `src/tools/futu_api.py` 中添加新函数
2. 在 `src/tools/api.py` 中集成新函数
3. 更新数据模型（如需要）

### 自定义数据格式
1. 修改 `src/data/models.py` 中的模型
2. 更新相应的转换函数
3. 测试数据兼容性

## 注意事项

1. **数据准确性**：富途API提供的数据仅供参考，投资决策请谨慎
2. **API限制**：注意富途API的调用频率限制
3. **时区处理**：港股交易时间与美股不同，注意时区转换
4. **货币单位**：港股以港币计价，注意货币单位统一
5. **法律合规**：使用API时请遵守相关法律法规

## 技术支持

如有问题，请：
1. 查看错误日志
2. 检查网络连接
3. 验证API配置
4. 联系技术支持

---

**免责声明**：本项目仅供学习和研究使用，不构成投资建议。使用前请仔细阅读相关API服务条款。
