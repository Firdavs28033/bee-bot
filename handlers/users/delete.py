import os
import pandas as pd
from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp

# Admin user IDs
ADMINS = [961458353, 5499407154]

# Path to the Excel file
file_path = "data/hisobot.xlsx"


# Function to check if a user is an admin
async def is_admin(user_id):
    return user_id in ADMINS


# Handler for the '/delete' command to delete all bookings
@dp.message_handler(Command('delete'))
async def delete_all_bookings(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply("Sizda bu komanda uchun ruxsat yo'q.")
        return

    if os.path.exists(file_path):
        os.remove(file_path)
        await message.reply("Barcha band qilingan joylar o'chirildi.")
    else:
        await message.reply("Hech qanday band qilingan joylar topilmadi.")


# Handler for the '/del' command to delete a booking by user ID
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
    await message.reply(f"User ID {user_id_to_delete} ga tegishli band qilingan joy o'chirildi.")
