from random import choice
from string import ascii_letters, digits


def generate_customid():
    return "".join(choice(ascii_letters + digits) for _ in range(6))
