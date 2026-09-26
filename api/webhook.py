from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot import (
    start, button_handler, acc_nokos, handle_message,
    BOT_TOKEN
)
import asyncio

app = Flask(__name__)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("acc", acc_nokos))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_message))


@app.route("/", methods=["GET"])
def index():
    return "Bot NOKOSS XIOLIM FREE is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            update_data = request.get_json(force=True)
            update = Update.de_json(update_data, application.bot)
            loop.run_until_complete(application.initialize())
            loop.run_until_complete(application.process_update(update))
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            print(f"ERROR: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "method not allowed"}), 405
