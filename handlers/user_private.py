from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.formatting import Bold, as_marked_section
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from keyboards import reply, inline
from database.orm_query import orm_get_products


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))  # chat type for this router to work


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник',
                         reply_markup=inline.get_callback_btns(btns={
                             'Нажми меня': 'some_1'
                         }))


@user_private_router.message(F.data.startswith('some_'))
async def counter(callback: types.CallbackQuery):
    number = int(callback.data.split('_')[-1])

    await callback.message.edit_text(
        text=f"Нажатий - {number}",
        reply_markup=inline.get_callback_btns(btns={
            'Нажми на меня еще раз': f"some_{number+1}"
        }))

