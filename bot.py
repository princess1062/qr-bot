import cv2
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAGh5BymbLksOzk999U_tsja6lVp3KsGQ1g"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("MASUK FUNCTION")

        if update.message:
            await update.message.reply_text("MASUK FUNCTION ✅")
        else:
            print("NO MESSAGE OBJECT")
            return

        # ambil semua jenis file
        file_id = None

        if update.message.photo:
            file_id = update.message.photo[-1].file_id

        elif update.message.document:
            file_id = update.message.document.file_id

        else:
            await update.message.reply_text("❌ Tak detect gambar")
            return

        file = await context.bot.get_file(file_id)

        path = "qr.jpg"
        await file.download_to_drive(path)

        await update.message.reply_text("📸 DOWNLOAD OK")

    except Exception as e:
        print("ERROR BESAR:", e)
        except:
            pass
