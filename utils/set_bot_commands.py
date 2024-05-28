# utils/set_bot_commands.py

from aiogram import types
from aiogram.types import BotCommandScopeChat
from aiogram.utils.exceptions import ChatNotFound

from data.config import ADMINS


async def set_default_commands(dp):
    # Commands for all users
    general_commands = [
        types.BotCommand("start", "Botni ishga tushurish"),
        types.BotCommand("help", "Yordam"),
    ]

    # Admin-only commands
    admin_commands = [
        types.BotCommand("doc", "Xisobot"),
        types.BotCommand("booked", "Band qilingan xonalar"),
        types.BotCommand("id", "Xona band qilganlarni user idsi va ism-familiyasi"),
        types.BotCommand("delete", "Band qilingan xonalarni o'chirish"),
        types.BotCommand("del", "user idga tegishli band qilingan joyni o'chirish"),
    ]

    # Set commands for all users
    await dp.bot.set_my_commands(general_commands)

    # Set commands for admins
    for admin_id in ADMINS:
        try:
            await dp.bot.set_my_commands(general_commands + admin_commands, scope=BotCommandScopeChat(chat_id=admin_id))
        except ChatNotFound:
            print(f"Chat not found for admin_id: {admin_id}")

