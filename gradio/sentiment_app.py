import gradio as gr
from transformers import pipeline

# 1. 加载一个预训练的情感分析模型 (我们的AI“大脑”)
#    这行代码会自动从Hugging Face社区下载并加载一个成熟的模型
#    第一次运行时会比较慢，因为它在下载模型文件，请耐心等待
sentiment_analyzer = pipeline("sentiment-analysis")

# 2. 定义我们的核心功能函数
#    它接收文本，并返回分析结果
def analyze_sentiment(text):
    # 模型返回的是一个列表，我们取第一个结果
    result = sentiment_analyzer(text)[0]
    # 从结果中提取标签（POSITIVE/NEGATIVE）和分数
    label = result['label']
    score = f"{result['score']:.2%}" # 将小数格式化为百分比
    return f"情感倾向: {label}\n置信度: {score}"

# 3. 创建并配置Gradio界面 (这次我们让它更漂亮一点)
demo = gr.Interface(
    fn=analyze_sentiment,
    # 使用更丰富的gr.Textbox组件，可以设置行数和占位提示符
    inputs=gr.Textbox(lines=3, placeholder="在这里输入你想分析的句子... (英文效果更佳)"),
    outputs="text",  # 输出依然是文本
    title="喵喵的情感分析小屋",
    description="输入一句话，让我来告诉你它的情感色彩是积极(POSITIVE)还是消极(NEGATIVE)。"
)

# 4. 启动应用
demo.launch()