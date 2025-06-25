# tools_utils.py
import json
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from pathlib import Path

# 状态结构
class GraphState(dict):
    users: List[Dict[str, Any]]
    ages: List[int]
    ages_file: str
    histogram_file: str

# 工具函数
def read_user_list(state: GraphState) -> GraphState:
    path = state.get("input_path", "users.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    users = data.get("users", [])
    print("✅ 已读取用户列表：", users)
    return { "users": users}

def extract_ages(state: GraphState) -> GraphState:
    users = state.get("users", [])
    print("✅ extract_ages已读取用户列表：", users)
    ages = [user["age"] for user in users]
    print("✅ 已提取年龄：", ages)
    return {"ages": ages}

def write_ages(state: GraphState) -> GraphState:
    ages = state.get("ages", [])
    out_path = state.get("ages_output_path", "ages.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ages, f, ensure_ascii=False, indent=2)
    print(f"✅ 年龄列表已保存到：{out_path}")
    return {"ages_file": out_path}

def plot_ages(state: GraphState) -> GraphState:
    ages = state.get("ages", [])
    if not ages:
        raise ValueError("没有可用的年龄数据")
    plt.figure()
    plt.hist(ages, bins=10, color="skyblue", edgecolor="black")
    plt.title("age histogram") # 设置标题  
    filename = "histogram.png"
    plt.savefig(filename)
    plt.close()
    print(f"✅ 已生成直方图图片：{filename}")
    return {"histogram_file": filename}