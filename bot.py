import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ================= KONFIGURASI =================
BOT_TOKEN = "8277774482:AAHgoV6Sd7QY04MVGl8zZ37uTPG0wSfsT2k"
OWNER_ID = 5280266010
OWNER_USERNAME = "@xiolim"

LINK_NOVUM = "https://t.me/ainovum_bot?start=ref_5280266010"
LINK_MINING = "https://t.me/MiningGRAM_Bot/mine?startapp=2FBQFBU"
LINK_HIFAMI = "https://s.hifamiapp.com/1/2lxOpRH3h"
VIDEO_NOTE_URL = "https://files.catbox.moe/jdkcdl.mp4"

MIN_KLAIM = 4  # Minimal Nokos untuk bisa klaim

TASK_INFO = {
    "1": {"reward": 1, "name": "NOVUM.AI"},
    "2": {"reward": 2, "name": "MININGRAM"},
    "3": {"reward": 7, "name": "HIFAMI APK"},
}

# Database sederhana (in-memory)
user_data = {}
START_TIME = time.time()


def get_runtime():
    uptime = int(time.time() - START_TIME)
    jam = uptime // 3600
    menit = (uptime % 3600) // 60
    detik = uptime % 60
    return f"{jam} jam {menit} menit {detik} detik"


def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"status": "none", "task": None, "nokos": 0, "klaim": 0}
    return user_data[user_id]


def get_main_menu(user_first_name):
    text = (
        f"NOKOSS XIOLIM\n"
        f"Owner: {OWNER_USERNAME} | Versi 1.0.0 | Runtime: {get_runtime()}\n\n"
        f"Halo {user_first_name}, selamat datang.\n"
        f"Selesaikan misi di bawah untuk mendapatkan Nokos gratis."
    )
    keyboard = [
        [
            InlineKeyboardButton("✅ Cek ID", callback_data="cek_id"),
            InlineKeyboardButton("📦 Stok Nokos", callback_data="stok_nokos"),
        ],
        [
            InlineKeyboardButton("📖 Baca Dulu", callback_data="read_first"),
            InlineKeyboardButton("🔑 OTP Bot", callback_data="otp_bot"),
        ],
        [InlineKeyboardButton("🎯 Ambil Misi", callback_data="ambil_misi")],
        [InlineKeyboardButton("🎁 Klaim Nokos", callback_data="klaim_nokos")],
    ]
    return text, InlineKeyboardMarkup(keyboard)


def back_button(callback="kembali"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data=callback)]])


