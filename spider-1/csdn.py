import json
from time import sleep

import redis
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from scrapy import Selector
from sqlalchemy.orm import sessionmaker

from model.PostPreview import *
from sqlalchemy import create_engine
from pprint import pprint

r = redis.Redis(host='localhost', port=6379, db=0)
engine = create_engine("mysql+pymysql://root:111111@localhost/spider")
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

# url获取
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
# # 文件保存 hrefs
# with open('hrefs.txt', 'w') as f:
#     for href in hrefs:
#         f.write(href + '\n')


# params = []
# # 凑params
# with open("hrefs.txt", 'r') as f:
#     for line in f:
#         url = line.strip()
#         suffix = url.split('/')[-1]
#         param = {
#             'componentIds': 'www-blog-recommend',
#             'cate1': f"{suffix}"
#         }
#         params.append(param)


def get(p):
    response = requests.get('https://cms-api.csdn.net/v1/web_home/select_content', headers=headers, params=p)
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

        # 查询是否存在url字段为1的记录
        result = conn.execute(PREVIEW.select().where(PREVIEW.c.url == item['url'])).fetchall()
        if len(result) == 0:
            conn.execute(PREVIEW.insert(), one)
            conn.commit()


# j = 20
# for p in params:
#     for i in range(100):
#         get(p)
#     j -= 1


def articleDownload():
    # result = conn.execute(PREVIEW.select(PREVIEW.c.url).where(PREVIEW.c.views > 50000)).fetchall()
    result = conn.execute(session.query(PREVIEW.c.url).filter(PREVIEW.c.views > 50000)).fetchall()
    for item in result:
        response = requests.get(item, headers=headers)
        selector = Selector(text=response.text)
        # html
        article = selector.xpath("//div[@id='content_views]").extract_first()
        # html to md
        md = markdownify(article)
        with open(f"X:\\spider-data\\article\\{item['title']}.md", 'w') as f:
            f.write(md)


def top10():
    result = r.zrevrange('csdn', 0, 9)
    for item in result:
        print(item)


# top10()

if __name__ == '__main__':
    articleDownload()
