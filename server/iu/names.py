import random
from iu.wordlist import WORDS


def get_star_name():
    word_count = random.randint(2, 3)

    words = []
    for i in range(word_count):
        word = random.choice(WORDS)
        words.append(word.capitalize())

    return " ".join(words)
