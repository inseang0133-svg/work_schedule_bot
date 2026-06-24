import os
import time
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

# ดึงค่าที่ตั้งเองก่อน ถ้าไม่มีให้ใช้ URL อัตโนมัติจาก Render
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or os.getenv("RENDER_EXTERNAL_URL")

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET",
    "work_schedule_secret"
)
LAST_ACTIVITY = 0

WAKEUP_THRESHOLD = 600
# 600 วินาที = 10 นาที

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    global LAST_ACTIVITY

    now = time.time()
    if now - LAST_ACTIVITY > WAKEUP_THRESHOLD:

        await update.message.reply_text(
            "👋 ฉันพร้อมสร้างรูปตารางงานแล้ว\n"
            "ส่งข้อมูลวันหยุดพนักงานมาได้เลย\n\n"
            "🔥ตัวอย่าง🔥:\n"
            "1.ฝน 4/10/14/25\n"
            "2.แก้ว 2/18/21/29\n"
            "3.ปาร์ตี้ 12/16/23/27\n"
            "หากผมเงียบ😴 หลังไม่ได้ใช้งานสักพัก\n"
            "💥ให้ส่งสติกเกอร์หรือข้อความอะไรก็ได้เพื่อปลุกฉัน แล้วรอฉันตอบ ค่อยส่งข้อมูล วันหยุด ผนง."
        )

    LAST_ACTIVITY = now
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
