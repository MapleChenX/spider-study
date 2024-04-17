import json

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def top10():
    result = r.zrevrange('csdn', 0, 9)
    for item in result:
        item_json = json.loads(item)
        print(item_json['title'])
        print(item_json['views'])
        print(item_json['url'])
top10()