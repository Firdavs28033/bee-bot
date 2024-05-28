
import os
import pandas as pd
from datetime import datetime, timedelta
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import ADMINS


file_path = "data/hisobot.xlsx"

# Ensure the data directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Define FSM states
class Form(StatesGroup):
    region = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    category_choice = State()
    room_choice = State()
    seat_choice = State()
    booking_days = State()

# Define category keyboard
category_markup = InlineKeyboardMarkup(row_width=1)
category_markup.add(
    InlineKeyboardButton("3-26 xonalar Ayollar", callback_data="category_1_26"),
    InlineKeyboardButton("27-37 xonalar Erkaklar", callback_data="category_27_37"),
    InlineKeyboardButton("38-47 xonalar Oilaviy", callback_data="category_38_47")
)

# Define regions
regions = [
    "Andijon viloyati",
    "Buxoro viloyati",
    "Farg‘ona viloyati",
    "Jizzax viloyati",
    "Xorazm viloyati",
    "Namangan viloyati",
    "Navoiy viloyati",
    "Qashqadaryo viloyati",
    "Qoraqalpog‘iston Respublikasi",
    "Samarqand viloyati",
    "Sirdaryo viloyati",
    "Surxondaryo viloyati",
    "Toshkent viloyati",
    "Toshkent shahri"
]

# Create inline keyboard markup for regions
regions_markup = InlineKeyboardMarkup(row_width=1)
for region in regions:
    regions_markup.add(InlineKeyboardButton(region, callback_data=f"region_{region}"))

# Function to save data to Excel
def save_to_excel(new_data):
    new_data_df = pd.DataFrame(new_data)
    if os.path.exists(file_path):
        existing_data_df = pd.read_excel(file_path)
        updated_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
    else:
        updated_data_df = new_data_df
    updated_data_df.to_excel(file_path, index=False)


# Start command handler
@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message):
    await Form.region.set()
    await message.reply("Xush kelibsiz! Viloyat tanlang:", reply_markup=regions_markup)

# Region choice handler
@dp.callback_query_handler(lambda c: c.data.startswith('region_'), state=Form.region)
async def process_region_choice(callback_query: types.CallbackQuery, state: FSMContext):
    region = callback_query.data.split('_', 1)[1]
    async with state.proxy() as data:
        data['region'] = region
    await Form.next()
    await callback_query.message.reply("Iltimos, Ism kiriting:")

