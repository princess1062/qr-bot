import cv2
import numpy as np
import time

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ChannelPostHandler,
    filters,
    ContextTypes
)

print("🚀 OMNI QR SCANNER STARTED")

# ================= CONFIG =================
BOT_TOKEN = "8740908330:AAGVH5VYVSUojAmIA08_JmUtAAH9BFQXoPU"
ADMIN_ID = 340757376

# ================= ENGINE =================
detector = cv2.QRCodeDetector()
cooldown = {}

# ================= ANTI SPAM =================
def anti_spam(user_id):
    now = time.time()
    if user_id in cooldown:
        if now - cooldown[user_id] < 1.5:
            return True
    cooldown[user_id] = now
    return False

# ================= QR VALIDATION =================
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

# ================= CORE HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message or update.channel_post

        if not message:
            return

        chat = message.chat

        # ignore spam
        if message.from_user and anti_spam(message.from_user.id):
            return

        file_id = None

        # PHOTO
        if message.photo:
            file_id = message.photo[-1].file_id

        # IMAGE DOCUMENT
        elif message.document and message.document.mime_type and message.document.mime_type.startswith("image"):
            file_id = message.document.file_id

        else:
            return

        # DOWNLOAD IMAGE (memory only)
        file = await context.bot.get_file(file_id)
        file_bytes = await file.download_as_bytearray()

        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # DECODE QR
        data, _, _ = detector.detectAndDecode(img)

        if not data:
            return

        print("QR FOUND:", data)

        if not is_valid_qr(data):
            return

        # SOURCE TYPE
        source = "UNKNOWN"

        if chat.type in ["group", "supergroup"]:
            source = f"Group: {chat.title}"

        elif chat.type == "channel":
            source = f"Channel: {chat.title}"

        else:
            source = "Private Chat"

        # ALERT TEXT
        text = f"""🚨 OMNI QR ALERT

📍 Source: {source}
👤 User: {message.from_user.first_name if message.from_user else "Channel"}
🔗 Data:
{data}
"""

        # SEND TO ADMIN
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

    except Exception as e:
        print("ERROR:", e)

# ================= MAIN =================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # GROUP + DM + PHOTO
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle))

    # CHANNEL POSTS
    app.add_handler(ChannelPostHandler(handle))

    print("🚀 OMNI MODE RUNNING")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
