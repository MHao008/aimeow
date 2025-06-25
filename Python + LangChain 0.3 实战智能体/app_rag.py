# app_rag.py
import streamlit as st
from rag_agent import query_rag

st.title("🔍 RAG 智能问答（连续问答版）")

# 初始化对话历史
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 聊天历史展示
for i, (user, bot) in enumerate(st.session_state.chat_history):
    st.markdown(f"**你：** {user}")
    st.markdown(f"**AI：** {bot}")

q = st.text_input("请输入问题", key="input")
if st.button("提交"):
    if q.strip():
        ans = query_rag(q)
        st.session_state.chat_history.append((q, ans))
        st.rerun()  # 立即刷新页面，显示新消息
        
        
# 运行：streamlit run app_rag.py