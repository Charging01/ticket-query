"""提取地址及其对应的代号"""


import re
import requests
from pprint import pprint

# 地址和代号网址
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'
# 获取url
response = requests.get(url, verify=False)    # 移除SSL认证
# 正则提取中文和代号  格式：列表 内包含多个元组，元组形式 （‘上海’，‘SHH’）
station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)   # 解析页面中中文和大写字母
# 定义打印信息 缩进4个空格
pprint(dict(station), indent=4)

