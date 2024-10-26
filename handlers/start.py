from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from database import create_user

start_router= Router(name=__name__)

@start_router.message(CommandStart())
async def start(message: Message) -> None:
    await create_user(message.from_user.id)

    await message.answer(
        """
Привет, сука! Если ты, блять, решил в последнюю неделю начинать готовиться к ЕГЭ по русскому, то тебе точно сюда! 😅 Забудь про всю ту херню, которую тебе вбивали в голову на уроках. Мы разберём все ошибки, которые ты, долбаеб, мог сделать на экзамене, и выжмем из твоего мозга всё, что ещё можно!

Этот бот — твой последний шанс перед ебаным экзаменом! Готовься, блять, так, чтобы потом не плеваться от своих же оценок. Хватит жевать сопли, давай за дело! 💪
        """
    )
