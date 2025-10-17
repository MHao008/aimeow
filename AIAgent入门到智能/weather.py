import requests
import json
import gzip

# 强烈建议你使用环境变量来存储Key，这里为了演示方便直接写入
# 请替换成你自己的Key
HEFENG_API_KEY = "YOUR_QWEATHER_API_KEY"
# 请替换成你的 API_HOST
API_HOST = "YOUR_API_HOST"



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
    url_lookup = f"{API_HOST}/geo/v2/city/lookup?location={city_name}"
    
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
        url_weather = f"{API_HOST}/v7/weather/now?location={location_id}"
        
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

# --- 本地测试 ---
if __name__ == "__main__":
    weather_info = get_realtime_weather("成都")
    print(weather_info)
