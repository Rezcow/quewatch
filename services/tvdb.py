import requests
import os

from dotenv import load_dotenv

load_dotenv()

TVDB_API_KEY = os.getenv(
    "TVDB_API_KEY"
)


# TOKEN

def get_tvdb_token():

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

    return data["data"]["token"]


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


# SERIES DETAILS

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