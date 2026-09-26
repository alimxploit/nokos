import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot import (
    start, button_handler, acc_nokos, handle_message,
    broadcast, stats, BOT_TOKEN
)

app = Flask(__name__)


def create_app():
    """Bikin application baru tiap request (Vercel-friendly)."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("acc", acc_nokos))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_message))
    return application


@app.route("/", methods=["GET"])
def index():
    return "Bot NOKOSS XIOLIM FREE is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method != "POST":
        return jsonify({"status": "method not allowed"}), 405

    try:
        update_data = request.get_json(force=True)
        application = create_app()

        async def process():
            await application.initialize()
            update = Update.de_json(update_data, application.bot)
            await application.process_update(update)
            await application.shutdown()

        asyncio.run(process())
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
