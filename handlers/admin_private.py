from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import admin_kb


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())


@admin_router.message(Command('admin'))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=admin_kb)


@admin_router.message(F.text == "Посмотреть список товаров")
async def starring_at_product(message: types.Message):
    await message.answer("Вот список товаров")


@admin_router.message(F.text == "Изменить товар")
async def change_product(message: types.Message):
    await message.answer("Вот список товаров")


@admin_router.message(F.text == "Удалить товар")
async def delete_product(message: types.Message):
    await message.answer("Выберите товар(ы) для удаления")


# next for FSM


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введите название заново',
        'AddProduct:description': 'Введите описание заново',
        'AddProduct:price': 'Введите стоимость заново',
        'AddProduct:image': 'Этот стейт последний',
    }


@admin_router.message(StateFilter(None), F.text == 'Добавить товар')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer('Введите название товара', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command('отмена'))  # * - any user state
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')  # * - any user state
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer('Действия отменены', reply_markup=admin_kb)


@admin_router.message(StateFilter('*'), Command('назад'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет - введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step

    await message.answer('вы вернулись к прошлому шагу')


@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание товара')
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели недопустимые данные, введите название товара')



@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите стоимость товара')
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите описания товара")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer('Загрузите изображение товара')
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите стоимость товара")


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)  # [-1] - highest resolution
    data = await state.get_data()
    try:
        await message.answer('Товар добавлен', reply_markup=admin_kb)
        await orm_add_product(session, data)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Непредвиденная ошибка: \n{str(e)}\n", reply_markup=admin_kb)
        await state.clear()

@admin_router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, отправьте фото товара")
