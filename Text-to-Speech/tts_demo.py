# -----------------------------------------------------
# 喵喵实战室：OpenAI TTS 语音合成器
# -----------------------------------------------------

# 导入openai库，我们未来强大的AI能力都来自于它
from openai import OpenAI
# 导入Path库，用于优雅地处理文件路径
from pathlib import Path

# --- 核心配置 ---
# 1. 初始化OpenAI客户端
#    因为我们已经设置了环境变量，所以这里无需再传入api_key参数
#    如果没设置使用注释方法调用

# client = OpenAI(base_url="https://apikfm.com/v1",api_key="sk-xxxxxx") # 使用 开发喵API 需要可以联系我
client = OpenAI()
# 2. 定义你想让AI朗读的文本内容
text_to_speak = "你好呀，我是AI喵智能体！今天天气真不错，我们一起用代码来创造声音吧！"

# 3. 定义保存音频的文件路径
#    Path(__file__).parent 会获取当前脚本所在的目录
#    然后我们用 / 操作符来拼接文件名，这比用字符串"+"更安全、更优雅
speech_file_path = Path(__file__).parent / "speech_demo_onyx.mp3"

# --- 开始语音合成 ---
print(f"准备朗读的文本: {text_to_speak}")
print("正在请求OpenAI生成语音，请稍候...")

# 4. 调用OpenAI的语音合成API，这是最核心的一步
response = client.audio.speech.create(
    # model: 模型选择，'tts-1'速度更快，'tts-1-hd'质量更高更清晰
    model="tts-1-hd",
    
    # voice: 声音选择，共6种，每一种都很有特色
    # alloy, echo, fable, onyx, nova, shimmer
    voice="nova",
    
    # input: 我们要转换的文本
    input=text_to_speak
)

# 5. 将API返回的音频流，直接保存到我们指定的文件中
#    stream_to_file是官方推荐的用法，它会高效地处理数据流
response.stream_to_file(speech_file_path)

print(f"🎉 语音生成成功！文件已保存到: {speech_file_path}")