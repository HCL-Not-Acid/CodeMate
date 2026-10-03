# CodeMate —— 智能代码助手 Agent

## 1. 项目简介

CodeMate 是一个基于大语言模型的智能代码助手 Agent，主要用于帮助用户完成编程相关任务。

本项目使用 Python 开发，通过调用阿里云 Model Studio 提供的 Qwen 大语言模型，实现代码生成、代码解释、代码分析和代码问题排查等功能。

同时，CodeMate 集成了两个工具：

1. Python 代码执行工具
2. 项目文件读取工具

当用户需要运行、测试或验证 Python 代码时，Agent 可以根据用户需求调用代码执行工具，并将工具返回的结果交给大语言模型进行进一步分析。

当用户需要查看、分析或检查项目中的文件时，Agent 可以自动调用文件读取工具，获取文件内容后交给大语言模型进行分析。

项目采用命令行（CLI）作为交互界面。

---

## 2. 项目功能

### 2.1 代码生成

用户可以向 CodeMate 描述编程需求，由大语言模型生成相应代码。

例如：

```text
请用 C 语言写一个程序，输入 5 个整数，计算它们的平均值。
```

CodeMate 可以根据需求生成完整的代码，并对代码进行简单解释。

### 2.2 代码解释

用户可以输入代码或询问编程概念，CodeMate 可以对代码和相关知识进行解释。

例如：

```text
什么是 C 语言的指针？
```

对于这类不需要外部工具的问题，CodeMate 可以直接调用大语言模型生成回答。

### 2.3 代码分析

CodeMate 可以根据用户提供的代码分析其中可能存在的问题，并给出修改建议。

如果分析过程中需要实际运行 Python 代码进行验证，Agent 可以自动调用代码执行工具。

### 2.4 Python 代码执行

CodeMate 集成了 Python 代码执行工具 `execute_python_code`。

当用户要求运行、测试或验证 Python 代码时，Agent 可以调用工具执行代码，并获取实际运行结果。

例如：

```text
请计算 1 到 1000 中所有偶数的和，并运行代码验证结果。
```

Agent 可以自动调用：

```text
execute_python_code
```

并根据工具返回的结果生成最终回答。

### 2.5 项目文件读取

CodeMate 集成了文件读取工具 `read_file`。

当用户要求查看、分析或检查某个项目文件时，Agent 可以自动调用该工具读取文件内容。

例如：

```text
请读取 main.py 文件，并告诉我这个文件的主要功能是什么。
```

Agent 会自动调用：

```text
read_file
```

读取 `main.py`，然后根据文件内容进行分析。

### 2.6 错误分析

如果代码运行过程中出现错误，CodeMate 可以读取工具返回的错误信息，并结合代码进行分析。

例如：

```python
numbers = [1, 2, 3, 4, 5]
print(numbers[5])
```

运行后会产生：

```text
IndexError: list index out of range
```

CodeMate 可以进一步解释该错误产生的原因，并给出修改建议。

### 2.7 上下文记忆

CodeMate 在一次程序运行过程中保存对话历史，因此可以结合前面的对话内容回答后续问题。

例如：

```text
用户：请计算 1 到 100 的和，并运行验证。

CodeMate：1 到 100 的和是 5050。

用户：你还记得前面让你计算的东西吗？

CodeMate：记得，前面计算的是 1 到 100 的和，结果是 5050。
```

这种上下文记忆可以让 Agent 在多轮对话中理解之前的信息。

需要注意的是，目前的上下文记忆保存在程序运行期间的内存中。

重新启动程序后，之前的对话历史不会保留。

---

## 3. 技术栈

- Python
- Qwen 大语言模型
- 阿里云 Model Studio
- OpenAI 兼容 API
- OpenAI Python SDK
- Python-dotenv
- Python subprocess
- 命令行 CLI

---

## 4. 项目结构

```text
CodeMate/
│
├── .env
├── .gitignore
├── README.md
├── DESIGN.md
├── agent.py
├── config.py
├── main.py
├── requirements.txt
├── test_tool.py
├── test_file_reader.py
│
└── tools/
    ├── __init__.py
    ├── code_executor.py
    └── file_reader.py
```

### 文件说明

