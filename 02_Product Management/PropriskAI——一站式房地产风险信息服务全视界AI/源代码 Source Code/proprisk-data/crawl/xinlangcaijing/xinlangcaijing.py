import requests
from lxml import html

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
    # Parse the HTML content
    tree = html.fromstring(html_content)

    # XPath to extract links
    xpath_expression = "//div[@class='part02']//ul[@class='list01']//li/a/@href"

    # Extract links
    links = tree.xpath(xpath_expression)

    return links

def main():
    biguiyuan_url = "https://stock.finance.sina.com.cn/hkstock/go.php/CompanyNews/page/{}/code/02007/.phtml"
    biguiyuan_page=34
    hengda_url="https://stock.finance.sina.com.cn/hkstock/go.php/CompanyNews/page/{}/code/03333/.phtml"
    hengda_page=34
    dayuecheng_url="https://stock.finance.sina.com.cn/hkstock/go.php/CompanyNews/page/{}/code/000031/.phtml"
    dayuecheng_page=33
    base_url = hengda_url
    all_links = []

    # Iterate over pages
    for page_num in range(1, hengda_page+1):
        url = base_url.format(page_num)
        html_content = get_html_source(url)
        if html_content:
            links = extract_links_from_html(html_content)
            all_links.extend(links)

    # Write links to a text file
    with open("hengda_links.txt", "w", encoding="utf-8") as file:
        for link in all_links:
            file.write(link + "\n")

    print("Links have been saved to links.txt")

if __name__ == "__main__":
    main()
