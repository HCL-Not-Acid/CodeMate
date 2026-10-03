import json

from openai import OpenAI

from config import API_KEY, BASE_URL, MODEL_NAME
from tools.code_executor import execute_python_code
from tools.file_reader import read_file


class CodeAgent:
    """CodeMate 的核心 Agent"""

    def __init__(self):
        self.api_key = API_KEY

        self.history = [
            {
                "role": "system",
                "content": """
你是 CodeMate，一个智能代码助手 Agent。

你的主要任务是帮助用户完成编程相关工作，包括：
1. 生成代码
2. 解释代码
3. 分析代码
4. 查找代码中的问题
5. 提供代码优化建议
6. 在必要时使用工具执行代码并验证结果

你需要：
- 优先使用清晰、易懂的方式回答问题
- 用户要求生成代码时，提供完整、可运行的代码
- 用户询问代码问题时，结合上下文回答
- 当用户要求运行、测试或验证 Python 代码时，可以使用代码执行工具
- 不要把自己介绍成通义千问，而要把自己称为 CodeMate
"""
            }
        ]

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=BASE_URL
        )

        # 告诉 Qwen：CodeMate 拥有哪些工具
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_python_code",
                    "description": "执行 Python 代码并返回运行结果。当用户要求运行、测试或验证 Python 代码时使用。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "需要执行的完整 Python 代码"
                            }
                        },
                        "required": ["code"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "读取指定文件的内容。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "文件的路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            }
        ]

    def ask(self, user_input):
        """处理用户问题，并在需要时调用工具"""

        # 1. 把用户问题加入对话历史
        self.history.append({
            "role": "user",
            "content": user_input
        })

        while True:

            # 2. 调用 Qwen，并把可用工具一起告诉它
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.history,
                tools=self.tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # 3. 把 Qwen 的回复加入历史
            self.history.append(assistant_message)

            # 4. 如果 Qwen 没有要求调用工具，直接返回最终答案
            if not assistant_message.tool_calls:
                return assistant_message.content

            # 5. Qwen 要求调用工具
            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name
                tool_arguments = json.loads(
                    tool_call.function.arguments
                )

                print(f"[Agent] 调用工具：{tool_name}")

                # 6. 根据工具名称执行对应的 Python 函数
                if tool_name == "execute_python_code":

                    code = tool_arguments["code"]

                    tool_result = execute_python_code(code)

                    # 把工具执行结果转换成字符串
                    tool_result_text = json.dumps(
                        tool_result,
                        ensure_ascii=False
                    )

                elif tool_name == "read_file":
                    file_path = tool_arguments["file_path"]
                    tool_result = read_file(file_path)
                    tool_result_text = json.dumps(
                        tool_result,
                        ensure_ascii=False
                    )
                else:
                    tool_result_text = "错误：未知工具"

                print("[Tool] 工具执行完成")

                # 7. 把工具结果返回给 Qwen
                self.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result_text
                })

            # 8. while 循环继续
            # Qwen 会读取工具结果并生成最终回答