import cv2
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8740908330:AAGh5BymbLksOzk999U_tsja6lVp3KsGQ1g"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MASUK FUNCTION ✅")

def main():
    print("BOT START")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, handle))

    app.run_polling()

if __name__ == "__main__":
    main()
