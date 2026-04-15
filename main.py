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



# Definitions
players = []

#Capitalised all cat cards + definitions of cards
DEFUSE = "🛡️•⩊•(defuse)"
NOPE = "🚫(nope)"
ATTACK = "⚔️(attack)"
SHUFFLE = "🔀(shuffle)"
SKIP = "🏃(skip)"
FAVOR = "🖤(favor)"
SEE = "👀(See the future)"
KITTEN = "💣"

CATS = ["🍉🐱", "🥔🐱", "🌈🐱"]

#Way of defining players
class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.alive = True
    def show_hand(self):
        i = 0
        print(f"{self.name}, here are your cards: ")
        for item in self.hand:
            i +=1
            print(f"{i}. {item}")

def create_deck():
    deck =([ATTACK] * 4 + [NOPE]*5 + [SHUFFLE]*4 + [SEE] * 5 + [FAVOR] * 4 + [SKIP] * 4 + CATS * 4)
    random.shuffle(deck)
    return deck

def show_cards():
    for player in players:
        player.show_hand()
        print("")
        input("Press enter when done... ")
        clear()

def playerslookaway():
    print("Other players look away now!!")
    for i in range(5):
        print(i)
    clear()

def deal_card(players,deck):
    for player in players:
        player.hand.append(DEFUSE)
        while len(player.hand) < 8:
            card = deck.pop()
            player.hand.append(card)
        

def getting_card():
    print("Wait")
    select = "Getting card..."
    for i in range(5):
        select += "."
        print(select, end = "\r")
        sleep(0.3)
    sleep(1)
    print(" ", len(select))
    clear()



def player_turn(player,deck):
    betterprint(f"{player.name}, what would you like to do?\n")
    print("1) Draw a card")
    print("2) Play a card")
    choice = input("")
    if choice == "1":
        draw_card(player,deck)
        check()
    elif choice == "2":
        use_card(player)
    else:
        pass

def draw_card(player,deck):
    card = deck.pop(0)
    player.hand.append(card)
    getting_card()
    betterprint(f"You drew a {card}!!!\n")
    sleep(2)
    player.show_hand()
    input("Done reading? Press Enter to move on...")
    clear()

def use_card(player):
    playerinput = int(input("Which card would you like to use?"))
    sleep(1)
    player.show_hand()
    player.hand.pop[playerinput-1]
    player.show_hand()


def check(player):
    if KITTEN in player.hand:
        print("OH NOOOO!!!! YOU PULLED AN EXPLODING KITTENN!! 💣💣💣")
        if DEFUSE in player.hand:
            reply = input("You have a defuse!! Do you wanna use it? (yes or no) ")
            if reply == "yes":
                player.hand.pop(DEFUSE)
                #how would i make it so that players see the announcement where this player used defuse and pulled an exploding kitten?
                #player given choice to place exploding kitten somewhere
                #deal with later
    pass


def intro():
    clear()
    betterprint("-Welcome to EXPLODDDINGGG KITTTEEENNNSSSS 💣💣💣-\n")
    betterprint("Do you know how to play?? (yes or no) ")
    play = input("")
    if play == "yes":
        pass
    else:
        print("In this game, the goal is to be the last player standing. Every player has a total of 8 cards including a defuse at the beginning of the game. Once it is your turn, you have the ability to use one of your cards which have ability like: See the Future where you see the next 3 cards in the deck or you can directly draw a card from the pile. Unless you place a card that directly skips your turn, you have to draw a card from the deck. If you draw the exploding kitten, you will need to use a diffuse to survive, if you do not have one, then too bad… you're dead. Good luck and have fun!!!")
        sleep(5)
        input("Done reading? Press Enter to move on...")
        clear()


def main():
    intro()
    
    numplayer = int(input("How many players are there? (2-4) "))
    while numplayer <2 or numplayer >4:
        numplayer = int(input("How many players are there? (2-4) "))
    for i in range(numplayer):
        name = input(f"Player {i+1}, what do I call you? ")
        players.append(Player(name))
    clear()
    
    deck = create_deck()
    deal_card(players,deck)
    show_cards()

    #add exploding kittens to deck after players recieved cards 
    for i in range(numplayer-1):
        deck.append(KITTEN)
    random.shuffle(deck)
    while True:
        for player in players:
            player_turn(player,deck)
        

    

main()
