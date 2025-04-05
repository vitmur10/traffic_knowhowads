import asyncio
import logging

from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import InputFile, FSInputFile, InputMediaPhoto, InputMediaVideo
from keyboard import order, inline_kb
from const import *
from aiogram import Bot, Dispatcher, Router, types
from database import add_or_update_user, get_all_users_with_block_status, save_users_to_csv, mark_user_blocked
from aiogram.types import ChatMemberUpdated


@router.message(Command("start"))
async def start(message: types.Message):
    """Обробник команди /start"""
    messag = """Привіт! Мене звати Юлія, я — експерт з залучення нового цільового трафіку в Інстаграм.

<a href="https://www.instagram.com/_a_s_t_e_r_i_/">_a_s_t_e_r_i_</a>

Мої учні та клієнти отримують <u>перші результати через 5-7 днів після отримання цієї стратегії.</u>

У цьому уроці я даю все, щоб ви могли самостійно вивчити матеріал і досягти результату максимально швидко:

<b>• Урок по стратегії та залученню трафіку</b>
<b>• Приклади працюючих стратегій для інстаграм-магазинів та експертів</b>

Вам знадобиться менше години для вивчення матеріалу і максимум тиждень для впровадження стратегії, якщо ваш продукт уже є, а акаунт упакований та може автоматично обробляти нову аудиторію.
Починайте! 👇🏻
"""
    add_or_update_user(message.from_user.id, message.from_user.username, "/start", 0)
    await bot.send_message(message.chat.id, messag, parse_mode="HTML")

    # Відправка відео
    thumbnail = FSInputFile("IMG_8227.PNG")
    await bot.send_video(message.chat.id, video=FILE_ID, thumbnail=thumbnail)

    # Запускаємо таймери у фоновому режимі
    asyncio.create_task(delayed_messages(chat_id=message.from_user.id, username=message.from_user.username))


# Функція для виведення статистики користувачів
async def get_user_stats():
    """Повертає статистику про користувачів: кількість заблокованих та не заблокованих"""
    users_with_status = get_all_users_with_block_status()  # Отримуємо всіх користувачів з їх статусом
    blocked_count = 0
    unblocked_count = 0

    for user in users_with_status:
        if user['blocked_status'] == "Заблоковано":
            blocked_count += 1
        else:
            unblocked_count += 1

    stats = f"Статистика користувачів:\n"
    stats += f"Загальна кількість користувачів: {len(users_with_status)}\n"
    stats += f"Заблоковано: {blocked_count}\n"
    stats += f"Не заблоковано: {unblocked_count}\n"

    return stats


# Обробка команди /stats u
@router.message(Command('stats_u'))
async def cmd_stats(message: types.Message):
    """Обробляє команду /stats та виводить статистику користувачів"""
    stats = await get_user_stats()  # Отримуємо статистику

    # Створюємо інлайн кнопку для завантаження CSV

    # Відправляємо статистику користувачеві з інлайн кнопкою
    await message.answer(stats, reply_markup=inline_kb)


# Обробка натискання на інлайн кнопку для завантаження CSV
@router.callback_query(lambda c: c.data == 'download_csv')
async def download_csv(callback_query: types.CallbackQuery):
    """Обробляє натискання на інлайн кнопку для завантаження CSV"""
    file_path = save_users_to_csv()  # Генеруємо CSV файл
    document = FSInputFile(file_path)  # обгортаємо шлях
    await bot.send_document(callback_query.from_user.id, document, caption="Ваша статистика користувачів у форматі CSV")

    # Підтвердження натискання кнопки
    await callback_query.answer("Файл CSV готовий для завантаження!")


