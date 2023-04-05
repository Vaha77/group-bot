from database.models import *
from data.config import ADMINS
from loader import bot,db,dp


async def add_user(user_id,name,username,time_now):
    with db:
        if not Users.select().where(Users.telegram_id == user_id).exists():
            Users.create(
                telegram_id=user_id,
                full_name=name,
                username=username,
                join_date=time_now
            )

            count = Users.select()
            msg = f"<a href='tg://user?id={user_id}'>{name}</a> bazaga qo'shildi.\nBazada {len(count)} ta foydalanuvchi bor."
            for user in ADMINS:
                await bot.send_message(user, msg)

async def add_admin(admin_id: int,admin_name: str,msg_id: int):
    with db:
        if not Admins.select().where(Admins.admin_id == admin_id).exists():
            Admins.create(
                admin_id=admin_id,
                admin_name=admin_name
            )
            text = f"<a href='tg://user?id={admin_id}'>{admin_name}</a> Admin qilindi"
            await bot.send_message(msg_id,text)

async def add_channel(channel_id,title):
    with db:
        if not Channels.select().where(Channels.channel_id == channel_id).exists():
            Channels.create(
                channel_id=channel_id,
                title=title
            )
            count = Channels.select()
            msg = f"<b>{title}</b> — guruh bazaga qo'shildi.\nBazada {len(count)} ta guruh bor."
            for user in ADMINS:
                await bot.send_message(user, msg)