import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BIND_URL = 'http://localhost:8000/api/auth/bind-telegram/'
TASKS_URL = 'http://localhost:8000/api/telegram-tasks/'

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_btn = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    kb = [[contact_btn]]
    reply_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Пожалуйста, отправьте свой номер телефона:",
        reply_markup=reply_markup
    )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    contact = update.message.contact

    if contact.user_id != user.id:
        await update.message.reply_text("❌ Пожалуйста, отправьте свой номер.")
        return

    phone = contact.phone_number
    normalized_phone = f"+{phone.lstrip('+')}"
    telegram_id = user.id
    # print(f"Телефон: {normalized_phone}")
    # print(f"Telegram ID: {telegram_id}")
    try:
        resp = requests.post(BIND_URL, json={
            "phone": normalized_phone,
            "telegram_id": telegram_id
        }, timeout=5)
        if resp.status_code == 200:
            await update.message.reply_text(
                "✅ Ваш номер телефона успешно связан!\nТеперь команду /mytasks отправив, вы сможете увидеть задачи, закреплённые за вами.",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                f"❌ Xatolik ({resp.status_code}): {resp.text}"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Serverga ulanib bo‘lmadi: {e}")

async def task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        resp = requests.get(TASKS_URL, params={'telegram_id': chat_id}, timeout=5)
        data = resp.json()
        if resp.status_code != 200 or not data:
            await context.bot.send_message(chat_id=chat_id, text="✅ Sizga hozircha task yo‘q.")
            return

        msg = "📋 *Sizga tegishli tasklar:*\n\n"
        msg += "`№  Nomi                          Status       Muddati`\n"

        for i, task in enumerate(data, 1):
            title = task['title']
            if len(title) > 30:
                title = title[:27] + "..."
            status = task['status']['name']

            def fmt(f):
                raw = task.get(f)
                try:
                    return datetime.fromisoformat(raw).strftime('%d.%m.%Y') if raw else '—'
                except:
                    return '—'

            created = fmt('created_at')
            updated = fmt('updated_at')
            due     = fmt('due_date')
            period = f"{created}→{updated}→{due}"

            msg += f"{i:<3} {title:<30} {status:<12} {period}\n"

        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Xatolik: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # Handler’lar
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CommandHandler("mytasks", task_handler))
    # Polling
    app.run_polling()

if __name__ == "__main__":
    main()

