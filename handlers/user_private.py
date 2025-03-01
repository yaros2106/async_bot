from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('я виртуальный помощник')


@user_private_router.message(F.text.lower() == 'меню')
@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer('Вот наше меню:')


@user_private_router.message(F.text.lower() == 'о нас')
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('О нас:')


@user_private_router.message(F.text.lower().contains('оплат'))
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    await message.answer('Варианты оплаты:')

@user_private_router.message(F.text.lower().contains('доставк'))
@user_private_router.message(Command('delivery'))
async def delivery_cmd(message: types.Message):
    await message.answer('Варианты доставки:')
