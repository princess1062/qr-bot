import cv2
import numpy as np
import time

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

print("🚀 BOT STARTED")

# ===================== CONFIG =====================
BOT_TOKEN = "8740908330:AAGVH5VYVSUojAmIA08_JmUtAAH9BFQXoPU"
ADMIN_ID = 340757376  # 

# ===================== SYSTEM =====================
detector = cv2.QRCodeDetector()
cooldown = {}

GROUPS = {}
SCAN_COUNT = {}

# ===================== ANTI SPAM =====================
def anti_spam(user_id):
    now = time.time()
    if user_id in cooldown:
        if now - cooldown[user_id] < 1.5:
            return True
    cooldown[user_id] = now
    return False

# ===================== VALID QR FILTER =====================
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

# ===================== HANDLE QR =====================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message
        if not message:
            return

        chat = message.chat

        # register group
        GROUPS[chat.id] = chat.title
        SCAN_COUNT[chat.id] = SCAN_COUNT.get(chat.id, 0) + 1

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

        print("QR DETECTED:", data)

        if not is_valid_qr(data):
            return

        # ALERT ADMIN
        text = f"""🚨 QR DETECTED

👥 Group: {chat.title}
👤 User: {message.from_user.first_name}
🔗 Data:
{data}
"""

        keyboard = [
    [InlineKeyboardButton("🔗 Open TNG Link", url=data)]
]

reply_markup = InlineKeyboardMarkup(keyboard)

await context.bot.send_message(
    chat_id=ADMIN_ID,
    text=text,
    reply_markup=reply_markup,
    disable_web_page_preview=False
)

    except Exception as e:
        print("ERROR:", e)

# ===================== DASHBOARD =====================
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "📊 GROUP DASHBOARD\n\n"

    for gid, title in GROUPS.items():
        count = SCAN_COUNT.get(gid, 0)
        text += f"{title} | Scans: {count}\n"

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

# ===================== MAIN =====================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # QR handler
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle))

    # dashboard command
    app.add_handler(CommandHandler("dashboard", dashboard))

    print("🚀 RUNNING...")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
