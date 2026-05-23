from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

import requests
import os

from dotenv import load_dotenv

load_dotenv()

TMDB_API = os.getenv("TMDB_API_KEY")


# SEARCH CONTENT

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


# GET TRAILER

def get_trailer(media_type, media_id):

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


# GET WATCH PROVIDERS

def get_watch_url(media_type, media_id):

    return (
        f"https://www.themoviedb.org/"
        f"{media_type}/{media_id}/watch"
    )


# GET SIMILAR URL

def get_similar_url(media_type, media_id):

    return (
        f"https://www.themoviedb.org/"
        f"{media_type}/{media_id}/recommendations"
    )


# MOVIE COMMAND

async def movie(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    if not query:

        await update.message.reply_text(
            "Uso: /movie interstellar"
        )

        return

    results = search_content(query)

    if not results:

        await update.message.reply_text(
            "No encontrado."
        )

        return

    item = results[0]

    media_type = item["media_type"]

    if media_type == "movie":

        title = item["title"]
        release = item.get(
            "release_date",
            "?"
        )

    else:

        title = item["name"]
        release = item.get(
            "first_air_date",
            "?"
        )

    rating = round(
        item["vote_average"],
        1
    )

    overview = item.get(
        "overview",
        "Sin descripción."
    )

    media_id = item["id"]

    poster_path = item.get("poster_path")

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

    else:

        poster_url = None

    trailer_url = get_trailer(
        media_type,
        media_id
    )

    watch_url = get_watch_url(
        media_type,
        media_id
    )

    similar_url = get_similar_url(
        media_type,
        media_id
    )

    media_label = (
        "🎬 Película"
        if media_type == "movie"
        else "📺 Serie"
    )

    text = f"""
<b>{title}</b>

{media_label}

⭐ <b>{rating}/10</b>

📅 {release}

📖 {overview}
"""

    buttons = []

    if trailer_url:

        buttons.append([
            InlineKeyboardButton(
                "🎬 Trailer",
                url=trailer_url
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "📺 Watch",
            url=watch_url
        ),

        InlineKeyboardButton(
            "🎲 Similar",
            url=similar_url
        )
    ])

    markup = InlineKeyboardMarkup(
        buttons
    )

    if poster_url:

        await update.message.reply_photo(
            photo=poster_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=markup
        )

    else:

        await update.message.reply_text(
            text=text,
            parse_mode="HTML",
            reply_markup=markup
        )