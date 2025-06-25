# mcp_client_agent.py
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    client = MultiServerMCPClient({"calc": {"command": "python", "args": ["mcp_server.py"], "transport": "stdio"}})
    tools = await client.get_tools()
    llm = ChatOpenAI(model_name="gpt-4.1", temperature=0, api_key="sk-xxxxx", base_url="https://apikfm.com/v1")
  
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True, handle_parsing_errors=True)
    print(await agent.ainvoke({"input": "请帮我算一下 12 加 30 等于几？"}))

asyncio.run(main())
