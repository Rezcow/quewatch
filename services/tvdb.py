import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

TVDB_API_KEY = os.getenv(
    "TVDB_API_KEY"
)

TVDB_TOKEN = None
TVDB_TOKEN_TIME = 0


# TOKEN

def get_tvdb_token():

    global TVDB_TOKEN
    global TVDB_TOKEN_TIME

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


# SEARCH

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
        params=params,
        timeout=8
    )

    data = response.json()

    return data.get(
        "data",
        []
    )


# LIGHT SERIES INFO

def get_tvdb_series(series_id):

    token = get_tvdb_token()

    url = (
        f"https://api4.thetvdb.com/v4/"
        f"series/{series_id}"
    )

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=8
    )

    data = response.json()

    return data.get(
        "data",
        {}
    )


# EPISODES

def get_tvdb_episodes(series_id):

    token = get_tvdb_token()

    url = (
        f"https://api4.thetvdb.com/v4/"
        f"series/{series_id}/episodes/default"
    )

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=8
    )

    data = response.json()

    return data.get(
        "data",
        {}
    )


# ANIME INFO

def get_anime_info(title):

    try:

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

        # LIGHT DETAILS

        details = get_tvdb_series(
            tvdb_id
        )

        # EPISODES

        episode_data = get_tvdb_episodes(
            tvdb_id
        )

        episodes = episode_data.get(
            "episodes",
            []
        )

        # COUNT REAL SEASONS

        seasons_found = set()

        total_episodes = 0

        latest_episode = None

        for ep in episodes:

            season = ep.get(
                "seasonNumber",
                0
            )

            number = ep.get(
                "number",
                0
            )

            air_date = ep.get(
                "aired"
            )

            # IGNORE SPECIALS

            if season <= 0:

                continue

            if number <= 0:

                continue

            seasons_found.add(
                season
            )

            total_episodes += 1

            # FIND NEXT EP

            if air_date:

                try:

                    air_ts = (
                        time.mktime(
                            time.strptime(
                                air_date,
                                "%Y-%m-%d"
                            )
                        )
                    )

                    if (
                        air_ts
                        > time.time()
                    ):

                        latest_episode = ep
                        break

                except:

                    pass

        return {

            "season_count":
            len(seasons_found),

            "episode_count":
            total_episodes,

            "next_episode":
            latest_episode,

            "status":
            details.get(
                "status",
                {}
            ).get(
                "name",
                ""
            )
        }

    except Exception as e:

        print(
            "TVDB ERROR:"
        )

        print(e)

        return None