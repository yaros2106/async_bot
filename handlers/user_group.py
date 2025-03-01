from string import punctuation
from aiogram import types, Router

from filters.chat_types import ChatTypeFilter


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))  # chat type for this router to work


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