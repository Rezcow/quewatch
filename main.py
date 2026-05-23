from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from dotenv import load_dotenv
from commands.movie import movie

from flask import Flask
from threading import Thread

import os

load_dotenv()

# FLASK APP

flask_app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")

TRAKT_CLIENT_ID = os.getenv(
    "TRAKT_CLIENT_ID"
)


@flask_app.route("/")
def home():
    return "QueWatch Online"


def run_web():

    flask_app.run(
        host="0.0.0.0",
        port=10000
    )


# START

async def start(update, context):

    await update.message.reply_text(
        "🎬 QueWatch online."
    )


# CONNECT TRAKT

async def connect(update, context):

    trakt_auth_url = (
        "https://trakt.tv/oauth/authorize"
        f"?response_type=code"
        f"&client_id={TRAKT_CLIENT_ID}"
        f"&redirect_uri=http://localhost:8080/callback"
    )

    buttons = [[
        InlineKeyboardButton(
            "🔗 Connect Trakt",
            url=trakt_auth_url
        )
    ]]

    markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "Conecta tu cuenta Trakt:",
        reply_markup=markup
    )


# WATCHLIST CALLBACK

async def watchlist_callback(update, context):

    query = update.callback_query

    await query.answer()

    movie_id = query.data.replace(
        "watch_",
        ""
    )

    await query.message.reply_text(
        f"✅ Agregado a Watchlist\n\nID: {movie_id}"
    )


# APP

app = (
    Application.builder()
    .token(TOKEN)
    .build()
)


# HANDLERS

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("movie", movie)
)

app.add_handler(
    CommandHandler("connect", connect)
)

app.add_handler(
    CallbackQueryHandler(
        watchlist_callback,
        pattern="^watch_"
    )
)


# START FLASK THREAD

Thread(target=run_web).start()

print("QueWatch iniciado...")

app.run_polling()