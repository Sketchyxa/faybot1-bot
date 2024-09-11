from db import get_balance, update_balance, add_user
import random

def play_heads_or_tails(user_id, bet_amount):
    balance = get_balance(user_id)
    
    if balance is None:
        return "Ошибка: пользователь не найден."
    
    if bet_amount > balance:
        return "Ошибка: недостаточно средств."
    
    result = random.choice(['Орел', 'Решка'])
    if result == 'Орел':
        update_balance(user_id, bet_amount)  # Победа
        return f"Вы выиграли! {result}. Ваш новый баланс: {get_balance(user_id)}"
    else:
        update_balance(user_id, -bet_amount)  # Проигрыш
        return f"Вы проиграли! {result}. Ваш новый баланс: {get_balance(user_id)}"

