import requests
import os

from dotenv import load_dotenv

load_dotenv()

TMDB_API = os.getenv(
    "TMDB_API_KEY"
)


# SEARCH

def search_content(query):

    url = (
        "https://api.themoviedb.org/3/search/multi"
    )

    params = {
        "api_key": TMDB_API,
        "query": query,
        "language": "es-ES"
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    return data["results"]


# DETAILS

def get_details(media_type,
                media_id):

    url = (
        f"https://api.themoviedb.org/3/"
        f"{media_type}/{media_id}"
    )

    params = {
        "api_key": TMDB_API,
        "language": "es-ES"
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()


# CREDITS

def get_credits(media_type,
                media_id):

    url = (
        f"https://api.themoviedb.org/3/"
        f"{media_type}/{media_id}/credits"
    )

    params = {
        "api_key": TMDB_API
    }

    response = requests.get(
        url,
        params=params
    )

    return response.json()


# TRAILER

def get_trailer(media_type,
                media_id):

    url = (
        f"https://api.themoviedb.org/3/"
        f"{media_type}/{media_id}/videos"
    )

    params = {
        "api_key": TMDB_API
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    for video in data["results"]:

        if (
            video["site"] == "YouTube"
            and video["type"] == "Trailer"
        ):

            return (
                "https://youtube.com/watch?v="
                + video["key"]
            )

    return None


# WATCH URL

def get_watch_url(media_type,
                  media_id):

    return (
        f"https://www.themoviedb.org/"
        f"{media_type}/{media_id}/watch"
    )


# SIMILAR URL

def get_similar_url(media_type,
                    media_id):

    return (
        f"https://www.themoviedb.org/"
        f"{media_type}/{media_id}"
    )