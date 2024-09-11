import telebot
import random
from db import create_db, get_balance, update_balance, create_user
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Создание базы данных при запуске
create_db()

# Игра "Орел и решка"
@bot.message_handler(commands=['flip'])
def coin_flip(message):
    user_id = message.from_user.id
    if get_balance(user_id) is None:
        create_user(user_id)
    balance = get_balance(user_id)

    if balance < 100:
        bot.reply_to(message, "Недостаточно монет для игры. Минимальная ставка — 100 монет.")
        return

    outcome = random.choice(['Орел', 'Решка'])
    bet = 100  # Ставка по умолчанию

    if outcome == 'Орел':
        update_balance(user_id, bet)
        bot.reply_to(message, f"Выпал Орел! Вы выиграли {bet} монет. Ваш текущий баланс: {balance + bet}")
    else:
        update_balance(user_id, -bet)
        bot.reply_to(message, f"Выпала Решка! Вы проиграли {bet} монет. Ваш текущий баланс: {balance - bet}")

# Запуск бота
bot.polling()

