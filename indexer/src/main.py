from tokenstore import TokenStore

store = TokenStore()
store.storeToken('token:123', '2')
store.storeToken('token:123', '1')
store.storeToken('token:123', '3')
store.storeToken('token:123', '1')
store.storeToken('token:123', '2')

store.storeToken('token:456', '1')
store.storeToken('token:456', '1')
store.storeToken('token:456', '1')
store.storeToken('token:234', '1')
store.storeToken('token:900', '1')

print(list(store.tokens()))

print(list(store.getTokensOnPage(1)))
