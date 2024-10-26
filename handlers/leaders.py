from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_all_users, edit_show, get_user, edit_name

leaders = Router()

async def get_leaderboard():
    users = await get_all_users()

    leaderboard = [user for user in users if user['show_in_leaderboard']]

    leaderboard = sorted(leaderboard, key=lambda x: x['correct_words'], reverse=True)

    return "\n".join(
        [f"{i+1}. {user['id'] if not user['visible_name'] else user['visible_name']}, Правильных слов: {user['correct_words']}"
                      for i, user in enumerate(leaderboard)])


@leaders.message(Command("leaderboard"))
async def show_leaderboard(message: Message):
    leaderboard_text = await get_leaderboard()
    await message.answer(f"🏆 Список лидеров:\n{leaderboard_text}" if leaderboard_text else "Список лидеров пуст.")


@leaders.message(Command("toggle_leaderboard"))
async def toggle_leaderboard(message: Message):
    user_id = message.from_user.id

    user = await get_user(user_id)

    new_show_value = not user["show_in_leaderboard"]
    await edit_show(user_id, new_show_value)

    status = "теперь отображаетесь" if new_show_value else "теперь скрыты"
    await message.answer(f"Вы {status} в списке лидеров.")


@leaders.message(Command("setname"))
async def set_name(message: Message):
    new_name = message.text.split(maxsplit=1)

    if len(new_name) < 2:
        await message.answer(
            "Пожалуйста, укажите новое имя после команды. Пример: /setname НовоеИмя"
        )
        return

    new_name = new_name[1]
    user_id = message.from_user.id

    await edit_name(user_id, new_name)

    await message.answer(f"Ваш ник был изменён на: {new_name}")
