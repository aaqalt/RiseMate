from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.database import User, session

set_location_router = Router()

class LocationState(StatesGroup):
    waiting_for_location = State()

@set_location_router.message(F.text.lower() == "/setlocation")
async def set_location_command(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Share Location", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("📍 Please send your city name or share your location:", reply_markup=kb)
    await state.set_state(LocationState.waiting_for_location)

@set_location_router.message(LocationState.waiting_for_location, F.text)
async def process_location_text(message: Message, state: FSMContext):
    location = message.text.strip()
    chat_id = message.from_user.id
    User.update(session, chat_id, location=location, latitude=None, longitude=None)

    await message.answer(f"✅ Your location has been set to: {location}", reply_markup=ReplyKeyboardRemove())
    await state.clear()

@set_location_router.message(LocationState.waiting_for_location, F.location)
async def process_location_geo(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    chat_id = message.from_user.id
    User.update(session, chat_id, latitude=lat, longitude=lon)

    await message.answer(f"✅ Your location has been set to: {lat}, {lon}", reply_markup=ReplyKeyboardRemove())
    await state.clear()
