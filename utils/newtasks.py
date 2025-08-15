import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.database import SessionLocal, Todo, User
import pytz

scheduler = AsyncIOScheduler()
tz = pytz.timezone("Asia/Tashkent")
async def clear_and_ask_tasks(send_message):
    session = SessionLocal()
    try:

        Todo.delete_all(session)

        users = session.query(User).all()

        for user in users:
            try:
                await send_message(
                    chat_id=user.chat_id,
                    text="🌙 Hello! All of your previous tasks has been deleted.\n Do you have any plans for tomorrow? Use /addtodo to add them."
                )
            except Exception as e:
                print(f"Failed to send message to {user.chat_id}: {e}")
    finally:
        session.close()

def start_scheduler(send_message):
    trigger = CronTrigger(hour=21, minute=0, timezone=tz)
    scheduler.add_job(clear_and_ask_tasks, trigger, args=[send_message])
    scheduler.start()
