## Personal Programming Project John Tjiu
import time
import random
from time import sleep
import os

#useful functions
def betterprint(text):
    for character in text:
        print(character, end = "", flush = True)
        sleep(0.02)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



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

#Way of defining players
class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.alive = True
    def show_hand(self):
        print(f"{self.name}, your hand ({self.hand})")

def playernames():
    players = []
    num = int(input("How many players are there? (2-4) "))
    for i in range(num):
        name = input(f"Player {i+1}, what do I call you? ")
        players.append(Player(name))
    print(players)
    return players
#kind of works?




def main():
    betterprint("-Welcome to EXPLODDDINGGG KITTTEEENNNSSSS 💣💣💣-\n")
    betterprint("Do you know how to play?? ")
    play = input("")
    if play == "yes":
        pass
    else:
        print("In this game, the goal is to be the last player standing. Every player has a total of 8 cards including a defuse at the beginning of the game. Once it is your turn, you have the ability to use one of your cards which have ability like: See the Future where you see the next 3 cards in the deck or you can directly draw a card from the pile. Unless you place a card that directly skips your turn, you have to draw a card from the deck. If you draw the exploding kitten, you will need to use a diffuse to survive, if you do not have one, then too bad… you're dead. Good luck and have fun!!!")
        sleep(5)
        wipe = input("Done reading? Press Enter to move on...")
        clear()

    playernames()

main()