import os
import sys

from flask import request
from flask_api import FlaskAPI

sys.path.append(os.path.abspath("../indexer/src"))
from searchengine import SearchEngine
from tokenstore import TokenStore

app = FlaskAPI(__name__)


@app.route("/")
def index():
    return app.send_static_file('htmls/index.html')


@app.route("/api/search", methods=["POST"])
def search() -> list:
    """
    curl -X POST http://127.0.0.1:5000/api/search -d  queries="hello world"
    """
    return search_engine.search(request.data.get("queries").lower().split(","))


if __name__ == "__main__":
    store = TokenStore()
    search_engine = SearchEngine(store)

    app.run(debug=True, host="0.0.0.0")
