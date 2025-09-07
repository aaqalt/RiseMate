# test_morning.py
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
from os import getenv
from utils.database import session, User
from utils.morning import send_morning  

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)

    test_user = session.query(User).filter(User.chat_id == 6645021338).first() 
    if not test_user:
        print("Test user not found in database!")
        return

    await send_morning(bot, test_user)

    await bot.session.close()  

if __name__ == "__main__":
    asyncio.run(main())
