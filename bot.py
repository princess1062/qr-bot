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

        # ambil file id
        file_id = None

        if message.photo:
            file_id = message.photo[-1].file_id

        elif message.document and message.document.mime_type.startswith("image"):
            file_id = message.document.file_id

        else:
            await message.reply_text("❌ Hantar gambar QR saja")
            return

        # download image
        file = await context.bot.get_file(file_id)

        path = "qr.jpg"
        await file.download_to_drive(path)

        print("DOWNLOAD OK")

        # decode QR
        img = cv2.imread(path)

        data, bbox, _ = detector.detectAndDecode(img)

        if data:
            await message.reply_text(f"✅ QR RESULT:\n{data}")
        else:
            await message.reply_text("❌ QR tak dapat detect")

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("❌ Error berlaku semasa proses QR")


def main():
    print("BOT STARTED")

    app = Application.builder().token(BOT_TOKEN).build()

    # hanya image sahaja trigger (lebih stable)
    app.add_handler(
        MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle)
    )

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
