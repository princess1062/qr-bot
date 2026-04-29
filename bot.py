async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("GAMBAR MASUK BOT")

    await update.message.reply_text("Gambar sampai bot ✅")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

# handler sini

app.add_handler(Messagehandler(filters.PHOTO, handle))

app.run_polling()
