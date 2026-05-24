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

            media_id = item["id"]

            details = get_details(
                media_type,
                media_id
            )

            credits = get_credits(
                media_type,
                media_id
            )

            # TITLE

            if media_type == "movie":

                title = details.get(
                    "title",
                    "Unknown"
                )

                release = details.get(
                    "release_date",
                    "?"
                )

                media_label = "🎬 Movie"

                runtime = details.get(
                    "runtime",
                    0
                )

                runtime_text = (
                    f"⏱ {runtime} min"
                    if runtime
                    else ""
                )

            else:

                title = details.get(
                    "name",
                    "Unknown"
                )

                release = details.get(
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

                runtime_text = (
                    f"📚 {seasons} temporadas\n"
                    f"🎞 {episodes} episodios"
                )

            # STATUS

            status = details.get(
                "status",
                ""
            )

            if status == "Returning Series":

                status_text = "📡 Returning Series"

            elif status == "Ended":

                status_text = "🏁 Ended"

            elif status == "Released":

                status_text = "✅ Released"

            elif status == "Planned":

                status_text = "🚧 Upcoming"

            else:

                status_text = status

            # NEXT EPISODE

            next_episode = details.get(
                "next_episode_to_air"
            )

            next_episode_text = ""

            if next_episode:

                ep_name = next_episode.get(
                    "name",
                    "?"
                )

                ep_date = next_episode.get(
                    "air_date",
                    "?"
                )

                ep_season = next_episode.get(
                    "season_number",
                    "?"
                )

                ep_number = next_episode.get(
                    "episode_number",
                    "?"
                )

                next_episode_text = (
                    f"\n📅 Próximo episodio:\n"
                    f"S{ep_season}"
                    f"E{ep_number}"
                    f" — {ep_name}\n"
                    f"{ep_date}"
                )

            # RATING

            rating = round(
                details.get(
                    "vote_average",
                    0
                ),
                1
            )

            # OVERVIEW

            overview = details.get(
                "overview",
                "Sin descripción."
            )

            if len(overview) > 220:

                overview = (
                    overview[:220]
                    + "..."
                )

            # GENRES

            genres = details.get(
                "genres",
                []
            )

            genre_names = [
                genre["name"]
                for genre in genres[:3]
            ]

            genres_text = " • ".join(
                genre_names
            )

            # CAST

            cast = credits.get(
                "cast",
                []
            )

            top_cast = [
                actor["name"]
                for actor in cast[:4]
            ]

            cast_text = ", ".join(
                top_cast
            )

            # DIRECTOR

            director = ""

            crew = credits.get(
                "crew",
                []
            )

            for person in crew:

                if person.get("job") == "Director":

                    director = person.get(
                        "name"
                    )

                    break

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

            markup = InlineKeyboardMarkup(
                buttons
            )

            # MESSAGE

            text = f"""
<a href="{poster_url}">‎</a>

<b>{title}</b>

{media_label}

⭐ <b>{rating}/10</b>

📅 {release}

{status_text}

{runtime_text}

🎭 {genres_text}

🎬 {director}

👥 {cast_text}

📖 {overview}

{next_episode_text}
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

        await update.inline_query.answer(
            inline_results,
            cache_time=1
        )

    except Exception as e:

        print("INLINE ERROR:")
        print(e)