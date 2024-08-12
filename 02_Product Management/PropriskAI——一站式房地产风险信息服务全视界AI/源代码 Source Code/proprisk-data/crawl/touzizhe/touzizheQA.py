import requests						# 发起网络请求
from bs4 import BeautifulSoup		# 解析HTML文本
import pandas as pd					# 处理数据
import os
import time			# 处理时间戳
import json			# 用来解析json文本

def fetchUrl(url,page):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        "Referer":"https: // ir.p5w.net / c / 000031 / questionlist.shtml"
    }

    payloads = {
        "pid": "B38B95185B1611E6AC91D89D67297B20",
        "source":None,
    }

    r = requests.post(url, headers=headers, data=json.dumps(payloads))
    if r.status_code == 200:
        try:
            return r.json()
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
    else:
        print(f"Request failed with status code: {r.status_code}")
    return None


if __name__ == "__main__":
    start = 1
    end = 1
    for page in range(start, end + 1):
        url = "https://ir.p5w.net/company/getCompanyInfo.shtml"
        html = fetchUrl(url, page)
        print(html)
