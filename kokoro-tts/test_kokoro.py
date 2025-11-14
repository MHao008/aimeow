# -----------------------------------------------------
# 喵喵实战室：Kokoro TTS 基础 Demo
# -----------------------------------------------------

from kokoro import KPipeline, KModel
import soundfile as sf
import torch
import time

print("正在加载Kokoro管线...")


device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_path = 'ckpts/kokoro/kokoro-v1_1-zh.pth'
config_path = 'ckpts/kokoro/config.json'
model = KModel(model=model_path, config=config_path).to(device).eval()

# 'a' 代表 American English
pipeline = KPipeline(lang_code='a', model=model) 

# 准备文本和声音（'af_sol'是一个美式女声）
text = "Hello world! I am AI Meow, and this is truly magical!"
voice = 'ckpts/kokoro/voices/af_sol.pt'

print(f"准备生成: '{text}' (声音: {voice})")
start_time = time.time()

# Kokoro 使用 'generator' (生成器) 来流式输出
generator = pipeline(text, voice=voice)

# 迭代生成器，获取最终的音频数据
# gs: generation speed, ps: phoneme speed
for i, (gs, ps, audio) in enumerate(generator):
    if i == 0:
        print("TTFA (首包音频延迟): %.2fs" % (time.time() - start_time))
    
    # audio 是一个numpy数组，我们在这里保存最后一块
    final_audio = audio

end_time = time.time()
print(f"总耗时: %.2fs" % (end_time - start_time))

# 保存到文件
output_file = 'output_en.wav'
sf.write(output_file, final_audio, 24000)
print(f"🎉 成功！音频已保存到 {output_file}")