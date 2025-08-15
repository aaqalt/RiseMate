from aiogram import types
from aiogram import Router

default_router = Router()

@default_router.message()
async def delete_unhandled_messages(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message {message.message_id}: {e}")
