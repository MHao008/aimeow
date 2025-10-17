import subprocess
import sys

def execute_python_code(code: str) -> str:
    """
    在本地的Python环境中执行一段Python代码字符串，并返回其标准输出(stdout)和标准错误(stderr)。
    
    警告：极度危险！此工具会在本机上真实地执行代码！
    请确保你完全理解你要求Agent执行的代码。
    
    参数:
    code (str): 要执行的Python代码字符串。例如: "print(1 + 1)" 或 "import os; print(os.getcwd())"
    
    返回:
    str: 包含代码的标准输出(stdout)和标准错误(stderr)的执行结果。
         如果执行超时（15秒）或发生其他异常，将返回错误信息。
    """
    print(f"--- [工具被调用：execute_python_code] ---")
    print(f"--- [工具入参：code={code}] ---")

    try:
        # 使用 subprocess.run 来执行代码
        # sys.executable 指向当前运行的Python解释器
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True, # 捕获标准输出和标准错误
            text=True,           # 以文本模式处理
            timeout=15,          # 设置15秒超时，防止无限循环
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            # 执行成功
            output = f"执行成功:\n--- STDOUT ---\n{result.stdout}\n"
        else:
            # 执行失败
            output = f"执行失败 (Return Code: {result.returncode}):\n--- STDERR ---\n{result.stderr}\n"
            
        print(f"--- [工具返回值 (部分)：{output[:100]}...] ---")
        return output

    except subprocess.TimeoutExpired:
        error_message = "错误：代码执行超时（15秒）。"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message
    except Exception as e:
        error_message = f"错误：执行代码时发生未知异常 - {e}"
        print(f"--- [工具异常：{error_message}] ---")
        return error_message

# --- 本地测试 ---
if __name__ == "__main__":
    # 测试1: 简单的计算
    code1 = "print(123 * 456)"
    print(f"测试1: {code1}\n{execute_python_code(code1)}")
    
    # 测试2: 导入库并打印当前工作目录
    code2 = "import os; print(os.getcwd())"
    print(f"测试2: {code2}\n{execute_python_code(code2)}")
    
    # 测试3: 一个错误的代码
    code3 = "print(1 / 0)"
    print(f"测试3: {code3}\n{execute_python_code(code3)}")