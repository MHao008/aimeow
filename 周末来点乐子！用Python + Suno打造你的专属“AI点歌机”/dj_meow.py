import requests
import time
import json

# 我们本地服务的地址
BASE_URL = "http://localhost:3000"

def create_song(prompt):
    """发送生成歌曲的指令"""
    url = f"{BASE_URL}/api/generate"
    payload = {
        "prompt": prompt,
        "make_instrumental": False,
        "wait_audio": False # 不等待音频完成，先拿任务ID
    }
    print("🎵 喵喵DJ正在发送制 任务...")
    resp = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return resp.json()

def get_song_info(song_ids):
    """查询歌曲状态"""
    url = f"{BASE_URL}/api/get?ids={song_ids}"
    resp = requests.get(url)
    return resp.json()

# === 主程序 ===
# 1. 定义你的神曲
my_prompt = "一首充满活力的中文流行歌曲，主题是周五下班后的自由和快乐，节奏轻快，带有电子乐元素。"

# 2. 开始生成
try:
    tasks = create_song(my_prompt)
    # Suno 一次生成两首，我们拿到它们的 ID
    song_ids = f"{tasks[0]['id']},{tasks[1]['id']}"
    print(f"🚀 任务已提交! ID: {song_ids}")

    # 3. 轮询等待完成
    print("⏳ 正在生成中 (可能需要几分钟，请耐心等待)...")
    while True:
        songs = get_song_info(song_ids)
        if songs[0]["status"] == 'streaming':
            print(f"{songs[0]['id']} ==> {songs[0]['audio_url']}")
            print(f"{songs[1]['id']} ==> {songs[1]['audio_url']}")
            break
        
        time.sleep(10) # 每10秒检查一次

    # 4. 展示结果
    print("\n✨ 生成完成！快去听听吧：")

except Exception as e:
    print(f"💥 发生错误: {e}")
    print("请检查你的本地服务是否正常运行 (http://localhost:3000)")