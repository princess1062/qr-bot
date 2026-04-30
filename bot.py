import cv2
import numpy as np
import time

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

print("🔥 SILENT PRO MAX STARTED")

BOT_TOKEN = "8740908330:AAGVH5VYVSUojAmIA08_JmUtAAH9BFQXoPU"
ADMIN_ID = 340757376

detector = cv2.QRCodeDetector()

# ================= ANTI DUPLICATE =================
last_seen = {}

def is_duplicate(data):
    now = time.time()
    if data in last_seen:
        if now - last_seen[data] < 3:
            return True
    last_seen[data] = now
    return False

# ================= QR FILTER =================
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

# ================= CORE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message or update.channel_post

        if not message:
            return

        file_id = None

        # image from photo
        if message.photo:
            file_id = message.photo[-1].file_id

        # image from document
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

        # filter QR
        if not is_valid_qr(data):
            return

        # anti duplicate
        if is_duplicate(data):
            return

        # source detect
        chat = message.chat
        source = "Private"

        if chat.type in ["group", "supergroup"]:
            source = f"Group: {chat.title}"

        elif chat.type == "channel":
            source = f"Channel: {chat.title}"

        # silent alert
        text = f"""🔥 SILENT PRO MAX ALERT

📍 Source: {source}
🔗 QR:
{data}
"""

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

    except Exception as e:
        print("ERROR:", e)

# ================= MAIN =================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # omni listener
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle))
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle))

    print("🔥 SILENT PRO MAX RUNNING")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
