import os
import json
import streamlit as st
from streamlit_float import *
from pathlib import Path
from PyPDF2 import PdfMerger
import tempfile
from services.client_init import client
from config import UPLOAD_DIR, RESOURCES_DIR


def join_json(file_path, data_now):
    """
    将新的 JSON 数据追加到文件中
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        data.append(data_now)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"JSON 文件操作失败: {str(e)}")


def upload_file(client, file_path):
    """
    将文件上传到 DashScope，返回文件 ID
    """
    try:
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")
        return file_object.id
    except Exception as e:
        st.error(f"文件上传到 DashScope 失败: {str(e)}")
        return None


def save_uploaded_file(uploaded_file, temp_dir):
    """
    保存单个上传的文件到临时目录，返回文件路径和文件名
    """
    try:
        file_path = Path(temp_dir) / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # st.success(f"文件 {uploaded_file.name} 已保存到 {file_path}")
        return file_path, uploaded_file.name
    except Exception as e:
        st.error(f"文件保存失败: {str(e)}")
        return None, None


def merge_uploaded_files(uploaded_files, temp_dir):
    """
    合并多个上传的 PDF 文件，返回合并后的文件路径和文件名
    """
    try:
        merger = PdfMerger()
        merged_pdf_path = Path(temp_dir) / "merged.pdf"

        # 临时文件列表，用于后续清理
        temp_files = []

        for uploaded_file in uploaded_files:
            # 创建临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(uploaded_file.getbuffer())
            temp_file.close()
            temp_files.append(temp_file.name)

            # 将临时文件添加到合并器
            merger.append(temp_file.name)

        # 将合并后的 PDF 保存到临时目录
        with open(merged_pdf_path, "wb") as f:
            merger.write(f)
        
        # 关闭合并器
        merger.close()

        # st.success(f"文件已合并并保存到 {merged_pdf_path}")

        # 清理临时文件
        for temp_file in temp_files:
            os.remove(temp_file)

        return merged_pdf_path, "merged.pdf"
    except Exception as e:
        st.error(f"文件合并失败: {str(e)}")
        return None, None


def render_file_uploader():
    """
    渲染文件上传组件
    """
    st.subheader("文件上传")

    # 初始化 session state
    if "file_id" not in st.session_state:
        st.session_state.file_id = ""
    
    if "file_path" not in st.session_state:
        st.session_state.file_path = ""

    uploaded_files = st.file_uploader(
        "请选择一个或多个 PDF 文件",
        type=["pdf"],
        key="pdf_uploader",
        accept_multiple_files=True,
    )

    if uploaded_files:
        
        try:
            if len(uploaded_files) == 1:
                # 保存单个文件
                file_path, file_name = save_uploaded_file(uploaded_files[0], UPLOAD_DIR)
            else:
                # 合并多个文件
                file_path, file_name = merge_uploaded_files(uploaded_files, UPLOAD_DIR)
            
            st.session_state.file_path = file_path

            if file_path and st.session_state.file_id == "":
                # print(len(uploaded_files))
                # 上传文件到 DashScope
                file_id = upload_file(client, file_path)
                if file_id:
                    st.session_state.file_id = file_id
                    data_now = {"filename": file_name, "file_id": file_id}
                    json_path = Path(RESOURCES_DIR) / "data.json"
                    join_json(json_path, data_now)
                    st.success(f"文件上传成功: {file_name}")
                return file_path
        except Exception as e:
            st.error(f"文件上传失败: {str(e)}")

    return None



# 渲染文件上传组件
# render_file_uploader()
