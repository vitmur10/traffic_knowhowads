from database import get_user_first_access_time
from datetime import datetime, timedelta

def calculate_delay_from_first_access(chat_id, target_hour, target_minute=0, target_day_offset=0):
    """
    Розраховує затримку до наступного дня/часу, відраховуючи від моменту, коли користувач вперше зайшов.
    :param chat_id: chat_id користувача.
    :param target_hour: Цільова година (0-23)
    :param target_minute: Цільова хвилина (0-59)
    :param target_day_offset: Скільки днів переносити в разі, якщо поточний час вже після вказаного.
    :return: Кількість секунд до наступного вказаного дня/часу
    """
    first_access_time = get_user_first_access_time(chat_id)

    if not first_access_time:
        return None  # Якщо користувач не знайдений в БД, повертаємо None

    # Визначаємо наступний день від моменту першого доступу
    if first_access_time.hour >= target_hour and first_access_time.minute >= target_minute:
        next_day = first_access_time + timedelta(days=target_day_offset + 1)
    else:
        next_day = first_access_time + timedelta(days=target_day_offset)

    target_time = next_day.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    # Якщо час ще не настав, обчислюємо затримку
    delay = (target_time - first_access_time).total_seconds()

    return delay