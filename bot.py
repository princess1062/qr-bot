print("VERSION BARU 123")

import cv2

from telegram import Update

from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAGh5BymbLksOzk999U_tsja6lVp3KsGQ1g"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📥 Gambar diterima")

        # CHECK jenis message
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
        elif update.message.document:
            file_id = update.message.document.file_id
        else:
            await update.message.reply_text("❌ Bukan gambar")
            return

        file = await context.bot.get_file(file_id)

        path = "qr.jpg"
        await file.download_to_drive(path)

        await update.message.reply_text("📸 Download OK")

        img = cv2.imread(path)

        if img is None:
            await update.message.reply_text("❌ Gagal baca gambar")
            return

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        print("DEBUG QR:", data)

        if not data:
            await update.message.reply_text("❌ Tak jumpa QR")
            return

        await update.message.reply_text(f"✅ QR Dikesan:\n{data}")

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(f"❌ ERROR:\n{e}")