async def delayed_messages(chat_id: int, username):
    """Функція для відправки повідомлень із затримкою"""
    await asyncio.sleep(7200)
    try:
        await bot.send_photo(
            chat_id,
            photo=FSInputFile("2.jpg"),
            caption="""Якщо Ви хочете прискорити свій ріст, Я можу допомогти Вам розібратись на особистій консультації та налаштувати для Вас воронку в Ваш акаунт\.
    
    Проходить у такому форматі\:
    
    • я присилаю Вам урок у записі по зв'язці та залученню трафіка 👆подивіться 💵  
    • після перегляду призначаємо дату, і у нас з Вами відео\-сесія *1,5 години*, на якій\:  
    ◦ я відповідаю на Ваші питання по темі уроку, структурі самого рилса і рекламі  
    ◦ роблю розбір, з якого персоналізуємо під Вас і робимо *2\-3 тригерящих оффера*, залишиться тільки вписати їх у свої рилси  
    ◦ розбір Вашого акаунту та продуктової лінійки  
    ◦ складаю *воронку* під Ваші продукти  
    ◦ Якщо у вас немає продуктів, розповім як їх створити у будь\-якій ніші або надам Вам готовий продукт  
    ◦ *7 днів зворотного зв'язку* після консультації  
    
    Вартість особистої консультації *1,5 години* \+ розробка *2\-3 воронок* **150$**  
     *Є розстрочки до 25 місяців, перший платіж тільки через місяць\!*  🔥
    """,
            reply_markup=order,
            parse_mode="MarkdownV2",
        )
        add_or_update_user(chat_id, username, "2", 0)

        await asyncio.sleep(3600)
        await asyncio.sleep(10)  # 3 хвилини
        await bot.send_photo(
            chat_id,
            photo=FSInputFile("3.jpg"),
            caption="""Щоб заробити <b><u>перші тисячі євро</u></b> на моїй зв'язці, потрібно визнати, що все, що Ви робили до цього, не працює.
    
    ❌ <i>ні запуски з програмами</i>,  
    ❌ <i>ні щоденні reels і stories</i>,  
    ❌ <i>ні випадкові продажі на вигорілу аудиторію</i>,  
    ❌ <i>ні все те, що Ви робили "до"</i>.
    
    🟢 <i>ЯКЩО ХОЧЕТЕ ЗРОБИТИ НОВИЙ РИВОК — ПОТРІБНО РОБИТИ ПО-НОВОМУ, НЕ ТАК, ЯК У ВАС БУЛО РАНІШЕ!</i>  
    
    ✅ <i>Все, що ВАМ потрібно — <b><u>впровадити мою зв'язку собі</u></b>, вона складається з:</i>  
    ➡ <i>ТРАФІКУ ПО МОЇЙ СИСТЕМІ + АВТОВОРОНКИ + АВТОМАТИЧНОЇ ОБРОБКИ ЗАЯВОК ЧЕРЕЗ ЧАТ-БОТА.</i>
    
    Я надаю <u>доступ до моїх фахівців, які зроблять усі налаштування для Вас за 7 днів</u> та Ви зможете отримати перші прибутки миттєво.
    
    Ми вирішуємо усі технічні питання — розробка воронок під Вас за <i>150$</i>, налаштування ботів від <i>250$</i> та надаємо інформацію з трафіку.
    
    <i>Є розстрочки до 25 місяців, перший платіж тільки через місяць!</i>🔥
    """,
            reply_markup=order,
            parse_mode="HTML",  # Використовуємо HTML форматування
        )
        add_or_update_user(chat_id, username, "3", 0)

        await asyncio.sleep(3600)

        await bot.send_message(
            chat_id,
            text="""Якщо у Вас є продукт — курси, товари, консультації, марафони, франшизи, послуги — і Ви хочете почати заробляти миттєво, скористайтеся <b>повним супроводом від моєї команди.</b>
    
    Я пропоную <b>зробити весь ваш запуск продажів за вас</b>, тільки в Instagram або в комбінації з сайтом під ваш бізнес, сайтом експерта. Це вам потрібно, якщо ви хочете:  
        •  Почати заробляти швидко  
        •  Монетизувати аудиторію  
        •  Отримувати приплив нових клієнтів
    """,
            parse_mode="HTML"  # Використовуємо HTML форматування
        )

        await bot.send_message(
            chat_id,
            """<b>Давайте налаштуємо Вам трафік за Вас!</b>
    
        <b>Що входить:</b>  
        
        • Особистий розбір вашого бізнесу  
        • Розробка 3–5 воронок  
        • Отрисовка та монтаж рекламних матеріалів  
        • Збірка та підключення робота  
        • Побудова тунелів продажів з прописаними текстами  
        • Список джерел трафіку : блогери, таргет, розсилки   
        • Автоматизація  
    
        Над проєктом працює <b>4 фахівці</b>
    
        <b>Ціна: 1000$</b>  
        
        Мої клієнти <b>заробляють з цієї методики від 5.000 до 12 000$ на місяць.</b>
    
        На всі мої послуги є розстрочка до 25 платежів, це означає, що ваш бізнес може обходитися вам від 40$ до 80$ на місяць, а заробляти ви зможете по кілька тисяч $$$$ одразу!
        """,
            reply_markup=order,
            parse_mode="HTML"  # Використовуємо HTML форматування
        )
        add_or_update_user(chat_id, username, "4", 0)

        await asyncio.sleep(3600)

        media = [
            InputMediaPhoto(media=FSInputFile("7.jpg")),
            InputMediaPhoto(media=FSInputFile("8.jpg")),
            InputMediaPhoto(media=FSInputFile("9.jpg")),
            InputMediaPhoto(media=FSInputFile("10.jpg")),
            InputMediaPhoto(media=FSInputFile("5.jpg")),
            InputMediaPhoto(media=FSInputFile("6.jpg")),
            InputMediaPhoto(media=FSInputFile("photo_2025-04-04_14-59-28.jpg")),
            InputMediaVideo(media=FSInputFile("IMG_8235.MP4")),
            InputMediaVideo(media=FSInputFile("IMG_8260.MOV")),
        ]

        # Додаємо caption до кожного медіафайлу
        media[0].caption = """
    <strong>Кейс: продаж курсів з кондитерства. Як ми заробляли до 500 € на день для клієнта</strong>
    Застосували <u>мою методику з залучення та обробки трафіку по формулі</u>: 
    
    •  безкоштовний курс з 5 уроків 👉🏻 видаємо за репост 
    •  робот надсилає уроки у телеграм-канал
    •  покупка основного продукту. 
    
    <strong>Результат:</strong> 150.000 переглядів рекламного Reels 👉🏻 1500 репостів 👉🏻 3-5 оплат кожен день від 85 € до 145 € 💶
    
    <strong><u>Методика окупилася за 1 тиждень.</u></strong>
    
    А тепер порахуємо: 
    
    •  3 оплати на день по 85 € — на рік ви отримуєте 93.075 €
    •  1 оплата на 145 € — на рік дає 52.925 €
    •  52.925 + 93.075 = 146.000 € на рік при затратах на команду просування від 1.000€ на місяць.
    """
        media[0].parse_mode = "HTML"  # Використовуємо HTML форматування

        # Надсилаємо медіа-групу
        await bot.send_media_group(chat_id=chat_id, media=media)

        # Відправляємо додаткове повідомлення
        await bot.send_message(
            chat_id=chat_id,
            text="Давайте налаштую Вам так само? Пишіть 👇🏼👇🏼👇🏼",
            reply_markup=order  # ваша клавіатура InlineKeyboardMarkup або інша
        )
        add_or_update_user(chat_id, username, "5", 0)

        await asyncio.sleep(36000)
        message1 = """Хочеш стати експертом, продавати в Інстаграм, але у тебе ❌<strong>немає продукту?</strong> ❗️
    
    🟢 <strong>Я надаю готовий продукт, як у мене!</strong> ✅😊
    
    <a href="https://knowhowads.com/">Knowhowads.com</a>"""

        message2 = """У Instagram зареєстровано 2 мільярди людей та 200 мільйонів компаній.
    
    В Instagram 1.28 мільярда активних користувачів щомісяця, і очікується, що до 2040 року річний обсяг продажу реклами досягне близько 2023 мільярдів доларів.
    
    Тільки 5% комерційних акаунтів зараз мають автоматизацію. Це означає, що спеціаліст, який може розповісти та показати механізми автоматичного просування в Instagram, стане найбільш затребуваним і заваленим роботою.
    
    Спеціаліст може шукати клієнтів за моєю методикою прямо в Instagram і <b>продавати послуги автоматизації по 1000$ - 2000$.</b>
    
    <u>Лише <strong>4 клієнти</strong> на місяць можуть принести вам <strong>8000$ вхідних оплат</strong>.</u>
    
    <strong>Моя система включає:</strong>
    
    • Пакет продуманих послуг  
    • Асортиментну матрицю  
    • Методологію трафіку  
    • Сайт під Вас, як експерта  
    • Індивідуальне навчання  
    • Налаштування платіжних систем  
    • Підряд працівників, <strong>доступ до моєї готової команди</strong>
    
    <strong>Готовий бізнес за моєю системою допоможе вам:</strong>
    
    • Оволіти справою, яка дійсно приносить гроші  
    • Отримати передбачуваний результат у вигляді доларів і євро. 💵💶  
    • Допомогу та ведення вашого запуску до першого клієнта!
    
    Все це налаштоване під ключ + індивідуальну підтримку я надаю <strong>за 2.000$</strong>
    
    Є розстрочка від 7 банків України до 25 платежів.
    
    Пишіть скоріше мені  
    👇🏼👇🏼👇🏼"""

        await bot.send_message(chat_id, message1, parse_mode="HTML")
        await bot.send_message(chat_id, message2, parse_mode="HTML", reply_markup=order)
    except TelegramAPIError.Forbidden:
        mark_user_blocked(chat_id)
