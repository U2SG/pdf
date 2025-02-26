import urllib.parse
import urllib3
import json
import re
import time
from typing import Optional, Dict
from config import APP_CODE

# 初始化全局变量
host = 'https://1b002.market.alicloudapi.com'
path = '/1b002'
appcode = APP_CODE
timeout = 10.0
cache_ttl = 600
http = urllib3.PoolManager()
cache = {}  # 缓存存储结构：{card_number: (timestamp, data)}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Authorization': f'APPCODE {appcode}'
}

def get_from_cache(card_number: str) -> Optional[Dict]:
    """从缓存中获取数据"""
    cached = cache.get(card_number)
    if not cached:
        return None
    
    timestamp, data = cached
    if time.time() - timestamp < cache_ttl:
        return data
    # 缓存过期后自动清理
    del cache[card_number]
    return None

def replace_card_numbers(text):
    pattern = r'(?<!\d)(\d{16,19})(?!\d)'

    def replacer(match):
        card_num = match.group()
        return query_bank_card(card_num)+card_num if query_bank_card(card_num) else card_num

    result_str = re.sub(pattern, replacer, text)
    return result_str

def save_to_cache(card_number: str, data: Dict):
    """保存数据到缓存"""
    cache[card_number] = (time.time(), data)

def query_bank_card(card_number: str) -> Optional[Dict]:
    """查询银行卡信息（带缓存功能）"""
    # 优先从缓存获取
    cached_data = get_from_cache(card_number)
    if cached_data is not None:
        print(f"命中缓存: {card_number}")
        return f'中国{cached_data["result"]["bank"]}股份有限公司{cached_data["result"]["city"]}分行'

    print(f"发起API请求: {card_number}")
    url = host + path
    
    try:
        body = {'bankcardno': card_number}
        encoded_body = urllib.parse.urlencode(body).encode('utf-8')
        
        response = http.request(
            'POST',
            url,
            body=encoded_body,
            headers=headers,
            timeout=timeout
        )
        
        if response.status != 200:
            print(f"API请求失败，状态码：{response.status}")
            return None

        content = response.data.decode('utf-8')
        
        try:
            result = json.loads(content)
            # 仅缓存成功结果
            if result.get("status") == "01":  # 假设API返回的成功状态码为01
                save_to_cache(card_number, result)
            return f'中国{result["result"]["bank"]}股份有限公司{result["result"]["city"]}分行'
        except json.JSONDecodeError:
            print("响应不是有效的JSON格式")
            return {"raw_response": content}

    except urllib3.exceptions.HTTPError as e:
        print(f"HTTP请求错误: {str(e)}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
    
    return None

def clear_cache():
    """清空所有缓存"""
    cache.clear()

# 使用示例
if __name__ == "__main__":
    card_number = '冻结被申请人林理名下的6217007200022023546账户内存款0元'
    print(replace_card_numbers(card_number))
    
    # # 第一次查询（走API）
    # result = query_bank_card(card_number)
    # print("第一次查询结果:", result)
    
    # # 第二次查询（走缓存）
    # result = query_bank_card(card_number)
    # print("第二次查询结果:", result)
    
    # # 清空缓存
    # clear_cache()
