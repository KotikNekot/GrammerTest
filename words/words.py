from json import load
from random import choice

from utils import draw_text_image

words = load(open("words/words.json", "r", encoding="utf-8"))
# words = load(open("words.json", "r", encoding="utf-8"))


def generate_accent_variations(word: str) -> list[str]:
    vowels = "аеёиоуыэюя"
    variations = []
    word = word.lower()

    for i, letter in enumerate(word):
        if letter.lower() in vowels:
            highlighted_word = (
                word[:i] + letter.upper() + word[i + 1:]
            )
            variations.append(highlighted_word)

    return variations



def get_word_variables_image() -> (str, list[str], bytes):
    random_word = choice(words)

    if isinstance(random_word, list):
        random_word = choice(random_word)

    io_image = draw_text_image(random_word)
    accent_variations = generate_accent_variations(random_word)

    return random_word, accent_variations, io_image
