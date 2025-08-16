from aiogram import types, Router
from aiogram.filters import Command
from utils.database import SessionLocal, User
from utils.get_weather import get_weather  # your current get_weather function

current_weather_router = Router()

@current_weather_router.message(Command('current_weather'))
async def current_weather_handler(message: types.Message):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.chat_id == message.chat.id).first()

        if user and user.latitude is not None and user.longitude is not None:
            lat, lon = user.latitude, user.longitude
        else:
            lat, lon = 41.2995, 69.2401

        weather_text, location_name = await get_weather(lat, lon)
        
        if weather_text:
            await message.answer(
                f"🌤 Current weather in <b>{location_name}</b>:\n{weather_text}\n"
                "To change the location send /setlocation",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                f"❌ Could not fetch weather for your location. Try again later.",
                parse_mode="HTML"
            )

    except Exception as e:
        await message.answer("⚠️ Something went wrong while fetching weather.")
        print(e)
    finally:
        session.close()
