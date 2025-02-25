import sys
import runpy

def main():
    # 设置 Streamlit 命令行参数
    sys.argv = ["streamlit", "run", "app.py"]
    # 运行 Streamlit
    runpy.run_module("streamlit", run_name="__main__")

if __name__ == "__main__":
    main()