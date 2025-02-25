import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESOURCES_DIR = os.path.join(DATA_DIR, 'resources')
UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')

# 创建必要的目录
for dir_path in [DATA_DIR, RESOURCES_DIR, UPLOAD_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

BASE_URL = "https://api.deepseek.com/v1"  # URL
DEEPSEEK_API_KEY = "sk-41ebc756e88549d4892ca52f4418e05a"  # API Key
DEEPSEEK_MODEL = "deepseek-chat"  # 默认模型名称