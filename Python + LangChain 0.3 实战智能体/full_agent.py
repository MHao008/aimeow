# full_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def main():
    wiki_tool = Tool.from_function(lambda q: WikipediaAPIWrapper().run(q), name="wiki", description="查询 Wikipedia")
    client = MultiServerMCPClient({"calc": {"command": "python", "args": ["mcp_server.py"], "transport": "stdio"}})
    mcp_tools = await client.get_tools()
    tools = [wiki_tool] + mcp_tools
    llm = ChatOpenAI(model="gpt-4.1", temperature=0, api_key="sk-xxxx", base_url="https://apikfm.com/v1")
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True, handle_parsing_errors=True)
    print(await agent.ainvoke({"input": "请查一下中国的国土面积是多少，然后用加法将这个面积数值加上 1000"}))

asyncio.run(main())
