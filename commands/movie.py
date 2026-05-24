from telegram import (
    Update,
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

    cast_text = "\n".join(
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

        poster_url = None

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
<b>{title}</b>

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

    # SEND

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