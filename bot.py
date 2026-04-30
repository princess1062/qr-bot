import cv2
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAEdPDwfzmA-rfzy1_20s4x46QA6MoFGCo8"

# QR DETECTOR
detector = cv2.QRCodeDetector()


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        message = update.message
        if not message:
            return

        print("MASUK FUNCTION")

        await message.reply_text("📥 Processing image...")

        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id

        elif message.document and message.document.mime_type.startswith("image"):
            file_id = message.document.file_id

        else:
            await message.reply_text("❌ Hantar gambar QR saja")
            return

        file = await context.bot.get_file(file_id)

        path = "qr.jpg"
        await file.download_to_drive(path)

        print("DOWNLOAD OK")

        img = cv2.imread(path)

        data, bbox, _ = detector.detectAndDecode(img)

        if data and (data.startswith("http://") or data.startswith("https://")):

            keyboard = [[InlineKeyboardButton("🔗 Open Link", url=data)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await message.reply_text(
                f"✅ QR DETECTED:\n{data}",
                reply_markup=reply_markup
            )

        else:
            await message.reply_text(f"✅ QR DETECTED:\n{data}")

    except Exception as e:
        print("ERROR:", e)
        if update.message:
            await update.message.reply_text("❌ Error berlaku semasa proses QR")
