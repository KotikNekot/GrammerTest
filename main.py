import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database import create_user_table
from handlers import start_router, accents_router, leaders

dp = Dispatcher()


async def main() -> None:
    bot = Bot(
        token="7721275788:AAEls8IjX-tT1BLOQ9PJ1-nLg9AZUcn03iQ",
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp.include_router(start_router)
    dp.include_router(accents_router)
    dp.include_router(leaders)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(create_user_table())
    asyncio.run(main())