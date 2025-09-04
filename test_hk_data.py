#!/usr/bin/env python3
"""
测试港股数据获取功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.tools.api import get_prices, get_price_data
from src.tools.futu_api import test_futu_api
import pandas as pd

def test_hk_stock_data():
    """测试港股数据获取"""
    print("=" * 50)
    print("测试港股数据获取功能")
    print("=" * 50)
    
    # 测试股票代码
    hk_tickers = ["00700", "0700", "00700.HK"]  # 腾讯控股的不同格式
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    
    for ticker in hk_tickers:
        print(f"\n测试股票代码: {ticker}")
        print("-" * 30)
        
        try:
            # 测试价格数据获取
            print(f"获取 {ticker} 从 {start_date} 到 {end_date} 的价格数据...")
            prices = get_prices(ticker, start_date, end_date)
            
            if prices:
                print(f"✅ 成功获取 {len(prices)} 条价格数据")
                print(f"第一条数据: {prices[0]}")
                print(f"最后一条数据: {prices[-1]}")
                
                # 测试DataFrame转换
                df = get_price_data(ticker, start_date, end_date)
                print(f"✅ 成功转换为DataFrame，形状: {df.shape}")
                print(f"DataFrame列名: {list(df.columns)}")
                print(f"前5行数据:")
                print(df.head())
                
            else:
                print("❌ 未获取到价格数据")
                
        except Exception as e:
            print(f"❌ 获取数据时出错: {e}")
    
    print("\n" + "=" * 50)
    print("测试富途API连接")
    print("=" * 50)
    
    # 测试富途API连接
    try:
        test_futu_api()
    except Exception as e:
        print(f"❌ 富途API测试失败: {e}")
        print("请确保：")
        print("1. 已安装futu-api依赖: poetry add futu-api")
        print("2. 已安装并运行富途客户端")
        print("3. 富途客户端API权限已开启")

def test_us_stock_data():
    """测试美股数据获取（原有功能）"""
    print("\n" + "=" * 50)
    print("测试美股数据获取功能（原有功能）")
    print("=" * 50)
    
    us_ticker = "AAPL"
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    
    try:
        print(f"获取 {us_ticker} 从 {start_date} 到 {end_date} 的价格数据...")
        prices = get_prices(us_ticker, start_date, end_date)
        
        if prices:
            print(f"✅ 成功获取 {len(prices)} 条价格数据")
            print(f"第一条数据: {prices[0]}")
        else:
            print("❌ 未获取到价格数据")
            
    except Exception as e:
        print(f"❌ 获取美股数据时出错: {e}")

if __name__ == "__main__":
    print("开始测试股票数据获取功能...")
    
    # 测试美股数据
    # test_us_stock_data()
    
    # 测试港股数据
    test_hk_stock_data()
    
    print("\n测试完成！")
