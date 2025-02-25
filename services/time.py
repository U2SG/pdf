import datetime

# 定义数字到汉字的映射
NUMBER_TO_CHINESE = {
    '0': '零',
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '七',
    '8': '八',
    '9': '九'
}

# 定义月份和日的特殊汉字
MONTHS = {
    1: '一月',
    2: '二月',
    3: '三月',
    4: '四月',
    5: '五月',
    6: '六月',
    7: '七月',
    8: '八月',
    9: '九月',
    10: '十月',
    11: '十一月',
    12: '十二月'
}

DAYS = {
    1: '一日',
    2: '二日',
    3: '三日',
    4: '四日',
    5: '五日',
    6: '六日',
    7: '七日',
    8: '八日',
    9: '九日',
    10: '十日',
    11: '十一日',
    12: '十二日',
    13: '十三日',
    14: '十四日',
    15: '十五日',
    16: '十六日',
    17: '十七日',
    18: '十八日',
    19: '十九日',
    20: '二十日',
    21: '二十一日',
    22: '二十二日',
    23: '二十三日',
    24: '二十四日',
    25: '二十五日',
    26: '二十六日',
    27: '二十七日',
    28: '二十八日',
    29: '二十九日',
    30: '三十日',
    31: '三十一日'
}

def number_to_chinese(number):
    """将数字转换为汉字"""
    return ''.join([NUMBER_TO_CHINESE[digit] for digit in str(number)])

def date_to_chinese(date):
    """将日期转换为汉字表示"""
    year = number_to_chinese(date.year)
    month = MONTHS[date.month]
    day = DAYS[date.day]
    return f"{year}年{month}{day}"

def main():
    # 获取当前日期
    today = datetime.date.today()

    # 将当前日期转换为汉字表示
    chinese_date = date_to_chinese(today)

    # 输出结果
    print(chinese_date)

if __name__ == "__main__":
    main()
