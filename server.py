import random
#from mcp.server.fastmcp import FastMCP
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
mcp = MCPServer("my-first-mcp")

# 给你的MCP服务起个名字
#mcp = FastMCP("my-first-mcp")

# 第一个工具:两数相加
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """计算两个数字的和"""
    return a + b

# 第二个工具:掷骰子
@mcp.tool()
def roll_dice(sides: int = 6) -> int:
    """掷一个骰子,返回1到sides之间的随机数,默认6面骰"""
    if sides < 1:
        raise ToolError("sides 必须是大于等于 1 的整数")
    return random.randint(1, sides)

# 启动服务
if __name__ == "__main__":
    mcp.run()
