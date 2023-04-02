import datetime
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from playhouse.shortcuts import model_to_dict
from filters.group import IsGroup
from filters.private_chat import IsPrivate
from keyboards.inline.add_group import keyboard

from data.config import ADMINS
from database.connections import *
from loader import dp, db, bot
from database.models import *
from utils.misc.check_ads import check_text


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # ADD USER IN DB
    await add_user(user_id,name,username,time_now)
    await bot.send_message(user_id,f"Assalomu alaykum, {name}!\n"
                         f"👮🏻‍♂ <b>Men sizga guruhlarni boshqarishingizga yordam beraman 👇</b>\n\n"
                         f"🖇 - <em>Guruhdan reklamalarni o'chiraman</em> \n "
                         f"🚫 - <em>Spam xabarlarni tozalayman</em> \n"
                         f"🛂 - <em>Odamlarni boshqarib turaman</em>\n"
                         f"🗑 - <em>Kirdi-chiqdilarni tozalayman</em>\n\n"
                         f"❗️Men to‘liq ishlashim uchun <b>ADMIN</b> qilib tayinlashingiz kerak",reply_markup=keyboard)


@dp.message_handler(IsGroup(),content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def new_chat(msg: types.Message):
    try:
        await msg.delete()
    except Exception as err:
        pass
#
@dp.message_handler(IsGroup(),content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat1(msg: types.Message):
    try:
        await msg.delete()
    except Exception as err:
        pass
    chat_id = msg["chat"]["id"]
    title = msg["chat"]["title"]
    await add_channel(chat_id,title)
    await msg.answer(f"Foydalanuvchi <a href='tg://user?id={msg['from']['id']}'>{msg['from']['first_name']}</a> — <a href='tg://user?id={msg['new_chat_members'][0]['id']}'>{msg['new_chat_members'][0]['first_name']}</a> ni qo'shdi.")

@dp.message_handler(IsGroup(),content_types=["text","video","photo","audio","file"])
async def delete_ads(msg: types.Message):
    chat_admins = await bot.get_chat_administrators(msg.chat.id)
    text = msg.text.lower()
    admin_list = []
    for i in chat_admins:
        admin_list.append(i["user"]["id"])
    print(admin_list)
    if await check_text(message=msg):
        if msg.from_user.id not in admin_list:
            await msg.delete()
            await msg.answer(f"{msg.from_user.get_mention(as_html=True)} Reklama tarqatmang !")
    admin_list.clear()
    print(admin_list)