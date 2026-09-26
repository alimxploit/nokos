import asyncio
import sys
import os

# Supaya bisa import bot.py yang ada di root project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from bot import (
    BOT_TOKEN, start, acc_nokos, stats, reply_user,
    button_handler, handle_message, logger
)

app = Flask(__name__)

# ---- Setup Application (Telegram) sekali saat cold start ----
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("acc", acc_nokos))
application.add_handler(CommandHandler("stats", stats))
application.add_handler(CommandHandler("reply", reply_user))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_message))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(application.initialize())


@app.route("/api/index", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        loop.run_until_complete(application.process_update(update))
    except Exception as e:
        logger.error(f"Error proses update: {e}")
    return "ok"


@app.route("/api/index", methods=["GET"])
def health():
    return "Bot NOKOSS XIOLIM FREE - webhook aktif ✅"
