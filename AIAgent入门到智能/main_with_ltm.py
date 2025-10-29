# -----------------------------------------------------
# 喵喵实战室：Agent长期记忆模块 (main_with_ltm.py)
# -----------------------------------------------------

import os
from langchain_classic.agents import create_react_agent
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.tools import tool, ToolRuntime # <- 导入ToolRuntime 
from langchain_openai import ChatOpenAI


# 导入我们之前创建的工具
from agent_tools import (
    get_realtime_weather, 
    get_stock_realtime_price,
    read_file,
    write_file,
    execute_python_code,
    write_file_wrapper
)
# 导入会话记忆相关
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory

# ！！！！！！！！！！！！！！！！！！！！
# 步骤1：导入“长期记忆”相关的新模块
# ！！！！！！！！！！！！！！！！！！！！
from langgraph.store.memory import InMemoryStore # <- LangGraph的内存存储
from dataclasses import dataclass            # <- 用于定义上下文结构
from typing_extensions import TypedDict      # <- 用于定义工具的结构化输入
from typing import Any

# --- 核心设置 (与上期相同) ---

# 设置你的API Keys (强烈推荐使用环境变量)
# 确保你已经设置了 OPENAI_API_KEY, HEFENG_API_KEY, TUSHARE_TOKEN
os.environ["OPENAI_API_KEY"] = "你的OpenAI API密钥"
os.environ["OPENAI_API_BASE"] = "https://apikfm.com/v1" # 这里使用我们自己的API，开发喵API 
# ...等等


# --- 步骤2：初始化“大脑” (与上期相同) ---
print("[1/6] 正在初始化大模型 '大脑'...")
# 我们选用gpt-4o，你也可以换成Moonshot或OpenAI
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
)

# --- 步骤3：初始化“长期记忆库” (Store) ---
print("[2/6] 正在初始化 '长期记忆库' (使用InMemoryStore)...")
# InMemoryStore 将数据存在内存字典里，程序重启会丢失
# 在生产环境中，你会换成 RedisStore, PostgresStore 等数据库后端
store = InMemoryStore()

# 讲解Store的数据组织：Namespace 和 Key
# 我们将用户信息存储在 "users" 这个 Namespace 下
# Key 就是每个用户的唯一ID
print("   数据将按 Namespace='users', Key=user_id 的方式组织。")

# ！！！可选：我们可以预先存入一些用户信息，模拟老用户！！！
store.put(
    ("users",),       # Namespace: 'users'分组
    "user_007",       # Key: 用户ID
    {"name": "邦德", "preferred_language": "中文"} # Value: 用户信息字典
)
print("   已预存 user_007 的信息。")


# --- 步骤4：定义“上下文”结构 (Context) ---
# 这个Context会在每次调用Agent时传入，告诉Agent当前是谁在对话
@dataclass
class AgentContext:
    user_id: str

# --- 步骤5：定义“长期记忆”读写工具 ---
print("[3/6] 正在创建 '长期记忆' 读写工具...")

# 5.1 定义写入工具的输入结构 (UserInfo)
# 使用TypedDict的好处是：为LLM提供了清晰的格式要求，
# LLM知道调用此工具时，必须生成包含'name'字段的字典作为Action Input。
class UserInfo(TypedDict):
    name: str

# 5.2 创建写入工具 (save_user_info)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[AgentContext]) -> str:
    """保存当前用户的基本信息，目前只支持保存'name'。"""
    print(f"--- [工具被调用：save_user_info] ---")
    print(f"--- [工具入参：user_info={user_info}] ---")
    # 从runtime中获取store和当前用户的context (由AgentExecutor注入)
    current_store: InMemoryStore = runtime.store
    current_user_id: str = runtime.context.user_id
    # 使用 Namespace="users", Key=current_user_id 存入数据
    current_store.put(("users",), current_user_id, user_info)
    return f"成功：已记住当前用户({current_user_id})的名字是 {user_info.get('name')}。"


