from agent import CodeAgent


def main():
    print("=" * 40)
    print("        CodeMate")
    print("   Intelligent Code Assistant")
    print("=" * 40)
    print("输入 exit 可以退出程序")
    print()

    agent = CodeAgent()

    while True:
        user_input = input("你：")

        if user_input.lower() == "exit":
            print("CodeMate：再见！")
            break

        if not user_input.strip():
            continue

        try:
            answer = agent.ask(user_input)
            print(f"CodeMate：{answer}")
            print()

        except Exception as e:
            print(f"CodeMate：调用模型时出现错误：{e}")
            print()


if __name__ == "__main__":
    main()