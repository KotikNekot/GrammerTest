from io import BytesIO
from asyncio import sleep

from PIL import Image, ImageDraw, ImageFont

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def timer(message: Message, state: FSMContext, word: str, limit: int) -> None:
    await sleep(limit)

    fsm_data = await state.get_data()

    if not fsm_data:
        return

    if fsm_data.get("correct_word") == word:
        await state.clear()

        await message.reply(
            "Время кончилось!"
        )



def create_keyboard(accent_variations: list[str]):
    rows = [accent_variations[i:i + 3] for i in range(0, len(accent_variations), 3)]

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=word, callback_data=f"accent_{word}") for word in row]
            for row in rows
        ]
    )
    return inline_kb



def draw_text_image(word: str) -> bytes:
    image_width, image_height = 960, 300
    background_color = (181,44,64,255)
    text_color = (255, 255, 255)
    font_size = 70

    image = Image.new('RGB', (image_width, image_height), color=background_color)
    image_io = BytesIO()
    draw = ImageDraw.Draw(image)

    word = word.upper()
    font = ImageFont.truetype("G_ari_bd.TTF", font_size)

    text_bbox = draw.textbbox((0, 0), word, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((image_width - text_width) // 2, (image_height - text_height) // 2)

    draw.text(position, word, fill=text_color, font=font)


    image.save(image_io, "png")

    return image_io.getvalue()

