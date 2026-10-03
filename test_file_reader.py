from tools.file_reader import read_file


result = read_file("main.py")

print("读取是否成功：", result["success"])
print("文件内容：")
print(result["content"])