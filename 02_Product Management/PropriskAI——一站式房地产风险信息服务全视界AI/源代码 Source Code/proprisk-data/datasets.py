import csv
import os
import pandas as pd

from pymongo import MongoClient

url_caiwubaogao="D:\\PythonProject\\huaqibei_AI\\proprisk-data\\data\\raw\\caiwubaogao\\Financial_Report_Data.csv"
url_cooked_caiwubaogao="D:\PythonProject\huaqibei_AI\proprisk-data\data\cooked\caiwubaogao\cooked_Financial_Report_Data.csv"
url_mongoDB="mongodb://localhost:27017/"


def cook_caiwubaogao(source_file, target_file):
    try:
        with open(source_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
    except FileNotFoundError:
        print("Source file not found.")
        return

    cooked_data = []
    for row in data:
        try:
            # column1 = float(row[0])
            # column2 = float(row[1])
            # product = column1 * column2
            # cooked_data.append([product])
            f1 = row[]
        except (ValueError, IndexError):
            print("Invalid data format in source file. Skipping row.")

    try:
        with open(target_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cooked_data)
        print(f"cooked_data results written to {target_file} successfully.")
    except IOError:
        print("Error writing to target file.")

