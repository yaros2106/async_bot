from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def phone_request_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить номер", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


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