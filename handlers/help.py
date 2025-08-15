from aiogram import Router,html
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command("help"))
async def command_help_handler(message: Message):
    await message.answer("""📖 RiseMate Command Guide

Here’s what I can do for you:

⏰ /settime HH:MM – <i>Set your daily briefing time</i>
📍 /setlocation – <i>Set your city for weather updates</i>
📝 /addtodo - – <i>Add a new task to your to-do list</i>
📋 /mytodos – <i>View your current tasks</i>

💡 <b>Tip: Set your time and location first so I can prepare your perfect morning update.</b>""")