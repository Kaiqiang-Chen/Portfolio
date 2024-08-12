import requests
import re
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

def extract_links_from_html(html_content):
    pattern = r'"infoCode":"(.*?)"'
    info_codes = re.findall(pattern, html_content)

    with open('yanbao_dayuecheng.txt', 'w') as file:
        for info_code in info_codes:
            file.write("https://data.eastmoney.com/report/info/"+info_code +".html" '\n')

def main():
    nandu_url = "https://data.eastmoney.com/report/603506.html"
    zhongnan_url="https://data.eastmoney.com/report/000961.html"
    dayuecheng_url="https://data.eastmoney.com/report/000031.html"
    base_url = dayuecheng_url
    html_content = get_html_source(base_url)

    if html_content:
        extract_links_from_html(html_content)

    print("Links have been saved to links.txt")

if __name__ == "__main__":
    main()
