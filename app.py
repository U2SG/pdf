import sys
import os
from streamlit_float import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from app.upload import render_file_uploader
from app.pdf import render_pdf_viewer
from app.chat import render_chat_interface, render_chat2_interface
from app.download import render_download_interface


def main():
    st.set_page_config(
        page_title="PDF",
        layout="wide",
        initial_sidebar_state="collapsed"  # 默认折叠左侧边栏
    )
    
    st.title("PDF")
    
    # 只使用两列，并调整比例，PDF区域窄一点，对话区域宽一点
    pdf_col, chat_col, down_col = st.columns([2, 1.5, 0.38])
    
    # 使用 sidebar 来放置文件上传组件
    with st.sidebar:
        render_file_uploader()
        # print(f'file_path: {file_path}')    
    
    file_path = st.session_state.file_path
    with pdf_col:
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "rb") as pdf_file:
                    render_pdf_viewer(pdf_file)
            except Exception as e:
                st.error(f"文件打开失败: {str(e)}")
    
    with chat_col:
        st.title("对话")
        # render_chat_interface()
        if file_path:
            render_chat_interface()
        else:
            st.info("请先上传PDF文件")
            render_chat2_interface()
    
    with down_col:
        render_download_interface()
        

if __name__ == "__main__":
    main()