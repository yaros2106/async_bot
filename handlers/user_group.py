from string import punctuation
from aiogram import types, Router, Bot
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))
user_group_router.edited_message.filter(ChatTypeFilter(['group', 'supergroup']))# chat type for this router to work


@user_group_router.message(Command('admin'))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id=chat_id)

    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == 'creator' or member.status == 'administrator'
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    print(admins_list)


def load_restricted_words(filename='restricted_words.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        print(f"Файл {filename} не найден, создайте его!")
        return set()


def clean_text(text: str):  # word deletion bypass
    return text.translate(str.maketrans('', '', punctuation))


restricted_words = load_restricted_words()


@user_group_router.edited_message()
@user_group_router.message()
async def check_restricted_words(message: types.Message):
    text = clean_text(message.text.lower())
    if any(phrase in text for phrase in restricted_words):
        await message.answer(f"{message.from_user.first_name}, соблюдайте порядок в чате!")
        await message.delete()