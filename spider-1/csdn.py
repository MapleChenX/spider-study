import json
from time import sleep

import redis
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from model.PostPreview import *
from sqlalchemy import create_engine
from pprint import pprint

engine = create_engine("mysql+pymysql://root:111111@localhost/spider", echo=True)
conn = engine.connect()
conn.execute(PREVIEW.delete())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}
# response = requests.get('https://www.csdn.net/', headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # 获取.navigation-right下的子标签a
# a_elements = soup.select('.navigation-right a')
#
# hrefs = []
#
# # 获取并打印a标签的href属性
# for a in a_elements:
#     hrefs.append(a.get('href'))
#     print(a.get('href'))
#
# for a in hrefs:
#     response = requests.get(a)
#
# response = requests.get('https://blog.csdn.net/nav/back-end', headers = headers)
# sel = Selector(text=response.text)
#
# Community = sel.xpath("//div[@class='Community']")
# header = Community.xpath("//span[@class='blog-text']/text()")
# desc = Community.xpath("//p[@class='desc']/text()")
#
# header_text = header.extract()
# desc_text = desc.extract()
# pprint(header_text)
#
# # 手工组装
# dict_list = [{'header': h, 'desc': d} for h, d in zip(header_text, desc_text)]
# conn.execute(PREVIEW.insert(), dict_list)
# conn.commit()

# 通过API获取json数据
params = {
    'componentIds': 'www-blog-recommend',
    'cate1': 'back-end'
}
r = redis.Redis(host='localhost', port=6379, db=0)


def get():
    response = requests.get('https://cms-api.csdn.net/v1/web_home/select_content', headers=headers, params=params)
    data = response.json()
    list1 = data['data']['www-blog-recommend']['info']  # json == dict load是 str -> json，dump是 json -> str
    for item in list1:
        item = item['extend']
        title = {'title': item['title']}
        desc = {'desc': item['desc']}
        url = {'url': item['url']}
        nickname = {'nickname': item['nickname']}
        certificate_info = {'certificate_info': item['certificate_info']}
        user_days = {'user_days': item['user_days']}
        actionInfo = {'actionInfo': item['actionInfo']}
        views = {'views': item['views']}

        # 整合为一个dict
        one = {**title, **desc, **url, **nickname, **certificate_info, **user_days, **actionInfo, **views}

        # filter
        r_title = r.get(item['title'])
        if r_title is not None:
            print('----已经爬取过了----')
            print(r_title)
            continue
        else:
            a = {**title, **url}
            r.set(item['title'], json.dumps(a), ex=60 * 60 * 5)
            # 热点排序
            r.zadd('csdn', {json.dumps(one): item['views']})

        conn.execute(PREVIEW.insert(), one)
        conn.commit()


for i in range(100):
    get()
    sleep(0.5)


def top10():
    result = r.zrevrange('csdn', 0, 9)
    for item in result:
        print(item)
top10()
