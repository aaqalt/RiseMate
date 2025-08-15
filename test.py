# test_morning.py
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
from os import getenv
from utils.database import session, User
from utils.morning import send_morning  # your async function

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)

    # Fetch your test user from DB
    test_user = session.query(User).filter(User.chat_id == 6645021338).first()  # replace with your chat_id
    if not test_user:
        print("Test user not found in database!")
        return

    # Send the morning update immediately
    await send_morning(bot, test_user)

    await bot.session.close()  # close the Bot session

if __name__ == "__main__":
    asyncio.run(main())
