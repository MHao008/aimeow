import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 🔐 设置 OpenAI API Key
os.environ["OPENAI_API_KEY"] = "你的OpenAI API密钥"
os.environ["OPENAI_API_BASE"] = "https://apikfm.com/v1" # 这里使用我们自己的API，开发喵API 

# 📄 加载你的本地文档
loader = TextLoader("test.txt", encoding='utf-8')
documents = loader.load()

# ✂️ 切分文档（每段最多500字符）
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 🔍 构建向量索引
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# 🤖 构建问答链
llm = ChatOpenAI(model_name="gpt-4o")  # 也可换成 gpt-4
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# 🧪 开始对话
while True:
    query = input("你想问什么？（输入 exit 退出）：")
    if query.lower() == "exit":
        break
    result = qa_chain.run(query)
    print("🤖 AI回答：", result)