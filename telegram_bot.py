import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = ""
BASE_FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Active Zone: ভিডিও, অডিও বা ছবি আপলোড করুন, আমি লিংক দেব।")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    media = None
    media_type = None

    if msg.video:
        media = msg.video
        media_type = '🎬 Video'
    elif msg.audio:
        media = msg.audio
        media_type = '🎵 Audio'
    elif msg.photo:
        media = msg.photo[-1]
        media_type = '🖼️ Image'
    elif msg.document:
        mime = msg.document.mime_type or ''
        if mime.startswith('video/'):
            media = msg.document
            media_type = '🎬 Video (Doc)'
        elif mime.startswith('audio/'):
            media = msg.document
            media_type = '🎵 Audio (Doc)'
        elif mime.startswith('image/'):
            media = msg.document
            media_type = '🖼️ Image (Doc)'

    if not media:
        await msg.reply_text("⚠️ সঠিক ভিডিও, অডিও, বা ছবি দিন।")
        return

    try:
        file_obj = await context.bot.get_file(media.file_id)
        file_path = file_obj.file_path
        link = file_path if file_path.startswith("http") else f"{BASE_FILE_URL}/{file_path}"

        await msg.reply_text(
            f"{media_type} লিংক:\n\nDownload ⬇️: {link}\nStream ▶️: {link}"
        )

    except Exception as e:
        await msg.reply_text("❌ সমস্যা হয়েছে, আবার চেষ্টা করুন।")
        print(f"Error: {e}")

async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 ভিডিও, অডিও বা ছবি পাঠান।")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    media_filter = (
        filters.VIDEO |
        filters.AUDIO |
        filters.PHOTO |
        filters.Document.VIDEO |
        filters.Document.AUDIO |
        filters.Document.IMAGE
    )
    app.add_handler(MessageHandler(media_filter, handle_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other))

    app.run_polling()

if __name__ == "__main__":
    main()
