from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.database import User,session

set_location_router = Router()

class LocationState(StatesGroup):
    waiting_for_location = State()

@set_location_router.message(F.text.lower() == "/setlocation")
async def set_location_command(message: Message, state: FSMContext):
    await message.answer("Please enter your city name:")
    await state.set_state(LocationState.waiting_for_location)

@set_location_router.message(LocationState.waiting_for_location)
async def process_location(message: Message, state: FSMContext):
    location = message.text.strip()
    chat_id = message.from_user.id
    User.update(session,chat_id,location=location)
    
    await message.answer(f"✅ Your location has been set to: {location}")
    await state.clear()
