from tools.code_executor import execute_python_code


code = """
print("Hello, CodeMate!")
print(1 + 2 + 3)
"""

result = execute_python_code(code)

print("执行是否成功：", result["success"])
print("执行结果：")
print(result["output"])