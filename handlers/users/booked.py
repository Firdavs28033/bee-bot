
import os
import pandas as pd
from aiogram import types
from aiogram.types import ParseMode
from loader import dp

file_path = "data/hisobot.xlsx"

ADMINS = [961458353, 5499407154]

# Handler for the '/booked' command to list booked rooms
@dp.message_handler(commands=['booked'])
async def cmd_booked(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply("Sizda bu komanda uchun ruxsat yo'q.")
        return

    # Check if the file exists
    if not os.path.exists(file_path):
        await message.reply("Xonalar band qilinmagan.")
        return

    # Read the Excel file
    existing_data_df = pd.read_excel(file_path)

    # Check if the data frame is empty
    if existing_data_df.empty:
        await message.reply("Xonalar band qilinmagan.")
        return

    # Group the data by room and format the output
    booked_rooms = existing_data_df.groupby('Xona').apply(
        lambda x: x[['O\'rin', 'Band tugash sanasi']].to_string(index=False)
    )

    # Create the response message
    response = "Band qilingan xonalar:\n\n"
    for room, details in booked_rooms.items():
        response += f"{room}-xona:\n{details}\n\n"

    # Send the response message
    await message.reply(response, parse_mode=ParseMode.MARKDOWN)