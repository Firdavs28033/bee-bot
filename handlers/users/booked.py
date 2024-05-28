
import os
import pandas as pd
from aiogram import types
from aiogram.types import ParseMode
from loader import dp

file_path = "data/hisobot.xlsx"


@dp.message_handler(commands=['booked'])
async def cmd_booked(message: types.Message):
    if not os.path.exists(file_path):
        await message.reply("Xonalar band qilinmagan.")
        return

    existing_data_df = pd.read_excel(file_path)
    if existing_data_df.empty:
        await message.reply("Xonalar band qilinmagan.")
        return

    booked_rooms = existing_data_df.groupby('Xona').apply(
        lambda x: x[['O\'rin', 'Band tugash sanasi']].to_string(index=False)
    )

    response = "Band qilingan xonalar:\n\n"
    for room, details in booked_rooms.items():
        response += f"{room}-xona:\n{details}\n\n"

    await message.reply(response, parse_mode=ParseMode.MARKDOWN)
