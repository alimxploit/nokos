from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from bot import (
    start, button_handler, acc_nokos, handle_message,
    broadcast, stats, BOT_TOKEN
)
import asyncio
import traceback

app = Flask(__name__)


def process_update_sync(update_data):
    """Proses update secara sinkron — Vercel-friendly."""
    try:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("acc", acc_nokos))
        application.add_handler(CommandHandler("broadcast", broadcast))
        application.add_handler(CommandHandler("stats", stats))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_message))

        update = Update.de_json(update_data, application.bot)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():
            await application.initialize()
            await application.process_update(update)
            await application.shutdown()

        loop.run_until_complete(run())
        loop.close()
        return True, None
    except Exception as e:
        return False, f"{e}\n{traceback.format_exc()}"


@app.route("/", methods=["GET"])
def index():
    return "Bot NOKOSS XIOLIM FREE is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method != "POST":
        return jsonify({"status": "method not allowed"}), 405

    try:
        update_data = request.get_json(force=True)
        success, error = process_update_sync(update_data)
        if success:
            return jsonify({"status": "ok"}), 200
        else:
            print(f"ERROR: {error}")
            return jsonify({"status": "error", "message": error}), 500
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
