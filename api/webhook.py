import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot import (
    start, button_handler, acc_nokos, handle_message,
    BOT_TOKEN
)

app = Flask(__name__)

_application = None

def get_app():
    global _application
    if _application is None:
        _application = ApplicationBuilder().token(BOT_TOKEN).build()
        _application.add_handler(CommandHandler("start", start))
        _application.add_handler(CommandHandler("acc", acc_nokos))
        _application.add_handler(CallbackQueryHandler(button_handler))
        _application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_message))
    return _application


@app.route("/", methods=["GET"])
def index():
    return "Bot NOKOSS XIOLIM FREE is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            update_data = request.get_json(force=True)
            application = get_app()
            update = Update.de_json(update_data, application.bot)

            async def process():
                await application.initialize()
                await application.process_update(update)
                await application.shutdown()

            asyncio.run(process())
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            print(f"ERROR: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "method not allowed"}), 405
