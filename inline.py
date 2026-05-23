from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent
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

        text = f"""
<b>{title}</b>

{media_label}

⭐ <b>{rating}/10</b>

📅 {release}

📖 {overview}
"""

        inline_results.append(

            InlineQueryResultArticle(

                id=str(uuid.uuid4()),

                title=title,

                description=(
                    f"{media_label} • "
                    f"{release}"
                ),

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