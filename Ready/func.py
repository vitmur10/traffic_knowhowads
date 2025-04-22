from database import get_user_first_access_time
from datetime import datetime, timedelta

def calculate_delay_from_first_access(chat_id, target_hour, target_minute=0, target_day_offset=0):
    first_access_time = get_user_first_access_time(chat_id)

    if not first_access_time:
        return None  # Якщо користувач не знайдений в БД, повертаємо None

    # Перевіряємо, чи first_access_time є строкою і перетворюємо її в datetime, якщо потрібно
    if isinstance(first_access_time, str):
        first_access_time = datetime.strptime(first_access_time, '%Y-%m-%d %H:%M:%S')  # Підлаштуйте формат, якщо потрібно

    # Логування для перевірки значень
    print(f"first_access_time: {first_access_time}")

    # Визначаємо наступний день від моменту першого доступу
    if first_access_time.hour >= target_hour and first_access_time.minute >= target_minute:
        next_day = first_access_time + timedelta(days=target_day_offset + 1)
    else:
        next_day = first_access_time + timedelta(days=target_day_offset)

    # Логування для перевірки next_day
    print(f"next_day: {next_day}")

    target_time = next_day.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    # Логування для перевірки target_time
    print(f"target_time: {target_time}")

    # Якщо час ще не настав, обчислюємо затримку
    delay = (target_time - first_access_time).total_seconds()

    # Якщо затримка від'ємна, це означає, що обчислений час вже минув
    if delay < 0:
        print("Затримка від'ємна, перевірте обчислення часу.")
        return None

    return delay
