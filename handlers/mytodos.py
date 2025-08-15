from aiogram import Router, types
from aiogram.filters import Command
from utils.database import Todo,session

mytodos_router = Router()

@mytodos_router.message(Command("mytodos"))
async def my_todos_handler(message: types.Message):
    user_id = message.from_user.id
    todos = session.query(Todo).filter(Todo.user_id == user_id).all()

    if not todos:
        await message.answer("📭 You don't have any tasks for now")
        return

    text = "📝 Your tasks:\n"
    for i, todo in enumerate(todos, 1):
        text += f"{i}. {todo.text}\n"

    await message.answer(text)
