import signal
import time
import threading
import requests
from lxml import etree
from queue import Queue
import redis
from bs4 import BeautifulSoup

import sys

sys.path.append('..')
from common.list import CompanyList

start_url = 'https://www.bing.com/search?q=%s'
link_queue = Queue()
threads_num = 50
threads = []
download_pages = 0
r = redis.Redis()
thread_on = True

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding': 'gzip, deflate',
           'cookie': 'DUP=Q=sBQdXP4Rfrv4P4CTmxe4lQ2&T=415111783&A=2&IG=31B594EB8C9D4B1DB9BDA58C6CFD6F39; MUID=196418ED32D66077102115A736D66479; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DDFFA87D3A894019942913899F5EC316&dmnchg=1; ENSEARCH=BENVER=1; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMC0wMy0xNlQwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjd9; ABDEF=V=13&ABDV=11&MRNB=1614238717214&MRB=0; _RwBf=mtu=0&g=0&cid=&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2021-02-25T07:47:40.5285039+00:00&e=; MUIDB=196418ED32D66077102115A736D66479; SerpPWA=reg=1; SRCHUSR=DOB=20190509&T=1614253842000&TPC=1614238646000; _SS=SID=375CD2D8DA85697D0DA0DD31DBAB689D; _EDGE_S=SID=375CD2D8DA85697D0DA0DD31DBAB689D&mkt=zh-cn; _FP=hta=on; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; dsc=order=ShopOrderDefault; ipv6=hit=1614260171835&t=4; SRCHHPGUSR=CW=993&CH=919&DPR=1&UTC=480&WTS=63749850642&HV=1614256571&BRW=HTP&BRH=M&DM=0'
           }


def fetch(url, company, valid_proxy_list, i):
    """请求并下载网页"""
    newsURL = company + '上游供应商名单'
    # newsURL = newsURL.encode('utf-8')
    proxies = {
        "http": "http://" + valid_proxy_list[i]["ip"] + ":" + valid_proxy_list[i]["port"]
    }
    print('************************************************')
    print(proxies)
    print('************************************************')
    req = requests.get(url % newsURL, headers=headers, proxies=proxies)
    # print(req.status_code)
    if req.status_code != 200:
        # req.raise_for_status()
        print("爬取失败")
        return None
    global download_pages
    download_pages += 1
    return req.text.replace('\t', '').replace('\r', '').replace('\n', '')
    # return req.text


def fetchNews(url):
    """请求并下载网页"""
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        # r.raise_for_status()
        print("*******爬取新闻失败*******")
        return None
    global download_pages
    download_pages += 1
    return r.text.replace('\t', '').replace('\r', '').replace('\n', '')


def parse_company(url):
    """处理新闻详情页面"""
    # r = requests.get(link)
    content = fetchNews(url)
    if content is None:
        return None
    selector2 = etree.HTML(content)
    # 所有的文本数据
    text = selector2.xpath('//*[@id="ArticleContent"]/div/div/text()')
    return text


def process_data(company, data, link, num):
    """处理数据"""
    if data:
        print(data)
        fileURL = 'C:\\Users\\asus\\Desktop\\pythonTest\\huaqibei\\数据集搜集\\data\\raw' \
                  '\\' + company + '\\news\\' + str(num) + '.txt'
        sourceInfo = '数据来源' + link
        with open(fileURL, 'w') as f:
            f.write(data)
            f.write(sourceInfo)
        print("写入完毕")


def download(i):
    while thread_on:
        # 阻塞 直到从队列中获取一条消息
        # link = link_queue.get()
        link = r.lpop('company.queue')
        # 当所有link遍历完线程结束
        if link:
            data = parse_company(link)
            process_data(data)
            print('remaining company: %s' % r.llen('company.queue'))
        time.sleep(0.2)
    print('thread-%s exit now' % i)


def sigint_handler(signum, frame):
    print('received Ctrl+C, wait for exit gracefully')
    global thread_on
    thread_on = False


