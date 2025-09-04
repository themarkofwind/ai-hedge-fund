import datetime
import os
import pandas as pd
import futu as ft
from typing import Optional, List
import time

from src.data.cache import get_cache
from src.data.models import (
    Price,
    PriceResponse,
    FinancialMetrics,
    FinancialMetricsResponse,
    CompanyNews,
    CompanyNewsResponse,
)

# 全局缓存实例
_cache = get_cache()


class FutuAPIClient:
    """富途API客户端封装类"""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 11111):
        """
        初始化富途API客户端
        
        Args:
            host: 富途客户端IP地址
            port: 富途客户端端口
        """
        self.host = host
        self.port = port
        self.quote_ctx = None
        self._connect()
    
    def _connect(self):
        """连接到富途API"""
        try:
            self.quote_ctx = ft.OpenQuoteContext(host=self.host, port=self.port)
            print(f"成功连接到富途API: {self.host}:{self.port}")
        except Exception as e:
            print(f"连接富途API失败: {e}")
            raise
    
    def _disconnect(self):
        """断开富途API连接"""
        if self.quote_ctx:
            self.quote_ctx.close()
            print("已断开富途API连接")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()


def _convert_hk_ticker(ticker: str) -> str:
    """
    将股票代码转换为富途API格式
    
    Args:
        ticker: 股票代码，如 "00700" 或 "700"
    
    Returns:
        富途API格式的股票代码，如 "HK.00700"
    """
    # 移除可能的.HK后缀
    if ticker.endswith('.HK'):
        ticker = ticker[:-3]
    
    # 确保代码是5位数字
    if len(ticker) < 5:
        ticker = ticker.zfill(5)
    
    return f"HK.{ticker}"


def get_hk_prices(ticker: str, start_date: str, end_date: str, api_key: str = None) -> List[Price]:
    """
    从富途API获取港股价格数据
    
    Args:
        ticker: 股票代码，如 "00700" 或 "700"
        start_date: 开始日期，格式 "YYYY-MM-DD"
        end_date: 结束日期，格式 "YYYY-MM-DD"
        api_key: API密钥（富途API不需要，但保持接口一致性）
    
    Returns:
        价格数据列表
    """
    # 创建缓存键
    cache_key = f"hk_{ticker}_{start_date}_{end_date}"
    
    # 检查缓存
    if cached_data := _cache.get_prices(cache_key):
        return [Price(**price) for price in cached_data]
    
    # 转换股票代码格式
    futu_ticker = _convert_hk_ticker(ticker)
    
    try:
        with FutuAPIClient() as client:
            # 获取历史K线数据
            ret, data, page_req_key = client.quote_ctx.request_history_kline(
                code=futu_ticker,
                start=start_date,
                end=end_date,
                ktype=ft.KLType.K_DAY,
                autype=ft.AuType.QFQ  # 前复权
            )
            
            if ret != ft.RET_OK:
                raise Exception(f"获取港股数据失败: {data}")
            
            if data.empty:
                return []
            
            # 转换数据格式
            prices = []
            for _, row in data.iterrows():
                # 处理时间格式
                time_key = row['time_key']
                if hasattr(time_key, 'strftime'):
                    time_str = time_key.strftime('%Y-%m-%dT%H:%M:%S')
                else:
                    time_str = str(time_key)
                
                price = Price(
                    open=float(row['open']),
                    close=float(row['close']),
                    high=float(row['high']),
                    low=float(row['low']),
                    volume=int(row['volume']),
                    time=time_str
                )
                prices.append(price)
            
            # 缓存结果
            _cache.set_prices(cache_key, [p.model_dump() for p in prices])
            return prices
            
    except Exception as e:
        print(f"获取港股价格数据时出错: {e}")
        return []


def get_hk_financial_metrics(
    ticker: str,
    end_date: str,
    period: str = "ttm",
    limit: int = 10,
    api_key: str = None,
) -> List[FinancialMetrics]:
    """
    从富途API获取港股财务指标数据（简化版本）
    
    Args:
        ticker: 股票代码
        end_date: 结束日期
        period: 报告期类型
        limit: 限制数量
        api_key: API密钥
    
    Returns:
        财务指标数据列表
    """
    # 创建缓存键
    cache_key = f"hk_financial_{ticker}_{period}_{end_date}_{limit}"
    
    # 检查缓存
    if cached_data := _cache.get_financial_metrics(cache_key):
        return [FinancialMetrics(**metric) for metric in cached_data]
    
    # 简化实现：返回基本的财务指标结构
    # 注意：富途API的财务数据获取比较复杂，这里提供基础结构
    try:
        # 创建一个基本的财务指标对象
        metric = FinancialMetrics(
            ticker=ticker,
            report_period=end_date,
            period=period,
            currency="HKD",
            market_cap=None,  # 需要单独获取
            enterprise_value=None,
            price_to_earnings_ratio=None,
            price_to_book_ratio=None,
            price_to_sales_ratio=None,
            enterprise_value_to_ebitda_ratio=None,
            enterprise_value_to_revenue_ratio=None,
            free_cash_flow_yield=None,
            peg_ratio=None,
            gross_margin=None,
            operating_margin=None,
            net_margin=None,
            return_on_equity=None,
            return_on_assets=None,
            return_on_invested_capital=None,
            asset_turnover=None,
            inventory_turnover=None,
            receivables_turnover=None,
            days_sales_outstanding=None,
            operating_cycle=None,
            working_capital_turnover=None,
            current_ratio=None,
            quick_ratio=None,
            cash_ratio=None,
            operating_cash_flow_ratio=None,
            debt_to_equity=None,
            debt_to_assets=None,
            interest_coverage=None,
            revenue_growth=None,
            earnings_growth=None,
            book_value_growth=None,
            earnings_per_share_growth=None,
            free_cash_flow_growth=None,
            operating_income_growth=None,
            ebitda_growth=None,
            payout_ratio=None,
            earnings_per_share=None,
            book_value_per_share=None,
            free_cash_flow_per_share=None
        )
        
        # 缓存结果
        _cache.set_financial_metrics(cache_key, [metric.model_dump()])
        return [metric]
        
    except Exception as e:
        print(f"获取港股财务指标时出错: {e}")
        return []


