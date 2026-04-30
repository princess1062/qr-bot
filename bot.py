import cv2
import numpy as np
import time

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

print("🚀 SEMI-AUTO QR SYSTEM STARTED")

BOT_TOKEN = "8740908330:AAGVH5VYVSUojAmIA08_JmUtAAH9BFQXoPU"
ADMIN_ID = 340757376

detector = cv2.QRCodeDetector()

# ================= MEMORY =================
registered_channels = set()
last_qr = {}

# ================= REGISTER CHANNEL =================
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    registered_channels.add(chat.id)

    await update.message.reply_text(
        f"✅ Channel registered\nID: {chat.id}"
    )

# ================= ANTI DUPLICATE =================
def is_duplicate(data):
    now = time.time()
    if data in last_qr and now - last_qr[data] < 3:
        return True
    last_qr[data] = now
    return False

# ================= QR VALIDATION =================
def is_valid_qr(data):
    if not data:
        return False
    d = data.lower()
    return any(x in d for x in ["http", "tng", "wallet", "wa.me"])

# ================= CORE HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message or update.channel_post

        if not message:
            return

        chat = message.chat

        # ================= SEMI-AUTO FILTER =================
        if chat.type == "channel" and chat.id not in registered_channels:
            return

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

        source = "Private"

        if chat.type in ["group", "supergroup"]:
            source = f"Group: {chat.title}"

        elif chat.type == "channel":
            source = f"Channel: {chat.title}"

        text = f"""🚨 SEMI-AUTO QR ALERT

📍 Source: {source}
🔗 QR:
{data}
"""

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

    except Exception as e:
        print("❌ ERROR:", e)

# ================= MAIN =================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # commands
    app.add_handler(CommandHandler("addchannel", add_channel))

    # global handler
    app.add_handler(MessageHandler(filters.ALL, handle))

    print("🚀 SEMI-AUTO SYSTEM RUNNING")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
