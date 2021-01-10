from flask.templating import render_template
import requests
from flask import Flask
from pprint import PrettyPrinter

API_KEY = "833dd9a67ff574327361b76a61d6cb13"

pp = PrettyPrinter(indent=4)

app = Flask(__name__)
# pp = PrettyPrinter(indent=4)


@app.route("/<query>", methods=["GET"])
def search(query):
    searchterm = str(query)
    movieid = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={searchterm}&page=1&append_to_response=videos,images"
    )
    # print(movieid)

    # print()

    # pp.pprint(movieid)

    tempid = movieid.json()

    print()

    # pp.pprint(tempid["results"])
    print()
    results = tempid["results"]
    overview = results[0]
    pp.pprint(overview["overview"])

    # movieinfo = requests.get(
    #     f"https://api.themoviedb.org/3/movie/{movieid}/credits?api_key=833dd9a67ff574327361b76a61d6cb13&language=en-US"
    # )
    # print(movieinfo)
    # tempinfo = movieinfo.json()
    # print(tempinfo)

    context = {
        # "movieinfo": tempinfo,
        "overview": overview,
    }
    return render_template("page.html", **context)


# movieinfo = requests.get(
#     f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query=what%20we%20do%20in%20the%20shadows&page=1"
# )