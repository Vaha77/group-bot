from aiogram.types import MessageEntity
from loader import dp, bot
from database.models import *


async def check_text(message):
    for entity in message.entities:
        if entity.type in ["url","text_link","mention"]:
            return True
    return False

