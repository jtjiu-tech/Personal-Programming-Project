## Personal Programming Project John Tjiu
import time
from colorist import rgb
import random
from time import sleep
import os
import pygame

#useful functions
def betterprint(text):
    for character in text:
        print(character, end = "",flush = True,)
        sleep(0.02)

def setupMusic():
    pygame.mixer.init

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Colours
def gold(string):
    rgb(string, 255, 204, 0)
    return string

def red(string):
    rgb(string, 255, 0, 0)
    return string






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
        print(f"{self.name}, Here are your cards: ")
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



def player_turn(player):
    clear()
    betterprint(f"{player.name}, what would you like to do?\n")
    print("1) Draw a card")
    print("2) Play a card")
    print("3) Display your cards")
    choice = input("")
    while choice != "1" and choice != "2" and choice != "3":
        if choice == "1":
            return choice
        elif choice == "2":
            return choice
        elif choice == "3":
            return choice
        print("Not an option")
        print("1) Draw a card")
        print("2) Play a card")
        print("3) Display your cards")
        choice = input("")






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
    clear()
    betterprint("Which card would you like to use?\n")
    player.show_hand()
    playerinput = int(input())
    sleep(1)
    while playerinput > len(player.hand):
        playerinput = int(input("Invalid input, which card would you like to use?"))
        player.show_hand()
    card_selected = player.hand[playerinput-1]
    player.hand.pop(playerinput-1)
    return card_selected




def card_played(card_selected,player):
    if card_selected == DEFUSE:
        betterprint("You can't use a defuse, you didn't pull an exploding kitten...")
        sleep(1)
        clear()
        return use_card(player)
    elif card_selected in CATS:
        cat_combos()
    elif card_selected == ATTACK:
        attack()
    elif card_selected == NOPE:
        nope()
    elif card_selected == SKIP:
        skip()
        return "Skipped"
    elif card_selected == SHUFFLE:
        shuffle()
    elif card_selected == FAVOR:
        favor()
    elif card_selected == SEE:
        seethefuture()


def attack(player):
    while ATTACK not in player.hand:
        print(f"{player} played a card")


def nope():
    pass

def skip():

    pass

def shuffle():
    pass

def favor():
    pass

def seethefuture():
    pass

def cat_combos(player,players):
    pass
            


    


def check(player):
    if KITTEN in player.hand:
        betterprint("OH NOOOO!!!! YOU PULLED AN EXPLODING KITTENN!! 💣💣💣")
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
    current = 0
    intro()
    numplayer = int(input("How many players are there? (2-4) "))
    while numplayer <2 or numplayer >4:
        numplayer = int(input("It needs to be between 2-4 players, sorryyyy, re-enter your number of players plzz "))
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


    while sum(player.alive for player in players) > 1:
        player = players[current]
        if not player.alive:
            current = current + 1
        player = players[current]
        
        choice = player_turn(player)
        if choice == "1":
            draw_card(player,deck)
            check(player)
        elif choice == "2":
            card_selected = use_card(player)
            card_played(card_selected,player)
        elif choice == "3":
            player.show_hand()
            input("Done reading? press enter to continue")
            clear()
            player_turn(player)

        current = (current+1) % len(players)


            
    winner = (player for player in players)
    betterprint(f"{winner.name} is the winner!!!")
            
main()
        

    


