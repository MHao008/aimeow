from openai import OpenAI

# 使用 开发喵API
client = OpenAI(api_key="sk-xxxxx", base_url="https://apikfm.com/v1")

prompt = """
你是SQL专家。根据下面表结构和问题生成SQL。
// schema
Table users(id INTEGER, name TEXT, age INTEGER);
Table orders(id INTEGER, user_id INTEGER, amount FLOAT);
// question
“查询所有年龄超过30岁的用户及其订单总额。”

请返回可执行 SQL 语句，并用三个反引号包裹。
"""
res = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
print(res.choices[0].message.content)
