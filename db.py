import sqlite3

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('bot_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Функция для создания таблиц в базе данных
def initialize_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 5000
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS game_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                amount INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        conn.commit()

# Функция для получения информации о пользователе
def get_user(user_id):
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return user

# Функция для добавления нового пользователя
def add_user(user_id, username):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()

# Функция для обновления баланса пользователя
def update_balance(user_id, amount):
    with get_db_connection() as conn:
        conn.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()

# Функция для получения баланса пользователя
def get_balance(user_id):
    user = get_user(user_id)
    return user['balance'] if user else None
