# 导入gradio库，我们叫它gr，这是一种约定俗成的简写
import gradio as gr

# 1. 定义你的核心函数 (这是你的应用的“大脑”)
#    这个函数接收一个参数`name`，并返回一个问候语。
def greet(name):
    # 当输入为空时，返回一个默认的问候
    if name is None or name.strip() == "":
        return "你好呀, 陌生人!"
    # 否则，返回个性化的问候
    return f"你好呀, {name}!"

# 2. 创建一个Gradio界面实例 (这是给“大脑”穿上“外衣”)
#    gr.Interface是Gradio的核心，它负责将函数包装成UI
demo = gr.Interface(
    fn=greet,  # fn: 指定要包装的函数，也就是我们上面定义的greet
    inputs="text",  # inputs: 定义输入组件的类型，'text'代表一个简单的文本输入框
    outputs="text"  # outputs: 定义输出组件的类型，这里也是一个文本框
)

# 3. 启动你的Web应用！(让世界看到它)
#    这行代码会启动一个本地Web服务器，并生成一个可访问的链接
demo.launch()