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
DEFUSE = "🛡️ •⩊•(defuse)"
NOPE = "🚫 (nope)"
ATTACK = "⚔️ (attack)"
SHUFFLE = "🔀 (shuffle)"
SKIP = "🏃 (skip)"
FAVOR = "🖤 (favor)"
SEE = "👀 (See the future)"
KITTEN = "💣"

CATS = ["🍉🐱", "🥔🐱", "🌈🐱"]


class Player:
    def __init__(self, name):
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


def deal_card(players, deck):
    for player in players:
        player.hand.append(DEFUSE)
        while len(player.hand) < 8:
            card = deck.pop()
            player.hand.append(card)


def options(player, deck):
    allow_skip = False
    not_end_turn = True

    while not_end_turn:

        for i, card in enumerate(player.hand):
            print(f"{i + 1}. {card}")

        print()

        print("What would you like to do?")
        print("1. Draw a card")
        print("2. Play a card")
        print("3. End turn")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            allow_skip = True
            draw_card(player, deck)

        elif choice == "2":
            allow_skip = True
            not_end_turn = play_card(player, deck)

        elif choice == "3":
            if allow_skip:
                print("You chose to end your turn\n")
                not_end_turn = False
            else:
                print("You cannot end your turn without drawing or playing a card.\n")
                options(player, deck)


def draw_card(player, deck):
    card = deck.pop()
    player.hand.append(card)
    print(f"You drew a {card} card!")
    if card == KITTEN:
        if DEFUSE in player.hand:
            print("You drew an exploding kitten but the defuse card saved you! The exploding kittens card is put back into the deck")
            player.hand.remove(DEFUSE)
            deck.insert(random.randint(0, len(deck)), KITTEN)
        else:
            print("You drew an exploding kitten and you have no defuse cards! You lose!")
            player.alive = False
    print()


def play_card(player, deck):
    print("Which card would you like to play?")

    choice = int(input("Enter the number of the card you want to play: ")) - 1
    card = player.hand.pop(choice)

    print(f"You played a {card} card!")

    if card == SEE:
        see_the_future(deck)
        return True
    
    elif card == SHUFFLE:
        random.shuffle(deck)
        print("The deck has been shuffled!")
        return True
    
    elif card == FAVOR:
        favor(player, players)
        return True
    
    elif card == SKIP:
        print("You skipped your turn!")
        return False
    
    elif card == ATTACK:
        attack(player, players, deck)
        return True
    
    elif card == DEFUSE:
        print("You cannot play a defuse card!")
        player.hand.append(DEFUSE)
        return True
    
    elif card == NOPE:
        print("You cannot play a nope card!")
        player.hand.append(NOPE)
        return True

def attack(player, players, deck):
    print(f"{player.name} played an attack card!")
    next_player = players[(players.index(player) + 1) % len(players)]
    print(f"{next_player.name}, you must draw two cards")
    if NOPE in next_player.hand:
        skip = input(f"{next_player.name}, you have a nope card! Do you want to play it? (y/n): ")
        if skip.lower() == "y":
            print("The attack was cancelled")
        else:
            draw_card(next_player, deck)
            draw_card(next_player, deck)

def see_the_future(deck):
    print("You see the future! Here are the next three cards in the deck:")
    for i in range(3):
        print(deck[-(i + 1)])
    print()


def favor(player, players):
    print("You played a favor card! Choose a player to ask for a card.")
    choice = int(input("Enter the number of the player you want to ask: ")) - 1
    chosen_player = players[choice]

    for i, card in enumerate(chosen_player.hand):
        print(f"{i + 1}. {card}")

    if NOPE in chosen_player.hand:
        skip = input(f"{chosen_player.name}, you have a nope card! Do you want to play it? (y/n): ")
        if skip.lower() == "y":
            print("The favor was cancelled")

    else:
        choice = int(input("Enter the number of the card you want to play: ")) - 1
        card = chosen_player.hand.pop(choice)
        player.hand.append(card)
        print(f"You received a {card} card from {chosen_player.name}!")


# def attack(player, players):
#     print(f"{player.name} played an attack card!")
#     next_player = players[(players.index(player) + 1) % len(players)]
#     print(f"{next_player.name}, you must take two turns in a row!")


def intro():
    print("Welcome to Exploding Kittens!")
    num_players = int(input("How many players are there? "))
    for i in range(num_players):
        name = input(f"Player {i+1}, please enter your name: ")
        players.append(Player(name))
    
    # for player in players:
    #     print(player.name, player.hand, player.alive)
    
    print("Great! Let's start the game!")
    return players


def main():
    turn = 0

    players = intro()
    deck = create_deck()
    deal_card(players, deck)

    while len(players) >= 1:  
        turn += 1
        if turn > len(players):
            turn = 1

        for player in players:
            if not player.alive:
                continue

        player = players[turn - 1]

        print(f"\n{player.name}'s turn!")
        # player.show_hand()

        options(player, deck)

    for player in players:
        if player.alive:
            print(f"{player.name} wins!")
            break

main()