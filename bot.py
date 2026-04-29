import cv2

from telegram import Update

from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "TOKEN_KAU"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("test")

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.PHOTO, handle))

    app.run_polling()

main()
