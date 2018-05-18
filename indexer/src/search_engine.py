

class Search_Engine:
    def __init__(self,store):
        self.token_store = store
        self.search_result = []

    def do_search(self,query):
        query = "token:"+query
        page_list = [value[0] for value in self.token_store._redis.zrevrange(query,0,-1,withscores=True)]

        #print(page_list)
        for page in page_list:
            decoded_page = self.token_store.decode(page)
            self.search_result.append(decoded_page[decoded_page.index(":")+1:])
        #self.search_result =  page_list
        #print(self.search_result)

    def do_show_result(self,limit):
        if len(self.search_result) == 0:
            print("NO Result Found")
        else:
            for index in range(min(len(self.search_result),limit)):
                #print(len(self.search_result))
                print(self.search_result[index])



