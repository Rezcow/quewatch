from telegram import (
    Update
)

from telegram.ext import (
    ContextTypes
)

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
                "No upcoming releases found."
            )

            return

        text = (
            "🔥 Próximos estrenos digitales\n\n"
        )

        for item in results:

            text += (
                f"🎬 {item['title']}\n"
                f"📅 {item['release']}\n"
                f"🔗 {item['link']}\n\n"
            )

        await update.message.reply_text(
            text
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

    text = "🔥 Digital Releases\n\n"

    for item in results:

        text += (
            f"🎬 {item['title']}\n"
            f"📅 {item['release']}\n"
            f"🔗 {item['link']}\n\n"
        )

    await update.message.reply_text(
        text
    )