| 文件 | 作用 |
|---|---|
| `main.py` | 程序入口，负责命令行交互 |
| `agent.py` | CodeMate 核心 Agent，实现模型调用、上下文管理和 Tool Calling |
| `config.py` | 读取 API Key 和模型配置 |
| `tools/__init__.py` | Python 工具包初始化文件，目前为空 |
| `tools/code_executor.py` | Python 代码执行工具 |
| `tools/file_reader.py` | 项目文件读取工具 |
| `test_tool.py` | 测试 Python 代码执行工具 |
| `test_file_reader.py` | 测试文件读取工具 |
| `requirements.txt` | 项目依赖 |
| `.env` | 保存 API Key 等敏感配置 |
| `.gitignore` | 防止敏感文件、虚拟环境和缓存文件被提交 |
| `README.md` | 项目说明文档 |
| `DESIGN.md` | Agent 架构和详细设计文档 |

> 注意：`.venv/` 和 `__pycache__/` 是 Python 虚拟环境及运行过程中产生的缓存目录，由于已经写入 `.gitignore`，因此不作为项目源代码提交。
>
> `.env` 中包含 API Key 等敏感信息，也不应提交到 GitHub 或 Gitee。

---

## 5. Agent 架构

CodeMate 的整体工作流程如下：

```text
用户输入
   ↓
CLI 命令行界面
   ↓
CodeMate Agent
   ↓
Qwen 大语言模型
   ↓
判断是否需要使用工具
   ↓
┌──────────────────────────────┐
│                              │
│ 不需要工具                   │ 需要工具
│                              │
↓                              ↓
直接生成回答             自动选择合适的工具
                               ↓
                    ┌──────────┴──────────┐
                    ↓                     ↓
          execute_python_code          read_file
                    ↓                     ↓
               执行 Python              读取文件
                    ↓                     ↓
                    └──────────┬──────────┘
                               ↓
                         获取工具结果
                               ↓
                         返回给 Agent
                               ↓
                      Qwen 分析工具结果
                               ↓
                         最终回答用户
```

CodeMate 的 Agent 并不是每次都调用工具。

如果用户只是询问编程知识，Agent 可以直接调用大语言模型回答。

如果用户要求执行代码或读取文件，Agent 可以根据任务需要自动选择对应工具。

---

## 6. Agent Loop

CodeMate 的核心 Agent Loop 为：

```text
用户输入
   ↓
LLM 判断用户需求
   ↓
判断是否需要调用工具
   ↓
Tool Calling
   ↓
工具执行
   ↓
获得工具结果
   ↓
将工具结果返回给 LLM
   ↓
LLM 根据工具结果继续处理
   ↓
生成最终回答
```

### 6.1 Python 代码执行示例

例如用户输入：

```text
请计算 1 到 100 的和，并使用 Python 代码运行验证结果。
```

CodeMate 的处理过程为：

```text
用户请求
   ↓
Qwen 判断需要执行 Python
   ↓
调用 execute_python_code
   ↓
Python 实际执行代码
   ↓
得到结果 5050
   ↓
结果返回 Qwen
   ↓
CodeMate 分析结果
   ↓
告诉用户计算结果
```

### 6.2 文件读取示例

例如用户输入：

```text
请读取 main.py 文件，并告诉我这个文件的主要功能是什么。
```

CodeMate 的处理过程为：

```text
用户请求
   ↓
Qwen 判断需要读取文件
   ↓
调用 read_file
   ↓
读取 main.py
   ↓
得到文件内容
   ↓
文件内容返回 Qwen
   ↓
Qwen 分析代码
   ↓
CodeMate 告诉用户文件主要功能
```

---

## 7. 工具设计

CodeMate 当前集成了两个工具：

### 7.1 execute_python_code

Python 代码执行工具。

功能：

> 执行 Python 代码并返回运行结果。

工具定义中向大语言模型描述了工具的名称、功能和参数。

工具接收到代码后：

1. 创建临时 Python 文件
2. 将代码写入临时文件
3. 使用当前 Python 解释器执行
4. 获取标准输出或错误信息
5. 将执行结果返回给 Agent
6. 删除临时文件

代码执行设置了 5 秒超时时间，用于避免代码长时间运行。

---

### 7.2 read_file

项目文件读取工具。

功能：

> 读取项目中的指定文件，并将文件内容返回给 Agent。

工具接收到文件路径后：

1. 检查文件是否存在
2. 检查目标是否为文件
3. 使用 UTF-8 编码打开文件
4. 读取文件内容
5. 将文件内容返回给 Agent
6. 如果读取过程中出现异常，则返回错误信息

例如：

```text
用户：
请读取 main.py 文件，并告诉我这个文件的主要功能是什么。

Agent：
调用 read_file

Tool：
读取 main.py

Agent：
根据读取到的代码分析文件功能

CodeMate：
向用户返回分析结果
```

---

### 7.3 Tool Calling

CodeMate 使用大语言模型提供的 Tool Calling 能力，让模型根据用户需求自动选择工具。

目前支持：

```text
execute_python_code
        ↓
执行 Python 代码
```

以及：

```text
read_file
        ↓
读取项目文件
```

整体流程为：

```text
用户输入
   ↓
CodeMate Agent
   ↓
LLM 判断是否需要工具
   ↓
┌───────────────────────┐
│                       │
↓                       ↓
execute_python_code   read_file
│                       │
↓                       ↓
执行 Python            读取文件
│                       │
└───────────┬───────────┘
            ↓
        工具执行结果
            ↓
          Agent
            ↓
        最终回答用户
```

---

## 8. 上下文记忆

CodeMate 使用对话历史保存当前程序运行过程中的上下文。

例如：

```text
用户：请计算 1 到 100 的和，并运行验证。

CodeMate：1 到 100 的和是 5050。

用户：你还记得前面让你计算的东西吗？

CodeMate：记得，前面计算的是 1 到 100 的和，结果是 5050。
```

这种上下文记忆可以让 Agent 在多轮对话中理解之前的信息。

目前的上下文记忆通过 `agent.py` 中的 `self.history` 实现，保存在程序运行期间的内存中。

重新启动程序后，之前的对话历史不会保留。

---

## 9. 错误处理

CodeMate 对模型调用、Python 代码执行和文件读取过程中的错误进行了基本处理。

### 9.1 模型调用错误

如果调用大语言模型过程中出现异常，程序会捕获异常并向用户提示错误信息。

### 9.2 Python 代码执行错误

如果 Python 代码运行失败，代码执行工具会返回错误信息。

例如：

```python
numbers = [1, 2, 3, 4, 5]
print(numbers[5])
```

工具会返回：

```text
IndexError: list index out of range
```

Agent 获取错误信息后，可以进一步分析错误原因，并向用户提供修改建议。

### 9.3 文件读取错误

如果用户要求读取不存在的文件，`read_file` 工具会返回文件不存在的错误信息。

例如：

```text
文件不存在：example.py
```

如果目标路径不是文件，也会返回相应提示。

### 9.4 执行超时

代码执行工具设置了 5 秒超时限制。

如果代码执行时间超过限制，则返回：

```text
代码执行超时，超过 5 秒。
```

---

## 10. 安装与运行

### 10.1 创建虚拟环境

```bash
python -m venv .venv
```

### 10.2 激活虚拟环境

Windows：

```bash
.venv\Scripts\activate
```

### 10.3 安装依赖

```bash
pip install -r requirements.txt
```

### 10.4 配置 API Key

在项目根目录创建 `.env` 文件：

```text
DASHSCOPE_API_KEY=你的API_KEY
```

API Key 不应直接写入 Python 源代码，也不应提交到 GitHub 或 Gitee。

### 10.5 启动程序

```bash
python main.py
```

启动后即可通过命令行与 CodeMate 进行对话。

输入：

```text
exit
```

即可退出程序。

---

## 11. 测试示例

### 11.1 测试普通编程问题

输入：

```text
什么是 C 语言的指针？
```

CodeMate 可以直接回答相关问题，不需要调用工具。

---

### 11.2 测试代码运行

输入：

```text
请计算 1 到 100 的和，并使用 Python 代码运行验证结果。
```

Agent 会调用：

```text
execute_python_code
```

并根据工具返回结果生成最终回答。

预期结果：

```text
1 到 100 的和是 5050。
```

---

### 11.3 测试代码错误分析

输入：

```text
请检查并运行下面这段 Python 代码，如果有错误，请告诉我错误原因并给出修改后的正确代码：

numbers = [1, 2, 3, 4, 5]
print(numbers[5])
```

Agent 会调用：

```text
execute_python_code
```

工具执行后会返回索引越界错误。

CodeMate 会根据错误信息分析：

```text
IndexError: list index out of range
```

并进一步解释：

- Python 列表索引从 0 开始
- `numbers` 中共有 5 个元素
- 合法索引范围是 `0` 到 `4`
- `numbers[5]` 访问了不存在的第 6 个元素

随后 CodeMate 可以给出相应的修改建议。

---

### 11.4 测试文件读取

输入：

```text
请读取 main.py 文件，并告诉我这个文件的主要功能是什么。
```

Agent 会调用：

```text
read_file
```

读取 `main.py` 的内容。

然后 CodeMate 会根据读取到的代码分析：

- `main.py` 是程序入口
- 创建 `CodeAgent`
- 提供命令行交互
- 接收用户输入
- 调用 `agent.ask()` 获取回答
- 支持输入 `exit` 退出程序
- 对异常进行基础处理

---

