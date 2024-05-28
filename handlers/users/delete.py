import os
import pandas as pd
from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from loader import dp


file_path = "data/hisobot.xlsx"

async def is_admin(user_id):
    return user_id in ADMINS

@dp.message_handler(Command('delete'))
async def delete_all_bookings(message: types.Message):
    if not await is_admin(message.from_user.id):
        await message.reply("Sizda bu komanda uchun ruxsat yo'q.")
        return

    if os.path.exists(file_path):
        os.remove(file_path)
        await message.reply("Barcha band qilingan joylar o'chirildi.")
    else:
        await message.reply("Hech qanday band qilingan joylar topilmadi.")

@dp.message_handler(Command('del'))
async def delete_booking_by_id(message: types.Message):
    if not await is_admin(message.from_user.id):
        await message.reply("Sizda bu komanda uchun ruxsat yo'q.")
        return

    try:
        user_id_to_delete = int(message.get_args())
    except ValueError:
        await message.reply("Iltimos, to'g'ri user ID ni kiriting.")
        return

    if not os.path.exists(file_path):
        await message.reply("Hech qanday band qilingan joylar topilmadi.")
        return

    existing_data_df = pd.read_excel(file_path)
    if user_id_to_delete not in existing_data_df['User ID'].values:
        await message.reply("Berilgan user ID topilmadi.")
        return

    updated_data_df = existing_data_df[existing_data_df['User ID'] != user_id_to_delete]
    updated_data_df.to_excel(file_path, index=False)
    await message.reply(f"User ID {user_id_to_delete} ga tegishli band qilinga joy o'chirildi.")