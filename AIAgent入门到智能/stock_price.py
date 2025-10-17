import tushare as ts
import os

# 同样，强烈建议使用环境变量
# os.environ['TUSHARE_TOKEN'] = 'YOUR_TUSHARE_TOKEN'
# pro = ts.pro_api(os.environ['TUSHARE_TOKEN'])

# 为了演示方便，我们暂时硬编码
TUSHARE_TOKEN = "YOUR_TUSHARE_TOKEN"

ts.set_token(TUSHARE_TOKEN)
# pro = ts.pro_api()

def get_stock_realtime_price(stock_code: str) -> str:
    """
    查询指定股票代码的最新实时行情价格。
    
    参数:
    stock_code (str): 必须是Tushare标准的股票代码, 格式为 'XXXXXX.SZ' (深圳) 或 'XXXXXX.SH' (上海)。
                      例如: '000001.SZ' (平安银行), '600519.SH' (贵州茅台)。
    
    返回:
    str: 一个包含股票名称、代码、最新价格、涨跌幅的格式化字符串。
         例如：'贵州茅台(600519.SH): 当前价格 1650.00, 涨跌幅 1.52%'。
         如果代码错误或未查询到，则返回错误信息。
    """
    print(f"--- [工具被调用：get_stock_realtime_price] ---")
    print(f"--- [工具入参：stock_code={stock_code}] ---")

    try:
        # Tushare的实时行情接口是 realtime_quote
        df = ts.realtime_quote(ts_code=stock_code)
        
        if df.empty:
            return f"错误：未查询到股票代码 '{stock_code}' 的实时行情。"
            
        # 提取第一行数据
        stock_data = df.iloc[0]
        
        
        # 格式化输出
        result_str = (
            f"{stock_data['NAME']}({stock_data['TS_CODE']}): "
            f"当前价格 {stock_data['PRICE']}, "
            f"涨跌幅 {stock_data['PRE_CLOSE']}, " # 注意：免费接口可能数据有延迟或不完整，这里仅为示例
            f"今日开盘 {stock_data['OPEN']}, "
            f"最高 {stock_data['HIGH']}, "
            f"最低 {stock_data['LOW']}"
        )
        
        print(f"--- [工具返回值：{result_str}] ---")
        return result_str
        
    except Exception as e:
        print(f"--- [工具内部错误：{e}] ---")
        return f"错误：调用Tushare API时发生异常 - {e}"

# --- 本地测试 ---
if __name__ == "__main__":
    stock_info = get_stock_realtime_price("600519.SH")
    print(stock_info)