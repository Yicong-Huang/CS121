import redis
import json

r = redis.Redis()
print('Loading bookkeeping.json...')
bookkeeping = json.load(open('./src/WEBPAGES_RAW/bookkeeping.json', 'r'))
print('Loaded bookkeeping.json.')

print('Saving bookkeeping.json into redis...')
r.set('file:bookkeeping.json', str(bookkeeping))
print('Saved bookkeeping.json into redis.')
