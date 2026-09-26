import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ================= KONFIGURASI =================
BOT_TOKEN = "8277774482:AAGRdBnJpjhz8RfnwZ4jjOkXWqrDfMxxgPg"
OWNER_ID = 5280266010
OWNER_USERNAME = "@limprincee"

LINK_NOVUM = "https://t.me/ainovum_bot?start=ref_5280266010"
LINK_MINING = "https://t.me/MiningGRAM_Bot/mine?startapp=2FBQFBU"
LINK_HIFAMI = "https://s.hifamiapp.com/1/2lxOpRH3h"

VIDEO_NOTE_URL = "https://files.catbox.moe/jdkcdl.mp4"

user_data = {}

# ================= FUNGSI HANDLER =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in user_data:
        user_data[user_id] = {"status": "none", "task": None, "nokos": 0}

    try:
        await context.bot.send_video_note(
            chat_id=update.effective_chat.id,
            video_note=VIDEO_NOTE_URL
        )
    except Exception as e:
        print(f"Gagal kirim video note: {e}")

    text = (
        f"🤖 **NOKOSS XIOLIM FREE**\n\n"
        f"┌ 📜 **SCRIPT NAME** : NOKOSS XIOLIM FREE\n"
        f"├ 👤 **OWNER** : {OWNER_USERNAME}\n"
        f"├ 📌 **VERSION** : 1.0.0\n"
        f"└ ⏱️ **RUNTIME** : Aktif\n\n"
        f"👋 Halo **{user.first_name}**!\n"
        f"Selamat datang di Bot Nokos Gratis.\n"
        f"Untuk mendapatkan **Nokos Gratis**, kamu harus menyelesaikan **Misi** terlebih dahulu.\n\n"
        f"📌 **Pilih menu di bawah ini:**"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ CEK ID", callback_data="cek_id"),
            InlineKeyboardButton("📦 STOK NOKOS", callback_data="stok_nokos")
        ],
        [
            InlineKeyboardButton("📖 READ FIRST", callback_data="read_first"),
            InlineKeyboardButton("🔑 OTP BOT", callback_data="otp_bot")
        ],
        [
            InlineKeyboardButton("🎯 AMBIL MISI (GRATIS NOKOS)", callback_data="ambil_misi")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "read_first":
        teks = (
            "📖 **READ FIRST (BACA DULU)**\n\n"
            "1. Bot ini 100% GRATIS.\n"
            "2. Kamu harus menyelesaikan misi yang tersedia.\n"
            "3. Jangan spam, nanti kena banned.\n"
            "4. Jika misi terbukti benar, Nokos akan dikirim ke chat ini.\n"
            "5. Ada 3 task dengan hadiah Nokos berbeda.\n\n"
            "Klik tombol di bawah untuk mulai misi."
        )
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "cek_id":
        await query.edit_message_text(
            f"🆔 **ID TELEGRAM KAMU:**\n`{user_id}`\n\nSimpan ID ini untuk keperluan klaim.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]])
        )

    elif data == "stok_nokos":
        teks = (
            "📦 **STOK NOKOS TERSEDIA**\n\n"
            "Saat ini stok Nokos yang tersedia:\n"
            "• Indonesia: ✅ Tersedia\n"
            "• Malaysia: ✅ Tersedia\n"
            "• Vietnam: ⏳ Kosong\n"
            "• Filipina: ✅ Tersedia\n\n"
            "**Cara Dapat Nokos:**\n"
            "Selesaikan misi di menu **AMBIL MISI** untuk mendapatkan Nokos gratis!"
        )
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "otp_bot":
        await query.edit_message_text(
            "🔑 **OTP BOT**\n\nFitur ini untuk menerima kode OTP dari Nokos yang kamu dapatkan nanti.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]])
        )

    elif data == "ambil_misi":
        teks = (
            "🎯 **PILIH MISI UNTUK MENDAPATKAN NOKOS GRATIS**\n\n"
            "Silakan pilih salah satu misi di bawah ini. "
            "Kamu bisa mengerjakan semuanya untuk mendapatkan total **10 Nokos**!\n\n"
            "**📌 Daftar Misi:**"
        )
        keyboard = [
            [InlineKeyboardButton("🟢 TASK 1: 1 NOKOS (NOVUM.AI)", callback_data="task1")],
            [InlineKeyboardButton("🟡 TASK 2: 2 NOKOS (MININGRAM)", callback_data="task2")],
            [InlineKeyboardButton("🔴 TASK 3: 7 NOKOS (HIFAMI APK)", callback_data="task3")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "task1":
        teks = (
            "🟢 **TASK 1: DAPATKAN 1 NOKOS**\n\n"
            "**Misi:**\n"
            "Cukup klik link di bawah ini untuk masuk ke bot NOVUM.AI (cuma buat tap/join).\n\n"
            f"🔗 **Link:** [KLIK DISINI UNTUK TASK 1]({LINK_NOVUM})\n\n"
            "**Syarat Klaim:**\n"
            "Setelah klik link, screenshot bukti bahwa kamu sudah masuk/join, lalu kirim ke bot ini.\n\n"
            "**Hadiah:** 1 Nokos"
        )
        keyboard = [
            [InlineKeyboardButton("✅ SAYA SUDAH SELESAI", callback_data="selesai_1")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")]
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    elif data == "task2":
        teks = (
            "🟡 **TASK 2: DAPATKAN 2 NOKOS**\n\n"
            "**Misi:**\n"
            "1. Masuk ke bot MiningGRAM lewat link di bawah.\n"
            "2. Selesaikan **SEMUA MISI** yang ada di dalam bot tersebut (di bagian Task).\n"
            "3. **PENTING:** Jangan kerjakan misi **Boost Grup** (lewati misi ini).\n\n"
            f"🔗 **Link:** [KLIK DISINI UNTUK TASK 2]({LINK_MINING})\n\n"
            "**Syarat Klaim:**\n"
            "Screenshot semua task yang sudah selesai (kecuali boost grup), lalu kirim ke bot ini.\n\n"
            "**Hadiah:** 2 Nokos"
        )
        keyboard = [
            [InlineKeyboardButton("✅ SAYA SUDAH SELESAI", callback_data="selesai_2")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")]
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    elif data == "task3":
        teks = (
            "🔴 **TASK 3: DAPATKAN 7 NOKOS**\n\n"
            "**Misi:**\n"
            "1. Download dan Install APK HiFami lewat link di bawah.\n"
            "2. Mainkan game di dalam APK tersebut.\n"
            "3. Naikkan tanaman (plant) kamu sampai **Level 20**.\n\n"
            f"🔗 **Link:** [KLIK DISINI UNTUK DOWNLOAD APK]({LINK_HIFAMI})\n\n"
            "**Syarat Klaim:**\n"
            "Screenshot tanaman kamu yang sudah Level 20, lalu kirim ke bot ini.\n\n"
            "**Hadiah:** 7 Nokos"
        )
        keyboard = [
            [InlineKeyboardButton("✅ SAYA SUDAH SELESAI", callback_data="selesai_3")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")]
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    elif data.startswith("selesai_"):
        task_num = data.split("_")[1]
        user_data[user_id]["status"] = "pending"
        user_data[user_id]["task"] = task_num

        await query.edit_message_text(
            f"⏳ **MENUNGGU VERIFIKASI TASK {task_num}**\n\n"
            "Misi kamu sedang diverifikasi oleh Admin. Mohon tunggu 1x24 jam.\n"
            "Jika terbukti benar, Nokos akan otomatis dikirim ke chat ini.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]])
        )
        try:
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"🔔 **PENGAJUAN MISI BARU**\n\nUser: `{user_id}`\nTask: {task_num}\nStatus: Pending\n\nSegera verifikasi!"
            )
        except:
            pass

    elif data == "kembali":
        await start(update, context)


async def acc_nokos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Kamu bukan owner!")
        return
    try:
        args = context.args
        target_id = int(args[0])
        jumlah_nokos = int(args[1])
        if target_id in user_data and user_data[target_id]["status"] == "pending":
            user_data[target_id]["status"] = "approved"
            user_data[target_id]["nokos"] += jumlah_nokos
            await context.bot.send_message(
                chat_id=target_id,
                text=f"🎉 **SELAMAT!**\n\nMisi kamu terbukti benar.\nKamu mendapatkan **{jumlah_nokos} Nokos**.\n\nTotal Nokos kamu: {user_data[target_id]['nokos']}\n\nGunakan dengan bijak!",
                parse_mode="Markdown"
            )
            await update.message.reply_text(f"✅ Berhasil mengirim {jumlah_nokos} Nokos ke {target_id}")
        else:
            await update.message.reply_text("❌ User tidak ditemukan atau status bukan pending.")
    except Exception as e:
        await update.message.reply_text("Format salah. Gunakan: `/acc <user_id> <jumlah_nokos>`")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.photo or update.message.document:
        await update.message.reply_text(
            "✅ **BUKTI DITERIMA!**\n\n"
            "Admin akan segera memverifikasi bukti kamu. Mohon tunggu 1x24 jam.\n"
            "Jika terbukti benar, Nokos akan dikirim ke chat ini.",
            parse_mode="Markdown"
        )
        try:
            await context.bot.forward_message(
                chat_id=OWNER_ID,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"📩 Bukti dari User ID: `{user_id}`\nTask: {user_data.get(user_id, {}).get('task', 'Unknown')}",
                parse_mode="Markdown"
            )
        except:
            pass
    else:
        await update.message.reply_text("Kirim screenshot bukti ya, bukan teks.")


# ================= INISIALISASI APPLICATION =================
def get_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("acc", acc_nokos))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_message))
    return app
