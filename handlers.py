import random
from telebot import TeleBot
from filters import contains_forbidden_word, contains_forbidden_phrase, URL_REGEX
from config import DELETE_DELAY
from heroes import HEROES
from db import get_user, add_user, get_balance
from game import play_heads_or_tails

def delete_message_and_notify(bot: TeleBot, chat_id, message_id, notification_text):
    try:
        bot.delete_message(chat_id, message_id)
        notification_message = bot.send_message(chat_id, notification_text)
        time.sleep(DELETE_DELAY)
        bot.delete_message(chat_id, notification_message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка удаления сообщения: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

def register_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.from_user.id
        username = message.from_user.username or "Неизвестный пользователь"
        
        if not get_user(user_id):
            add_user(user_id, username)
            bot.send_message(message.chat.id, f"Добро пожаловать, {username}! Ваш баланс: {get_balance(user_id)}")
        else:
            bot.send_message(message.chat.id, f"Добро пожаловать обратно, {username}! Ваш баланс: {get_balance(user_id)}")

    @bot.message_handler(content_types=['photo', 'video', 'document'])
    def handle_media_messages(message):
        chat_id = message.chat.id
        if message.caption and (contains_forbidden_phrase(message.caption) or message.forward_from and message.forward_from.is_bot):
            delete_message_and_notify(bot, chat_id, message.message_id, "Сообщение удалено из-за наличия рекламы")

    @bot.message_handler(func=lambda message: True)
    def handle_text_messages(message):
        chat_id = message.chat.id
        text = message.text.lower()
        user_id = message.from_user.id

        if contains_forbidden_word(text) or contains_forbidden_phrase(text) or re.search(URL_REGEX, text) or (message.forward_from and message.forward_from.is_bot):
            delete_message_and_notify(bot, chat_id, message.message_id, "Сообщение удалено из-за использования запрещённых слов, фраз или ссылок.")

        if text.startswith("бот, назови рандомного героя") or \
           text.startswith("бот, на ком мне сегодня заруинить") or \
           text.startswith("бот, на ком мне победить"):
            hero = random.choice(HEROES)
            bot.send_message(chat_id, f"Я выбираю: {hero}")

        elif text.startswith("бот, орел или решка") or text.startswith("бот, сыграем в орел и решка"):
            _, bet_amount = text.split(maxsplit=1)
            try:
                bet_amount = int(bet_amount)
                response = play_heads_or_tails(user_id, bet_amount)
                bot.send_message(chat_id, response)
            except ValueError:
                bot.send_message(chat_id, "Ошибка: неверная сумма ставки. Укажите целое число.")

    @bot.edited_message_handler(func=lambda message: True)
    def handle_edited_messages(message):
        chat_id = message.chat.id
        text = message.text.lower()

        if contains_forbidden_word(text) or contains_forbidden_phrase(text) or re.search(URL_REGEX, text):
            delete_message_and_notify(bot, chat_id, message.message_id, "Сообщение удалено из-за использования запрещённых слов, фраз или ссылок после редактирования.")

    @bot.message_handler(func=lambda message: message.forward_from and message.forward_from.is_bot)
    def handle_forwarded_from_bots(message):
        chat_id = message.chat.id
        delete_message_and_notify(bot, chat_id, message.message_id, "Сообщение удалено, так как оно было переслано от другого бота.")

