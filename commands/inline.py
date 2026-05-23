from telegram import (
    InlineQueryResultPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from commands.movie import (
    search_content
)

import uuid


async def inline_search(update,
                        context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query.query

    if not query:
        return

    try:

        results = search_content(query)

        inline_results = []

        for item in results[:10]:

            media_type = item.get(
                "media_type"
            )

            if media_type not in [
                "movie",
                "tv"
            ]:
                continue

            # MOVIES

            if media_type == "movie":

                title = item.get(
                    "title",
                    "Unknown"
                )

                release = item.get(
                    "release_date",
                    "?"
                )

                media_label = "🎬 Movie"

            # TV

            else:

                title = item.get(
                    "name",
                    "Unknown"
                )

                release = item.get(
                    "first_air_date",
                    "?"
                )

                media_label = "📺 TV"

            rating = round(
                item.get(
                    "vote_average",
                    0
                ),
                1
            )

            overview = item.get(
                "overview",
                "No description."
            )

            if not overview:
                overview = "No description."

            poster_path = item.get(
                "poster_path"
            )

            if poster_path:

                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

            else:

                poster_url = (
                    "https://via.placeholder.com/500x750?text=No+Image"
                )

            tmdb_id = item.get("id")

            tmdb_url = (
                f"https://www.themoviedb.org/"
            )

            if media_type == "movie":

                tmdb_url += f"movie/{tmdb_id}"

            else:

                tmdb_url += f"tv/{tmdb_id}"

            caption = f"""
<b>{title}</b>

{media_label}

⭐ <b>{rating}/10</b>

📅 {release}

📖 {overview}
"""

            buttons = [

                [
                    InlineKeyboardButton(
                        "🍿 TMDB",
                        url=tmdb_url
                    )
                ],

                [
                    InlineKeyboardButton(
                        "🔎 Buscar Trailer",
                        url=(
                            "https://www.youtube.com/results"
                            f"?search_query={title}+trailer"
                        )
                    )
                ]
            ]

            markup = InlineKeyboardMarkup(
                buttons
            )

            inline_results.append(

                InlineQueryResultPhoto(

                    id=str(uuid.uuid4()),

                    photo_url=poster_url,

                    thumbnail_url=poster_url,

                    title=title,

                    description=(
                        f"{media_label} • "
                        f"{release}"
                    ),

                    caption=caption,

                    parse_mode="HTML",

                    reply_markup=markup
                )
            )

        await update.inline_query.answer(
            inline_results,
            cache_time=1
        )

    except Exception as e:

        print("INLINE ERROR:")
        print(e)