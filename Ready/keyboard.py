from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

order = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="ЗАМОВИТИ ", url="https://t.me/yuliagobysh")],]
)


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Завантажити CSV", callback_data="download_csv")],]
)
write= InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="НАПИСАТИ", url="https://t.me/yuliagobysh")],]
)