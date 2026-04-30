import cv2
import numpy as np
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

print("🚀 REAL TIME QR ALERT STARTED")

BOT_TOKEN = "8740908330:AAEdPDwfzmA-rfzy1_20s4x46QA6MoFGCo8"

detector = cv2.QRCodeDetector()

ADMIN_ID = 340757376

cooldown = {}


def anti_spam(user_id):
    now = time.time()
    if user_id in cooldown:
        if now - cooldown[user_id] < 1.5:
            return True
    cooldown[user_id] = now
    return False


def is_valid_qr(data: str) -> bool:
    if not data:
        return False

    d = data.lower()
    return any(x in d for x in [
        "http",
        "tng",
        "tngd",
        "touchngo",
        "wallet",
        "wa.me"
    ])


async def send_alert(context, message, data):

    # 🚀 REAL TIME ALERT FORMAT
    text = f"""🚨 REAL TIME QR ALERT

👥 Group: {message.chat.title}
👤 User: {message.from_user.first_name}
🆔 User ID: {message.from_user.id}

🔗 DATA:
{data}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message
        if not message:
            return

        if message.chat.type not in ["group", "supergroup"]:
            return

        if anti_spam(message.from_user.id):
            return

        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id

        elif message.document and message.document.mime_type and message.document.mime_type.startswith("image"):
            file_id = message.document.file_id

        else:
            return

        file = await context.bot.get_file(file_id)
        file_bytes = await file.download_as_bytearray()

        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        data, _, _ = detector.detectAndDecode(img)

        if not data:
            return

        print("QR:", data)

        if not is_valid_qr(data):
            return

        # ⚡ REAL TIME ALERT SEND (NO DELAY)
        await send_alert(context, message, data)

    except Exception as e:
        print("ERROR:", e)


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle)
    )

    print("🚀 REAL TIME MODE RUNNING")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
