from aiogram.utils.formatting import Bold, as_list, as_marked_section


categories = ['Еда', 'Кофе']

description_for_info_pages = {
    "main": "Добро пожаловать!",
    "about": "Кофейня Такая-то.\nРежим работы - круглосуточно.",
    "payment": as_marked_section(
        Bold('Варианты оплаты:'),
        '💳 Онлайн',
        '💰 Наличные при получении',
        '🏠 В заведении',
        marker='• '
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold('Варианты доставки:'),
            '🚀 Курьером (до 30 минут)',
            '🏠 Самовывоз из кофейни',
            '📍 Доставка через сервисы (Яндекс, Delivery Club)',
            marker='• '
        ),
    ).as_html(),
    'catalog': 'Категории:',
    'cart': 'В корзине ничего нет!'
}