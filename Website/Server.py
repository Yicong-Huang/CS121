from flask import request,redirect
from flask_api import FlaskAPI

'''
delete next 4 lines if files are in the same folder
'''
import sys
import os
#print(os.path.abspath("..") + "/indexer/src")
sys.path.append(os.path.abspath("..")+"/indexer/src")


from searchengine import SearchEngine
from tokenstore import TokenStore

app = FlaskAPI(__name__)


@app.route("/")
def index():
    return app.send_static_file('htmls/index.html')


@app.route("/api/search", methods=["POST"])
def search():
    """
    curl -X POST http://0.0.0.0:5000/api/search -d  queries="hello world"
    """
    queries = request.data.get("queries")
    #print(queries)
    return search_engine.show_search(queries) or []


if __name__ == "__main__":
    store = TokenStore()
    search_engine = SearchEngine(store)

    app.run(debug=True,host="0.0.0.0")
