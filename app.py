from flask.templating import render_template
import requests
from flask import Flask
from pprint import PrettyPrinter
from urllib.parse import urlencode
from collections import ChainMap

TMDB_API_KEY = "833dd9a67ff574327361b76a61d6cb13"
OMDB_API_KEY = "e91e99e3"

pp = PrettyPrinter(indent=4)

app = Flask(__name__)


@app.route("/<query>", methods=["GET"])
def sanitizeQuery(query):
    safeQuery = {"query": {query}}
    urlencode(safeQuery)
    return safeQuery


def getMovieInfo(query):
    id = getMovieID(query)

    path = f"https://api.themoviedb.org/3/movie/{id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=videos%2Cimage"
    movieInfo = requests.get(path).json()
    # posterBase = requests.get(
    #     f"https://api.themoviedb.org/3/configuration?api_key=833dd9a67ff574327361b76a61d6cb13"
    # ).json()
    ratings = getRatings(movieInfo["imdb_id"])
    context = {
        "movieInfo": movieInfo,
        # "movieGenre": movieInfo["genres"][0]["name"],
        # "movieTitle": movieInfo["original_title"],
        # "movieOverview": movieInfo["overview"],
        "moviePoster": f"https://image.tmdb.org/t/p/w500" + movieInfo["poster_path"],
        "movieTrailer": f"https://youtube.com/embed/"
        + str(movieInfo["videos"]["results"][0]["key"]),
        "ratings": ratings,
    }
    return render_template("page.html", **context)


def getMovieID(query):
    path = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&page=1"
    movieid = requests.get(path).json()
    newid = movieid["results"][0]["id"]
    return newid

    # ratingJSON[imdbJSON["Ratings"][0]["Source"]] = ratings[0]["Value"]
    # ratingJSON[imdbJSON["Ratings"][1]["Source"]] = ratings[[1]["Value"]
    # ratingJSON[imdbJSON["Ratings"][2]["Source"]] = ratings[2]["Value"]


def getRatings(id):
    path = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={id}"
    imdbJSON = requests.get(path).json()
    ratingDict = imdbJSON["Ratings"]
    return ratingDict


if __name__ == "__main__":
    app.run(debug=True)