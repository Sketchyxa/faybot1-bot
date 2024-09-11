import telebot
from config import BOT_TOKEN
from handlers import register_handlers
from db import initialize_db

# Инициализация базы данных
initialize_db()

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Регистрация обработчиков
register_handlers(bot)

# Запуск бота
bot.polling()
