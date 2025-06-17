import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# 🔐 توکن رباتت رو اینجا بذار
BOT_TOKEN = '8069913983:AAHMYIXdTqI2MIF2X-sEXvK4gluQe1HBw4g'

# 📣 آیدی کانالت با @
CHANNEL_USERNAME = '@Jameliznudess12'

# ✅ چک می‌کنه که کاربر عضو کانال هست یا نه
def check_membership(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get('result', {}).get('status', '')
    return status in ['member', 'administrator', 'creator']

# 🎯 وقتی کاربر /start می‌زنه
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if check_membership(user_id):
        update.message.reply_text("✅ شما عضو کانال هستید. حالا عکس‌ها برایتان ارسال می‌شود:")
        for i in range(1, 6):  # ارسال 5 عکس
            with open(f"photo{i}.jpg", "rb") as photo:
                context.bot.send_photo(chat_id=user_id, photo=photo)
    else:
        # ❌ اگر عضو نبود، پیام همراه دکمه عضویت بفرست
        button = [[InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        reply_markup = InlineKeyboardMarkup(button)
        update.message.reply_text("❌ برای دریافت عکس‌ها لطفاً اول در کانال عضو شوید.", reply_markup=reply_markup)

# ⚙️ راه‌اندازی ربات
def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
