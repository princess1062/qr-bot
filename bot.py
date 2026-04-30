import cv2
import numpy as np
import os
import logging
import time

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

print("🚀 ENTERPRISE WEBHOOK QR SYSTEM STARTED")

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8740908330:AAGVH5VYVSUojAmIA08_JmUtAAH9BFQXoPU"
ADMIN_ID = 340757376

PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

detector = cv2.QRCodeDetector()

# ================= MEMORY =================
qr_history = {}
seen_count = {}

# ================= ANTI SPAM =================
def is_duplicate(data):
    now = time.time()
    if data in qr_history and now - qr_history[data] < 3:
        return True
    qr_history[data] = now
    return False

# ================= QR VALIDATION =================
def is_valid_qr(data):
    if not data:
        return False

    d = data.lower()
    return any(x in d for x in [
        "http",
        "tng",
        "wallet",
        "wa.me",
        "tngd"
    ])

# ================= CORE HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message or update.channel_post

        if not message:
            return

        chat = message.chat

        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id

        elif message.document and message.document.mime_type:
            if message.document.mime_type.startswith("image"):
                file_id = message.document.file_id

        if not file_id:
            return

        file = await context.bot.get_file(file_id)
        file_bytes = await file.download_as_bytearray()

        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        data, _, _ = detector.detectAndDecode(img)

        if not data:
            return

        if not is_valid_qr(data):
            return

        if is_duplicate(data):
            return

        # ================= TRACKING =================
        seen_count[data] = seen_count.get(data, 0) + 1

        source = "Private"

        if chat.type in ["group", "supergroup"]:
            source = f"Group: {chat.title}"

        elif chat.type == "channel":
            source = f"Channel: {chat.title}"

        # ================= ALERT =================
        text = f"""🚨 ENTERPRISE QR ALERT

📍 Source: {source}
🔗 QR:
{data}

📊 Seen: {seen_count[data]} times
"""

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

    except Exception as e:
        print("❌ ERROR:", e)

# ================= WEBHOOK START =================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, handle))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

    print("🚀 ENTERPRISE WEBHOOK RUNNING")

if __name__ == "__main__":
    main()
