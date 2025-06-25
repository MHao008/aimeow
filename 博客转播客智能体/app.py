# app.py
import os
import streamlit as st
from uuid import uuid4
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.eleven_labs import ElevenLabsTools
from agno.utils.audio import write_audio_to_file


# Streamlit 页面设置
st.set_page_config(page_title="🎙️ 博客转播客智能体", layout="centered")
st.title("🎙️ 博客转播客智能体")

# 安全录入密钥
with st.sidebar:
    st.header("API 密钥配置")
    openai_api_key = st.text_input("🧠 OpenAI/API Key", type="password", key="OPENAI_API_KEY", help="用于摘要", on_change=lambda: os.environ.update({"OPENAI_API_KEY": st.session_state.OPENAI_API_KEY}))
    firecrawl_api_key = st.text_input("🧠 Firecrawl Key", type="password", key="FIRECRAWL_API_KEY", help="用于抓取博客内容", on_change=lambda: os.environ.update({"FIRECRAWL_API_KEY": st.session_state.FIRECRAWL_API_KEY}))
    elevenlabs_api_key = st.text_input("🧠 ElevenLabs Key", type="password", key="ELEVEN_LABS_API_KEY", help="用于 TTS 合成", on_change=lambda: os.environ.update({"ELEVEN_LABS_API_KEY": st.session_state.ELEVEN_LABS_API_KEY}))
    st.write("请务必输入以上三个密钥后开始使用。")

# 主流程
url = st.text_input("📥 输入博客 URL")
if st.button("生成播客"):
    if not url:
        st.error("请先输入博客 URL")
        st.stop()
    try:
        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key
        os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key

        # 初始化 Agent
        agent = Agent(
            name="BlogToPodcast",
            agent_id="blog_to_podcast_agent",
            model=OpenAIChat(id="gpt-4o", base_url="https://apikfm.com/v1"), # 支持开发喵API
            tools=[
                FirecrawlTools(),
                ElevenLabsTools(
                    voice_id="JBFqnCBsd6RMkjVDRZzb",
                    model_id="eleven_multilingual_v2",
                    target_directory="audio_generations"
                )
            ],
            instructions=[
                "用户提供博客 URL",
                "1. 使用 FirecrawlTools 抓取文章全文",
                "2. 使用模型生成不超过2000字符的摘要",
                "3. 使用 ElevenLabsTools 将摘要转成音频"
            ],
            markdown=True,
            debug_mode=True
        )
        prefix = "将以下博客转为播客节目："
        rendering: RunResponse = agent.run(f"{prefix} {url}")
        # 读取音频
        audio_base64 = rendering.audio[0].base64_audio
        st.success("✅ 播客生成成功")
        st.audio(audio_base64, format="audio/wav")
        # 可选保存音频文件
        if st.checkbox("保存到本地"):
            os.makedirs("audio_generations", exist_ok=True)
            fn = f"audio_generations/podcast_{uuid4().hex}.wav"
            write_audio_to_file(audio=audio_base64, filename=fn)
            st.write(f"已保存为 `{fn}`")
    except Exception as e:
        st.error(f"生成失败：{e}")
