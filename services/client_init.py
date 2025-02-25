from openai import OpenAI

def initialize_openai_client():
    """
    初始化 OpenAI 客户端
    """
    return OpenAI(
        api_key="sk-b2d753f9e6844cecb23cdce4608d1898",  
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", 
    )

# 初始化 client 并导出
client = initialize_openai_client()