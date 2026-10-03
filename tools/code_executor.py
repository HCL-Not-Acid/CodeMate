import subprocess
import sys
import tempfile
import os


def execute_python_code(code):
    """
    执行 Python 代码，并返回运行结果。
    """

    temp_file = None

    try:
        # 创建临时 Python 文件
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name

        # 执行 Python 文件
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        # 返回执行结果
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout
            }

        return {
            "success": False,
            "output": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "代码执行超时，超过 5 秒。"
        }

    except Exception as e:
        return {
            "success": False,
            "output": f"代码执行出现错误：{e}"
        }

    finally:
        # 删除临时文件
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)