# First name handler
@dp.message_handler(state=Form.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await Form.next()
    await message.reply("Iltimos, familiya kiriting:")

# Last name handler
@dp.message_handler(state=Form.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await Form.next()
    await message.reply("Telefon nomerni kiriting")

# Phone number handler
# Phone number handler
@dp.message_handler(state=Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await Form.next()
    await message.reply("Iltimos kategoriya tanlang:", reply_markup=category_markup)


# Category choice handler
@dp.callback_query_handler(lambda c: c.data.startswith('category_'), state=Form.category_choice)
async def process_category_choice(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data.split('_')[1] + '_' + callback_query.data.split('_')[2]
    room_range = {
        '1_26': range(3, 27),
        '27_37': range(27, 38),
        '38_47': range(38, 48)
    }[category]

    async with state.proxy() as data:
        data['category_choice'] = category

    await Form.room_choice.set()
    await show_available_rooms(callback_query.message, room_range)

async def show_available_rooms(message: types.Message, room_range):
    markup = InlineKeyboardMarkup(row_width=5)
    for room in room_range:
        button_text = f" {room}-xona"
        markup.insert(InlineKeyboardButton(button_text, callback_data=f"room_{room}"))
    await message.reply("Xona tanlang?", reply_markup=markup)

# Room choice handler
@dp.callback_query_handler(lambda c: c.data.startswith('room_'), state=Form.room_choice)
async def process_room_choice(callback_query: types.CallbackQuery, state: FSMContext):
    room_choice = int(callback_query.data.split('_')[1])
    async with state.proxy() as data:
        data['room_choice'] = room_choice

        # Determine the valid seat range based on room number
        if 3 <= room_choice <= 16:
            max_seats = 3
        elif room_choice == 17:
            max_seats = 2
        elif room_choice == 18:
            max_seats = 3
        elif 19 <= room_choice <= 26:
            max_seats = 2
        elif room_choice == 27:
            max_seats = 4
        elif room_choice == 28:
            max_seats = 3
        elif 29 <= room_choice <= 30:
            max_seats = 6
        elif room_choice == 31:
            max_seats = 3
        elif 32 <= room_choice <= 33:
            max_seats = 5
        elif 34 <= room_choice <= 36:
            max_seats = 4
        elif room_choice == 37:
            max_seats = 3
        elif 38 <= room_choice <= 47:
            max_seats = 2
        else:
            await callback_query.message.answer("Yaroqli xona raqamini kiriting.")
            return

        data['max_seats'] = max_seats

    await Form.next()
    await callback_query.message.answer(f"Siz tanlagan xona: {room_choice}.", reply_markup=types.ReplyKeyboardRemove())
    await callback_query.message.answer(f"Iltimos, ushbu o'rinlardan birini tanlang (1-{max_seats}):")


# Seat choice handler
@dp.message_handler(state=Form.seat_choice)
async def process_seat_choice(message: types.Message, state: FSMContext):
    seat_choice = message.text
    if not seat_choice.isdigit():
        await message.reply("Yaroqli joy raqamini kiriting.")
        return

    seat_choice = int(seat_choice)
    async with state.proxy() as data:
        room_choice = data['room_choice']
        max_seats = data['max_seats']

        if not (1 <= seat_choice <= max_seats):
            await message.reply(f"Ushbu xonada {max_seats} ta joy bor. Yaroqli joy raqamini kiriting (1-{max_seats}).")
            return

        data['seat_choice'] = seat_choice

    # Check if the seat is already taken and provide the availability information
    if os.path.exists(file_path):
        existing_data_df = pd.read_excel(file_path)
        seat_taken = existing_data_df[
            (existing_data_df['Xona'] == data['room_choice']) & (existing_data_df['O\'rin'] == int(seat_choice))]

        if not seat_taken.empty:
            latest_booking_date = seat_taken['Band tugash sanasi'].max()
            await message.reply(f"Ushbu joy {latest_booking_date} sanagacha band qilingan. Iltimos boshqa o'rin tanlang.")
            return

    await Form.next()
    await message.reply("Ushbu o'rinni necha kungacha band qilmoqchisiz?")

# Booking days handler
@dp.message_handler(state=Form.booking_days)
async def process_booking_days(message: types.Message, state: FSMContext):
    booking_days = message.text
    if not booking_days.isdigit() or int(booking_days) <= 0:
        await message.reply("Iltimos yaroqli son kiriting(Masalan: 1).")
        return

    async with state.proxy() as data:
        data['booking_days'] = booking_days
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=int(booking_days))
        data['booking_end_date'] = end_date

    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else 'N/A'
    city = data['region']
    name = data['first_name'] + ' ' + data['last_name']
    phone = data['phone_number']
    room = data['room_choice']
    seat = data['seat_choice']

    new_data = {
        'user_id': [user_id],
        'username': [username],
        'Yashash joyi': [city],
        'Ism-familiyasi': [name],
        'Tel. nomeri': [phone],
        'Xona': [room],
        'O\'rin': [seat],
        'Band qilgan muddati (kun)': [booking_days],
        'Band boshlanish sanasi': [start_date],
        'Band tugash sanasi': [end_date]
    }

    save_to_excel(new_data)

    user_info = (f"Yashash joyi: {data['region']}\n"
                 f"Ismi: {data['first_name']}\n"
                 f"Familiyasi: {data['last_name']}\n"
                 f"Telefon nomeri: {data['phone_number']}\n"
                 f"Tanlagan xonasi: {data['room_choice']}\n"
                 f"Tanlagan o'rni: {data['seat_choice']}\n"
                 f"Necha kunga band qilgani: {booking_days} kun. ({data['booking_end_date']} gacha band qilindi)")

    await message.reply(user_info)
    await message.reply(f"Ma'lumotingiz uchun rahmat. Admin tez orada siz bilan bog'lanadi, {message.from_user.first_name}")

    for admin in ADMINS:
        await bot.send_message(admin, f"Yangi foydalanuvchi qo'shildi:\n{user_info}")


    state_data = await state.get_data()
    if state_data:
        await state.finish()