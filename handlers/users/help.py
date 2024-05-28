from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        "Buyruqlar:",
        "/start - Botni ishga tushurish",
        "/help - Yordam"
    ]

    admin_text = [
        "Buyruqlar:",
        "/start - Botni ishga tushurish",
        "/help - Yordam",
        "/doc - Hisobot",
        "/booked - Band qilingan xonalar",
        "/id - Xona band qilganlarni user idsi va ism-familiyasi",
        "/delete - Band qilingan xonalarni hammasini o'chirish",
        "/del user_id - ID tegishli bo'lgan userni o'chirish"
    ]

    user_id = message.from_user.id
    if user_id in ADMINS:
        await message.reply("\n".join(admin_text))
    else:
        await message.reply("\n".join(text))
