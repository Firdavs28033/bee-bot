import os
import pandas as pd
from aiogram import types
from aiogram.types import ParseMode
from loader import dp, bot
from data.config import ADMINS
from .start import file_path



"""ADMIN COMMANDS"""
@dp.message_handler(commands='doc', state='*')
async def user(message: types.Message):
    await message.answer("Salom")
    for admin_id in ADMINS:
        await bot.send_document(admin_id, types.InputFile(file_path))
        await bot.send_message(961458353,  "Document yuborildi")


@dp.message_handler(commands='rec', state='*')
async def rec(message: types.Message):
    await message.answer("Rasm yuboring")



"""Hamma userlarga o'zimiz xohlagan xabarni yuborish"""
@dp.message_handler(commands='users', state='*')
async def send_to_all_users(message: types.Message):
    custom_message = message.get_args()
    if not custom_message:
        await message.reply("Usage: /users <message>")
        return

    if os.path.exists(file_path):
        existing_data_df = pd.read_excel(file_path)
        users = existing_data_df['user_id'].tolist()
        for user in users:
            try:
                await bot.send_message(user, text=custom_message)
                print(f"Message sent to {user}")
            except Exception as e:
                print(f"Failed to send message to {user}: {e}")
    else:
        await message.reply("User data file not found.")

"""Bitta userga xabar yuborish"""
@dp.message_handler(commands=['send'], state='*')
async def send_to_one_user(message: types.Message):
    command_args = message.get_args().split()
    if len(command_args) >= 2:
        user_id = int(command_args[0])
        custom_message = " ".join(command_args[1:])
        try:
            await bot.send_message(user_id, text=custom_message, parse_mode=ParseMode.HTML)
            await message.reply(f"Message sent to {user_id}")
        except Exception as e:
            await message.reply(f"Failed to send message to {user_id}: {e}")
    else:
        await message.reply("Usage: /send <user_id> <message>")

"""Admin uchun user ID va ism familiyalarni yuborish"""
@dp.message_handler(commands=['id'], state='*')
async def send_user_ids(message: types.Message):
    for ADMIN_ID in ADMINS:
        if str(message.from_user.id) != ADMIN_ID:
            await message.reply("You are not authorized to use this command.")
            return

        if os.path.exists(file_path):
            existing_data_df = pd.read_excel(file_path)
            user_data = existing_data_df[['user_id', 'Ism-familiyasi']].to_dict('records')
            user_info = "\n".join([f"ID: {user['user_id']}, Name: {user['Ism-familiyasi']}" for user in user_data])

            await bot.send_message(ADMIN_ID, text=f"User List:\n{user_info}")
        else:
            await message.reply("User data file not found.")