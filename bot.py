import cv2
from pyzbar.pyzbar import decode
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAGh5BymbLksOzk999U_tsja6lVp3KsGQ1g"

ALLOWED = ["tng", "tngdigital", "touchngo"]

def check(text):
    text = text.lower()
    return any(x in text for x in ALLOWED)

def scan(path):
    img = cv2.imread(path)
    qr = decode(img)
    return [i.data.decode("utf-8") for i in qr]

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    path = "qr.jpg"
    await file.download_to_drive(path)

    data = scan(path)

    if not data:
        await update.message.reply_text("❌ Tak jumpa QR")
        return

    for d in data:
        if check(d):
            await update.message.reply_text(f"🔔 MATCH TNG:\n{d}")
        else:
            await update.message.reply_text(f"⚠️ NOT MATCH:\n{d}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle))

    print("Bot running...")
    app.run_polling()

main()
