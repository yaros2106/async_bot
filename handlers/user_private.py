from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content

from keyboards.inline import MenuCallBack
from keyboards.reply import phone_request_keyboard
from database.orm_query import orm_add_to_cart, orm_add_user


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))  # chat type for this router to work


@user_private_router.callback_query(F.data == "order_delivery")
async def process_order_callback(callback: types.CallbackQuery):
    delivery_options = "\n".join([
        "🚀 Курьером (до 30 минут)",
        "🏠 Самовывоз из кофейни",
        "📍 Доставка через сервисы (Яндекс, Delivery Club)"
    ])

    text = f"<b>Варианты доставки:</b>\n{delivery_options}\n\nВыберите способ:"

    await callback.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="🚀 Курьером")],
                [types.KeyboardButton(text="🏠 Самовывоз")],
                [types.KeyboardButton(text="📍 Доставка через сервисы")]
            ],
            resize_keyboard=True
        )
    )
    await callback.answer()  # Закрываем анимацию "Загрузка..."


@user_private_router.message(lambda msg: msg.text in ["🚀 Курьером", "🏠 Самовывоз", "📍 Доставка через сервисы"])
async def ask_phone(message: types.Message):
    await message.answer(
        "Для оформления заказа отправьте ваш номер телефона:",
        reply_markup=phone_request_keyboard()
    )

@user_private_router.message(lambda msg: msg.contact)
async def process_phone(message: types.Message):
    await message.answer(
        "Спасибо! Ваш заказ принят. Оператор свяжется с вами для уточнения деталей.",
        reply_markup=types.ReplyKeyboardRemove()
    )


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name='main')
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Товар добавлен в корзину.")


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):

    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()




