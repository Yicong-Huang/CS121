import redis
import json

r = redis.Redis().pipeline()
bookkeeping = json.load(open('./src/WEBPAGES_RAW/bookkeeping.json', 'r'))

bookkeeping = {"p:"+page: url for page, url in bookkeeping.items()}

for key, val in bookkeeping.items():
    r.set(key, val)

r.execute()
