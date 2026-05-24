import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

TVDB_API_KEY = os.getenv(
    "TVDB_API_KEY"
)

# CACHE TOKEN

TVDB_TOKEN = None
TVDB_TOKEN_TIME = 0


# GET TOKEN

def get_tvdb_token():

    global TVDB_TOKEN
    global TVDB_TOKEN_TIME

    # REUSE TOKEN 23 HOURS

    if (
        TVDB_TOKEN
        and (
            time.time()
            - TVDB_TOKEN_TIME
        ) < 82800
    ):

        return TVDB_TOKEN

    url = (
        "https://api4.thetvdb.com/v4/login"
    )

    payload = {
        "apikey": TVDB_API_KEY
    }

    response = requests.post(
        url,
        json=payload
    )

    data = response.json()

    token = data["data"]["token"]

    TVDB_TOKEN = token

    TVDB_TOKEN_TIME = time.time()

    return token


# SEARCH SERIES

def search_tvdb_series(name):

    token = get_tvdb_token()

    url = (
        "https://api4.thetvdb.com/v4/search"
    )

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    params = {
        "query": name,
        "type": "series"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    return data.get(
        "data",
        []
    )


# GET SERIES DETAILS

def get_tvdb_series(series_id):

    token = get_tvdb_token()

    url = (
        f"https://api4.thetvdb.com/v4/"
        f"series/{series_id}/extended"
    )

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers
    )

    data = response.json()

    return data.get(
        "data",
        {}
    )


# DETECT ANIME

def is_anime(details):

    genres = details.get(
        "genres",
        []
    )

    genre_names = [
        genre.get(
            "name",
            ""
        )
        for genre in genres
    ]

    origin = details.get(
        "originalCountry",
        ""
    )

    return (
        "Animation"
        in genre_names
        and origin == "jpn"
    )


# GET ANIME INFO

def get_anime_info(title):

    results = search_tvdb_series(
        title
    )

    if not results:

        return None

    anime = results[0]

    tvdb_id = anime.get(
        "tvdb_id"
    )

    if not tvdb_id:

        return None

    details = get_tvdb_series(
        tvdb_id
    )

    seasons = details.get(
        "seasons",
        []
    )

    real_seasons = []

    total_episodes = 0

    for season in seasons:

        season_number = season.get(
            "number",
            0
        )

        # IGNORE SPECIALS

        if season_number <= 0:

            continue

        # EPISODE COUNT

        episode_count = (
            season.get(
                "episodes",
                0
            )
            or season.get(
                "episodeCount",
                0
            )
            or 0
        )

        # IGNORE EMPTY /
        # FUTURE PLACEHOLDERS

        if episode_count <= 0:

            continue

        # IGNORE WEIRD
        # DUPLICATE COURS

        season_name = str(
            season.get(
                "name",
                ""
            )
        ).lower()

        if (
            "special"
            in season_name
        ):

            continue

        real_seasons.append(
            season
        )

        total_episodes += (
            episode_count
        )

    return {

        "season_count":
        len(real_seasons),

        "episode_count":
        total_episodes,

        "tvdb_data":
        details
    }