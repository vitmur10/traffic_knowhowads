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
            is_blocked INTEGER DEFAULT 0 -- 0 = не заблоковано, 1 = заблоковано
        );
    """)
    conn.commit()
    conn.close()


def add_or_update_user(user_id: int, username: str, last_message: str, chat_id: int, is_blocked: int = 0):
    """Додає або оновлює користувача в базі даних"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (user_id, username, last_message, is_blocked)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            last_message = excluded.last_message,
            is_blocked = excluded.is_blocked;
    """, (user_id, username, last_message,  is_blocked))
    conn.commit()
    conn.close()


def get_all_users():
    """Повертає всіх користувачів з їх ID, ім'ям та останнім повідомленням"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, last_message FROM users")
    users = cur.fetchall()  # Тепер ми отримуємо всі необхідні поля
    conn.close()
    return users


def get_all_users_with_block_status():
    """Повертає всіх користувачів з їх ID, ім'ям, останнім повідомленням та статусом блокування"""
    users_basic = get_all_users()
    formatted_users = []

    if not users_basic:
        return formatted_users

    user_ids = [user[0] for user in users_basic]

    # Підключення до бази даних
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Формуємо правильний SQL з багатьма плейсхолдерами
    placeholders = ",".join("?" for _ in user_ids)
    query = f"SELECT user_id, is_blocked FROM users WHERE user_id IN ({placeholders})"
    cur.execute(query, user_ids)

    block_statuses = {user_id: is_blocked for user_id, is_blocked in cur.fetchall()}
    conn.close()

    for user in users_basic:
        user_id, username, last_message = user
        is_blocked = block_statuses.get(user_id, 0)
        blocked_status = "Заблоковано" if is_blocked == 1 else "Не заблоковано"

        formatted_users.append({
            "user_id": user_id,
            "username": username,
            "last_message": last_message,
            "blocked_status": blocked_status
        })

    return formatted_users


def save_users_to_csv(file_path: str = None):
    """Зберігає всіх користувачів у форматі CSV з автоматичним шляхом до файлу, якщо не передано"""
    users = get_all_users_with_block_status()

    # Визначаємо поля CSV
    fields = ["user_id", "username", "last_message", "blocked_status"]

    # Генеруємо ім'я файлу, якщо не вказано
    if not file_path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"users_{timestamp}.csv"

    # Записуємо дані в CSV файл
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




