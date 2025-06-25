# search_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key="sk-xxxxx", base_url="https://apikfm.com/v1")
wiki = WikipediaAPIWrapper()
wiki_tool = Tool.from_function(
    lambda query: wiki.run(query),
    name="wiki-search",
    description="用于根据关键词查询 Wikipedia 内容"
)

agent = initialize_agent([wiki_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
print(agent.run("中国的首都是哪？"))
