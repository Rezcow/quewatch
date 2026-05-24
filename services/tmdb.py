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

    all_results = {}

    # ENGLISH SEARCH

    params_en = {
        "api_key": TMDB_API,
        "query": query,
        "language": "en-US"
    }

    response_en = requests.get(
        url,
        params=params_en
    )

    data_en = response_en.json()

    for item in data_en.get(
        "results",
        []
    ):

        media_type = item.get(
            "media_type"
        )

        if media_type not in [
            "movie",
            "tv"
        ]:
            continue

        unique_key = (
            f"{media_type}_"
            f"{item.get('id')}"
        )

        all_results[unique_key] = item

    # SPANISH SEARCH
    # OVERWRITE ENGLISH RESULTS
    # SO WE KEEP SPANISH TITLES

    params_es = {
        "api_key": TMDB_API,
        "query": query,
        "language": "es-ES"
    }

    response_es = requests.get(
        url,
        params=params_es
    )

    data_es = response_es.json()

    for item in data_es.get(
        "results",
        []
    ):

        media_type = item.get(
            "media_type"
        )

        if media_type not in [
            "movie",
            "tv"
        ]:
            continue

        unique_key = (
            f"{media_type}_"
            f"{item.get('id')}"
        )

        # SPANISH REPLACES ENGLISH

        all_results[unique_key] = item

    filtered = list(
        all_results.values()
    )

    # SMART SORT

    query_lower = query.lower()

    def score(item):

        title = (
            item.get("title")
            or item.get("name")
            or ""
        ).lower()

        original = (
            item.get("original_title")
            or item.get("original_name")
            or ""
        ).lower()

        popularity = item.get(
            "popularity",
            0
        )

        vote_count = item.get(
            "vote_count",
            0
        )

        points = 0

        if query_lower == title:

            points += 1000

        if query_lower == original:

            points += 1000

        if query_lower in title:

            points += 500

        if query_lower in original:

            points += 500

        points += popularity

        points += (
            vote_count / 100
        )

        return points

    filtered.sort(
        key=score,
        reverse=True
    )

    return filtered


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