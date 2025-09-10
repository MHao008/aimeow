import torch
from TTS.api import TTS

# from functools import partial

# # 替换 torch.load，确保 weights_only=False
# torch_load_org = torch.load
# torch.load = partial(torch_load_org, weights_only=False)


# 1. 检查是否有可用的GPU (NVIDIA显卡)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. 定义模型名称和文件路径

#    XTTSv2是高质量的多语言声音克隆模型

model_name ="tts_models/multilingual/multi-dataset/xtts_v2"

#    你的声音样本文件，请确保它和脚本在同一目录下

speaker_wav_path ="my.mp3" # <-- 请修改为你的文件名



#    你希望AI用你的声音说出的文本
text_to_clone ="这是由人工智能克隆的我，如果喜欢我们的话，请关注我们，我们会持续更新新的内容，喜欢的话请点赞收藏转发，谢谢大家"


#    最终生成的音频文件保存路径
output_path ="cloned_voice_output.wav"

# 3. 初始化TTS模型
#    第一次运行时，程序会自动从网上下载模型文件（约2-3GB）
#    请务必保持网络通畅，并耐心等待！
print("正在加载TTS模型，首次运行会自动下载，请耐心等待...")
tts = TTS(model_name, progress_bar=False).to(device)

# 4. 执行声音克隆！
print(f"\n准备使用 '{speaker_wav_path}' 的声音，朗读以下文本：")
print(f"'{text_to_clone}'")
print("开始克隆，请稍候...")

#    调用tts_to_file方法，这是最核心的一步
#    text: 要合成的文本
#    speaker_wav: 你的声音样本文件路径
#    language: 文本的语言（'zh-cn'代表简体中文）
#    file_path: 输出音频的保存路径
tts.tts_to_file(
    text=text_to_clone,
    speaker_wav=speaker_wav_path,
    language="zh-cn",
    file_path=output_path
)
print(f"\n🎉 声音克隆成功！音频文件已保存到: {output_path}")
# 可能出现错误：   AttributeError: 'GPT2InferenceModel' object has no attribute 'generate'
# 降级依赖即可  python -m pip install transformers==4.33.0

