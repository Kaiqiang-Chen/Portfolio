# -*- coding: utf-8 -*-

import csv
import os
import pandas as pd

from pymongo import MongoClient

url_caiwubaogao="D:\\PythonProject\\huaqibei_AI\\proprisk-data\\data\\raw\\caiwubaogao\\Financial_Report_Data.csv"
url_mongoDB="mongodb://localhost:27017/"
db = ["touzizhe", "xinlangcaijing", "yanbao"]


def sanitize_filename(filename):
    # 替换文件名中的特殊字符
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\r', '\n', '\t', '\x0b', '\x0c']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename


def link_with_mongoDB(url_mongoDB, dbstr, output_path):
    # 连接本地MongoDB数据库
    print("连接本地MongoDB数据库")
    client = MongoClient(url_mongoDB)
    db = client[dbstr]
    collectionlist = db.list_collections()
    # print("------------------")
    # print(collectionlist)
    file_base_path = output_path
    for col in collectionlist:
        output_path = file_base_path
        # print(col)
        print(col['name'])
        collections = db[col['name']]
        print(collections)
        cursor = collections.find({})

        output_path += f"\\{dbstr}"
        output_path += f"\\{col['name']}"
        # 确保输出路径存在
        os.makedirs(output_path, exist_ok=True)

        # 将新闻内容转换为txt文档
        for document in cursor:
            # print(document)
            title = document["title"]
            content = document["content"]

            # 替换文件中的特殊命名符
            title = sanitize_filename(title)

            file_path = os.path.join(output_path, f"{title}.txt")
            # 创建并写入文本文件
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
                print(f"已生成文件: {title.encode('utf-8')}.txt")


def read_data_from_caiwubaogao(url):
    # print(os.getcwd())
    with open(url, "r", encoding="utf-8") as f:
        datasets = pd.read_csv(url)
        print('-----------')
        print(datasets)
        reader = csv.reader(f)
        print(type(reader))
        for data in reader:
            print(data)
            print(data[2])


if __name__ == "__main__":
    # 将MongoDB数据转换为需要的.txt文件
    # output_path = "C:\\Users\\asus\Desktop\\news"
    # link_with_mongoDB(url_mongoDB, "touzizhe", output_path)

    read_data_from_caiwubaogao(url_caiwubaogao)