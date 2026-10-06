# CodeMate —— 智能代码助手 Agent

CodeMate 是一个基于大语言模型的智能代码助手 Agent，使用 Python 开发，基于阿里云 Model Studio 提供的 Qwen 模型实现。

CodeMate 通过命令行与用户交互，可以完成代码生成、代码解释、代码分析，并在需要时调用工具执行 Python 代码或读取项目文件。

## 功能

- **代码生成**：根据用户需求生成代码
- **代码解释**：解释代码和编程概念
- **代码分析**：分析代码问题并提供修改建议
- **Python 代码执行**：调用 `execute_python_code` 工具运行和验证 Python 代码
- **文件读取**：调用 `read_file` 工具读取并分析项目文件
- **上下文记忆**：在一次程序运行期间保留对话历史
- **错误处理**：处理模型调用、代码执行和文件读取过程中的常见错误

## 技术栈

- Python
- Qwen 大语言模型
- 阿里云 Model Studio
- OpenAI 兼容 API
- OpenAI Python SDK
- python-dotenv
- CLI

## 项目结构

```text
CodeMate/
├── README.md
├── DESIGN.md
├── agent.py
├── config.py
├── main.py
├── requirements.txt
├── test_tool.py
├── test_file_reader.py
└── tools/
    ├── __init__.py
    ├── code_executor.py
    └── file_reader.py
```

主要文件：

| 文件 | 作用 |
|---|---|
| `main.py` | 程序入口，负责命令行交互 |
| `agent.py` | CodeMate 核心 Agent，实现模型调用、上下文管理和 Tool Calling |
| `config.py` | 读取 API 和模型配置 |
| `tools/code_executor.py` | Python 代码执行工具 |
| `tools/file_reader.py` | 项目文件读取工具 |
| `test_tool.py` | 测试代码执行工具 |
| `test_file_reader.py` | 测试文件读取工具 |
| `requirements.txt` | 项目依赖 |
| `DESIGN.md` | 项目详细设计文档 |

## 快速开始

### 1. 创建虚拟环境

```bash
python -m venv .venv
```

### 2. 激活虚拟环境

Windows：

```bash
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

在项目根目录创建 `.env` 文件：

```text
DASHSCOPE_API_KEY=你的API_KEY
```

API Key 不要直接写入源代码，也不要提交到 GitHub。

### 5. 运行

```bash
python main.py
```

输入：

```text
exit
```

即可退出程序。

## 使用示例

### 代码生成

```text
请用 C 语言写一个程序，输入 5 个整数，计算它们的平均值。
```

### Python 代码执行

```text
请计算 1 到 1000 中所有偶数的和，并运行代码验证结果。
```

Agent 会根据任务需要调用：

```text
execute_python_code
```

并返回实际运行结果。

### 文件读取

```text
请读取 main.py 文件，并告诉我这个文件的主要功能是什么。
```

Agent 会根据任务需要调用：

```text
read_file
```

读取文件后再生成回答。

## Agent 工作流程

```text
用户输入
   ↓
CodeMate Agent
   ↓
Qwen 大语言模型
   ↓
判断是否需要工具
   ↓
┌───────────────┬
│ 不需要工具     │ 需要工具       
↓               ↓
直接回答       调用工具
                ↓
        获取工具执行结果
                ↓
        返回给大语言模型
                ↓
             最终回答
```

## 项目文档

项目的详细设计、Agent Loop、Tool Calling、工具设计、上下文记忆、错误处理以及安全限制等内容，请参考：

**[DESIGN.md](DESIGN.md)**

## 注意事项

- `.env` 包含 API Key，不应提交到 GitHub。
- `.venv/` 和 `__pycache__/` 不属于项目源代码。
- Python 代码执行工具设置了 5 秒超时，但目前不是完整的安全沙箱，仅用于课程项目和受控测试环境。
- 当前上下文记忆只在程序运行期间有效，重启程序后不会保留。

## 项目说明

CodeMate 是《软件工程与项目实践》课程中的 Agent 实践项目，用于学习和实践大语言模型调用、Prompt 设计、Agent Loop、Tool Calling 和工具集成等基本技术。