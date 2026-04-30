print("VERSION BARU 123")

import cv2

from telegram import Update

from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAGh5BymbLksOzk999U_tsja6lVp3KsGQ1g"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("START SCAN")

        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        path = "qr.jpg"
        await file.download_to_drive(path)

        await update.message.reply_text("GAMBAR DOWNLOAD OK")

        img = cv2.imread(path)

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        print("DEBUG QR:", data)

        if not data:
            await update.message.reply_text("❌ Tak jumpa QR")
            return

        await update.message.reply_text(f"QR:\n{data}")

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(f"ERROR: {e}")