# 1. 获取代理IP列表
def get_proxy_list():
    # 构造请求头，模拟浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    # 请求代理IP网页
    # url = "http://www.zdopen.com/ShortProxy/GetIP/?api&akey&timespan=5&type=1"
    url = "https://www.89ip.cn/index_1.html"
    response = requests.get(url, headers=headers)

    # 解析网页获取代理IP列表
    soup = BeautifulSoup(response.text, "html.parser")
    proxy_list = []
    table = soup.find("table", {"class": "layui-table"})
    if (table == None):
        print("获取代理IP失败")
        return None
    for tr in table.find_all("tr"):
        td_list = tr.find_all("td")
        if len(td_list) > 0:
            ip = td_list[0].text.strip()
            port = td_list[1].text.strip()
            type = td_list[3].text.strip()
            proxy_list.append({
                "ip": ip,
                "port": port,
                "type": type
            })
    return proxy_list


# 2. 验证代理IP可用性
def verify_proxy(proxy):
    # 构造请求头，模拟浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    # 请求目标网页并判断响应码
    url = "http://www.baidu.com"
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


# 3. 测试代理IP列表可用性
def test_proxy_list(proxy_list):
    valid_proxy_list = []
    for proxy in proxy_list:
        if verify_proxy(proxy):
            valid_proxy_list.append(proxy)
    """企图在本地存储可用的IP池，但是发现读取数据速度居然跟再爬一次速度差不多"""
    # # 将验证通过的代理信息写入proxies.txt文件
    # with open('C:\\Users\\asus\\Desktop\\pythonTest\\huaqibei\\数据集搜集\\scripts\\proxies.txt', 'w') as file:
    #     for proxy in valid_proxy_list:
    #         # 将代理信息转换为字符串格式并写入文件
    #         proxy_str = f"{proxy['ip']}:{proxy['port']} - {proxy['type']}\n"
    #         file.write(proxy_str)
    # print("代理信息已写入proxies.txt文件。")
    return valid_proxy_list
    # return proxy_list


if __name__ == '__main__':
    start_time = time.time()
    # 获取代理IP列表
    print("正在获取代理IP...")
    proxy_list = get_proxy_list()
    # 验证代理IP可用性
    print("正在验证IP有效性...")
    valid_proxy_list = test_proxy_list(proxy_list)
    print("IP有效性验证完毕")
    # 输出可用代理IP
    print("有效代理IP列表：")
    for proxy in valid_proxy_list:
        print(proxy)
    num = 1
    for company in CompanyList:
        # 请求入口页面
        htmlText = fetch(start_url, company, valid_proxy_list, num)
        num += 1
        selector = etree.HTML(htmlText)
        # print('------------------------------------------------')
        # print(htmlText)
        # print('------------------------------------------------')
        # 解析入口页面：通过前端页面的开发者工具，找到所有需要的链接
        links = selector.xpath("// *[ @ id = 'b_results'] / li / h2 / a /@href")
        if not links:
            print('公司', company, '信息爬取失败')
        else:
            print('公司', company, '的所有新闻链接', links)
            i = 1
            for link in links:
                data = parse_company(link)
                process_data(company, data, link, i)
                i += 1
        # for link in links:
        #     if r.sadd('company.seen', link):
        #         r.rpush('company.queue', link)
        # # 启动线程 并将线程对象放入一个列表保存
        # for i in range(threads_num):
        #     t = threading.Thread(target=download, args=(i + 1,))
        #     t.start()
        #     threads.append(t)
        #
        # signal.signal(signal.SIGINT, sigint_handler)
        # # 阻塞队列 直到队列被清空
        # link_queue.join()
        # # 向队列发送N个None 以通知线程退出
        # for i in range(threads_num):
        #     link_queue.put(None)
        # # 退出线程
        # for t in threads:
        #     t.join()
        #
        # const_seconds = time.time() - start_time
