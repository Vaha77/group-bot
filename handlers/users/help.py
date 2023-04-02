import datetime

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from database.connections import add_user
from loader import dp,bot


@dp.message_handler(CommandHelp())
async def help_user(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    await add_user(user_id, name, username, time_now)
    msg = f"Bot Tomonidan foydalanuvchiga yordam ko'rsatish bo'limi\n" \
          f"Buyruqlar:\n/start — Botni ishga tushirish\n" \
          f"/help — Yordam Ko'rsatish va Bot ishlash tartibi\n\n" \
          f"<b>Botni ishlash tartibi</b>\n\n" \
          f"Assalomu alaykum, {name}!\n" \
          f"👮🏻‍♂ <b>Men sizga guruhlarni boshqarishingizga yordam beraman 👇</b>\n\n" \
          f"🖇 - <em>Guruhdan reklamalarni o'chiraman</em> \n " \
          f"🚫 - <em>Spam xabarlarni tozalayman</em> \n" \
          f"🛂 - <em>Odamlarni boshqarib turaman</em>\n" \
          f"🗑 - <em>Kirdi-chiqdilarni tozalayman</em>\n\n" \
          f"❗️Men to‘liq ishlashim uchun <b>ADMIN</b> qilib tayinlashingiz kerak"


    await bot.send_message(message.from_user.id,msg)
