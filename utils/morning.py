# utils/morning_update.py
import asyncio
from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.get_quote import get_quote
from utils.get_weather import get_weather
from utils.database import SessionLocal, User, Todo

TIMEZONE = pytz.timezone("Asia/Tashkent")
scheduler = AsyncIOScheduler(timezone=TIMEZONE)


async def send_morning(bot, user):
    session = SessionLocal()
    try:
        todos = session.query(Todo).filter(Todo.user_id == user.chat_id).all()
        todo_text = "\n".join(f"{i+1}. {t.text}" for i, t in enumerate(todos)) or "No tasks today!"

        lat, lon = user.latitude, user.longitude
        loc_name = user.location or "Tashkent"

        # get_weather returns (weather_text, location_name)
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
        print(f"✅ Morning message sent to {user.chat_id}")
    except Exception as e:
        print(f"❌ Failed to send morning message to {user.chat_id}: {e}")
    finally:
        session.close()


def schedule_user_jobs(bot):
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            if not user.pr_time:
                continue

            scheduler.add_job(
                lambda u=user: asyncio.create_task(send_morning(bot, u)),
                trigger="cron",
                hour=user.pr_time.hour,
                minute=user.pr_time.minute,
                id=f"morning_{user.chat_id}",
                replace_existing=True,
            )
            print(f"⏰ Scheduled job for user {user.chat_id} at {user.pr_time}")
    finally:
        session.close()


def start_morning_scheduler(bot):
    schedule_user_jobs(bot)
    if not scheduler.running:
        scheduler.start()
        print("🚀 Morning scheduler started!")
