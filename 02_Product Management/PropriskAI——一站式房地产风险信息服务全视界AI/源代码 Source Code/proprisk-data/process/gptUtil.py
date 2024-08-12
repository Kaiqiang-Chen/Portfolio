# -*- coding: utf-8 -*-
import os

import httpx
import openai
from openai import OpenAI
from pymongo import MongoClient
import csv

mongoDB = "mongodb://localhost:27017/"
client = OpenAI(
    base_url="https://api.chatgptid.net/v1",
    api_key="sk-01UfQL9xaHq21toVB6930f096529457284245f75F850A71b",
    http_client=httpx.Client(
        base_url="https://api.chatgptid.net/v1",
        follow_redirects=True,
    ),
)
# client = OpenAI(
#     base_url="https://api.chatgptid.net/v1",
#     api_key="sk-vZzLdBOOKY5dFTIB79BaC6633cEc4dC0B05dB4C5Dc6eD40b"
# )
db_list = ['yanbao', 'xinlangcaijing', 'touzizhe']
checkpoint_file = "checkpoint.txt"  # 用于保存检查点的文件


def rename_collection(database, old_collection, new_collection):
    client = MongoClient(mongoDB)
    db = client[database]
    db[old_collection].rename(new_collection)
    print('集合重命名成功')
    client.close()


def sanitize_filename(filename):
    # 替换文件名中的特殊字符
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\r', '\n', '\t', '\x0b', '\x0c']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename


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


def analyze_text_with_gpt3_5(text, company, supplier):
    # 检查text文本
    text = check_text_tokens(text, 15000)
    # print(f'{text}')
    # # 使用GPT-3.5分析文本
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": f"分析以下文本，判断房地产公司{company}是否对供应商{supplier}有不良影响,要求所得结论必须从文本信息中直接获取，不可擅自推断！！！"
    #                                     f"是否有影响的评判标准为:文本当中是否出现二者明确的金钱交易往来!!!这个很重要！！！"
    #                                     f"要求文本依据跟其对应的输出内容在同一行"
    #                                     f"文本内容为：\n{text}\n"
    #                                     f"要求输出格式为：\n"
    #                                     f"房地产公司名称：{company}\n"
    #                                     f"供应商名称：{supplier}\n"
    #                                     f"是否有影响：(0表示没有 1表示有) \n"
    #                                     f"依据（简要找到产生影响的文本依据就可）：\n"
    #                                     f"如果没有影响，那么文本依据部分为空"}
    #     ]
    # )
    # return completion
    while True:
        try:
            # 使用GPT-3.5分析文本
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",
                     "content": f"分析以下文本，判断房地产公司{company}是否对供应商{supplier}有不良影响,要求所得结论必须从文本信息中直接获取，不可擅自推断！！！"
                                f"是否有影响的评判标准为:文本当中是否出现二者明确的金钱交易往来!!!这个很重要！！！"
                                f"要求文本依据跟其对应的输出内容在同一行"
                                f"要求每个输出格式只有一个values值"
                                f"文本内容为：\n{text}\n"
                                f"要求输出格式为：\n"
                                f"房地产公司名称：{company}\n"
                                f"供应商名称：{supplier}\n"
                                f"是否有影响：(0表示没有 1表示有) \n"
                                f"依据（简要找到产生影响的文本依据就可）：\n"
                                f"如果没有影响，那么文本依据部分为空"}
                ]
            )
            return completion
        except openai.BadRequestError as e:
            if 'This model\'s maximum context length is 16385' in str(e):
                print("Maximum context length exceeded. Skipping this data.")
                return None
            else:
                print(f'Error occurred: {e}')
        except Exception as e:
            print(f'Error occurred: {e}')


def analyze_text_until_correct_format(text, company_name, supplier):
    while True:
        result = analyze_text_with_gpt3_5(text, company_name, supplier)
        if result is None:
            return None
        result = result.choices[0].message.content
        flag, temp = is_result_format_correct(result)
        if flag:
            return temp


