from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from utils.database import User,session

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message):
    fullname = message.from_user.full_name
    await message.answer(("""🌅Hello , {name}!
I’m RiseMate — your personal daily companion 🤝✨

☀️ Every day, I’ll bring you:

- 🌤 <i>Today’s weather for your city</i>
- 💪 <i>Motivational quotes to start your day right</i>
- 📝 <i>Your personal to-do list</i>

📅 You can set the time, add tasks, and customize everything just for you.

<b>Let’s rise and shine together!</b> 🌟
Type /settime to choose your daily update time, or /help to see all my commands.""").format(name=fullname))
    user = User(chat_id=message.from_user.id,fullname=fullname)
    user.save(session)