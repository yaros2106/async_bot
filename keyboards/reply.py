from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


statr_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Меню"),
        KeyboardButton(text="О кафе"),
        ],
        [
        KeyboardButton(text="Варианты доставки"),
        KeyboardButton(text="Варианты оплаты"),
        ],
        [
        KeyboardButton(text="Оставить отзыв")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Добавить товар"),
        KeyboardButton(text="Ассортимент"),
        ],
        [
        KeyboardButton(text="Добавить/Изменить баннер")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

del_kbd = ReplyKeyboardRemove()