def is_result_format_correct(result):
    temp = {}
    try:
        lines = result.split('\n')
        for line in lines:
            if '：' in line:
                key, value = line.split('：')
                temp[key.strip()] = value.strip()
        if '房地产公司名称' in temp.keys() and "供应商名称" in temp.keys() \
                and "是否有影响" in temp.keys() \
                and "依据" in temp.keys():
            return True, temp
        else:
            return False, temp
    except Exception as e:
        print(f"Error occurred: {e}")
        return False, temp


def save_result(temp, source_url):
    # temp = {}
    # lines = result.split('\n')
    # for line in lines:
    #     # print(line)
    #     if '：' in line:
    #         key, value = line.split('：')
    #         temp[key.strip()] = value.strip()
    # 打印字典形式的输出结果
    # print(output)
    if temp['是否有影响'] == '1':
        temp['依据来源'] = source_url
        # # 完善组织机构代码
        # client = MongoClient(mongoDB)
        # db_suppliers = client['gongyingshang']
        # suppliers_information = db_suppliers['suppliers_information']
        # documents = suppliers_information.find({})
        # for document in documents:
        #     if document['供应商']==temp['企业名称']:
        #         temp['组织机构代码'] = document['组织机构代码']
        #         break
        valueList = temp.values()
        with open('D:\PythonProject\huaqibei_AI\proprisk-'
                  'data\data\cooked\Affected_Suppliers_List.csv', 'a',
                  encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(valueList)
            print(f'-----该新闻表示：{temp["供应商名称"]}受到房地产公司{temp["房地产公司名称"]}的影响-----')
            print('-----已成功写入文件中-----')
            return True
    else:
        print(f'*****该新闻表示：{temp["供应商名称"]}未受到房地产公司{temp["房地产公司名称"]}的影响*****')
        return False


def process_data(url_mongoDB, news_dbstr):
    # 连接本地MongoDB数据库 房地产公司+供应商
    client = MongoClient(url_mongoDB)

    print("连接本地MongoDB 房地产舆情信息相关数据库...")
    db_news = client[news_dbstr]
    # print(collectionlist_news)

    print("连接本地MongoDB 房地产公司与供应商相关数据库...")
    db_corporation = client["gongyingshang"]
    collectionlist_supplier = db_corporation["company_suppliers"]
    cursor_supplier = collectionlist_supplier.find({})
    # print(cursor_supplier)

    print("连接本地MongoDB 房地产公司信息相关数据库...")
    collectionlist_company = db_corporation["company_information"]
    cursor_company = collectionlist_company.find({})
    # print(cursor_company)

    # 聚合查询
    pipeline = [
        {
            "$lookup": {
                "from": "company_suppliers",
                "localField": "企业名称",
                "foreignField": "企业名称",
                "as": "suppliers"
            }
        },
        {
            "$unwind": "$suppliers"
        },
        {
            "$project": {
                "_id": 0,
                "企业名称": 1,
                "股票代码": 1,
                "供应商": "$suppliers.供应商",
                "数据来源": "$suppliers.数据来源"
            }
        }
    ]

    cursor = collectionlist_company.aggregate(pipeline)

    # print('-------------')
    # for collection_name in collectionlist_news:
    #     print(collection_name)
    #     print(collection_name['name'])
    # print('-------------')
    # 读取检查点
    try:
        with open(checkpoint_file, "r") as f:
            last_position = int(f.read())
        with open('checkpoint2.txt', 'r') as f2:
            last_position2 = int(f2.read())
        with open('checkpoint3.txt', 'r') as f3:
            last_position3 = int(f3.read())
    except FileNotFoundError:
        last_position = 0

    for index, document in enumerate(cursor):
        # print(document)
        if index < last_position:
            print(f'从checkpoint.txt中读取已经分析了多少条公司-供应商数据')
            continue  # 跳过已经处理过的数据
        # 用来标识二者之间是否有影响
        flag = False
        company_name = document['企业名称']
        stock_code = document['股票代码']
        supplier = document['供应商']
        collectionlist_news = db_news.list_collections()
        # 遍历news_dbstr数据库中具有相应名称的collection
        for index2, collection_news in enumerate(collectionlist_news):
            if index2 < last_position2:
                print(f'正在读取上次执行后的断点数据checkpoint2.txt')
                continue  # 跳过已经处理过的数据
            # print(collection_news['name'])
            # stock_code 示例
            # stock_code = 'sz000560'
            stock_code = stock_code[-6:]
            # print(stock_code)
            if stock_code in collection_news['name']:
                print(f'正在数据库{news_dbstr}的集合{collection_news["name"]}中查找公司{company_name}的相关数据...')
                print(f"正在读取房地产公司{company_name} ({stock_code})与供应商{supplier}的相关数据")
                news = db_news[collection_news['name']]
                documents = news.find({})
                for index3, document2 in enumerate(documents):
                    if index3 < last_position3:
                        print(f'从checkpoint3.txt中已经分析了多少条新闻')
                        continue  # 跳过已经处理过的数据
                    # print(document)
                    # print(f'正在检索新闻：{sanitize_filename(document2["title"])}...')
                    # print(f'正在检索新闻：{document2["title"].encode("utf-8", "ignore")}...')
                    try:
                        print(f'正在检索新闻：{document2["title"]}...')
                    except UnicodeEncodeError:
                        print(f'正在检索新闻：{document2["title"].encode("utf-8", "ignore")}...')
                    text = document2['content']
                    # source_url = document2['url']
                    source_url = 'xinlangcaijing'
                    # result = analyze_text_with_gpt3_5(text, company_name, supplier)
                    # result = result.choices[0].message.content
                    temp = analyze_text_until_correct_format(text, company_name, supplier)
                    # print(f"文件的分析结果：\n{result}")
                    if temp is not None:
                        flag = save_result(temp, source_url)
                    with open('checkpoint3.txt', "w") as f:
                        f.write(str(index3 + 1))  # 下次从下一个位置开始处理
                    if flag:
                        with open('checkpoint3.txt', 'w') as f:
                            f.write('0')
                        break
                with open('checkpoint2.txt', "w") as f:
                    f.write(str(index2 + 1))  # 下次从下一个位置开始处理
                break
        # 处理完毕后，保存当前位置作为检查点
        with open('checkpoint3.txt', 'w') as f:
            f.write('0')
        with open('checkpoint2.txt', 'w') as f:
            f.write('0')
        with open(checkpoint_file, "w") as f:
            f.write(str(index + 1))  # 下次从下一个位置开始处理
        if flag:
            continue
        # else:
        #     print(f'数据库{news_dbstr}中未找到{company_name} ({stock_code}) 的相关新闻')
    # for document in cursor_company:
    #     # print(document['企业名称'])
    #     company_name = document['企业名称']
    #     stock_code = document['股票代码']

    # for col_com in collectionlist_news:
    #     # 查找对应房地产公司的相关新闻
    #     print(col_com)
    #     # if(col_com["name"] == "hengda"):
    #     #     print(col_com["name"])


def main():
    # 假设您有一个文本文件列表
    text_files = ["file1.txt"]

    for file in text_files:
        with open(file, 'r') as f:
            text = f.read()
            result = analyze_text_with_gpt3_5(text)
            print(f"文件 {file} 的分析结果：{result}")


if __name__ == "__main__":
    # main()
    # analyze_text_with_gpt3_5()
    # rename_collection('xinlangcaijing', 'hengda', '003333')
    print(os.getcwd())
    # 测试能否成功写入csv文件
    # with open('test', 'r') as f:
    #     text = f.read()
    #     result = analyze_text_with_gpt3_5(text, '恒大集团有限公司', '广田集团')
    #     result = result.choices[0].message.content
    #     save_result(result, 'https://new.qq.com/rain/a/20230731A0881N00')

    print('***********************************************************')
    print(f'正在分析xinlangcaijing数据库当中的数据...')
    process_data(mongoDB, 'xinlangcaijing')
    print(f'数据库xinlangcaijing分析完成！')

    # for db in db_list:
    #     print('***********************************************************')
    #     print(f'正在分析{db}数据库当中的数据...')
    #     process_data(mongoDB, db)
    #     print(f'数据库{db}分析完成！')
