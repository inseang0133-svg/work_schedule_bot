import os
from dotenv import load_dotenv
from core.parser import parse_input
from core.validator import validate_employees
from core.validator import validate_input
from core.schedule_engine import build_schedule

from renderer.image_renderer import (
    create_canvas,
    draw_month_layout
)
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

PORT = int(os.getenv("PORT", 10000))

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET",
    "work_schedule_secret"
)

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        text = update.message.text.strip()

        employees = parse_input(text)

        validate_input(employees)

        schedule = build_schedule(employees)

        image, draw = create_canvas(schedule)

        image = draw_month_layout(
            image,
            draw,
            schedule
        )

        output_path = "output/schedule.png"

        image.save(
            output_path,
            dpi=(300, 300)
        )

        await update.message.reply_photo(
            photo=open(output_path, "rb")
        )

    except Exception as e:

        await update.message.reply_text(
            str(e)
        )

def main():

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot Started (Webhook Mode)")

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=WEBHOOK_URL,
    secret_token=WEBHOOK_SECRET,
    drop_pending_updates=True
)


if __name__ == "__main__":
    main()
