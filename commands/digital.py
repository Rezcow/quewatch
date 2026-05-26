from telegram import (
    Update
)

from telegram.ext import (
    ContextTypes
)

from collections import defaultdict

from services.digital import (
    search_digital_release,
    get_upcoming_digital
)


async def digital(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(
        context.args
    )

    # UPCOMING RELEASES

    if not query:

        results = get_upcoming_digital()

        if not results:

            await update.message.reply_text(
                "No se encontraron próximos estrenos digitales."
            )

            return

        text = (
            "🔥 <b>Próximos estrenos digitales</b>\n\n"
        )

        grouped = defaultdict(list)

        for item in results:

            date_key = item[
                "release_date"
            ].strftime(
                "%d %b %Y"
            ).upper()

            grouped[
                date_key
            ].append(item)

        for date_group in grouped:

            text += (
                f"📅 <b>{date_group}</b>\n\n"
            )

            for item in grouped[
                date_group
            ]:

                rating = item.get(
                    "rating",
                    "?"
                )

                text += (
                    f"🎬 <b>{item['title']}</b>\n"
                    f"⭐ {rating}/10\n"
                    f"🎥 Digital Release\n\n"
                )

        text += (
            "📡 Fuente: DVDReleaseDates"
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

        return

    # SEARCH MODE

    results = search_digital_release(
        query
    )

    if not results:

        await update.message.reply_text(
            "No encontrado."
        )

        return

    text = (
        "🔥 <b>Digital Releases</b>\n\n"
    )

    for item in results:

        text += (
            f"🎬 <b>{item['title']}</b>\n"
            f"📅 {item['release']}\n"
            f"🔗 {item['link']}\n\n"
        )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )