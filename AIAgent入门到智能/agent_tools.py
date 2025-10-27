import requests
import json
import gzip
import tushare as ts
import os
from pydantic import BaseModel, Field, ValidationError

# 强烈建议你使用环境变量来存储Key，这里为了演示方便直接写入
# 请替换成你自己的Key
HEFENG_API_KEY = "YOUR_QWEATHER_API_KEY"
# 请替换成你的 API_HOST
HEFENG_API_HOST = "YOUR_API_HOST"





   
    
# 为了演示方便，我们暂时硬编码
TUSHARE_TOKEN = "YOUR_TUSHARE_TOKEN"


def get_realtime_weather(city_name: str) -> str:
    """
    查询指定城市的实时天气信息。
    
    参数:
    city_name (str): 必须是标准的中文城市名称，例如 '北京', '上海', '深圳市'。
    
    返回:
    str: 一个包含天气、温度、风向的格式化字符串。
         例如：'北京: 晴, 实时温度25℃, 东北风3级'。
         如果城市未找到或查询失败，则返回错误信息。
    """
    print(f"--- [工具被调用：get_realtime_weather] ---")
    print(f"--- [工具入参：city_name={city_name}] ---")

    # === 第1步：通过城市名获取Location ID ===
    url_lookup = f"{HEFENG_API_HOST}/geo/v2/city/lookup?location={city_name}"
    
    headers = {
        "X-QW-Api-Key": f"{HEFENG_API_KEY}",
        "Accept": "application/json"
    }
        
    try:
        resp = requests.get(url=url_lookup, headers=headers)

        # 优先使用 requests 自动解码并解析 JSON
        try:
            data = resp.json()
        except ValueError:
            # 如果解析失败，尝试手动解压（以防服务器返回了 gzip 内容但没有正确的 Header）
            try:
                raw = resp.content
                try:
                    decompressed = gzip.decompress(raw)
                except OSError:
                    # 不是 gzip 或 解压失败，直接用 raw
                    decompressed = raw
                    
                data = json.loads(decompressed.decode('utf-8'))
            except Exception as e:
                print(f"解析响应JSON失败: {e}")
                return None

                # 检查返回结构并提取 location
            if not isinstance(data, dict):
                print("响应格式不是预期的 JSON 对象。")
                return None
                
        if data.get("code") != "200" or not data.get("location"):
            return f"错误：未找到城市 '{city_name}' 的Location ID。"

        location_id = data["location"][0]["id"]

        # === 第2步：通过Location ID获取实时天气 ===
        url_weather = f"{HEFENG_API_HOST}/v7/weather/now?location={location_id}"
        
        response_weather = requests.get(url=url_weather, headers=headers)
        response_weather.raise_for_status()
        data_weather = response_weather.json()
        
        if data_weather.get("code") != "200":
            return f"错误：获取 '{city_name}' 天气失败。"

        now = data_weather["now"]
        result_str = (
            f"{city_name} (ID: {location_id}): "
            f"天气: {now['text']}, "            
            f"实时温度: {now['temp']}℃, "
            f"体感温度: {now['feelsLike']}℃, "
            f"风向: {now['windDir']}, "
            f"风力等级: {now['windScale']}级"
        )
        
        print(f"--- [工具返回值：{result_str}] ---")
        return result_str
    except requests.exceptions.RequestException as e:
        print(f"--- [工具调用异常：{e}] ---")
        return f"错误：API请求异常 - {e}"
    except Exception as e:
        print(f"--- [工具内部错误：{e}] ---")
        return f"错误：处理数据时发生未知错误 - {e}"
 

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
    
    
from pathlib import Path

