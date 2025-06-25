# mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool(name="add", description="计算两个整数的和")
def add(a: int, b: int) -> dict:
    return {"result": f"{a} + {b} = {a + b}"}

@mcp.tool(name="sub", description="计算两个整数的差")
def sub(a: int, b: int) -> dict:
    return {"result": f"{a} - {b} = {a - b}"}

if __name__ == "__main__":
    mcp.run(transport="stdio")  # 使用 stdio 方法运行服务
