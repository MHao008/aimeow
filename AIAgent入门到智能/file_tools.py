# -----------------------------------------------------
# 喵喵实战室：Agent本地文件工具
# -----------------------------------------------------
from pathlib import Path

def read_file(file_path: str) -> str:
    """
    读取指定路径的文本文件内容。
    
    参数:
    file_path (str): 要读取的文件的完整路径。例如: 'D:/docs/report.txt' 或 'logs/today.log'。
    
    返回:
    str: 文件的文本内容。
         如果文件不存在或读取失败，则返回详细的错误信息。
    """
    print(f"--- [工具被调用：read_file] ---")
    print(f"--- [工具入参：file_path={file_path}] ---")
    
    try:
        # 使用Pathlib确保路径处理的健壮性
        p = Path(file_path)
        
        if not p.exists():
            print(f"--- [工具错误：文件不存在 {file_path}] ---")
            return f"错误：文件路径 '{file_path}' 不存在。"
            
        if not p.is_file():
            print(f"--- [工具错误：路径不是文件 {file_path}] ---")
            return f"错误：路径 '{file_path}' 不是一个文件。"

        # 读取文件内容
        with p.open('r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"--- [工具返回值：成功读取 {len(content)} 字符] ---")
        return content
        
    except Exception as e:
        error_message = f"错误：读取文件 '{file_path}' 时发生异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message



def write_file(file_path: str, content: str) -> str:
    """
    将指定的文本内容写入到指定路径的文件中。
    如果文件已存在，它将被覆盖。如果目录不存在，将尝试创建它。
    
    参数:
    file_path (str): 要写入的文件的完整路径。例如: 'output/result.txt'
    content (str): 要写入文件的文本内容。
    
    返回:
    str: 一个表示操作成功的确认信息。
         如果写入失败，则返回详细的错误信息。
    """
    print(f"--- [工具被调用：write_file] ---")
    print(f"--- [工具入参：file_path={file_path}, content_len={len(content)}] ---")
    
    try:
        # 使用Pathlib创建父目录（如果不存在）
        p = Path(file_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件内容，使用utf-8编码
        with p.open('w', encoding='utf-8') as f:
            f.write(content)
            
        success_message = f"成功：内容已写入文件 '{file_path}'。"
        print(f"--- [工具返回值：{success_message}] ---")
        return success_message
        
    except Exception as e:
        error_message = f"错误：写入文件 '{file_path}' 时发生异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message

# --- 本地测试 ---
if __name__ == "__main__":
    # 测试写入
    write_result = write_file("test_output/hello.txt", "你好，Agent！这是你创建的文件。")
    print(write_result)
    
    # 测试读取
    read_result = read_file("test_output/hello.txt")
    print(read_result)
    
    # 测试读取不存在的文件
    read_fail_result = read_file("non_existent_file.txt")
    print(read_fail_result)