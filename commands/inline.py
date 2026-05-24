from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from services.tmdb import (
    search_content,
    get_details,
    get_credits,
    get_trailer,
    get_watch_url,
    get_similar_url
)

import traceback
import uuid


async def inline_search(update,
                        context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query.query

    if not query:
        return

    try:

        results = search_content(query)

        inline_results = []

        # LIMIT RESULTS
        # KEEP INLINE FAST

        for item in results[:5]:

            try:

                media_type = item.get(
                    "media_type"
                )

                if media_type not in [
                    "movie",
                    "tv"
                ]:
                    continue

                media_id = item["id"]

                # DETAILS

                details = get_details(
                    media_type,
                    media_id
                )

                # MOVIE

                if media_type == "movie":

                    title = item.get(
                        "title",
                        "Unknown"
                    )

                    original_title = details.get(
                        "original_title",
                        title
                    )

                    release = item.get(
                        "release_date",
                        "?"
                    )

                    media_label = "🎬 Movie"

                    runtime = details.get(
                        "runtime",
                        0
                    )

                    extra_info = ""

                    if runtime:

                        extra_info = (
                            f"⏱ {runtime} min"
                        )

                # TV

                else:

                    title = item.get(
                        "name",
                        "Unknown"
                    )

                    original_title = details.get(
                        "original_name",
                        title
                    )

                    release = item.get(
                        "first_air_date",
                        "?"
                    )

                    media_label = "📺 TV"

                    seasons = details.get(
                        "number_of_seasons",
                        0
                    )

                    episodes = details.get(
                        "number_of_episodes",
                        0
                    )

                    extra_info = ""

                    if seasons > 0:

                        extra_info += (
                            f"📚 {seasons} temporadas\n"
                        )

                    if episodes > 0:

                        extra_info += (
                            f"🎞 {episodes} episodios"
                        )

                # STATUS

                status = details.get(
                    "status",
                    ""
                )

                if status == "Returning Series":

                    status_text = (
                        "📡 Returning Series"
                    )

                elif status == "Ended":

                    status_text = (
                        "🏁 Ended"
                    )

                elif status == "Released":

                    status_text = (
                        "✅ Released"
                    )

                elif status == "Planned":

                    status_text = (
                        "🚧 Upcoming"
                    )

                elif status == "In Production":

                    status_text = (
                        "🎥 In Production"
                    )

                else:

                    status_text = status

                # RATING

                rating = round(
                    details.get(
                        "vote_average",
                        0
                    ),
                    1
                )

                # OVERVIEW

                overview = item.get(
                    "overview",
                    "Sin descripción."
                )

                if not overview:

                    overview = (
                        "Sin descripción."
                    )

                # LONGER OVERVIEW

                if len(overview) > 900:

                    overview = (
                        overview[:900]
                        + "..."
                    )

                # GENRES

                genres = item.get(
                    "genre_ids",
                    []
                )

                genre_map = {
                    28: "Acción",
                    12: "Aventura",
                    16: "Animación",
                    35: "Comedia",
                    80: "Crimen",
                    18: "Drama",
                    14: "Fantasía",
                    27: "Horror",
                    9648: "Misterio",
                    10749: "Romance",
                    878: "Ciencia ficción",
                    53: "Thriller"
                }

                genre_names = []

                for genre_id in genres[:3]:

                    if genre_id in genre_map:

                        genre_names.append(
                            genre_map[genre_id]
                        )

                genres_text = " • ".join(
                    genre_names
                )

                # POSTER

                poster_path = details.get(
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

                # BUTTONS

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
                        "🧠 Similar",
                        url=similar_url
                    )
                ])

                # ADVANCED BUTTON

                buttons.append([

                    InlineKeyboardButton(
                        "📖 Anime Details",
                        switch_inline_query_current_chat=(
                            f"/movie {title}"
                        )
                    )
                ])

                markup = InlineKeyboardMarkup(
                    buttons
                )

                # MESSAGE

                text = f"""
<a href="{poster_url}">‎</a>

<b>{title}</b>

<blockquote>{original_title}</blockquote>

{media_label}

⭐ <b>{rating}/10</b>

📅 {release}

{status_text}

{extra_info}

🎭 {genres_text}

📖 {overview}
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

                        reply_markup=markup,

                        input_message_content=(
                            InputTextMessageContent(
                                message_text=text,
                                parse_mode="HTML"
                            )
                        )
                    )
                )

            except Exception:

                traceback.print_exc()

                continue

        await update.inline_query.answer(
            inline_results,
            cache_time=1
        )

    except Exception:

        print("INLINE ERROR:")
        traceback.print_exc()