from flask.templating import render_template
import requests
from flask import Flask
from pprint import PrettyPrinter

API_KEY = "833dd9a67ff574327361b76a61d6cb13"

pp = PrettyPrinter(indent=4)

app = Flask(__name__)
# pp = PrettyPrinter(indent=4)


class MovieDB:
    API_KEY = "833dd9a67ff574327361b76a61d6cb13"

    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3/"


class Search(MovieDB):
    def movie(self, query):


#     movieinfo = requests.get(
#         f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=en-US&append_to_response=videos%2Cimage

    def getMovieID(self, query):

        query.replace(" ", "%")
        query.replace("'", "%27")

        path = f"/search/movie?{API_KEY}&query={query}&page=1"

        movieid = requests.get(self.base_url + path).json()

        movieid = movieid["results"][0]["id"]

        return movieid


# @app.route("/<query>", methods=["GET"])
# def search(query):
#     searchterm = str(query)
#     movieid = requests.get(
#         f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={searchterm}&page=1"
#     )

#     tempid = movieid.json()

#     id = tempid["results"][0]["id"]

#     movieinfo = requests.get(
#         f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=en-US&append_to_response=videos%2Cimages"
#     )

#     imagepath = requests.get(
#         f"https://api.themoviedb.org/3/configuration?api_key=833dd9a67ff574327361b76a61d6cb13"
#     ).json()

#     movieinfo = movieinfo.json()

#     pp.pprint(movieinfo)

#     print()

#     # trailer = requests.get(f"http")

#     # pp.pprint(tempid["results"])
#     print()
#     results = tempid["results"]
#     overview = results[0]
#     # pp.pprint(overview["overview"])
#     # print()
#     # pp.pprint(overview)

#     # movieinfo = requests.get(
#     #     f"https://api.themoviedb.org/3/movie/{movieid}/credits?api_key=833dd9a67ff574327361b76a61d6cb13&language=en-US"
#     # )
#     # print(movieinfo)
#     # tempinfo = movieinfo.json()
#     # print(tempinfo)

#     context = {
#         # "movieinfo": tempinfo,
#         "overview": overview,
#     }
#     return render_template("page.html", **context)


# # movieinfo = requests.get(
# #     f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query=what%20we%20do%20in%20the%20shadows&page=1"
# # )