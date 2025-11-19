# -----------------------------------------------------
# 喵喵实战室：Agent知识库工具 (knowledge_tools.py)
# -----------------------------------------------------

import requests
import json
import os

# --- 从环境变量或配置文件中读取你的Dify密钥 ---
# 确保在运行前设置好环境变量
# export DIFY_API_KEY="your_secret_key"
# export DIFY_API_URL="https://api.dify.ai/v1" (Dify云端的地址，本地部署请修改)

DIFY_API_KEY = os.environ.get("DIFY_API_KEY")
# 注意：这里的URL是Dify API的“聊天”端点
DIFY_API_URL = os.environ.get("DIFY_API_URL", "https://api.dify.ai/v1") + "/chat-messages"


def query_dify_knowledge_base(query: str) -> str:
    """
    一个专用于查询“AI喵智能体”公众号内部知识的工具。
    当你需要回答关于 "AI Agent"、"Dify"、"Ollama"、"Stable Diffusion"
    等我们教程中特定内容的问题时，请使用此工具。
    请勿用此工具查询天气、股票或执行代码。
    
    参数:
    query (str): 用户关于私有知识的具体问题。
    
    返回:
    str: Dify知识库返回的答案。
    """
    print(f"--- [工具被调用：query_dify_knowledge_base] ---")
    print(f"--- [工具入参：query={query}] ---")

    if not DIFY_API_KEY:
        return "错误：DIFY_API_KEY 未设置。无法查询知识库。"

    # Dify API的请求头
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    # Dify API的请求体
    # "conversation_id" 确保Dify内部也能管理上下文
    # "query" 是用户的提问
    # "user" 是一个唯一的用户标识
    body = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking", # 我们需要一个同步的答案，而不是流式
        "conversation_id": "", 
        "user": "my_agent_system"
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, data=json.dumps(body))
        response.raise_for_status() # 如果请求失败则抛出异常
        
        response_json = response.json()
        
        # 解析Dify返回的答案
        answer = response_json.get("answer", "未在知识库中找到明确答案。")
        
        print(f"--- [工具返回值：{answer[:100]}...] ---")
        return answer

    except requests.exceptions.RequestException as e:
        error_message = f"错误：连接Dify知识库失败 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message
    except Exception as e:
        error_message = f"错误：解析Dify响应时发生异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message

# --- 本地测试 ---
if __name__ == "__main__":
    if not DIFY_API_KEY:
        print("请先设置 DIFY_API_KEY 和 DIFY_API_URL 环境变量！")
    else:
        # 假设你的知识库里有关于ReAct的文章
        test_query = "ReAct是什么？"
        answer = query_dify_knowledge_base(test_query)
        print(f"\n测试提问：{test_query}")
        print(f"知识库回答：{answer}")