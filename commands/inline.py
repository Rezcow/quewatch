from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent
)

from telegram.ext import ContextTypes

from commands.movie import (
    search_content,
    get_trailer,
    get_watch_url,
    get_similar_url
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

            media_id = item["id"]

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
                    "https://via.placeholder.com/300x450"
                )

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

            text = f"""
<a href="{poster_url}">‎</a>

<b>{title}</b>

{media_label}

⭐ <b>{rating}/10</b>

📅 {release}

📖 {overview}

🎬 Trailer:
{trailer_url if trailer_url else "No disponible"}

📺 Watch:
{watch_url}

🎲 Similar:
{similar_url}
"""

            inline_results.append(

                InlineQueryResultArticle(

                    id=str(uuid.uuid4()),

                    title=title,

                    description=(
                        f"{media_label} • "
                        f"{release} • "
                        f"{rating}/10"
                    ),

                    thumbnail_url=poster_url,

                    input_message_content=(
                        InputTextMessageContent(
                            message_text=text,
                            parse_mode="HTML"
                        )
                    )
                )
            )

        await update.inline_query.answer(
            inline_results,
            cache_time=1
        )

    except Exception as e:

        print("INLINE ERROR:")
        print(e)