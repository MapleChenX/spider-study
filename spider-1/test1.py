from scrapy import Selector
import requests

url = 'https://movie.douban.com/top250'
# 定义自定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

# 使用 POST 请求参数发送请求
response = requests.get(url, headers=headers)
s = Selector(text=response.text)
x = '//div[@class="info"]//span[@class="title"][1]/text()'
e = s.xpath(x).extract()
# content = e[0]
# print(content)
for a in e:
    print(a)

