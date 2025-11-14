# -----------------------------------------------------
# 喵喵实战室：Kokoro TTS 中英混合 Demo
# -----------------------------------------------------

from kokoro import KPipeline, KModel
import soundfile as sf
import torch
import time

device = 'cuda' if torch.cuda.is_available() else 'cpu'
REPO_ID = 'hexgrad/Kokoro-82M-v1.1-zh'
model_path = 'ckpts/kokoro/kokoro-v1_1-zh.pth'
config_path = 'ckpts/kokoro/config.json'
model = KModel(model=model_path, config=config_path).to(device).eval()

# 英文
en_pipeline = KPipeline(lang_code='a', repo_id=REPO_ID, model=False)
def en_callable(text):
    if text == 'Kokoro':
        return 'kˈOkəɹO'
    elif text == 'Sol':
        return 'sˈOl'
    return next(en_pipeline(text)).phonemes

def speed_callable(len_ps):
    speed = 0.8
    if len_ps <= 83:
        speed = 1
    elif len_ps < 183:
        speed = 1 - (len_ps - 83) / 500
    return speed * 1.1

print("正在加载Kokoro中文管线 (lang_code='z')...")
# 'z' 代表 Mandarin Chinese
pipeline_cn = KPipeline(lang_code='z', repo_id=REPO_ID, model=model, en_callable=en_callable)

# 准备一段中英混合的文本
text = "你好，我是AI喵智能体。今天我们来测试一下Kokoro的Python API，看看它在处理RAG和AI Agent这种专业词汇时，效果怎么样。"
# 我们可以指定一个中文声音，或者让它用默认的
voice = 'ckpts/kokoro/voices/zf_001.pt' # (这是一个示例中文声音，你也可以用 'zm_010')

print(f"准备生成: '{text}'")
start_time = time.time()

# 迭代生成器
generator = pipeline_cn(text, voice=voice, speed=speed_callable)
for i, (gs, ps, audio) in enumerate(generator):
    if i == 0:
        print("TTFA (首包音频延迟): %.2fs" % (time.time() - start_time))
    final_audio = audio

end_time = time.time()
print(f"总耗时: %.2fs" % (end_time - start_time))

# 保存到文件
output_file = 'output_mixed.wav'
sf.write(output_file, final_audio, 24000)
print(f"🎉 成功！中英混合音频已保存到 {output_file}")

# (你可以再加一个纯中文的测试)
pure_chinese_text = "喜欢我们的内容的话，可以关注我们的公众号：AI喵智能体。我们会分享最新的AI技术和应用，欢迎大家关注！"
print(f"准备生成纯中文: '{pure_chinese_text}'")
generator_cn = pipeline_cn(pure_chinese_text, voice=voice, speed=speed_callable)
for i, (gs, ps, audio) in enumerate(generator_cn):
    final_audio_cn = audio
sf.write('output_cn.wav', final_audio_cn, 24000)
print(f"🎉 成功！纯中文音频已保存到 output_cn.wav")