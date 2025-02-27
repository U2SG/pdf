import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESOURCES_DIR = os.path.join(DATA_DIR, 'resources')
UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')

# 创建必要的目录
for dir_path in [DATA_DIR, RESOURCES_DIR, UPLOAD_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"  # URL
DEEPSEEK_API_KEY = "cab7b475-daca-4faa-a6ac-2725d5f50dcf"  # API Key
DEEPSEEK_MODEL_V3 = "ep-20250227113253-f6rx2"  # 默认模型名称
DEEPSEEK_MODEL_R1 = "ep-20250227115539-c6kt7"
APP_CODE = "d9aaa8eea48742caa9ee2df1b6b55a7b"