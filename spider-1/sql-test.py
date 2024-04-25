import json
from time import sleep

import pymysql
import requests
from markdownify import markdownify
from scrapy import Selector
import redis
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='111111',
    database='spider',
    charset='utf8mb4',  # 设置字符集，避免中文乱码
    cursorclass=pymysql.cursors.DictCursor  # 返回字典类型的游标，方便使用键值对访问结果
)
rredis = redis.Redis(host='localhost', port=6379)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

url = 'https://www.csdn.net/'


def home():
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    ul_def_sel = selector.xpath("//ul[@class='def']")
    hrefs = ul_def_sel.xpath("//li/a/@href").extract()
    # list join queue
    for i in hrefs:
        rredis.lpush('csdn_home', i)

def comsumer1():
    res = requests.get(rredis.lpop('csdn_home'))
    selector = Selector(text=res.text)
    community = selector.xpath("//div[@class='Community']")
    a = community.xpath("//*[@class=' active-blog']//*[@class='content']/a")

    hrefs = a.xpath("//@href").extract()
    titles = a.xpath("//*[@class='blog-text']/text()").extract()
    # 组装hrefs和title为字典数组
    for href, title in zip(hrefs, titles):
        a = {"href": href, "title": title}
        # 信息单体载入redis
        rredis.lpush('csdn_preview', a)

        # 数据持久化，但是这个表我还没创建
        with conn.cursor() as cursor:
            sql = "INSERT INTO `csdn` (`url`, `title`) VALUES (%s, %s)"
            cursor.execute(sql, (href, title))
        conn.commit()


if __name__ == '__main__':
    a = {"href": "https://blog.csdn.net/", "title": "CSDN"}

    rredis.lpush('csdn_home', json.dumps(a))
    g1 = rredis.lpop('csdn_home').decode('utf-8')
    g1_dict = json.loads(g1)
    print(g1)

    # print('\n')
    # g1 = rredis.lpop('csdn_home').decode('utf-8')
    # print(g1)
    # produce home url
    home()

    # 多线程编程
    # 一个comsumer1就是一个任务
    executor = ThreadPoolExecutor(max_workers=10)
    executor.submit(comsumer1)
    executor.submit(comsumer1)



