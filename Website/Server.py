from flask import request,redirect
from flask_api import FlaskAPI

from searchengine import SearchEngine
from tokenstore import TokenStore

app = FlaskAPI(__name__)


@app.route("/")
def index():
    return app.send_static_file('htmls/index.html')


@app.route("/api/search", methods=["POST"])
def search():
    """
    curl -X POST http://127.0.0.1:5000/api/search -d  queries="hello world"
    """
    queries = request.data.get("queries")
    return search_engine.show_search(queries) or []

@app.route("/api/go",methods=["POST"])
def go():

    redirect("search.html")


if __name__ == "__main__":
    store = TokenStore()
    search_engine = SearchEngine(store)

    app.run(debug=True)