# 5.3 创建读取工具 (get_user_info)
@tool
def get_user_info(runtime: ToolRuntime[AgentContext]) -> str:
    """查询当前用户的基本信息。"""
    print(f"--- [工具被调用：get_user_info] ---")
    
    # 从runtime中获取store和当前用户的context
    current_store: InMemoryStore = runtime.store
    current_user_id: str = runtime.context.user_id
    print(f"--- [查询用户ID：{current_user_id}] ---")
    
    # 使用 Namespace="users", Key=current_user_id 读取数据
    user_info_value = current_store.get(("users",), current_user_id)
    
    if user_info_value:
        # LangChain InMemoryStore 的值封装在 .value 属性中，所以 user_info_value.value 才是我们存入的字典
        stored_value = user_info_value.value
        if isinstance(stored_value, str):
            # 兼容早期存入 JSON 字符串的情况
            try:
                stored_value = json.loads(stored_value)
            except json.JSONDecodeError:
                pass
            
        user_name = user_info_value.value.get("name", "未知")
        result = f"当前用户({current_user_id})的名字是: {user_name}。"
    else:
        result = f"当前用户({current_user_id})的信息不存在。"
    print(f"--- [工具返回值：{result}] ---")
    return result

# --- 步骤6：将所有工具（包括新工具）加入列表 ---
print("[4/6] 正在封装所有工具 '双手'...")
tools = [
    # (此处省略与上期相同的Web工具和本地工具定义代码)

    # ！！！！！！！！！！！！！！！！！！！！
    # <-- 新增长期记忆工具 -->
    # ！！！！！！！！！！！！！！！！！！！！
    save_user_info,
    get_user_info
]
tool_names = ", ".join([tool.name for tool in tools])

# --- 步骤7：升级Prompt模板 ---
print("[5/6] 正在加载 ReAct 思考框架...")
react_prompt_template_with_memory = """
回答以下问题，尽你所能。

使用以下格式：

Question: 你必须回答的输入问题
Thought: 你应该时刻思考该做什么
Action: 采取的行动，如果需要使用工具则必须是[{tool_names}]中的一个
Action Input: 你的行动输入
  
Observation: 你的行动结果
... (这个 Thought/Action/Action Input/Observation 的过程可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 原始输入问题的最终答案

开始！

**重要的是，在你的“Thought”中，要时刻参考之前的聊天记录。**

"""
# prompt = PromptTemplate.from_template(react_prompt_template_with_memory)

# --- 步骤8：！！！组装Agent执行器 (关键变更)！！！ ---
print("[6/6] 正在组装Agent执行器 (加入长期记忆)...")


# ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 关键：在创建create_agent时，传入store和context_schema
# 这样Agent在调用工具时，ToolRuntime才能访问到它们
# ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
agent_executor = create_agent(
    model=llm,
    system_prompt=react_prompt_template_with_memory,
    tools=tools,
    store=store,                 # <- 把我们的内存存储传进去
    context_schema=AgentContext  # <- 告诉执行器上下文的结构
)

# --- 步骤9：对话循环 (需要传入Context) ---
# chat_history = ChatMessageHistory()
current_user = "user_123" # 假设当前用户是 user_123

print(f"\n--- 具备长期记忆的Agent 已启动 (当前用户: {current_user}) ---")
print("--- (输入 '退出' 来结束对话) ---")

while True:
    try:
        user_input = input("👤 你：")
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("🤖 Agent: 拜拜！下次再聊！")
            break
        
        
        # # 把历史记录取出来
        # history_messages = chat_history.messages

        # # 当前用户的新输入
        # new_message = HumanMessage(content=user_input)

        # # 拼接成完整消息序列
        # input_messages = history_messages + [new_message]

        # ！！！！！！！！！！！！！！！！！！！！！！！！！！
        # 关键：调用invoke时，传入当前的Context (包含user_id)
        # ！！！！！！！！！！！！！！！！！！！！！！！！！！
        result = agent_executor.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            # 将当前用户信息作为上下文传入
            context=AgentContext(user_id=current_user)
        )

        print(f"result: {result}")
        ai_output = result["messages"][-1].content
        print(f"🤖 Agent: {ai_output}")

        # chat_history.add_user_message(HumanMessage(content=user_input))
        # chat_history.add_ai_message(AIMessage(content=ai_output))

    except Exception as e:
        print(f"\n--- Agent 运行出错 ---")
        print(e)
        import traceback
        traceback.print_exc()