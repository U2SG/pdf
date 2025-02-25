import streamlit as st
from services.client_init import client
import os
from config import UPLOAD_DIR

# 删除文件夹中的所有文件
def delete_files_in_folder(folder_path):
    try:
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"文件夹 {folder_path} 不存在")
            return

        # 获取文件夹中的所有文件和子文件夹
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # 如果是文件，则删除
            if os.path.isfile(file_path):
                os.remove(file_path)

        print(f"文件夹 {folder_path} 内的所有文件已删除")
    except Exception as e:
        print(f"发生错误: {e}")

# 获取所有的文件ID
def get_all_file_id():
    file_stk = client.files.list()
    return file_stk

# 删除上传的文件
def delete_file(file_id):
    file_object = client.files.delete(file_id)
    return file_object

def render_download_interface():

    # # 创建一个状态变量来跟踪是否需要输入文件名
    # if 'input_file_name' not in st.session_state:
    #     st.session_state.input_file_name = False
    
    # # 初始化文件名
    # file_name = "example.csv"

    if "file_stream" in st.session_state:
        try:       
            st.download_button(
                label="下载文件",
                data=st.session_state.file_stream,
                file_name="结果.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"下载文件失败: {str(e)}")
    else:
        st.info("等待生成结果")

    if st.button("清除文件"):
        delete_files_in_folder(UPLOAD_DIR)
        for file in get_all_file_id():
            if file.id not in ['file-fe-kWLhL9uiGSetIMxHC1mMoUVA','file-fe-P5nO8RM76ht2qqjIwUiVANIJ']:
                delete_file(file.id)