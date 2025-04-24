import asyncio
import logging
from func import calculate_delay_from_first_access
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import InputFile, FSInputFile, InputMediaPhoto, InputMediaVideo
from keyboard import order, inline_kb, write
from const import *
from aiogram import Bot, Dispatcher, Router, types, F
from database import add_or_update_user, get_all_users_with_block_status, save_users_to_csv, mark_user_blocked, get_user_first_access_time
from aiogram.types import ChatMemberUpdated


@router.message(Command("start"))
async def start(message: types.Message):
    """Обробник команди /start"""
    messag = """Привіт!

Я Юлія Гобиш, фахівець з управління проектами електронної комерціі. 


<a href="https://www.instagram.com/_a_s_t_e_r_i_/">_a_s_t_e_r_i_</a>

@yuliagobysh 

Інтернет-магазин вартістю всього лише 3.500$ може продавати товари на суму близько <strong>300.000$ на рік</strong>, керуючись повністю пошуковою рекламою та віддаленою командою.

Це автопілотні доходи, вам залишається тільки відправляти товар і забирати гроші з пошти.

Відео — це мій особистий досвід ведення цього бізнесу протягом 15 років в Україні.

Починайте 
⬇️

"""
    add_or_update_user(message.from_user.id, message.from_user.username, "/start", 0)
    await bot.send_message(message.chat.id, messag, parse_mode="HTML")

    # Відправка відео
    await bot.send_video(chat_id=message.chat.id, video=FILE_ID)

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


    try:
        await asyncio.sleep(60*10)
        await bot.send_media_group(chat_id=chat_id, media=[
            InputMediaPhoto(media=FSInputFile("4/1.jpg")),
            InputMediaPhoto(media=FSInputFile("4/2.jpg")),
            InputMediaPhoto(media=FSInputFile("4/3.jpg")),
            InputMediaPhoto(media=FSInputFile("4/4.jpg")),
            InputMediaPhoto(media=FSInputFile("4/5.jpg")),
            InputMediaPhoto(media=FSInputFile("4/6.jpg")),

        ])
        await bot.send_message(chat_id=chat_id, text="""Цей сайт доступний для придбання. 👇🏼
https://buybrands.com.ua/ """)
        await bot.send_message(
            chat_id,
            text="""
<strong>Ціна 3.500$</strong>

<strong>Що входить у вартість:</strong>

● Повнофункціональний інтернет-магазин

● Заповнений каталог із 3000 позицій товарів

● Команда з маркетінгу 

● Підключені постачальники

<strong>Окремо оплачується:</strong>

● Соціальні мережі: зйомка, дизайн, стратегія, реклама — від 1 500$ на місяць

● Рекламний бюджет на Google — від 500$ на місяць

Можна працювати в Україні або увімкнути польську мову на сайті (входить у комплект) та працювати на дві країни. Загалом доступно 12 мов.

На всі мої послуги є розстрочка від 7 банків України до 25 місяців. ✅👇🏼

""",
            reply_markup=order,
            parse_mode="HTML",
        )
        add_or_update_user(chat_id, username, "2", 0)
        await bot.send_media_group(chat_id=chat_id, media=[
            InputMediaPhoto(media=FSInputFile("кейс1.jpg")),
            InputMediaPhoto(media=FSInputFile("кейс2.jpg")),
            InputMediaPhoto(media=FSInputFile("кейс3.jpg")),
            InputMediaPhoto(media=FSInputFile("кейс4.jpg")),
            InputMediaPhoto(media=FSInputFile("кейс5.jpg")),
            InputMediaPhoto(media=FSInputFile("кейс6.jpg")),

        ])
        await bot.send_message(chat_id, """Цей сайт має соковитий дизайн 😍також доступний для придбання. 👇🏼
https://balibeauty.com.ua/""")
        await bot.send_message(
            chat_id,
            text="""
<strong>Ціна 3.500$</strong>

<strong>Що входить у вартість:</strong>

● Повнофункціональний інтернет-магазин

● Заповнений каталог із 3000 позицій товарів

● Команда з маркетінгу 

● Підключені постачальники

<strong>Окремо оплачується:</strong>

● Соціальні мережі: зйомка, дизайн, стратегія, реклама — від 1 500$ на місяць

● Рекламний бюджет на Google — від 500$ на місяць

Можна працювати в Україні або увімкнути польську мову на сайті (входить у комплект) та працювати на дві країни. Загалом доступно 12 мов.

На всі мої послуги є розстрочка від 7 банків України до 25 місяців. ✅👇🏼

""",
            reply_markup=order,
            parse_mode="HTML",  # Використовуємо HTML форматування
        )

        add_or_update_user(chat_id, username, "3", 0)
        await asyncio.sleep(3600)
        await bot.send_message(chat_id, "https://wayforpay.com/uk/payparts", parse_mode="HTML")
        await bot.send_message(
            chat_id,
            text="""
Друзі, наразі вам доступна розтрочка на купівлю інтернет-магазинів до 25 платежів 
Від 7 банків України. 💶💵

Налаштовую розтрочку кожному індівідуально, пишіть у особисті повідомлення. 👇🏼
""",reply_markup=order,
            parse_mode="HTML"  # Використовуємо HTML форматування
        )
        add_or_update_user(chat_id, username, "4", 0)
        delay = calculate_delay_from_first_access(chat_id, target_day_offset=0, target_hour=11)
        await asyncio.sleep(delay)
        # Надсилаємо медіа-групу
        await bot.send_photo(chat_id=chat_id, photo=FSInputFile("5/5.jpg"), caption="""
Привіт! 😊Додаю фото відправок замовлень з мого інтернет-магазину люкс косметики. 
 
На моєму прикладі можете побачити <ins>попит на товари,</ins> та які <ins>обсяги</ins> менеджер з обробки замовлень вивозить Новою поштою 2 рази на день. 
 
Саме такі магазини, з  однорідними товарами у мене у продажу.

""", parse_mode="HTML")
        media_two = [
            InputMediaPhoto(media=FSInputFile("5/5_11.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_12.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_1_2025-04-19_16-16-44.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_1_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_2_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_3_2025-04-19_16-16-44.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_3_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_4_2025-04-19_16-16-44.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_4_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_5_2025-04-19_16-16-44.jpg")),

        ]
        media_three = [
            InputMediaPhoto(media=FSInputFile("5/photo_5_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_6_2025-04-19_16-16-44.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_5_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_7_2025-04-19_16-16-44.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_7_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_8_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_9_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_10_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_11_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_12_2025-04-19_16-17-35.jpg")),

        ]
        media_four = [
            InputMediaPhoto(media=FSInputFile("5/photo_13_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_14_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_15_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_16_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_17_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_18_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_19_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_20_2025-04-19_16-17-35.jpg")),
            InputMediaPhoto(media=FSInputFile("5/photo_21_2025-04-19_16-17-35.jpg")),

        ]
        await bot.send_media_group(chat_id=chat_id, media=[
            InputMediaPhoto(media=FSInputFile("5/5_1.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_2.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_3.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_4.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_5.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_6.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_7.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_8.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_9.jpg")),
            InputMediaPhoto(media=FSInputFile("5/5_10.jpg")),
        ])
        await bot.send_media_group(chat_id=chat_id, media=media_two)
        await bot.send_media_group(chat_id=chat_id, media=media_three)
        await bot.send_media_group(chat_id=chat_id, media=media_four)
        await bot.send_media_group(chat_id=chat_id,
                                   media=[InputMediaPhoto(media=FSInputFile("5/photo_22_2025-04-19_16-17-35.jpg")),
                                          InputMediaPhoto(media=FSInputFile("5/photo_23_2025-04-19_16-17-35.jpg")),
                                          InputMediaPhoto(media=FSInputFile("5/photo_24_2025-04-19_16-17-35.jpg"))])
        add_or_update_user(chat_id, username, "5", 0)
        await asyncio.sleep(3600*4)
        # Відправляємо додаткове повідомлення
        await bot.send_message(
            chat_id=chat_id,
            text="""А це 👇🏻ті ж самі відправки з мого інтернет-магазину у грошах. 
 
На моєму прикладі можете побачити попит на товари, та на які  суми замовляють. 
Магазин отримує від 50% прибутку з суми замовлення.


""",
            reply_markup=order  # ваша клавіатура InlineKeyboardMarkup або інша
        )
        media = [
            InputMediaPhoto(media=FSInputFile("6/photo_1_2025-04-19_16-19-34.jpg")),
            InputMediaPhoto(media=FSInputFile("6/photo_2_2025-04-19_16-19-34.jpg")),
            InputMediaPhoto(media=FSInputFile("6/photo_3_2025-04-19_16-19-34.jpg")),
            InputMediaPhoto(media=FSInputFile("6/photo_4_2025-04-19_16-19-34.jpg")),
            InputMediaPhoto(media=FSInputFile("6/photo_5_2025-04-19_16-19-34.jpg")),
            InputMediaPhoto(media=FSInputFile("6/photo_6_2025-04-19_16-19-34.jpg")),
        ]
        await bot.send_media_group(chat_id=chat_id, media=media)
        add_or_update_user(chat_id, username, "6", 0)
        await asyncio.sleep(3600*3)
        await bot.send_message(
            chat_id=chat_id,
            text="""<strong>Постачальники</strong> - це офіційні дистриб'ютори брендів в Україні. 

Постачальники проводять регулярні презентації новинок товарів, та вас, як власника (власницю) інтернет-магазину будуть запрошувати на спеціальні заходи та дарувати подарунки. 🤩

Зазвичай це лекції від дерматологів з Великобританії, Франції, або огляди нових лінійок. 

<strong>МОЇ САЙТИ ПРАЦЮЮТЬ ПО СИСТЕМІ ДРОПШИППІНГ</strong>

Деякі бренди виставляли стартові закупки у розмірі від 1.000Є до 15.000Є,  я вже їх робила та маю активні контракти, якими можу поділитися зі своїми покупцями. 

<strong>Але 95% дистриб'юторів  працюють <ins>від 1 одиниці товару.</ins></strong>

Деякі власники магазинів приїжджають до Києва на такі події на день, якщо магазин розташований у іншому місті. 
👇🏻

    """,
            reply_markup=order  # ваша клавіатура InlineKeyboardMarkup або інша
            , parse_mode="HTML")

        await bot.send_media_group(chat_id=chat_id, media=[
            InputMediaPhoto(media=FSInputFile("7/photo_1_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_2_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_3_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_4_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_5_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_6_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_7_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_8_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_9_2025-04-19_21-53-56.jpg")),
        ])
        await bot.send_media_group(chat_id=chat_id, media=[
            InputMediaVideo(media="BAACAgIAAxkBAAIHh2gGIUWOsQxfSDmHx3o0mKnxcpM1AAICcwACwE4wSPXIuEkH9rfbNgQ"),
            InputMediaVideo(media="BAACAgIAAxkBAAIHiGgGIUWlnTAPc54ZPBxHMgmhUKAIAAIEcwACwE4wSKQEFdHwc47-NgQ"),
            InputMediaVideo(media="BAACAgIAAxkBAAIHhmgGIUVxy6GhLHsYPMrdvpXV7vCDAAIDcwACwE4wSNGbpHuEZ_1lNgQ")])
        await bot.send_media_group(chat_id=chat_id, media=[InputMediaPhoto(media=FSInputFile("7/photo_10_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_11_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_13_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_12_2025-04-19_21-53-56.jpg")),
            InputMediaPhoto(media=FSInputFile("7/photo_14_2025-04-19_21-53-56.jpg")),
        ])
        add_or_update_user(chat_id, username, "7", 0)
        delay = calculate_delay_from_first_access(chat_id, target_day_offset=0, target_hour=11)
        await asyncio.sleep(delay)
        await bot.send_message(
            chat_id=chat_id,
            text="""<strong>Кейс 675 000 грн через кошик з інтернет-магазину 

Інтернет-магазин косметики</strong> запустили з 0 до <strong>330.000 грн на момент запису цього кейсу.

Працює і далі, Update виторг вже склав 677 000 грн</strong> через кошик. 

Вланиця орендувала офіс у Києві, викуповує товар та розвиває справу далі. 

        """,
            reply_markup=order  # ваша клавіатура InlineKeyboardMarkup або інша
            , parse_mode="HTML")
        media = [
            InputMediaVideo(media=FSInputFile("video_2025-04-19_17-26-56.mp4")),
        ]
        await bot.send_media_group(chat_id=chat_id, media=media)

        add_or_update_user(chat_id, username, "8", 0)
        await asyncio.sleep(3600*4)
        await bot.send_message(
            chat_id=chat_id,
            text="""<strong>Кейс 1 мільйон 700 тисяч грн через кошик з інтернет-магазину</strong>

Цей магазин запустили під клієнта минулого року. 

За кілька місяців сайт зробив прибуток <strong>1.700 000 грн</strong> та продовжує працювати.  

Щоб придбати подібний сайт пишіть мені 👇🏼""",
            reply_markup=order
            , parse_mode="HTML")
        media = [
            InputMediaVideo(media=FSInputFile("IMG_5621.MP4")),
        ]
        await bot.send_media_group(chat_id=chat_id, media=media)
        add_or_update_user(chat_id, username, "9", 0)
        await asyncio.sleep(3600*3)

        await bot.send_message(
            chat_id=chat_id,
            text=""" Відгуки про співпрацю зі мною 👇🏻""", parse_mode="HTML", reply_markup=write)
        await bot.send_media_group(chat_id=chat_id, media=[
            InputMediaVideo(media="BAACAgIAAxkBAAIF5mgGHYmE7vAMQogddXem623KyAs4AAKrcgACwE4wSPwGlvr7xMl5NgQ"),
            InputMediaVideo(media=FSInputFile("відгук2.MP4"))
            ])

        await bot.send_media_group(chat_id=chat_id, media=[InputMediaVideo(media=FSInputFile("відгук3.MP4")),
                                                           InputMediaVideo(media=FSInputFile("відгук4.MP4")),
                                                           ])

        add_or_update_user(chat_id, username, "10", 0)
        delay = calculate_delay_from_first_access(chat_id, target_day_offset=0, target_hour=11)
        await asyncio.sleep(delay)
        await bot.send_media_group(chat_id=chat_id, media=[InputMediaPhoto(media=FSInputFile("11/1.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/2.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/3.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/4.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/5.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/6.jpg"))
                                                           ])
        await bot.send_media_group(chat_id=chat_id, media=[InputMediaPhoto(media=FSInputFile("11/7.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/8.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/9.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/10.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/11.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/12.jpg")),
                                                           InputMediaPhoto(media=FSInputFile("11/13.jpg"))
                                                           ])
        await bot.send_message(
            chat_id=chat_id,
            text="""<strong>Пакет “Впевнений старт” інтернет магазин + соц мережі</strong>
      
Якщо Ви хочете швидкий старт, то разом з сайтом я пропоную запуск реклами у соц мережах:

 ● <strong>художнє оформлення</strong> —  йдеться про зовнішній вигляд  (дизайн Reels → оформлення аккаунту)

 ● <strong>проектування</strong> — розробка 2-3 воронок, тунелів продажів, стратегія реклами.

 ● <strong>автоматизація</strong> — збірка та підключення робота. 

Результатом буде налаштування та запуск продажів товарів у тому числі через Інстаграм. 

<strong>Ціна:</strong> магазин 3500$ + соц мережі 1500$ = <strong>5.000$</strong>

<strong>Вклавши у фундамент свого бізнесу таку невелику суму ви <ins>вирішуєте раз і назавжди питання з чергою покупців на товари,</ins> отримуєте <ins>впевненість та спокій.</ins></strong>
""",
            reply_markup=order
            , parse_mode="HTML")
        add_or_update_user(chat_id, username, "11", 0)
        delay = calculate_delay_from_first_access(chat_id, target_day_offset=0, target_hour=11)
        await asyncio.sleep(delay)
        await bot.send_message(
            chat_id=chat_id,
            text="""Якщо для вас актуальний запуск власного інтернет-магазину, але ви не знаєте, з чого почати 
— запрошую вас на <strong>безкоштовну стратегічну сесію,</strong> на якій я покажу всі переваги автоматизованого онлайн-бізнесу:
            
        1.Як знаходити клієнтів ✅


        2.Які товари продавати ✅


        3.Яку нішу обрати ✅


Мої магазини підходять для будь-яких товарів. У них можна змінити дизайн, логотип, назву.

Головне — <strong>моя автоматизована система продажів,</strong> яка дозволяє виходити на виторг від <strong>300 000$ на рік і більше.</strong>

Ми навчилися вирішувати такі завдання.

Пишіть мені в повідомлення @yuliagobysh, домовимось про зустріч у Zoom і разом складемо <strong>покроковий план дій</strong> для побудови вашого товарного бізнесу.
""", reply_markup=write
            , parse_mode="HTML")
        add_or_update_user(chat_id, username, "12", 0)

    except TelegramAPIError:
        mark_user_blocked(chat_id)
