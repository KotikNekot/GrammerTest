from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, \
    BufferedInputFile, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command

from database import add_correct
from utils import create_keyboard, timer
from words.words import get_word_variables_image

accents_router = Router()


class AccentsState(StatesGroup):
    awaiting_answer = State()
    stats = State()


@accents_router.message(Command("cancel"))
@accents_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()

    await message.answer("Cancelled.")


@accents_router.message(Command("accents", "ударения"))
async def accents(message: Message, state: FSMContext):
    word, variations, image = get_word_variables_image()

    await state.update_data(correct=0, mistakes=0, correct_word=word)

    await message.answer_photo(
        photo=BufferedInputFile(image, filename="image.png"),
        caption=f"Выберите правильное ударение к слову: \"{word.upper()}\"",
        reply_markup=create_keyboard(variations)
    )

    await state.set_state(AccentsState.awaiting_answer)
    await timer(message, state, word, 10)


@accents_router.callback_query(F.data.startswith('accent_'))
async def check_answer(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    if not user_data:
        await call.message.reply(
            "Данное сообщение уже не доступно! Пожалуйста, начните с начала написав /accents"
        )
        return

    word, variations, image = get_word_variables_image()
    correct_word = user_data.get("correct_word")
    selected_word = call.data.split('_')[1]

    if selected_word == correct_word:
        user_data["correct"] += 1
        await add_correct(call.from_user.id)
        caption = f"Правильно, ударение в прошлом слове падает на: {selected_word}\n\n"
    else:
        user_data["mistakes"] += 1
        caption = f"Вы допустили ошибку! Правильно: {correct_word}, вы выбрали: {selected_word}\n\n"


    await state.update_data(correct=user_data["correct"], mistakes=user_data["mistakes"], correct_word=word)

    await call.message.edit_media(
        media=InputMediaPhoto(media=BufferedInputFile(image, filename="image.png"))
    )
    await call.message.edit_caption(
        reply_markup=create_keyboard(variations),
        caption=caption + f"Выберите правильное ударение к слову: \"{word.upper()}\"\n\n"
                f"Правильно: {user_data['correct']}, Ошибок: {user_data['mistakes']}"
    )

    await timer(call.message, state, word, 10)
