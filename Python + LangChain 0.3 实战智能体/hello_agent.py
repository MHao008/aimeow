# hello_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import Tool, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# 1. 初始化 LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key="sk-xxxx", base_url="https://apikfm.com/v1")

# 2. 创建搜索工具
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)


# 3. 将工具封装成 LangChain 工具
tools = [Tool.from_function(wiki.run, name="wiki-search",
                            description="用于从维基百科搜索内容")]

# 4. 构建 Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# 5. 互动测试
if __name__ == "__main__":
    question = "中国最高的山峰叫什么名字？"
    print("问题:", question)
    answer = agent.invoke(question)
    print("回答:", answer)
