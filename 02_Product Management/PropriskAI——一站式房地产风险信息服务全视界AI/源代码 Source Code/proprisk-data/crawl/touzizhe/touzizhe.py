import requests
import re

base_url = "https://wxly.p5w.net/api/data/gettrssearch?code=000031&page={}&size=20"

for i in range(1,3):
    url = base_url.format(i)
    response = requests.get(url)

    source_code = response.text

    pattern = r'"DOCURL":"(.*?)"'
    doc_urls = re.findall(pattern, source_code)

    with open("dayuecheng_links","a",encoding="utf-8") as file:
        for doc_url in doc_urls:
            file.write(doc_url+"\n")