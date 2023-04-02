import asyncio
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

#local file
from playhouse.shortcuts import model_to_dict

from data.config import ADMINS, ADMINS_NAME
from loader import dp, db, bot
from keyboards.default.admins_menu import menu
from aiogram.types import ReplyKeyboardRemove
from states.send_ads import Advers
from database.models import *
from filters.private_chat import IsPrivate


try:
    @dp.message_handler(IsPrivate(), text="/admin", user_id=ADMINS)
    async def show_menu(msg: types.Message):
        await msg.answer(text=f'Xush kelibsiz {msg.from_user.full_name} - ADMIN', reply_markup=menu)


    @dp.message_handler(IsPrivate(),text="👤 Foydalanuvchilar", user_id=ADMINS)
    async def all_user(msg: types.Message):
        users = Users.select()
        text = f"Bazada {len(users)} ta foydalanuvchi bor:\n\n"
        await bot.send_message(msg.from_user.id, text)


    @dp.message_handler(text="👮🏼‍♂️ Adminlar", user_id=ADMINS)
    async def show_admins(msg: types.Message):
        text = f"Botda {len(ADMINS)} ta admin bor:\n\n"
        num = 0
        a = ''
        for i in range(0, len(ADMINS)):
            num += 1
            a += f"{num}. <a href='tg://user?id={ADMINS[i]}'>{ADMINS_NAME[i]} [{ADMINS[i]}]</a>\n"
        text += a
        await bot.send_message(msg.from_user.id, text)


    @dp.message_handler(IsPrivate(),text="📝 Xabar Yuborish", user_id=ADMINS)
    async def check_adver(msg: types.Message):
        await msg.answer("Xabarni yuboring:")
        await Advers.text.set()


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
            print(user)
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
except:
    print('Bu foydalanuvchi admin emas')


@dp.message_handler(commands="admin")
async def check_admin(msg: types.Message):
    await msg.answer(f"{msg.from_user.full_name}. Siz ADMIN emassiz 🧐.")
