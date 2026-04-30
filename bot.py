import cv2
import numpy as np
import re
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

print("🚀 TNG PRO BOT STARTED")

BOT_TOKEN = "8740908330:AAEdPDwfzmA-rfzy1_20s4x46QA6MoFGCo8"

detector = cv2.QRCodeDetector()

user_cooldown = {}


def anti_spam(user_id):
    now = time.time()
    if user_id in user_cooldown:
        if now - user_cooldown[user_id] < 2:
            return True
    user_cooldown[user_id] = now
    return False


def is_tng_qr(data: str) -> bool:
    if not data:
        return False

    data_lower = data.lower()

    # 🔥 STRICT TNG PATTERNS
    patterns = [
        "tng",
        "tngd",
        "touchngo",
        "tngdigital",
        "my.tngdigital",
        "tngd.page.link",
        "wallet",
        "payment"
    ]

    return any(p in data_lower for p in patterns)


def extract_amount(data: str):
    # cari amount dalam QR (RM 10.50 etc)
    match = re.search(r"(\d+\.\d{2}|\d+)", data)
    if match:
        return match.group()
    return None


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message
        if not message:
            return

        user_id = message.from_user.id

        if anti_spam(user_id):
            return

        await message.reply_text("💰 Scanning TNG QR...")

        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id

        elif message.document and message.document.mime_type.startswith("image"):
            file_id = message.document.file_id

        else:
            await message.reply_text("❌ Hantar gambar QR sahaja")
            return

        file = await context.bot.get_file(file_id)
        file_bytes = await file.download_as_bytearray()

        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        data, _, _ = detector.detectAndDecode(img)

        print("QR RAW:", data)

        if not data:
            await message.reply_text("❌ QR tak dapat detect")
            return

        # 🚫 BLOCK NON TNG
        if not is_tng_qr(data):
            await message.reply_text(
                "❌ Bukan Touch ’n Go QR\n\n⚠️ QR ini ditolak oleh sistem TNG PRO"
            )
            return

        # 💰 extract amount (kalau ada)
        amount = extract_amount(data)

        response = f"💰 TNG QR DETECTED\n\n🔗 Data:\n{data}"

        if amount:
            response += f"\n💵 Amount detected: RM {amount}"

        await message.reply_text(response)

    except Exception as e:
        print("ERROR:", e)
        if update.message:
            await update.message.reply_text("❌ Error scanning TNG QR")


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle)
    )

    print("🚀 TNG PRO RUNNING...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
