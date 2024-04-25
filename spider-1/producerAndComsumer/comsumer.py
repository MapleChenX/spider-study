import redis

rredis = redis.Redis(host='localhost', port=6379)

# Subscribe to the channel
pubsub = rredis.pubsub()
pubsub.subscribe('my_channel')

for message in pubsub.listen():
    if message['type'] == 'message':
        message = message["data"].decode("utf-8")
        print('Received data:', message)
