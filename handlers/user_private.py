from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.formatting import Bold, as_marked_section
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from keyboards import reply
from database.orm_query import orm_get_products


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))  # chat type for this router to work


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('я виртуальный помощник', reply_markup=reply.statr_kb)


@user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}'
        )
    await message.answer('Вот наше меню:', reply_markup=reply.del_kbd)


@user_private_router.message(F.text.lower() == 'о кафе')
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('О нас:', reply_markup=reply.del_kbd)


@user_private_router.message(F.text.lower().contains('оплат'))
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Варианты оплаты:'),
        '💳 Онлайн',
        '💰 Наличные при получении',
        '🏠 В заведении',
        marker='• '
    )
    await message.answer(text.as_html(), reply_markup=reply.del_kbd)


@user_private_router.message(F.text.lower().contains('доставк'))
@user_private_router.message(Command('delivery'))
async def delivery_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Варианты доставки:'),
        '🚀 Курьером (до 30 минут)',
        '🏠 Самовывоз из кофейни',
        '📍 Доставка через сервисы (Яндекс, Delivery Club)',
        marker='• '
    )
    await message.answer(text.as_html(), reply_markup=reply.del_kbd)