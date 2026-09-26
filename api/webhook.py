import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from bot import get_application

app = Flask(__name__)
application = get_application()

# Vercel butuh Flask app-nya
@app.route("/", methods=["GET"])
def index():
    return "Bot NOKOSS XIOLIM FREE is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    """Endpoint yang dipanggil Telegram saat ada update."""
    if request.method == "POST":
        try:
            update_data = request.get_json(force=True)
            update = Update.de_json(update_data, application.bot)
            
            # Jalankan bot secara async di event loop terpisah
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(application.process_update(update))
            loop.close()
            
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"status": "method not allowed"}), 405
