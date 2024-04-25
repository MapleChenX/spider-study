import redis

rredis = redis.Redis(host='localhost', port=6379)

data = ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5']

for item in data:
    rredis.publish('my_channel', item)