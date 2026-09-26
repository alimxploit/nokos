import logging
import time
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import Forbidden, TelegramError

# ================= KONFIGURASI =================
BOT_TOKEN = "8277774482:AAHgoV6Sd7QY04MVGl8zZ37uTPG0wSfsT2k"
OWNER_ID = 5280266010
OWNER_USERNAME = "@limprincee"

LINK_NOVUM = "https://t.me/ainovum_bot?start=ref_5280266010"
LINK_MINING = "https://t.me/MiningGRAM_Bot/mine?startapp=2FBQFBU"
LINK_HIFAMI = "https://s.hifamiapp.com/1/2lxOpRH3h"
VIDEO_NOTE_URL = "https://files.catbox.moe/jdkcdl.mp4"

MIN_KLAIM = 4
START_TIME = time.time()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_data = {}


def get_runtime():
    uptime = int(time.time() - START_TIME)
    jam = uptime // 3600
    menit = (uptime % 3600) // 60
    detik = uptime % 60
    return f"{jam} Jam {menit} Menit {detik} Detik"


def get_main_menu(first_name):
    text = (
        f"🤖 **NOKOSS XIOLIM FREE**\n\n"
        f"┌ 📜 **SCRIPT NAME** : NOKOSS XIOLIM FREE\n"
        f"├ 👤 **OWNER** : {OWNER_USERNAME}\n"
        f"├ 📌 **VERSION** : 1.0.0\n"
        f"└ ⏱️ **RUNTIME** : {get_runtime()}\n\n"
        f"👋 Halo **{first_name}**!\n"
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
        ],
        [
            InlineKeyboardButton("🎁 KLAIM NOKOS", callback_data="klaim_nokos")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ================= HANDLER =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in user_data:
        user_data[user_id] = {
            "status": "none", "task": None, "nokos": 0, "klaim": 0,
            "first_name": user.first_name, "username": user.username or ""
        }
    else:
        user_data[user_id]["first_name"] = user.first_name
        user_data[user_id]["username"] = user.username or ""

    try:
        await context.bot.send_video_note(
            chat_id=update.effective_chat.id,
            video_note=VIDEO_NOTE_URL
        )
    except Exception as e:
        logger.error(f"Gagal kirim video note: {e}")

    text, reply_markup = get_main_menu(user.first_name)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    first_name = query.from_user.first_name

    if user_id not in user_data:
        user_data[user_id] = {
            "status": "none", "task": None, "nokos": 0, "klaim": 0,
            "first_name": first_name, "username": ""
        }

    user = user_data[user_id]

    if data == "kembali":
        text, reply_markup = get_main_menu(first_name)
        try:
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception:
            pass

    elif data == "read_first":
        teks = (
            "📖 **READ FIRST (BACA DULU)**\n\n"
            "1. Bot ini 100% GRATIS.\n"
            "2. Kamu harus menyelesaikan misi yang tersedia.\n"
            "3. Jangan spam, nanti kena banned.\n"
            "4. Jika misi terbukti benar, Nokos akan dikirim ke chat ini.\n"
            "5. Ada 3 task dengan hadiah Nokos berbeda.\n"
            f"6. Minimal **{MIN_KLAIM} Nokos** untuk bisa klaim.\n\n"
            "Klik tombol di bawah untuk mulai misi."
        )
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "cek_id":
        saldo = user.get("nokos", 0)
        await query.edit_message_text(
            f"🆔 **ID TELEGRAM KAMU:**\n`{user_id}`\n\n"
            f"💰 **Saldo Nokos:** {saldo}\n"
            f"🎁 **Minimal Klaim:** {MIN_KLAIM}\n\n"
            f"Simpan ID ini untuk keperluan klaim.",
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

    elif data == "klaim_nokos":
        saldo = user.get("nokos", 0)
        sisa = MIN_KLAIM - saldo

        if saldo < MIN_KLAIM:
            teks = (
                f"🎁 **KLAIM NOKOS**\n\n"
                f"❌ **Belum bisa klaim!**\n\n"
                f"💰 Saldo Nokos kamu: **{saldo}**\n"
                f"📌 Minimal klaim: **{MIN_KLAIM}**\n"
                f"📊 Kurang: **{sisa} Nokos**\n\n"
                f"Selesaikan misi dulu di menu **AMBIL MISI** untuk menambah saldo."
            )
            keyboard = [
                [InlineKeyboardButton("🎯 AMBIL MISI", callback_data="ambil_misi")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]
            ]
        else:
            user_data[user_id]["nokos"] -= MIN_KLAIM
            user_data[user_id]["klaim"] += 1
            user_updated = user_data[user_id]
            teks = (
                f"🎉 **KLAIM BERHASIL!**\n\n"
                f"✅ Kamu berhasil klaim **1 Nokos**!\n\n"
                f"📊 **Detail:**\n"
                f"• Saldo sebelumnya: {saldo}\n"
                f"• Dikurangi: {MIN_KLAIM}\n"
                f"• Sisa saldo: {user_updated['nokos']}\n"
                f"• Total klaim: {user_updated['klaim']}\n\n"
                f"Nokos akan dikirim oleh Admin ke chat ini. Mohon tunggu."
            )
            keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]]

            try:
                await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=f"🎁 **KLAIM NOKOS BARU**\n\nUser: `{user_id}`\nNama: {first_name}\nTotal klaim: {user_updated['klaim']}\n\nSegera kirim Nokos!"
                )
            except Exception as e:
                logger.error(f"Gagal notif owner: {e}")

        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

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

    # ============ KONFIRMASI ============
    elif data.startswith("selesai_"):
        task_num = data.split("_")[1]
        user_data[user_id]["status"] = "pending"
        user_data[user_id]["task"] = task_num

        teks = (
            f"📸 **KIRIM BUKTI SEKARANG**\n\n"
            f"Task: **TASK {task_num}**\n\n"
            f"**Cara Kirim Bukti:**\n"
            f"1. Tekan tombol 📎 (klip) di bawah kolom chat\n"
            f"2. Pilih **Galeri** atau **File**\n"
            f"3. Pilih screenshot bukti kamu\n"
            f"4. Kirim ke chat ini\n\n"
            f"**Setelah kirim, klik tombol di bawah ini:**\n\n"
            f"⚠️ *Bukti akan diverifikasi oleh Admin dalam 1x24 jam.*"
        )
        keyboard = [
            [InlineKeyboardButton("✅ SAYA SUDAH KIRIM BUKTI", callback_data=f"konfirmasi_{task_num}")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")]
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("konfirmasi_"):
        task_num = data.split("_")[1]
        user_data[user_id]["status"] = "pending"
        user_data[user_id]["task"] = task_num

        await query.edit_message_text(
            f"⏳ **MENUNGGU VERIFIKASI TASK {task_num}**\n\n"
            "Bukti kamu sedang diverifikasi oleh Admin. Mohon tunggu 1x24 jam.\n"
            "Jika terbukti benar, Nokos akan otomatis ditambahkan ke saldo kamu.\n\n"
            "💡 Kamu bisa cek saldo di menu **CEK ID**.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="kembali")]])
        )
        try:
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"🔔 **PENGAJUAN MISI BARU**\n\nUser: `{user_id}`\nNama: {first_name}\nTask: {task_num}\nStatus: Pending\n\nSegera verifikasi!"
            )
        except Exception as e:
            logger.error(f"Gagal notif owner: {e}")

    # ============ OWNER ACC / TOLAK ============
    elif data.startswith("acc_"):
        parts = data.split("_")
        target_id = int(parts[1])
        jumlah = int(parts[2])

        if user_id != OWNER_ID:
            await query.answer("❌ Hanya owner yang bisa ACC!", show_alert=True)
            return

        if target_id not in user_data:
            user_data[target_id] = {
                "status": "approved", "task": None, "nokos": 0, "klaim": 0,
                "first_name": "", "username": ""
            }

        user_data[target_id]["status"] = "approved"
        user_data[target_id]["nokos"] += jumlah
        total = user_data[target_id]["nokos"]

        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=f"🎉 **SELAMAT!**\n\nMisi kamu terbukti benar.\nKamu mendapatkan **{jumlah} Nokos**.\n\nTotal saldo Nokos kamu: **{total}**\n\nGunakan menu **KLAIM NOKOS** untuk klaim (minimal {MIN_KLAIM}).",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Gagal kirim ke user: {e}")

        await query.edit_message_text(
            f"✅ **BERHASIL ACC**\n\n"
            f"👤 User: `{target_id}`\n"
            f"💰 Ditambah: {jumlah} Nokos\n"
            f"📊 Total saldo user: {total}",
            parse_mode="Markdown"
        )

    elif data.startswith("tolak_"):
        target_id = int(data.split("_")[1])

        if user_id != OWNER_ID:
            await query.answer("❌ Hanya owner yang bisa TOLAK!", show_alert=True)
            return

        if target_id in user_data:
            user_data[target_id]["status"] = "rejected"

        try:
            await context.bot.send_message(
                chat_id=target_id,
                text="❌ **BUKTI DITOLAK**\n\nBukti kamu tidak valid atau tidak sesuai ketentuan.\n\nSilakan coba lagi dengan bukti yang benar.",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Gagal kirim ke user: {e}")

        await query.edit_message_text(
            f"❌ **BUKTI DITOLAK**\n\n👤 User: `{target_id}`",
            parse_mode="Markdown"
        )


# ================= OWNER COMMANDS =================

async def acc_nokos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Kamu bukan owner!")
        return
    try:
        args = context.args
        target_id = int(args[0])
        jumlah_nokos = int(args[1])

        if target_id not in user_data:
            user_data[target_id] = {
                "status": "approved", "task": None, "nokos": 0, "klaim": 0,
                "first_name": "", "username": ""
            }

        user_data[target_id]["status"] = "approved"
        user_data[target_id]["nokos"] += jumlah_nokos
        user_updated = user_data[target_id]

        await context.bot.send_message(
            chat_id=target_id,
            text=f"🎉 **SELAMAT!**\n\nMisi kamu terbukti benar.\nKamu mendapatkan **{jumlah_nokos} Nokos**.\n\nTotal saldo Nokos kamu: **{user_updated['nokos']}**\n\nGunakan menu **KLAIM NOKOS** untuk klaim (minimal {MIN_KLAIM}).",
            parse_mode="Markdown"
        )
        await update.message.reply_text(f"✅ Berhasil menambah {jumlah_nokos} Nokos ke user {target_id}")
    except Exception as e:
        await update.message.reply_text(f"Format salah. Gunakan: `/acc <user_id> <jumlah_nokos>`\nError: {e}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    total = len(user_data)
    await update.message.reply_text(
        f"📊 **STATISTIK BOT**\n\n"
        f"👥 Total user: {total}\n"
        f"⏱️ Runtime: {get_runtime()}",
        parse_mode="Markdown"
    )


# ================= HANDLER PESAN =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = user_data.get(user_id, {"task": "Unknown", "first_name": "-"})

    if update.message.photo or update.message.document:
        task = user.get("task", "Unknown")
        task_nokos = {"1": 1, "2": 2, "3": 7}
        jumlah = task_nokos.get(str(task), 1)

        await update.message.reply_text(
            f"✅ **BUKTI DITERIMA!**\n\n"
            f"Task: **TASK {task}**\n\n"
            f"Bukti kamu sedang diverifikasi oleh Admin. Mohon tunggu 1x24 jam.\n"
            f"Jika terbukti benar, Nokos akan ditambahkan ke saldo kamu.\n\n"
            f"💡 Cek saldo di menu **CEK ID**.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎁 KLAIM NOKOS", callback_data="klaim_nokos")],
                [InlineKeyboardButton("🔙 Menu Utama", callback_data="kembali")]
            ])
        )

        try:
            await context.bot.forward_message(
                chat_id=OWNER_ID,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
            # Kirim pesan ke owner DENGAN TOMBOL ACC
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    f"📩 **BUKTI BARU MASUK**\n\n"
                    f"👤 User: `{user_id}`\n"
                    f"📛 Nama: {user.get('first_name', '-')}\n"
                    f"🎯 Task: {task}\n"
                    f"💰 Hadiah: {jumlah} Nokos\n"
                    f"📌 Status: Pending\n\n"
                    f"Pilih aksi di bawah:"
                ),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"✅ ACC ({jumlah} Nokos)", callback_data=f"acc_{user_id}_{jumlah}")],
                    [InlineKeyboardButton("❌ TOLAK", callback_data=f"tolak_{user_id}")]
                ])
            )
        except Exception as e:
            logger.error(f"Gagal forward: {e}")

    elif update.message.text and not update.message.text.startswith("/"):
        await update.message.reply_text(
            "📸 **KIRIM SCREENSHOT BUKTI YA**\n\n"
            "Tekan tombol 📎 di bawah, pilih **Galeri**, lalu pilih screenshot bukti kamu.\n\n"
            "Kalau belum ambil misi, klik tombol di bawah:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 AMBIL MISI", callback_data="ambil_misi")]
            ])
        )


# ================= MAIN =================

def main():
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, Me
