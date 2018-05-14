import redis

from functools import reduce

def decode(str):
  return str.decode('utf-8')

class TokenStore:
  def __init__(self):
    self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)

  def storeToken(self, token, page):
    if self.r.rpush(token, page) is False:
      raise RuntimeError('Error: Failed to storeIndex(token: %s, page: %s)!', token, page)

  def tokens(self):
    return map(lambda x: decode(x), self.r.scan_iter('token:*'))

  def tokenOccurrencePairs(self):
    for token in self.tokens():
      occurrence = self.r.lrange(token, 0, -1)
      yield (token, map(lambda x: decode(x), occurrence))

  def getTokensOnPage(self, page):
    return (key for key, val in self.tokenOccurrencePairs() if str(page) in val)
