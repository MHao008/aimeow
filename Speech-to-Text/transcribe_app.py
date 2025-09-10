import whisper
import os

# 设置模型名称
model_name = "base"
# 设置模型文件路径
model_dir = "./models"


def transcribe_audio(audio_path):
    """
    将音频文件转换为文字
    
    参数:
        audio_path: 音频文件的路径
    返回:
        转换后的文字内容
    """

    # 加载模型 (可选择不同大小的模型: tiny, base, small, medium, large)
    model = whisper.load_model(model_name, download_root=model_dir)


    # 执行转录
    result = model.transcribe(audio_path)
    
    # 返回转录文本
    return result["text"]


def save_text(content, file_name):
    # 将结果保存到 results文件夹下
    if not os.path.exists("results"):
        os.makedirs("results")

    path = f"results/{file_name}"
    # 使用 utf-8 编码
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path


if __name__ == "__main__":
    # 示例使用
    # 当前目录下有一个音频文件 "meeting.mp3"
    audio_file = "./meeting.mp3"  # 替换为你的音频文件路径
    text = transcribe_audio(audio_file)
    print("转录结果:", text)