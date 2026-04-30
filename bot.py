import cv2
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAGh5BymbLksOzk999U_tsja6lVp3KsGQ1g"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("MASUK FUNCTION ✅")

        if not update.message or not update.message.photo:
            await update.message.reply_text("❌ Bukan gambar")
            return

        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        path = "qr.jpg"
        await file.download_to_drive(path)

        await update.message.reply_text("📸 GAMBAR BERJAYA DOWNLOAD")

    except Exception as e:
        print("ERROR:", e)
        try:
            await update.message.reply_text(f"ERROR: {e}")
        except:
            pass
