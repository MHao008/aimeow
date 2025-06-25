# rag_chat.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

emb = OpenAIEmbeddings(model="text-embedding-3-small", api_key="sk-xxxx", base_url="https://apikfm.com/v1")
retriever = Chroma(persist_directory="./kb_db", embedding_function=emb).as_retriever(search_kwargs={"k":3})

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chat = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model_name="gpt-4.1", temperature=0, api_key="sk-xxxx", base_url="https://apikfm.com/v1"),
    retriever=retriever,
    memory=memory
)

def chat_loop():
    while True:
        q = input("你问：")
        if q.lower() in ["exit","退出"]:
            break
        res = chat.invoke({"question": q})
        print("AI：", res["answer"])


# chat_loop()