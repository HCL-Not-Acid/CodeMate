import os


def read_file(file_path):
    """
    读取指定文件的内容，并返回结果。
    """

    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {
                "success": False,
                "content": f"文件不存在：{file_path}"
            }

        # 检查是否是文件
        if not os.path.isfile(file_path):
            return {
                "success": False,
                "content": f"目标不是文件：{file_path}"
            }

        # 读取文件
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:
            content = f.read()

        return {
            "success": True,
            "content": content
        }

    except Exception as e:
        return {
            "success": False,
            "content": f"读取文件时出现错误：{e}"
        }