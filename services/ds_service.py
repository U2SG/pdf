import logging
from functools import lru_cache
from typing import List, Dict, Generator
from openai import OpenAI
from config import BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL

logger = logging.getLogger(__name__)

@lru_cache(maxsize=None)
def initialize_deepseek_client() -> OpenAI:
    """
    初始化 DeepSeek 客户端
    """
    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=BASE_URL, 
    )

client = initialize_deepseek_client()

class ChatService:
    def __init__(self):
        """
        初始化 ChatService 实例，设置默认的模型名称。
        """
        self.model = DEEPSEEK_MODEL
    
    def get_response(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        获取流式响应
        :param messages: 消息列表，每条消息为字典格式，包含 "role" 和 "content" 字段
        :return: 流式响应的生成器
        :raises Exception: 如果请求失败，抛出异常
        """
        try:
            return client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                stream=True,
                response_format={"type": "json_object"},
                # stream_options={"include_usage": True}
            )
        except Exception as e:
            logger.error(f"回答生成失败: {str(e)}", exc_info=True)
            raise Exception(f"回答生成失败: {str(e)}")



