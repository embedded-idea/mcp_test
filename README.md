# my-first-mcp

一个用来练习的最小 [MCP](https://modelcontextprotocol.io) 服务,基于官方 Python SDK(`mcp`),通过 stdio 与客户端通信,可以直接接入 Claude Code。

## 提供的工具

| 工具 | 参数 | 说明 |
|---|---|---|
| `add_numbers` | `a: float`, `b: float` | 计算两个数字的和 |
| `roll_dice` | `sides: int = 6` | 掷一个骰子,返回 1 到 `sides` 之间的随机整数 |

`roll_dice` 在 `sides < 1` 时会返回明确的错误信息:`sides 必须是大于等于 1 的整数`。

## 环境要求

- Python 3.13 或更高
- [uv](https://docs.astral.sh/uv/)

## 安装与运行

```bash
git clone git@github.com:embedded-idea/mcp_test.git
cd mcp_test
uv sync            # 安装依赖
uv run server.py   # 启动服务(stdio 模式,通常由客户端拉起,不需要手动运行)
```

## 接入 Claude Code

把 `/path/to/mcp_test` 换成本项目所在的绝对路径:

```bash
claude mcp add my-first-mcp -- uv run --directory /path/to/mcp_test server.py
```

添加后,在 Claude Code 里输入 `/mcp` 查看连接状态。修改 `server.py` 之后,需要在 `/mcp` 里重新连接该服务,新代码才会生效。

之后可以直接对 Claude 说:

- "用 MCP 工具算一下 4 加 3"
- "帮我掷一个 20 面的骰子"

## 项目结构

```
server.py              MCP 服务入口,定义两个工具
pyproject.toml         项目与依赖配置(依赖 mcp>=2.2.0)
src/practice1/         uv 生成的包骨架,与 MCP 服务无关
```

## 开发笔记

- 工具抛出普通异常(如 `ValueError`)时,MCP 框架会把它视为崩溃,只向客户端返回 `Error executing tool <name>`,详细原因只写入服务端日志。想让客户端看到具体原因,需要抛出 `mcp.server.mcpserver.exceptions.ToolError`。
- 已知限制:`add_numbers` 的结果溢出为无穷大时(例如 `1e308 + 1e308`),JSON 无法表示 `inf`,客户端会收到 `null`。
