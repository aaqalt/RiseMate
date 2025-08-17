# utils/morning_update.py
import asyncio
from datetime import datetime, time
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.get_quote import get_quote
from utils.get_weather import get_weather
from utils.database import SessionLocal, User, Todo

scheduler = AsyncIOScheduler()
TIMEZONE = pytz.timezone("Asia/Tashkent")  

async def send_morning(bot, user):
    session = SessionLocal()
    try:
        todos = session.query(Todo).filter(Todo.user_id == user.chat_id).all()
        todo_text = "\n".join(f"{i+1}. {t.text}" for i, t in enumerate(todos)) or "No tasks today!"

        lat, lon = user.latitude, user.longitude
        loc_name = user.location or "Tashkent"

        weather_text, location_name = await get_weather(lat=lat, lon=lon, location_name=loc_name)
        quote = await get_quote()

        message = (
            f"Good morning, {user.fullname}! ☀️\n"
            f"Here’s your morning update for <b>{datetime.now(TIMEZONE).date()}:</b>\n\n"
            f"<b>🌤 Weather in {location_name}:</b> {weather_text}\n"
            f"<b>💪 Quote:</b> <i>{quote}</i>\n\n"
            f"<b>📝 Your To-Do List:</b>\n<i>{todo_text}</i>"
        )

        await bot.send_message(chat_id=user.chat_id, text=message, parse_mode="HTML")
    finally:
        session.close()

async def check_and_send(bot):
    session = SessionLocal()
    try:
        now = datetime.now(TIMEZONE)
        users = session.query(User).all()
        for user in users:
            pr_time = user.pr_time or time(19, 0) 
            if pr_time.hour == now.hour and pr_time.minute == now.minute:
                asyncio.create_task(send_morning(bot, user))
    finally:
        session.close()

def start_morning_scheduler(bot):
    scheduler.add_job(lambda: asyncio.create_task(check_and_send(bot)), "cron", second=0, timezone=TIMEZONE)
    scheduler.start()
