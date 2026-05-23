from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler
)

from dotenv import load_dotenv

from commands.movie import movie
from commands.inline import inline_search

from flask import Flask
from threading import Thread

import os

load_dotenv()

# FLASK

flask_app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")


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


# APP

app = (
    Application.builder()
    .token(TOKEN)
    .build()
)


# HANDLERS

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CommandHandler(
        "movie",
        movie
    )
)

app.add_handler(
    InlineQueryHandler(
        inline_search
    )
)


# START FLASK

Thread(
    target=run_web
).start()

print("QueWatch iniciado...")

app.run_polling()