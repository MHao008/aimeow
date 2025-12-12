import torch
import torchaudio
import soundfile as sf
from pathlib import Path
from transformers import AutoTokenizer, WhisperFeatureExtractor, AutoConfig, AutoModelForCausalLM

# -----------------------------
# 固定配置
# -----------------------------
WHISPER_FEAT_CFG = {
    "chunk_length": 30,
    "feature_extractor_type": "WhisperFeatureExtractor",
    "feature_size": 128,
    "hop_length": 160,
    "n_fft": 400,
    "n_samples": 480000,
    "nb_max_frames": 3000,
    "padding_side": "right",
    "padding_value": 0.0,
    "processor_class": "WhisperProcessor",
    "return_attention_mask": False,
    "sampling_rate": 16000,
}

def load_audio(path, target_sr=16000):
    wav, sr = sf.read(path)
    if wav.ndim > 1:  # 多声道取第一声道
        wav = wav[:, 0]
    wav = torch.tensor(wav, dtype=torch.float32).unsqueeze(0)
    if sr != target_sr:
        wav = torchaudio.transforms.Resample(sr, target_sr)(wav)
        sr = target_sr
    return wav, sr

def get_audio_token_length(seconds, merge_factor=2):
    # 计算音频token长度
    def get_T_after_cnn(L_in, dilation=1):
        for padding, kernel_size, stride in eval("[(1,3,1)] + [(1,3,2)] "):
            L_out = L_in + 2 * padding - dilation * (kernel_size - 1) - 1
            L_out = 1 + L_out // stride
            L_in = L_out
        return L_out

    mel_len = int(seconds * 100)
    audio_len_after_cnn = get_T_after_cnn(mel_len)
    audio_token_num = (audio_len_after_cnn - merge_factor) // merge_factor + 1
    return min(audio_token_num, 1500 // merge_factor)


def build_prompt(audio_path, tokenizer, feature_extractor, merge_factor):
    # wav, sr = load_audio(str(audio_path))
    wav, sr = torchaudio.load(str(audio_path))
    wav = wav[:1, :]
    if sr != feature_extractor.sampling_rate:
        wav = torchaudio.transforms.Resample(sr, feature_extractor.sampling_rate)(wav)

    tokens = []
    tokens += tokenizer.encode("<|user|>\n")

    audios, audio_offsets, audio_length = [], [], []
    chunk_size = 30 * feature_extractor.sampling_rate
    
    # 分块处理音频
    for start in range(0, wav.shape[1], chunk_size):
        chunk = wav[:, start:start + chunk_size]
        mel = feature_extractor(
            chunk.numpy(),
            sampling_rate=feature_extractor.sampling_rate,
            return_tensors="pt",
            padding="max_length",
        )["input_features"]

        audios.append(mel)

        seconds = chunk.shape[1] / feature_extractor.sampling_rate
        num_tokens = get_audio_token_length(seconds, merge_factor)

        tokens += tokenizer.encode("<|begin_of_audio|>")
        audio_offsets.append(len(tokens))
        tokens += [0] * num_tokens
        tokens += tokenizer.encode("<|end_of_audio|>")
        audio_length.append(num_tokens)

    tokens += tokenizer.encode("<|user|>\nPlease transcribe this audio into text")
    tokens += tokenizer.encode("<|assistant|>\n")

    return {
        "input_ids": torch.tensor([tokens]),
        "audios": torch.cat(audios, dim=0),
        "audio_offsets": [audio_offsets],
        "audio_length": [audio_length],
        "attention_mask": torch.ones(1, len(tokens)),
    }


def run_asr(model_dir, audio_path):
    print("🎤 开始识别音频：", audio_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    feature_extractor = WhisperFeatureExtractor(**WHISPER_FEAT_CFG)

    config = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, config=config, trust_remote_code=True, torch_dtype=torch.bfloat16
    ).to(device)
    model.eval()

    batch = build_prompt(audio_path, tokenizer, feature_extractor, config.merge_factor)

    model_inputs = {
        "inputs": batch["input_ids"].to(device),
        "attention_mask": batch["attention_mask"].to(device),
        "audios": batch["audios"].to(device, dtype=torch.bfloat16),
        "audio_offsets": batch["audio_offsets"],
        "audio_length": batch["audio_length"],
    }

    prompt_len = batch["input_ids"].shape[1]

    with torch.inference_mode():
        generated = model.generate(
            **model_inputs,
            max_new_tokens=128,
            do_sample=False,
        )

    transcript_ids = generated[0, prompt_len:].cpu().tolist()
    result = tokenizer.decode(transcript_ids, skip_special_tokens=True)
    print("\n-------- 📝 识别结果 --------")
    print(result)
    print("-----------------------------\n")
    return result


if __name__ == "__main__":
    # 请确保模型路径正确！
    model_path = "./zai-org/GLM-ASR-Nano-2512"
    
    # run_asr(model_path, "./audio/example_en.wav")
    # run_asr(model_path, "./audio/example_zh.mp3")
    
    # 🔥 重点测试：粤语识别
    run_asr(model_path, "./audio/example_yy.mp3")
