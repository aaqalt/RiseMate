from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.database import Todo,session

addtodo_router = Router()

class AddTodoStates(StatesGroup):
    waiting_for_task = State()

@addtodo_router.message(F.text == "/addtodo")
async def cmd_addtodo(message: Message, state: FSMContext):
    await message.answer("Please enter your task:")
    await state.set_state(AddTodoStates.waiting_for_task)

@addtodo_router.message(AddTodoStates.waiting_for_task)
async def process_task(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    task_text = message.text.strip()

    new_todo = Todo(user_id=chat_id, text=task_text)
    session.add(new_todo)
    session.commit()

    await message.answer(f"✅ Task added: {task_text}")
    await state.clear()