# ================= HANDLER =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id)

    try:
        await context.bot.send_video_note(
            chat_id=update.effective_chat.id,
            video_note=VIDEO_NOTE_URL,
        )
    except Exception as e:
        logging.warning(f"Gagal kirim video note: {e}")

    text, reply_markup = get_main_menu(user.first_name)
    await update.message.reply_text(text, reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    first_name = query.from_user.first_name
    user = get_user(user_id)

    # ---------- Kembali ke menu utama ----------
    if data == "kembali":
        text, reply_markup = get_main_menu(first_name)
        try:
            await query.edit_message_text(text, reply_markup=reply_markup)
        except Exception:
            pass

    elif data == "read_first":
        teks = (
            "Baca dulu sebelum mulai:\n\n"
            "1. Bot ini gratis, tanpa biaya apa pun.\n"
            "2. Selesaikan misi sesuai instruksi.\n"
            "3. Jangan spam pengajuan, akun bisa diblokir.\n"
            "4. Nokos dikirim setelah misi diverifikasi Admin.\n"
            f"5. Klaim minimal {MIN_KLAIM} Nokos.\n\n"
            "Tekan Ambil Misi untuk mulai."
        )
        await query.edit_message_text(teks, reply_markup=back_button())

    elif data == "cek_id":
        await query.edit_message_text(
            f"ID Telegram kamu: {user_id}\n"
            f"Saldo Nokos: {user['nokos']}\n"
            f"Minimal klaim: {MIN_KLAIM}",
            reply_markup=back_button(),
        )

    elif data == "stok_nokos":
        teks = (
            "Stok Nokos saat ini:\n"
            "- Indonesia: tersedia\n"
            "- Malaysia: tersedia\n"
            "- Vietnam: kosong\n"
            "- Filipina: tersedia\n\n"
            "Selesaikan misi di menu Ambil Misi untuk mendapat Nokos gratis."
        )
        await query.edit_message_text(teks, reply_markup=back_button())

    elif data == "otp_bot":
        await query.edit_message_text(
            "OTP Bot digunakan untuk menerima kode OTP dari Nokos yang sudah kamu dapatkan.",
            reply_markup=back_button(),
        )

    # ---------- Klaim Nokos ----------
    elif data == "klaim_nokos":
        saldo = user["nokos"]
        if saldo < MIN_KLAIM:
            sisa = MIN_KLAIM - saldo
            teks = (
                f"Belum bisa klaim.\n\n"
                f"Saldo Nokos: {saldo}\n"
                f"Minimal klaim: {MIN_KLAIM}\n"
                f"Kurang: {sisa} Nokos\n\n"
                f"Selesaikan misi dulu untuk menambah saldo."
            )
            keyboard = [
                [InlineKeyboardButton("🎯 Ambil Misi", callback_data="ambil_misi")],
                [InlineKeyboardButton("🔙 Kembali", callback_data="kembali")],
            ]
            await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            # Minta konfirmasi dulu sebelum memotong saldo
            teks = (
                f"Konfirmasi klaim Nokos\n\n"
                f"Saldo saat ini: {saldo}\n"
                f"Akan dipotong: {MIN_KLAIM}\n"
                f"Sisa setelah klaim: {saldo - MIN_KLAIM}\n\n"
                f"Lanjutkan klaim?"
            )
            keyboard = [
                [
                    InlineKeyboardButton("✅ Ya, klaim", callback_data="konfirmasi_klaim"),
                    InlineKeyboardButton("❌ Batal", callback_data="kembali"),
                ]
            ]
            await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "konfirmasi_klaim":
        saldo = user["nokos"]
        if saldo < MIN_KLAIM:
            # Saldo berubah di antara waktu konfirmasi, cegah double-klaim
            await query.edit_message_text(
                "Saldo tidak mencukupi lagi untuk klaim ini.",
                reply_markup=back_button(),
            )
        else:
            user["nokos"] -= MIN_KLAIM
            user["klaim"] += 1
            teks = (
                f"Klaim berhasil.\n\n"
                f"Saldo sebelumnya: {saldo}\n"
                f"Dipotong: {MIN_KLAIM}\n"
                f"Sisa saldo: {user['nokos']}\n"
                f"Total klaim: {user['klaim']}\n\n"
                f"Nokos akan dikirim Admin ke chat ini, mohon tunggu."
            )
            await query.edit_message_text(teks, reply_markup=back_button())

            try:
                await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=(
                        f"Klaim Nokos baru\n"
                        f"User: {user_id}\n"
                        f"Nama: {first_name}\n"
                        f"Total klaim: {user['klaim']}\n\n"
                        f"Segera kirim Nokos."
                    ),
                )
            except Exception as e:
                logging.warning(f"Gagal notifikasi owner (klaim): {e}")

    # ---------- Daftar misi ----------
    elif data == "ambil_misi":
        teks = (
            "Pilih misi untuk mendapatkan Nokos gratis.\n"
            "Kerjakan semua untuk total 10 Nokos.\n\n"
            "Daftar misi:"
        )
        keyboard = [
            [InlineKeyboardButton("🟢 Task 1 - 1 Nokos (Novum.ai)", callback_data="task1")],
            [InlineKeyboardButton("🟡 Task 2 - 2 Nokos (MiningGRAM)", callback_data="task2")],
            [InlineKeyboardButton("🔴 Task 3 - 7 Nokos (Hifami APK)", callback_data="task3")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="kembali")],
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "task1":
        teks = (
            "Task 1 - 1 Nokos\n\n"
            "Klik link di bawah untuk masuk ke bot Novum.ai (cukup tap/join).\n\n"
            f"Link: {LINK_NOVUM}\n\n"
            "Setelah itu, kirim screenshot bukti join ke chat ini."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Saya sudah selesai", callback_data="konfirmasi_selesai_1")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")],
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif data == "task2":
        teks = (
            "Task 2 - 2 Nokos\n\n"
            "1. Masuk ke bot MiningGRAM lewat link di bawah.\n"
            "2. Selesaikan semua task di dalam bot.\n"
            "3. Lewati task Boost Grup, tidak perlu dikerjakan.\n\n"
            f"Link: {LINK_MINING}\n\n"
            "Setelah itu, kirim screenshot bukti task selesai."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Saya sudah selesai", callback_data="konfirmasi_selesai_2")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")],
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif data == "task3":
        teks = (
            "Task 3 - 7 Nokos\n\n"
            "1. Download dan install APK HiFami lewat link di bawah.\n"
            "2. Mainkan game di dalamnya.\n"
            "3. Naikkan tanaman sampai Level 20.\n\n"
            f"Link: {LINK_HIFAMI}\n\n"
            "Setelah itu, kirim screenshot tanaman Level 20."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Saya sudah selesai", callback_data="konfirmasi_selesai_3")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="ambil_misi")],
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    # ---------- Konfirmasi sebelum submit (mencegah dobel pengajuan) ----------
    elif data.startswith("konfirmasi_selesai_"):
        task_num = data.split("_")[-1]
        teks = (
            f"Konfirmasi pengajuan Task {task_num}\n\n"
            "Pastikan kamu sudah benar-benar menyelesaikan misi ini.\n"
            "Pengajuan palsu bisa membuat akun kamu diblokir.\n\n"
            "Lanjutkan pengajuan?"
        )
        keyboard = [
            [
                InlineKeyboardButton("✅ Ya, ajukan", callback_data=f"selesai_{task_num}"),
                InlineKeyboardButton("❌ Batal", callback_data=f"task{task_num}"),
            ]
        ]
        await query.edit_message_text(teks, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("selesai_"):
        task_num = data.split("_")[1]

        # Cegah pengajuan dobel untuk task yang sama saat masih pending
        if user["status"] == "pending" and user["task"] == task_num:
            await query.edit_message_text(
                f"Task {task_num} sudah diajukan sebelumnya dan masih menunggu verifikasi.",
                reply_markup=back_button(),
            )
            return

        user["status"] = "pending"
        user["task"] = task_num

        await query.edit_message_text(
            f"Pengajuan Task {task_num} terkirim.\n\n"
            "Menunggu verifikasi Admin, maksimal 1x24 jam.\n"
            "Nokos akan otomatis ditambahkan jika terbukti benar.",
            reply_markup=back_button(),
        )

        reward = TASK_INFO.get(task_num, {}).get("reward", 0)
        task_name = TASK_INFO.get(task_num, {}).get("name", "-")
        owner_keyboard = [
            [
                InlineKeyboardButton("✅ Verifikasi", callback_data=f"verify_{user_id}_{task_num}"),
                InlineKeyboardButton("❌ Tolak", callback_data=f"reject_{user_id}_{task_num}"),
            ]
        ]
        try:
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=(
                    f"🔔 Pengajuan misi baru\n"
                    f"User: {user_id}\n"
                    f"Nama: {first_name}\n"
                    f"Task: {task_num} ({task_name})\n"
                    f"Reward: {reward} Nokos\n"
                    f"Status: Pending\n\n"
                    f"Tunggu bukti screenshot sebelum menekan Verifikasi."
                ),
                reply_markup=InlineKeyboardMarkup(owner_keyboard),
            )
        except Exception as e:
            logging.warning(f"Gagal notifikasi owner (misi): {e}")

    # ---------- Owner verifikasi / tolak misi lewat tombol ----------
    elif data.startswith("verify_") or data.startswith("reject_"):
        if user_id != OWNER_ID:
            await query.answer("Kamu bukan owner.", show_alert=True)
            return

        action, target_id_str, task_num = data.split("_")
        target_id = int(target_id_str)
        target = get_user(target_id)

        if target["status"] != "pending" or target["task"] != task_num:
            await query.edit_message_text(
                query.message.text + "\n\n⚠️ Sudah diproses sebelumnya.",
            )
            return

        task_name = TASK_INFO.get(task_num, {}).get("name", "-")

        if action == "verify":
            reward = TASK_INFO.get(task_num, {}).get("reward", 0)
            target["status"] = "approved"
            target["nokos"] += reward

            await query.edit_message_text(
                query.message.text + f"\n\n✅ Diverifikasi. +{reward} Nokos diberikan.",
            )
            try:
                await context.bot.send_message(
                    chat_id=target_id,
                    text=(
                        f"Misi Task {task_num} ({task_name}) kamu terverifikasi.\n"
                        f"Kamu mendapatkan {reward} Nokos.\n"
                        f"Total saldo Nokos: {target['nokos']}\n\n"
                        f"Gunakan menu Klaim Nokos untuk klaim (minimal {MIN_KLAIM})."
                    ),
                )
            except Exception as e:
                logging.warning(f"Gagal kirim notifikasi verifikasi ke user: {e}")
        else:
            target["status"] = "rejected"
            await query.edit_message_text(
                query.message.text + "\n\n❌ Ditolak.",
            )
            try:
                await context.bot.send_message(
                    chat_id=target_id,
                    text=(
                        f"Pengajuan Task {task_num} ({task_name}) kamu ditolak.\n"
                        f"Pastikan bukti screenshot sesuai instruksi, lalu ajukan ulang."
                    ),
                )
            except Exception as e:
                logging.warning(f"Gagal kirim notifikasi penolakan ke user: {e}")


async def acc_nokos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Owner konfirmasi misi user -> tambah saldo Nokos."""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Kamu bukan owner.")
        return

    try:
        args = context.args
        target_id = int(args[0])
        jumlah_nokos = int(args[1])
    except Exception as e:
        await update.message.reply_text(f"Format salah. Gunakan: /acc <user_id> <jumlah_nokos>\nError: {e}")
        return

    if target_id not in user_data:
        await update.message.reply_text("User tidak ditemukan.")
        return

    target = user_data[target_id]
    target["status"] = "approved"
    target["nokos"] += jumlah_nokos

    try:
        await context.bot.send_message(
            chat_id=target_id,
            text=(
                f"Misi kamu terverifikasi.\n"
                f"Kamu mendapatkan {jumlah_nokos} Nokos.\n"
                f"Total saldo Nokos: {target['nokos']}\n\n"
                f"Gunakan menu Klaim Nokos untuk klaim (minimal {MIN_KLAIM})."
            ),
        )
    except Exception as e:
        logging.warning(f"Gagal kirim notifikasi ke user: {e}")

    await update.message.reply_text(f"Berhasil menambah {jumlah_nokos} Nokos ke user {target_id}.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if update.message.photo or update.message.document:
        await update.message.reply_text(
            "Bukti diterima. Admin akan memverifikasi maksimal 1x24 jam."
        )
        try:
            await context.bot.forward_message(
                chat_id=OWNER_ID,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id,
            )
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"Bukti dari user {user_id}, task: {user.get('task', 'Unknown')}",
            )
        except Exception as e:
            logging.warning(f"Gagal forward bukti ke owner: {e}")
    else:
        await update.message.reply_text("Kirim screenshot bukti, bukan teks.")
    
