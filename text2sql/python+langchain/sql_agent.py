# sql_agent.py
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///example.db")
llm = ChatOpenAI(model="gpt-4o", api_key="sk-xxxx", base_url="https://apikfm.com/v1", temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm, return_direct=True)
tools = toolkit.get_tools()

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
print(agent.run("帮我查询每个用户的订单总金额，有多少用户总额超过100"))