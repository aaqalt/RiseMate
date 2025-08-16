from aiogram import types, Router
from utils.database import SessionLocal, User
from utils.get_weather import get_weather

current_weather = Router()

@current_weather.message(commands=["current_weather"])
async def current_weather_handler(message: types.Message):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.chat_id == message.chat.id).first()

        location = user.location if user and user.location else "Tashkent"

        weather = await get_weather(location)
        if weather:
            await message.answer(f"🌤 Current weather in <b>{location}</b>: {weather}\nTo change the location send /setlocation", parse_mode="HTML")
        else:
            await message.answer(f"❌ Could not fetch weather for <b>{location}</b>. Try again later.", parse_mode="HTML")

    except Exception as e:
        await message.answer("⚠️ Something went wrong while fetching weather.")
        print(e)
    finally:
        session.close()
