## Personal Programming Project John Tjiu
import time
import random
from time import sleep


def betterprint(text):
    for character in text:
        print(character, end = "", flush = True)
        sleep(0.02)


#card definitions
DEFUSE = "🛡️•⩊•"
NOPE = "🚫"
ATTACK = "⚔️"
SHUFFLE = "🔀"
SKIP = "🏃"
FAVOR = "🖤"
SEE = "👀"
KITTEN = "💣"

CATS = ["🍉🐱", "🥔🐱", "🌈🐱"]


