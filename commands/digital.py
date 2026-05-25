from telegram import (
    Update
)

from telegram.ext import (
    ContextTypes
)

from services.digital import (
    search_digital_release
)


async def digital(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(
        context.args
    )

    if not query:

        await update.message.reply_text(
            "Uso: /digital dune"
        )

        return

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