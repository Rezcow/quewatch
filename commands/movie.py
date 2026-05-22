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


async def movie(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Uso: /movie interstellar"
        )
        return

    search_url = (
        "https://api.themoviedb.org/3/search/movie"
    )

    params = {
        "api_key": TMDB_API,
        "query": query,
        "language": "es-ES"
    }

    response = requests.get(
        search_url,
        params=params
    )

    data = response.json()

    if not data["results"]:
        await update.message.reply_text(
            "No encontrado."
        )
        return

    movie = data["results"][0]

    title = movie["title"]

    rating = round(
        movie["vote_average"],
        1
    )

    overview = movie["overview"]

    release = movie["release_date"]

    movie_id = movie["id"]

    poster_url = (
        "https://image.tmdb.org/t/p/w500"
        + movie["poster_path"]
    )

    # TRAILER

    video_url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/videos"
    )

    video_params = {
        "api_key": TMDB_API
    }

    video_response = requests.get(
        video_url,
        params=video_params
    )

    video_data = video_response.json()

    trailer_url = None

    for video in video_data["results"]:

        if (
            video["site"] == "YouTube"
            and video["type"] == "Trailer"
        ):

            trailer_url = (
                "https://youtube.com/watch?v="
                + video["key"]
            )

            break

    text = f"""
🎬 <b>{title}</b>

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
            "✅ Add to Watchlist",
            callback_data=f"watch_{movie_id}"
        )
    ])

    markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_photo(
        photo=poster_url,
        caption=text,
        parse_mode="HTML",
        reply_markup=markup
    )