# rag_agent.py
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

llm = ChatOpenAI(model_name="gpt-4.1", temperature=0, api_key="sk-xxxx", base_url="https://apikfm.com/v1")
emb = OpenAIEmbeddings(model="text-embedding-3-small", api_key="sk-xxxx", base_url="https://apikfm.com/v1")

retriever = Chroma(persist_directory="./kb_db", embedding_function=emb).as_retriever(search_kwargs={"k":3})

retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
combine_docs_chain = create_stuff_documents_chain(
    llm, retrieval_qa_chat_prompt
)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)



def query_rag(question: str):
    res = retrieval_chain.invoke({"input": question})
    print(res)
    return res["answer"]


# q = query_rag("开发喵AI涵盖哪些模型？")
