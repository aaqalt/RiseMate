# utils/morning_update.py
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.get_quote import get_quote
from utils.get_weather import get_weather
from utils.database import SessionLocal, User, Todo

scheduler = AsyncIOScheduler()


async def send_morning(bot, user):
    session = SessionLocal()
    try:
        todos = session.query(Todo).filter(Todo.user_id == user.chat_id).all()
        todo_text = "\n".join(f"{i+1}. {t.text}" for i, t in enumerate(todos)) or "No tasks today!"

        if user.location:
            weather = await get_weather(user.location)
        else:
            weather = "🌍 Location not set"

        quote = await get_quote()

        message = (
            f"Good morning, {user.fullname}! ☀️\n"
            f"Here’s your morning update for <b>{datetime.now().date()}:</b>\n\n"
            f"<b>🌤 Weather in {user.location or 'Unknown'}:</b> {weather}\n"
            f"<b>💪 Quote:</b> <i>{quote}</i>\n\n"
            f"<b>📝 Your To-Do List:</b>\n<i>{todo_text}</i>"
        )

        await bot.send_message(chat_id=user.chat_id, text=message, parse_mode="HTML")
    finally:
        session.close()


def start_morning_scheduler(bot):
    """Schedule the morning updates for all users."""
    loop = asyncio.get_event_loop()

    def schedule_user_job(user):
        scheduler.add_job(
            lambda u=user: asyncio.run_coroutine_threadsafe(send_morning(bot, u), loop),
            "cron",
            hour=user.pr_time.hour,
            minute=user.pr_time.minute,
        )

    session = SessionLocal()
    try:
        users = session.query(User).all() 
        for user in users:
            schedule_user_job(user)
        scheduler.start()
    finally:
        session.close()
