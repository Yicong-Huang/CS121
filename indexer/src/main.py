from tokenstore import TokenStore

store = TokenStore()
store.storeToken('123', '2')
store.storeToken('123', '1')
store.storeToken('123', '3')
store.storeToken('123', '1')
store.storeToken('123', '2')

store.storeToken('456', '1')
store.storeToken('456', '1')
store.storeToken('456', '1')
store.storeToken('234', '1')
store.storeToken('900', '1')

# print(list(store.tokens()))

# print(list(store.getTokensOnPage(1)))

# print(store.tf('900', '1'))

print(store.idf(1,2))
