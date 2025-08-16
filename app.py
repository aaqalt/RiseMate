import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv  # type: ignore

from handlers import *
from utils.database import init_db
from utils.morning import start_morning_scheduler
from utils.newtasks import start_scheduler

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router,help_router,settime_router,set_location_router,addtodo_router,mytodos_router,current_weather_router,default_router)
    start_scheduler(bot.send_message)
    start_morning_scheduler(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    init_db()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())