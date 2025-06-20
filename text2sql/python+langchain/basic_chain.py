# basic_chain.py

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase

# 初始化数据库
db = SQLDatabase.from_uri("sqlite:///example.db")

# 初始化模型
llm = ChatOpenAI(
    model="gpt-4o",
    api_key="sk-xxxx",  # 替换为你的 key
    base_url="https://apikfm.com/v1",
    temperature=0
)

# 自定义 Prompt
prompt = PromptTemplate(
    input_variables=["table_info", "query"],
    template="""
你是一个会写 SQL 的 AI。
请直接输出 SQL 查询语句，不要解释。不需要任何其他内容，只要 SQL 语句，不要加 ```sql 或 ``` 包裹。
表结构：
{table_info}
问题：
{query}
"""
)



# 构建链：生成 SQL
generate_sql_chain = prompt | llm | StrOutputParser()

# 构建总链：先取 table_info -> 然后生成 SQL -> 然后执行 SQL
chain = RunnableMap({
    "table_info": lambda _: db.get_table_info(),
    "query": lambda x: x["query"]
}) | generate_sql_chain | (lambda sql: db.run(sql))

# 运行
result = chain.invoke({"query": "查询用户 Bob 的订单总金额"})
print(result)