def read_file(file_path: str) -> str:
    """
    读取指定路径的文本文件内容。
    
    参数:
    file_path (str): 要读取的文件的完整路径。例如: 'D:/docs/report.txt' 或 'logs/today.log'。
    
    返回:
    str: 文件的文本内容。
         如果文件不存在或读取失败，则返回详细的错误信息。
    """
    print(f"--- [工具被调用：read_file] ---")
    print(f"--- [工具入参：file_path={file_path}] ---")
    
    try:
        # 使用Pathlib确保路径处理的健壮性
        p = Path(file_path)
        
        if not p.exists():
            print(f"--- [工具错误：文件不存在 {file_path}] ---")
            return f"错误：文件路径 '{file_path}' 不存在。"
            
        if not p.is_file():
            print(f"--- [工具错误：路径不是文件 {file_path}] ---")
            return f"错误：路径 '{file_path}' 不是一个文件。"

        # 读取文件内容
        with p.open('r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"--- [工具返回值：成功读取 {len(content)} 字符] ---")
        return content
        
    except Exception as e:
        error_message = f"错误：读取文件 '{file_path}' 时发生异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message



def write_file(file_path: str, content: str) -> str:
    """
    将指定的文本内容写入到指定路径的文件中。
    如果文件已存在，它将被覆盖。如果目录不存在，将尝试创建它。
    
    参数:
    file_path (str): 要写入的文件的完整路径。例如: 'output/result.txt'
    content (str): 要写入文件的文本内容。
    
    返回:
    str: 一个表示操作成功的确认信息。
         如果写入失败，则返回详细的错误信息。
    """
    print(f"--- [工具被调用：write_file] ---")
    print(f"--- [工具入参：file_path={file_path}, content_len={len(content)}] ---")
    
    try:
        # 使用Pathlib创建父目录（如果不存在）
        p = Path(file_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件内容，使用utf-8编码
        with p.open('w', encoding='utf-8') as f:
            f.write(content)
            
        success_message = f"成功：内容已写入文件 '{file_path}'。"
        print(f"--- [工具返回值：{success_message}] ---")
        return success_message
        
    except Exception as e:
        error_message = f"错误：写入文件 '{file_path}' 时发生异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message
    
import subprocess
import sys

def execute_python_code(code: str) -> str:
    """
    在本地的Python环境中执行一段Python代码字符串，并返回其标准输出(stdout)和标准错误(stderr)。
    
    警告：极度危险！此工具会在本机上真实地执行代码！
    请确保你完全理解你要求Agent执行的代码。
    
    参数:
    code (str): 要执行的Python代码字符串。例如: "print(1 + 1)" 或 "import os; print(os.getcwd())"
    
    返回:
    str: 包含代码的标准输出(stdout)和标准错误(stderr)的执行结果。
         如果执行超时（15秒）或发生其他异常，将返回错误信息。
    """
    print(f"--- [工具被调用：execute_python_code] ---")
    print(f"--- [工具入参：code={code}] ---")

    try:
        # 使用 subprocess.run 来执行代码
        # sys.executable 指向当前运行的Python解释器
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True, # 捕获标准输出和标准错误
            text=True,           # 以文本模式处理
            timeout=15,          # 设置15秒超时，防止无限循环
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            # 执行成功
            output = f"执行成功:\n--- STDOUT ---\n{result.stdout}\n"
        else:
            # 执行失败
            output = f"执行失败 (Return Code: {result.returncode}):\n--- STDERR ---\n{result.stderr}\n"
            
        print(f"--- [工具返回值 (部分)：{output[:100]}...] ---")
        return output

    except subprocess.TimeoutExpired:
        error_message = "错误：代码执行超时（15秒）。"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message
    except Exception as e:
        error_message = f"错误：执行代码时发生未知异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message
    
    
# 3. 为多参数工具定义输入模式 (Pydantic)
# 我们为 write_file 工具定义一个专门的输入“数据类”
class WriteFileInput(BaseModel):
    file_path: str = Field(description="要写入的文件的完整路径。例如: 'output/report.md'")
    content: str = Field(description="要写入文件的完整文本内容。")

# 4. 创建新的“包装函数”
def write_file_wrapper(json_string_input: str) -> str:
    """
    一个安全的包装器，用于解析JSON字符串并调用 write_file。
    它会清理输入的字符串（如去除换行符），然后解析它。
    参数:
    json_string_input (str): 一个必须是JSON格式的字符串, 
                             例如: '{"file_path": "report.md", "content": "..."}'
    """
    print(f"--- [工具被调用：write_file_wrapper] ---")
    print(f"--- [工具入参 (原始JSON串): {repr(json_string_input)}] ---")
    
    try:
        # 1. 清理字符串：去除首尾空白（这会移除 \n）
        cleaned_string = json_string_input.strip()
        
        # 2. 解析JSON
        data = json.loads(cleaned_string)
        
        # 3. Pydantic 验证
        validated_data = WriteFileInput(**data)
        
        # 4. 调用原始函数
        return write_file(
            file_path=validated_data.file_path,
            content=validated_data.content
        )
    except json.JSONDecodeError as e:
        return f"错误：Action Input不是一个有效的JSON字符串。错误: {e}. 原始输入: {json_string_input}"
    except ValidationError as e:
        return f"错误：JSON中的字段无效。{e}. 原始输入: {json_string_input}"
    except Exception as e:
        return f"错误：执行write_file_wrapper时发生未知错误。{e}"    