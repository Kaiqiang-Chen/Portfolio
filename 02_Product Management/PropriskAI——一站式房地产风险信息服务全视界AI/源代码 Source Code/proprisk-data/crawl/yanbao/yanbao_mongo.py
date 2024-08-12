# coding=utf-8
import requests
import json
import re
from datetime import datetime
from pymongo import MongoClient
from gne import GeneralNewsExtractor


def get_html_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查是否请求成功
        response.encoding = response.apparent_encoding
        html_source = response.text
        return html_source
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None


class YanbaoInfoSpider:
    def __init__(self):
        self.results = []

    def fetch_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def parse(self, url, response):
        cont = get_html_source(url)
        extractor = GeneralNewsExtractor()
        result = extractor.extract(cont, noise_node_list=['//div[@class="comment-list"]'])

        new_information = result

        self.results.append(new_information)

    def save_results_to_mongodb(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['yanbao']
        collection = db['biguiyuan']

        for result in self.results:
            collection.insert_one(result)  # 将结果插入到MongoDB集合中

    def save_results_to_file(self, filename="yanbao_results_final.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            for result in self.results:
                file.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":

    with open("yanbao_dayuecheng.txt", "r", encoding="utf-8") as file:
        start_urls = [line.strip() for line in file.readlines()]

    spider = YanbaoInfoSpider()

    for url in start_urls:
        response = spider.fetch_url(url)
        if response:
            spider.parse(url, response)

    spider.save_results_to_mongodb()
    print("yanbao-info执行完毕")