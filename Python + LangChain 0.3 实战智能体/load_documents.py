# load_documents.py
from langchain.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 加载文档
loader = TextLoader("knowledge_base.txt")
docs = loader.load()

# 创建嵌入模型
emb = OpenAIEmbeddings(model="text-embedding-3-small", api_key="sk-xxxxx", base_url="https://apikfm.com/v1")
# 创建向量存储
vector_store = Chroma.from_documents(
    collection_name="knowledge",
    embedding=emb,
    persist_directory="./kb_db",
    documents=[docs[0]]
)

