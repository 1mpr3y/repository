from dotenv import load_dotenv
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
    Updater
)

# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# logger = logging.getLogger(__name__)

# Токен бота
load_dotenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN"))


# /start
async def start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_keyboard = [
    [InlineKeyboardButton("👤 Профиль", callback_data='profile'),
     InlineKeyboardButton("💎 Подписка", callback_data='subscribe')],
    [InlineKeyboardButton("🎁 Запустить", callback_data='launch'),
     InlineKeyboardButton("👥 О нас", callback_data='info')],
    [InlineKeyboardButton("🇺🇸 Language", callback_data='language'),
     InlineKeyboardButton("⚙️ Настройки", callback_data='settings')],
    [InlineKeyboardButton("✉️ Реферальная система", callback_data='referral')]
]
    reply_markup = InlineKeyboardMarkup(first_keyboard)
    await update.message.reply_text("<b>Привет! Я бот, который повторяет твои сообщения.</b>", reply_markup=reply_markup, parse_mode="html")

# Назад
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    first_keyboard = [
    [InlineKeyboardButton("👤 Профиль", callback_data='profile'),
     InlineKeyboardButton("💎 Подписка", callback_data='subscribe')],
    [InlineKeyboardButton("🎁 Запустить", callback_data='launch'),
     InlineKeyboardButton("👥 О нас", callback_data='info')],
    [InlineKeyboardButton("🇺🇸 Language", callback_data='language'),
     InlineKeyboardButton("⚙️ Настройки", callback_data='settings')],
    [InlineKeyboardButton("✉️ Реферальная система", callback_data='referral')]
]
    reply_markup = InlineKeyboardMarkup(first_keyboard)
    await query.edit_message_text("Привет! Я бот, который повторяет твои сообщения.", reply_markup=reply_markup)
# Профиль
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id) # Запрос айди
    user_fullname = (update.effective_user.full_name) # Запрос имени
    user_name = (update.effective_user.name) # Запрос юзернейма
    query = update.callback_query
    second_keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(second_keyboard)
    await query.edit_message_text(f"ℹ️ <b>Ваша информация</b>\n• ID: <b>{user_id}</b>\n• Имя: <b>{user_fullname}</b>\n• Юзернейм: <b>{user_name}</b>\n\n<b>📊 Статистика</b>\n• Приобретено подписок: <b>0</b>\n• Поймано NFT: <b>0</b>\n• Бизнес-аккаунт: <b>не подключен</b>", reply_markup=reply_markup, parse_mode="html")

# Функция обработки нажатий на кнопки
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data == "profile":
        await show_profile(update, context)
    elif data == "subscribe":
        await query.answer()
        await query.edit_message_text(text="Вы нажали Новую кнопку 1")
    elif data == "back":
        await show_menu(update, context)
    else:
        await query.answer()
        await query.edit_message_text(text="Неизвестная кнопка")

# Эхо-функция для повторения сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(user_message)

# Основная логика запуска приложения
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация команд
    app.add_handler(CommandHandler("start", start_menu))   # команда /start
    app.add_handler(CallbackQueryHandler(handle_buttons))       # обработка кликов по кнопкам
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))  # повторение сообщений

    # Запуск бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()