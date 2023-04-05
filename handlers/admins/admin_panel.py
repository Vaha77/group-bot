# packages
import asyncio
import datetime

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from playhouse.shortcuts import model_to_dict

#local file
from database.connections import add_user
from keyboards.inline.cancel import cancel
from keyboards.inline.for_admin import inc_dec
from loader import dp, db, bot
from keyboards.default.admins_menu import menu
from aiogram.types import ReplyKeyboardRemove
from states.add_admin import Add_Admin
from states.send_ads import Advers
from database.models import *
from database.connections import *
from filters.private_chat import IsPrivate


adm = Admins.select()
aaa = [model_to_dict(item) for item in adm]
ADMINS = []
ADMINS_NAME = []
for i in aaa:
    ADMINS.append(i["admin_id"])
    ADMINS_NAME.append(i["admin_name"])

try:
    @dp.message_handler(IsPrivate(), commands="admin", user_id=ADMINS)
    async def show_menu(msg: types.Message):
        await msg.answer(text=f'Xush kelibsiz {msg.from_user.full_name} - ADMIN', reply_markup=menu)


    @dp.message_handler(IsPrivate(),text="👤 Foydalanuvchilar", user_id=ADMINS)
    async def all_user(msg: types.Message):
        users = Users.select()
        text = f"Bazada {len(users)} ta foydalanuvchi bor:\n\n"
        await bot.send_message(msg.from_user.id, text)


    @dp.message_handler(IsPrivate(),text="👮🏼‍♂️ Adminlar", user_id=ADMINS)
    async def show_admins(msg: types.Message):
        text = f"Botda {len(ADMINS)} ta admin bor:\n\n"
        num = 0
        a = ''
        for i in range(0, len(ADMINS)):
            num += 1
            a += f"{num}. <a href='tg://user?id={ADMINS[i]}'>{ADMINS_NAME[i]} [{ADMINS[i]}]</a>\n"
        text += a
        await bot.send_message(msg.from_user.id, text,reply_markup=inc_dec)

    @dp.callback_query_handler(text_contains="admin:")
    async def add_adminaa(call: CallbackQuery, state:FSMContext):
        await call.answer(cache_time=60)
        await call.message.delete()
        t = await call.message.answer("Yangi Admin ning Telegram ID sini kiriting: ")
        await state.update_data(
            {"message_id":t.message_id}
        )
        await Add_Admin.admin_id.set()

    @dp.message_handler(IsPrivate(),state=Add_Admin.admin_id)
    async def get_id(msg: types.Message,state:FSMContext):
        xabar = await msg.answer("Yangi Admin ning Ismini kiriting: ")
        await state.update_data(
            {"admin_id": msg.text,
             "t":xabar.message_id}
        )
        await Add_Admin.admin_name.set()

    @dp.message_handler(IsPrivate(),state=Add_Admin.admin_name)
    async def get_admin_name(msg: types.Message, state:FSMContext):
        await state.update_data(
            {"admin_name":msg.text}
        )
        data = await state.get_data()
        admin_id = data["admin_id"]
        admin_name = data["admin_name"]
        print(admin_name,admin_id)
        await add_admin(admin_id,admin_name,msg.from_user.id)
        x1 = data["message_id"]
        x2 = data["t"]
        await bot.delete_message(msg.chat.id,x1)
        await bot.delete_message(msg.chat.id,x2)
        await state.finish()

    @dp.message_handler(IsPrivate(),text="📝 Xabar Yuborish", user_id=ADMINS)
    async def check_adver(msg: types.Message):
        await msg.answer("Xabarni yuboring:",reply_markup=cancel)
        await Advers.text.set()

    @dp.callback_query_handler(state=Advers.text, text="bekor_qilish_btn")
    async def cancel_send_ads(call:CallbackQuery, state:FSMContext):
        await call.answer("Xabar yuborish bekor qilindi.",show_alert=True)
        await call.message.delete()
        await state.finish()

    @dp.message_handler(IsPrivate(),state=Advers.text, content_types=['text', 'video', 'photo', 'audio', 'location'],
                        user_id=ADMINS)
    async def send_ads(msg: types.Message, state: FSMContext):
        use = Users.select()
        users = [model_to_dict(item) for item in use]
        text_caption = msg.caption
        text_type = msg.content_type
        send_user = 0
        send_error = 0
        for user in users:
            user_id = user["telegram_id"]
            try:
                if text_type == 'sticker':
                    return
                elif text_type == 'text':
                    await bot.send_message(user_id, msg.text)
                    await asyncio.sleep(0.05)
                elif text_type == 'video':
                    await bot.send_video(user_id, msg.video.file_id, caption=text_caption)
                    await asyncio.sleep(0.05)
                elif text_type == 'photo':
                    await bot.send_photo(user_id, msg.photo[-1].file_id, caption=text_caption)
                    await asyncio.sleep(0.05)
                elif text_type == 'audio':
                    await bot.send_audio(user_id, msg.audio)
                    await asyncio.sleep(0.05)
                elif text_type == 'location':
                    lat = msg.location['latitude']
                    lon = msg.location['longitude']
                    await bot.send_location(user_id, lat, lon)
                    await asyncio.sleep(0.05)
                send_user += 1
            except Exception:
                send_error += 1
                continue
        if send_user == 0:
            await bot.send_message(msg.from_user.id, 'Xech kimga yuborilmadi')
        else:
            await bot.send_message(msg.from_user.id,
                                   f"Jonatildi: <b>{send_user + send_error}</b> ta foydalanuvchiga\n"
                                   f"Aktiv A'zolar: <b>{send_user}</b> ta \n"
                                   f"Ban bergan a'zolar: <b>{send_error}</b> ta\n")
        await state.finish()

    @dp.message_handler(IsPrivate(),text="🔙 Chiqish", user_id=ADMINS)
    async def send_adver(msg: types.Message):
        await msg.answer("Siz ADMIN PANEL dan chiqdingiz", reply_markup=ReplyKeyboardRemove(True))

except Exception as err:
    pass


@dp.message_handler(IsPrivate(),commands="admin")
async def check_admin(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    await add_user(user_id, name, username, time_now)
    await bot.send_message(message.from_user.id, f"{message.from_user.full_name}. Siz ADMIN emassiz 🧐.")
