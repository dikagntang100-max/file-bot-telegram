import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- KONFIGURASI ---
BOT_TOKEN = "8754264351:AAG2WSsKv7fqB0bU8dsG8AcTrpDMG4M4tyY"
GROUP_ID = -1004483065655
GROUP_LINK = "https://t.me/+d-W_foAg0AthNTU1"
FILE_TO_SEND = "https://cozy-puppy-3a46a9.netlify.app/"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Fungsi untuk mengecek apakah user sudah join
async def is_user_joined(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        # Cek status: member, administrator, atau creator
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Error cek member {user_id}: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    joined = await is_user_joined(context, user_id)
    
    if joined:
        # Jika sudah join, langsung kirim link
        text = f"✅ Kamu sudah join grup!\n\nIni link yang kamu minta:\n{FILE_TO_SEND}"
        await update.message.reply_text(text)
    else:
        # Jika belum join, tampilkan tombol
        keyboard = [
            [InlineKeyboardButton("📥 Masuk Grup Telegram", url=GROUP_LINK)],
            [InlineKeyboardButton("✅ Saya Sudah Join, Verifikasi!", callback_data="verify_join")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            "Halo! Untuk mendapatkan link, kamu wajib masuk ke grup Telegram kami terlebih dahulu.\n\n"
            "1. Klik tombol **Masuk Grup Telegram** di bawah.\n"
            "2. Setelah join, kembali ke sini dan klik **Saya Sudah Join, Verifikasi!**."
        )
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def verify_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    joined = await is_user_joined(context, user_id)
    
    if joined:
        # Jika berhasil verifikasi, edit pesan dan kirim link
        text = f"✅ Verifikasi berhasil!\n\nIni link yang kamu minta:\n{FILE_TO_SEND}"
        await query.edit_message_text(text=text)
    else:
        # Jika gagal, beri pesan error yang jelas
        text = "❌ Gagal verifikasi. Pastikan kamu sudah benar-benar masuk ke grup, lalu coba klik tombol verifikasi lagi."
        await query.edit_message_text(text=text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_button, pattern="^verify_join$"))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
