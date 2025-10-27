# -----------------------------------------------------
# 喵喵实战室：Agent组装车间 (main.py)
# -----------------------------------------------------

import os
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool

# ！！！！！！！！！！！！！！！！！！！！
# 步骤1：导入我们的大模型“大脑”

# ！！！！！！！！！！！！！！！！！！！！
from langchain_openai import ChatOpenAI

# ！！！！！！！！！！！！！！！！！！！！
# 步骤2：导入我们亲手打造的“工具箱”
# ！！！！！！！！！！！！！！！！！！！！
from agent_tools import (
    get_realtime_weather, 
    get_stock_realtime_price,
    read_file,
    write_file,
    execute_python_code,
    write_file_wrapper
)

# -----------------------------------------------------
# 核心设置
# -----------------------------------------------------

# 设置你的API Keys (强烈推荐使用环境变量)
# 确保你已经设置了 OPENAI_API_KEY, HEFENG_API_KEY, TUSHARE_TOKEN
os.environ["OPENAI_API_KEY"] = "你的OpenAI API密钥"
os.environ["OPENAI_API_BASE"] = "https://apikfm.com/v1" # 这里使用我们自己的API，开发喵API 
# ...等等


# -----------------------------------------------------
# 步骤3：初始化“大脑” (LLM)
# -----------------------------------------------------
print("[1/4] 正在初始化大模型 '大脑'...")
# 我们选用智谱GLM-4，你也可以换成Moonshot或OpenAI
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1, # Agent执行任务，温度调低，确保稳定性
)

# -----------------------------------------------------
# 步骤4：将Python函数“封装”成Agent能用的Tool
# -----------------------------------------------------
print("[2/4] 正在封装工具 '双手'...")

# 关键：我们将Python函数 + 详细的docstring描述，一起打包成Tool对象
# Agent的“大脑”只会去读 'description' 里的内容来决定用哪个工具！
tools = [
    Tool(
        name="QueryWeather",
        func=get_realtime_weather,
        description="""查询指定城市的实时天气信息。
                   参数: city_name (str): 必须是标准的中文城市名称，例如 '北京', '上海', '深圳市'。
                   返回: str: 包含天气、温度、风向的格式化字符串。"""
    ),
    Tool(
        name="QueryStockPrice",
        func=get_stock_realtime_price,
        description="""查询指定股票代码的最新实时行情价格。
                   参数: stock_code (str): 必须是Tushare标准的股票代码, 格式为 'XXXXXX.SZ' 或 'XXXXXX.SH'。
                   例如: '000001.SZ' (平安银行), '600519.SH' (贵州茅台)。"""
    ),
    Tool(
        name="ReadFile",
        func=read_file,
        description="""读取指定路径的文本文件内容。
                   参数: file_path (str): 要读取的文件的完整路径。"""
    ),
    Tool(
        name="WriteFile",
        func=write_file_wrapper,
        description="""将指定的文本内容写入到指定路径的文件中。
                   如果文件已存在，它将被覆盖。
                   参数: 必须是一个JSON格式的字符串。
                   JSON格式: {{"file_path": "要写入的文件的完整路径", "content": "要写入文件的文本内容"}}"""
    ),
    Tool(
        name="ExecutePythonCode",
        func=execute_python_code,
        description="""在本地的Python环境中执行一段Python代码字符串。
                   警告：这是一个高风险工具！
                   参数: code (str): 要执行的Python代码字符串。例如: "print(1 + 1)"
                   返回: str: 包含代码的标准输出和标准错误。"""
    )
]

# -----------------------------------------------------
# 步骤5：创建 ReAct 提示词模板 (Agent的“行动纲领”)
# -----------------------------------------------------
print("[3/4] 正在加载 ReAct 思考框架...")

# 这段提示词是LangChain提供的标准ReAct模板
# 它告诉Agent如何思考、如何使用工具、如何给出最终答案
# 我们从Hub上拉取一个中文优化过的模板（如果需要，或使用默认英文模板）
# 简化的模板示意：
react_prompt_template = """
回答以下问题，尽你所能。你可以使用以下工具：

{tools}

使用以下格式：

Question: 你必须回答的输入问题
Thought: 你应该时刻思考该做什么
Action: 采取的行动，必须是[{tool_names}]中的一个
Action Input: 你的行动输入
    *** 重要规则 ***
    1. 如果工具的描述中包含 "Input schema" (输入 schema)，你的 'Action Input' **必须**是一个严格的、单行的 JSON 对象字符串，其键和值必须匹配该 schema。
       例如: {{"file_path": "some/path.txt", "content": "要写入的内容"}}
    2. 如果工具的描述中没有 "Input schema" (例如它只需要一个简单的字符串，像 QueryWeather)，则 'Action Input' 应该只是那个字符串值。
       例如: 上海
    *****************
Observation: 你的行动结果
... (这个 Thought/Action/Action Input/Observation 的过程可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 原始输入问题的最终答案

开始！

Question: {input}
Thought:{agent_scratchpad}
"""

# 将模板字符串转换为LangChain的PromptTemplate对象
prompt = PromptTemplate.from_template(react_prompt_template)

# -----------------------------------------------------
# 步骤6：创建Agent执行器
# -----------------------------------------------------
print("[4/4] 正在组装Agent执行器...")

# "create_react_agent" 负责将 大脑(llm) 和 提示词(prompt) 绑定在一起
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# "AgentExecutor" 是Agent的“心跳”，它负责运行整个 ReAct 循环
# verbose=True 让我们能看到Agent的完整思考过程！
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, # ！！！！！！一定要打开，看“心路历程”
    handle_parsing_errors=True # 处理可能的输出格式错误
)

# -----------------------------------------------------
# 步骤7：见证奇迹的时刻！
# -----------------------------------------------------

print("\n--- Agent 已启动，准备接收任务 ---")

# 这是一个需要跨工具协作的“超级复杂”的任务
complex_task = (
    "帮我查询一下 '贵州茅台'(600519.SH) 的当前股价，"
    "然后再查询一下 '上海' 的天气。"
    "最后，把这两项信息汇总，写入一个名为 'report.md' 的文件中。"
)

try:
    # 运行Agent
    result = agent_executor.invoke({"input": complex_task})
    
    print("\n--- Agent 任务完成 ---")
    print(f"最终结果: {result['output']}")

except Exception as e:
    print(f"\n--- Agent 运行出错 ---")
    print(e)