from flask import Flask, request, render_template
import requests

TMDB_API_KEY = "833dd9a67ff574327361b76a61d6cb13"
OMDB_API_KEY = "e91e99e3"

app = Flask(__name__)


@app.route("/")
def home():
    """
    First served page with the search box
    """
    return render_template("base.html")


@app.route("/search")
def getMovieInfo():
    """
    Converts query to movie ID, looks it up using the two API's
    and sends relevant information
    to the results movie page.

    Args:
        None - function is called in the base.html
        search box with the query

    Returns:
        movie.html - Result page of the searched movie
    """
    query = request.args["search"]
    id = getMovieID(query)

    path = f"https://api.themoviedb.org/3/movie/{id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=videos%2Cimage"
    movieInfo = requests.get(path).json()

    ratings = getRatings(movieInfo["imdb_id"])
    streamSources = getMovieSources(id)
    movieCast = getMovieCast(id)
    suggestedMovies = getMovieRecommendations(id)

    context = {
        "movieInfo": movieInfo,
        "moviePoster": f"https://image.tmdb.org/t/p/w500" + movieInfo["poster_path"],
        "movieTrailer": f"https://youtube.com/embed/"
        + str(movieInfo["videos"]["results"][0]["key"]),
        "ratings": ratings,
        "streamSources": streamSources,
        "movieCast": movieCast,
        "suggestedMovies": suggestedMovies,
    }
    return render_template("movie.html", **context)


def getMovieID(query):
    """
    Helper function to convert the user query into a
    usable ID number for API lookups

    Args:
        query: String representation of the user's desired
                    movie to lookup
    Returns:
        movieID: Integer ID for TMDB lookup
    """
    path = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&page=1"
    movieJSON = requests.get(path).json()
    movieID = movieJSON["results"][0]["id"]
    return movieID


def getRatings(id):
    """
    Helper function to pull ratings from IMDB,
    Rotten Tomatoes, and Metacritic from OMDB

    Args:
        id: Integer movie ID for OMDB lookup

    Returns:
        ratingResults: List of dictionaries holding the
                    source, rating of each website as
                    key, value pairs
    """
    path = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={id}"
    imdbJSON = requests.get(path).json()
    ratingResults = imdbJSON["Ratings"]
    return ratingResults


def getMovieSources(id):
    """
    Helper function to gather streaming/purchase availability from TMDB

    Args:
        id: Integer movie ID for TMDB source lookup

    Returns:
        streamSources: List of dictionaries holding the sources
                    where the movie is available for some kind of
                    purchase, rent, or stream. Feeds to a generic page
                    TMDB page as there is no API to query streaming services for
                    their movie links
    """
    path = f" https://api.themoviedb.org/3/movie/{id}/watch/providers?api_key={TMDB_API_KEY}"
    streamJSON = requests.get(path).json()
    streamSources = streamJSON["results"]["US"]
    return streamSources


def getMovieCast(id):
    """
    Helper function to get the movie cast from TMDB

    Args:
        id: Integer movie ID for TMDB source lookup

    Returns:
        castList: List of dictionaries holding the
        cast, including names, character played,
        and profile pictures.
    """
    path = f" https://api.themoviedb.org/3/movie/{id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    creditsJSON = requests.get(path).json()
    castList = creditsJSON["cast"]
    return castList


def getMovieRecommendations(id):
    """
    Helper function to get the recommendations from TMDB

    Args:
        id: Integer movie ID for TMDB source lookup

    Returns:
        suggestionsList: List of dictionaries holding the
                movies recommended to the user if they
                liked this one.
    """
    path = f"https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={TMDB_API_KEY}&language=en-US&page=1"
    suggestionsJSON = requests.get(path).json()
    suggestionsList = suggestionsJSON["results"]
    return suggestionsList


@app.route("/contact")
def contactForm():
    """
    Contact form, not functional
    """
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)