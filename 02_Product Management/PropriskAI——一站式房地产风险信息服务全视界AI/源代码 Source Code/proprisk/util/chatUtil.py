# -*- coding: utf-8 -*-
import os

import httpx
import openai
from openai import OpenAI
from pymongo import MongoClient
import csv

mongoDB = "mongodb://localhost:27017/"
client = MongoClient(mongoDB)
db = client['gongyingshang']
client = OpenAI(
    base_url="https://api.chatgptid.net/v1",
    api_key="sk-01UfQL9xaHq21toVB6930f096529457284245f75F850A71b",
    http_client=httpx.Client(
        base_url="https://api.chatgptid.net/v1",
        follow_redirects=True,
    ),
)


# 截断文本函数
def truncate_text(text, max_tokens):
    """
    Truncates text to a maximum number of tokens.

    Args:
        text (str): The input text to be truncated.
        max_tokens (int): The maximum number of tokens allowed.

    Returns:
        str: The truncated text.
    """
    tokens = text.split()  # 将文本分割成单词列表
    truncated_tokens = tokens[:max_tokens]  # 取前 max_tokens 个单词
    truncated_text = ' '.join(truncated_tokens)  # 将单词列表重新组合成文本
    return truncated_text


# 检查文本是否超出token限制
def check_text_tokens(text, max_tokens):
    # 计算content的token值
    # content_tokens = sum(len(token.split()) for token in text.split())
    content_tokens = 0
    for line in text.split('\n'):
        line_tokens = 0
        for token in line.split():
            line_tokens += len(token.split())
        content_tokens += line_tokens
    # print(content_tokens)

    # 检查content的token值是否超过了模型最大长度限制
    if content_tokens > 15000:
        # 如果超过了限制，进行截断
        text = truncate_text(text, max_tokens)
    return text


# 房地产简介
def generate_real_estate_introduction(info):
    try:
        # 使用GPT-3.5分析文本
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f'根据以下房地产公司的信息，输出一个房地产公司的简介\n'
                            f'要求综合这家房地产公司的所有信息'
                            f'{info}'
                            f'输出格式为:\n'
                            f'简介：{info["企业名称"]}是...'}
            ]
        )
        result = completion.choices[0].message.content
        return result
    except openai.BadRequestError as e:
        if 'This model\'s maximum context length is 16385' in str(e):
            print("Maximum context length exceeded. Skipping this data.")
            return None
        else:
            print(f'Error occurred: {e}')
    except Exception as e:
        print(f'Error occurred: {e}')


# 流动性危机几率原因
def generate_LRP_introduction(LRP_data):
    try:
        # 使用GPT-3.5分析文本
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f'根据以下房地产公司的各项指标信息以及流动性危机爆发概率，输出一个该房地产公司流动性风险爆发机率为{LRP_data["Risk_Radio"]}的原因\n'
                            f'将其中的英文指标翻译为中文'
                            f'{LRP_data}'
                            f'输出格式为:\n'
                            f'原因：{LRP_data["Company"]}...'}
            ]
        )
        result = completion.choices[0].message.content
        return result
    except openai.BadRequestError as e:
        if 'This model\'s maximum context length is 16385' in str(e):
            print("Maximum context length exceeded. Skipping this data.")
            return None
        else:
            print(f'Error occurred: {e}')
    except Exception as e:
        print(f'Error occurred: {e}')


# 供应商简介
def generate_supplier_introduction(info):
    try:
        # 使用GPT-3.5分析文本
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f'根据以下房地产的供应商公司的信息，输出一个供应商的简介\n'
                            f'要求综合这家供应商公司的所有信息'
                            f'{info}'
                            f'输出格式为:\n'
                            f'简介：{info["供应商"]}是...'}
            ]
        )
        result = completion.choices[0].message.content
        return result
    except openai.BadRequestError as e:
        if 'This model\'s maximum context length is 16385' in str(e):
            print("Maximum context length exceeded. Skipping this data.")
            return None
        else:
            print(f'Error occurred: {e}')
    except Exception as e:
        print(f'Error occurred: {e}')


# 供应商受影响程度原因
def generate_affected_reason(supplier_affected, degree_of_influence):
    try:
        # 使用GPT-3.5分析文本
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f'根据以下供应商公司的各项指标信息以及受影响程度，输出一个该供应商公司受房地产公司的影响程度为{degree_of_influence}的原因\n'
                            f'将其中的英文指标翻译为中文'
                            f'{supplier_affected}'
                            f'输出格式为:\n'
                            f'原因：{supplier_affected["Company"]}...'}
            ]
        )
        result = completion.choices[0].message.content
        return result
    except openai.BadRequestError as e:
        if 'This model\'s maximum context length is 16385' in str(e):
            print("Maximum context length exceeded. Skipping this data.")
            return None
        else:
            print(f'Error occurred: {e}')
    except Exception as e:
        print(f'Error occurred: {e}')


if __name__ == "__main__":
    # collection = db['company_information']
    # text = collection.find_one({'企业名称': '华夏幸福基业股份有限公司'})
    # introduction = generate_real_estate_introduction(text)
    # print(introduction)

    # supplier = db['supplier_information']
    # supplier_one = supplier.find_one({'供应商': '苏州禧屋住宅科技股份有限公司'})
    # supplier_info = generate_supplier_introduction(supplier_one)
    # print(supplier_info)

    real_estate = db['Real_Estate_LRP_data']
    LR = real_estate.find_one({'Stock Code': '02007'})
    LR_reason = generate_LRP_introduction(LR)
    print(LR_reason)