### 11.5 测试文件读取工具

可以单独运行：

```bash
python test_file_reader.py
```

测试文件读取工具。

预期结果类似：

```text
读取是否成功： True
文件内容：
...
```

---

### 11.6 测试代码执行工具

可以单独运行：

```bash
python test_tool.py
```

测试 Python 代码执行工具。

预期结果类似：

```text
执行是否成功： True
执行结果：
Hello, CodeMate!
6
```

---

## 12. 项目特点

本项目通过一个简单的代码助手场景，实现了 Agent 开发中的几个基本组成部分：

- 大语言模型调用
- Prompt 设计
- Agent Loop
- Tool Calling
- Python 工具执行
- 文件读取工具
- 工具结果反馈
- 多轮上下文记忆
- 基本错误处理

项目采用模块化结构，将 Agent 核心逻辑和工具功能分离。

目前工具模块包括：

```text
tools/
├── code_executor.py
└── file_reader.py
```

这种结构便于后续继续增加其他工具。

---

## 13. Agent 核心流程说明

CodeMate 的核心逻辑位于 `agent.py` 中。

程序首先将用户输入加入对话历史，然后调用 Qwen 大语言模型。

模型可以根据用户需求选择不同的处理方式。

### 13.1 情况一：不需要工具

如果用户只是询问编程知识，例如：

```text
什么是 C 语言的指针？
```

Agent 会直接将问题交给大语言模型，由模型生成回答。

处理流程：

```text
用户问题
   ↓
Qwen
   ↓
生成回答
   ↓
返回用户
```

---

### 13.2 情况二：需要执行 Python

如果用户要求实际运行 Python 代码，例如：

```text
请运行下面的代码：

print(1 + 2 + 3)
```

模型会请求调用：

```text
execute_python_code
```

Agent 程序收到工具调用请求后，执行对应的 Python 函数。

然后将工具执行结果重新加入对话历史，再次调用模型。

处理流程：

```text
用户问题
   ↓
Qwen
   ↓
请求调用 execute_python_code
   ↓
Agent 执行 Python
   ↓
获得执行结果
   ↓
结果返回 Qwen
   ↓
Qwen 分析结果
   ↓
最终回答
```

---

### 13.3 情况三：需要读取文件

如果用户要求查看项目中的文件，例如：

```text
请读取 main.py，并分析它的主要功能。
```

模型会请求调用：

```text
read_file
```

Agent 程序收到工具调用请求后，执行文件读取函数。

然后将文件内容加入对话流程，再次调用模型。

处理流程：

```text
用户问题
   ↓
Qwen
   ↓
请求调用 read_file
   ↓
Agent 读取文件
   ↓
获得文件内容
   ↓
文件内容返回 Qwen
   ↓
Qwen 分析代码
   ↓
最终回答
```

这构成了 CodeMate 的基本 Agent Loop。

---

## 14. 安全与限制

目前 CodeMate 的工具主要用于课程作业中的功能演示和学习。

### 14.1 Python 代码执行限制

代码执行工具设置了 5 秒超时限制，并会在执行完成后删除临时 Python 文件。

但是，目前的执行环境并不是完全隔离的安全沙箱，因此不应该将不可信的恶意代码直接交给该工具执行。

后续如果继续完善项目，可以考虑增加更加严格的代码执行隔离机制。

### 14.2 文件读取限制

目前 `read_file` 主要用于课程项目中的文件读取和代码分析。

它可以检查文件是否存在以及目标是否为文件，但目前没有实现完整的权限控制和路径沙箱机制。

因此不应将其视为一个完整的安全文件访问系统。

---

## 15. 后续扩展

后续可以进一步增加：

- 代码搜索工具
- 更多编程语言的代码执行
- 自动生成测试代码
- 代码重构建议
- 更完善的错误重试机制
- Web 图形界面
- 更完善的代码执行安全隔离
- 更完善的文件访问权限控制

---

## 16. 总结

CodeMate 是一个面向软件工程课程实践的简单代码助手 Agent。

项目以 Qwen 大语言模型为核心，通过 Agent Loop 将大语言模型与 Python 代码执行工具、文件读取工具连接起来，使模型不仅能够生成和解释代码，还能够根据用户需求调用外部工具执行代码或读取项目文件，并根据工具返回的真实结果进行进一步分析。

通过本项目可以学习和实践：

1. 大语言模型 API 调用
2. Prompt 设计
3. Agent 基本架构
4. Tool Calling
5. Agent Loop
6. 工具执行与结果反馈
7. 文件读取工具
8. 上下文记忆
9. 基本错误处理
10. Python 项目模块化组织