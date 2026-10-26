import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- KONFIGURASI ---
BOT_TOKEN = "8754264351:AAG2WSsKv7fqB0bU8dsG8AcTrpDMG4M4tyY"
GROUP_ID = -1004483065655
GROUP_LINK = "https://t.me/+d-W_foAg0AthNTU1"
FILE_TO_SEND = "https://indirect-bronze-ectgsr9f.edgeone.dev/"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            await update.message.reply_text("✅ Kamu sudah join grup! Ini link file yang kamu minta:\n\n" + FILE_TO_SEND)
            return
    except Exception as e:
        logging.info(f"User {user_id} belum join atau error: {e}")

    keyboard = [
        [InlineKeyboardButton("📥 Masuk Grup Telegram", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ Saya Sudah Join, Verifikasi!", callback_data="verify_join")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "Halo! Untuk mendapatkan file, kamu wajib masuk ke grup Telegram kami terlebih dahulu.\n\n"
        "1. Klik tombol **Masuk Grup Telegram** di bawah.\n"
        "2. Setelah join, kembali ke sini dan klik **Saya Sudah Join, Verifikasi!**."
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def verify_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        
        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text(text="✅ Verifikasi berhasil! Ini link file kamu:\n\n" + FILE_TO_SEND)
        else:
            await query.edit_message_text(
                text="❌ Kamu masih terdeteksi belum join grup. Silakan join dulu melalui tombol di atas, lalu klik verifikasi lagi."
            )
            
    except Exception as e:
        logging.error(f"Error verifying user {user_id}: {e}")
        await query.edit_message_text(
            text="❌ Gagal verifikasi. Pastikan kamu sudah benar-benar masuk ke grup, lalu coba klik tombol verifikasi lagi."
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_button, pattern="^verify_join$"))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
