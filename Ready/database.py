import asyncio
import csv
import sqlite3
from const import *
from datetime import datetime


# Ініціалізація бази даних
def init_db():
    """Ініціалізація бази даних і створення таблиці, якщо її ще немає"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            last_message TEXT,
            is_blocked INTEGER DEFAULT 0, -- 0 = не заблоковано, 1 = заблоковано
            joined_at TEXT -- дата та час, коли користувач вперше запустив бота
        );
    """)
    conn.commit()
    conn.close()


def add_or_update_user(user_id: int, username: str, last_message: str, chat_id: int, is_blocked: int = 0):
    """Додає або оновлює користувача в базі даних"""
    joined_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Спочатку перевіримо, чи вже є такий користувач
    cur.execute("SELECT joined_at FROM users WHERE user_id = ?", (user_id,))
    result = cur.fetchone()

    if result is None:
        # Якщо користувача немає — вставити з joined_at
        cur.execute("""
            INSERT INTO users (user_id, username, last_message, is_blocked, joined_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, last_message, is_blocked, joined_at))
    else:
        # Якщо користувач є — оновити інші поля, joined_at залишити незмінним
        cur.execute("""
            UPDATE users
            SET username = ?, last_message = ?, is_blocked = ?
            WHERE user_id = ?
        """, (username, last_message, is_blocked, user_id))

    conn.commit()
    conn.close()


def get_all_users():
    """Повертає всіх користувачів з їх ID, ім'ям, останнім повідомленням і joined_at"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, last_message, joined_at FROM users")
    users = cur.fetchall()
    conn.close()
    return users


def get_all_users_with_block_status():
    """Повертає всіх користувачів з ID, ім'ям, останнім повідомленням, статусом блокування та joined_at"""
    users_basic = get_all_users()
    formatted_users = []

    if not users_basic:
        return formatted_users

    user_ids = [user[0] for user in users_basic]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    placeholders = ",".join("?" for _ in user_ids)
    query = f"SELECT user_id, is_blocked FROM users WHERE user_id IN ({placeholders})"
    cur.execute(query, user_ids)
    block_statuses = {user_id: is_blocked for user_id, is_blocked in cur.fetchall()}
    conn.close()

    for user in users_basic:
        user_id, username, last_message, joined_at = user
        is_blocked = block_statuses.get(user_id, 0)
        blocked_status = "Заблоковано" if is_blocked == 1 else "Не заблоковано"

        formatted_users.append({
            "user_id": user_id,
            "username": username,
            "last_message": last_message,
            "joined_at": joined_at,
            "blocked_status": blocked_status
        })

    return formatted_users


def save_users_to_csv(file_path: str = None):
    """Зберігає всіх користувачів у форматі CSV з автоматичним шляхом до файлу, якщо не передано"""
    users = get_all_users_with_block_status()

    fields = ["user_id", "username", "last_message", "joined_at", "blocked_status"]

    if not file_path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"users_{timestamp}.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(users)

    return file_path


def mark_user_blocked(user_id: int):
    """Позначає користувача як заблокованого"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET is_blocked = 1
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()


def get_user_first_access_time(chat_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('SELECT first_access_time FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]  # Повертаємо час першого доступу
    else:
        return None  # Якщо користувач не знайдений