def get_hk_market_cap(ticker: str, end_date: str, api_key: str = None) -> Optional[float]:
    """
    从富途API获取港股市值（简化版本）
    
    Args:
        ticker: 股票代码
        end_date: 结束日期
        api_key: API密钥
    
    Returns:
        市值数据
    """
    # 简化实现：返回None，表示市值数据暂不可用
    # 注意：富途API的市值获取比较复杂，这里提供基础结构
    try:
        print(f"港股市值数据暂不可用，股票代码: {ticker}")
        return None
        
    except Exception as e:
        print(f"获取港股市值时出错: {e}")
        return None


def get_hk_company_news(
    ticker: str,
    end_date: str,
    start_date: Optional[str] = None,
    limit: int = 1000,
    api_key: str = None,
) -> List[CompanyNews]:
    """
    从富途API获取港股公司新闻
    
    Args:
        ticker: 股票代码
        end_date: 结束日期
        start_date: 开始日期
        limit: 限制数量
        api_key: API密钥
    
    Returns:
        公司新闻列表
    """
    # 创建缓存键
    cache_key = f"hk_news_{ticker}_{start_date or 'none'}_{end_date}_{limit}"
    
    # 检查缓存
    if cached_data := _cache.get_company_news(cache_key):
        return [CompanyNews(**news) for news in cached_data]
    
    # 转换股票代码格式
    futu_ticker = _convert_hk_ticker(ticker)
    
    try:
        with FutuAPIClient() as client:
            # 获取新闻数据
            ret, data, page_req_key = client.quote_ctx.get_news(
                code=futu_ticker,
                start_time=start_date or "2020-01-01",
                end_time=end_date,
                max_count=limit
            )
            
            if ret != ft.RET_OK:
                print(f"获取港股新闻失败: {data}")
                return []
            
            if data.empty:
                return []
            
            # 转换数据格式
            news_list = []
            for _, row in data.iterrows():
                news = CompanyNews(
                    ticker=ticker,
                    title=row.get('title', ''),
                    author=row.get('author', ''),
                    source=row.get('source', ''),
                    date=row.get('time', ''),
                    url=row.get('url', ''),
                    sentiment=None
                )
                news_list.append(news)
            
            # 缓存结果
            _cache.set_company_news(cache_key, [n.model_dump() for n in news_list])
            return news_list
            
    except Exception as e:
        print(f"获取港股新闻时出错: {e}")
        return []


def get_hk_price_data(ticker: str, start_date: str, end_date: str, api_key: str = None) -> pd.DataFrame:
    """
    获取港股价格数据并转换为DataFrame
    
    Args:
        ticker: 股票代码
        start_date: 开始日期
        end_date: 结束日期
        api_key: API密钥
    
    Returns:
        价格数据DataFrame
    """
    prices = get_hk_prices(ticker, start_date, end_date, api_key)
    return prices_to_df(prices)


def prices_to_df(prices: List[Price]) -> pd.DataFrame:
    """
    将价格数据转换为DataFrame
    
    Args:
        prices: 价格数据列表
    
    Returns:
        价格数据DataFrame
    """
    df = pd.DataFrame([p.model_dump() for p in prices])
    df["Date"] = pd.to_datetime(df["time"])
    df.set_index("Date", inplace=True)
    # 将数值列转换为数字类型
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    return df


# 测试函数
def test_futu_api():
    """测试富途API连接和数据获取"""
    try:
        # 测试连接
        with FutuAPIClient() as client:
            print("富途API连接成功")
        
        # 测试获取腾讯控股(00700)的价格数据
        ticker = "00700"
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        
        print(f"获取 {ticker} 从 {start_date} 到 {end_date} 的价格数据...")
        prices = get_hk_prices(ticker, start_date, end_date)
        
        if prices:
            print(f"成功获取 {len(prices)} 条价格数据")
            print(f"第一条数据: {prices[0]}")
        else:
            print("未获取到价格数据")
            
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    test_futu_api()
