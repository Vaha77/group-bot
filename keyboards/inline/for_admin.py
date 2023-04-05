from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

inc_dec = InlineKeyboardMarkup(row_width=2)
inc = InlineKeyboardButton(text="➕ Qo'shish",callback_data="admin:inc")
# dec = InlineKeyboardButton(text="➖ O'chirish",callback_data="admin:dec")
inc_dec.add(inc)