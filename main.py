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
    pygame.mixer.init()

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
        for i,item in enumerate(self.hand,1):
            print(f"{i}. {item}")

def select_target(current_player, players):
    available = [p for p in players if p.alive and p != current_player]
    # checks if the list is empty
    if not available:
        betterprint("No other players available!")
        return None
    betterprint("Choose a target player\n")
    for i,player in enumerate(available):
        print(f"{i+1} {player.name}")
    choice = input("Enter player name\n")
    
    while True:
        choice = int(choice)
        if 1 <= choice <= len(available):
            return available[choice - 1]
        else:
            choice = input(f"Enter a number between 1 and {len(available)}:  ")



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
    while True:
        betterprint(f"{player.name}, what would you like to do?\n")
        print("1) Draw a card")
        print("2) Play a card")
        print("3) Display your cards")
        choice = input("")
        if choice in ["1","2","3"]:
            return choice
        else:
            print("Not an option\n")






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
    betterprint("Which card would you like to use? (enter a number)\n")
    player.show_hand()
    while True:
        try:
            playerinput = int(input())
            if 0 < playerinput < len(player.hand):
                break
            betterprint(f"Enter a number between 1 and {len(player.hand)}")
        except ValueError:
            betterprint(f"Enter a number between 1 and {len(player.hand)}")
    card_selected = player.hand[playerinput - 1]
    player.hand.pop(playerinput - 1)
    return card_selected




def card_played(card_selected,player,players,deck):
    if card_selected == DEFUSE:
        betterprint("You can't use a defuse, you didn't pull an exploding kitten...")
        sleep(1)
        clear()
        return use_card(player)
    elif card_selected in CATS:
        return cat_combos(player,players)
    elif card_selected == ATTACK:
        return attack(player,players)
    elif card_selected == NOPE:
        return nope()
    elif card_selected == SKIP:
        return skip(player)
    elif card_selected == SHUFFLE:
        return shuffle(deck)
    elif card_selected == FAVOR:
        return favor(player,players)
    elif card_selected == SEE:
        return seethefuture(deck)


def attack(player,players):
    betterprint(f"{player.name} played ATTACK! Next player takes 2 turns\n")
    sleep(1)
    return "attack"
    #handle in main loop

def nope():
    betterprint("NOPE! The previous action is cancelled\n")
    return "nope"
    #handle in main loop

def skip(player):
    betterprint(f"{player.name} used SKIP! Their turn is skipped\n")
    sleep(1)
    return "skipped"
    #handle in main loop

def shuffle(deck):
    betterprint("Shuffling the deck...\n")
    random.shuffle(deck)
    sleep(1)
    betterprint("Deck shuffled")
    return "shuffled"
    #should work

def favor(current_player,players):
    target = select_target(current_player,players)
    if target is None:
        return "favor_failed"

    betterprint(f"{current_player.name} is asking for a card from {target.name}!")

    sleep(1)

    betterprint(f"{target.name}, here are your cards:")
    target.show_hand()
    card = input(f"{target.name}, which card would you give to {current_player.name}? (enter number): ")
    while True:
        try:
            card = int(card)
            if 1 < card < len(target.hand):
                break
            else:
                card = input(f"invalid choice!!! Choose a number between 1 and {len(target.hand)}")
        except ValueError:
            print(f"Invalid choice!!! Choose a number between 1 and {len(target.hand)}")

    cardindex = card -1
    stolencard = target.hand.pop(cardindex)
    current_player.hand.append(stolencard)
    betterprint(f"{current_player.name} has recieved {stolencard} from {target.name}!")
    return "favor_done"
    #should work


def seethefuture(deck):
    select = "Looking into the future..."
    for i in range(5):
        select += "."
        print(select, end = "\r")
        sleep(0.3)
    sleep(1)
    print(" ", len(select))
    top_cards = deck[:3]
    for i,card in enumerate(top_cards,1):
        print(f"{i}: {card}")
    sleep(2)
    input("Press enter to continue...")
    clear()
    return "Seen_the_future"
    #should work

def cat_combos(player,players):
    cat_cards_in_hand = [card for card in player.hand if card in CATS]
    
    if len(cat_cards_in_hand) <2:
        betterprint("You don't have enough cat cards to make a combo! You need at least 2 cat cards.")
        return "cat_failed"

    cats = []
    for cat in CATS:
        if cat_cards_in_hand.count(cat) >= 2:
            cats.append(cat)
    
    if not cats:
        betterprint("You don't have two of the same cat cards to make a combo!!!")
        betterprint("You have:\n")
        for cat in CATS:
            count = cat_cards_in_hand.count(cat)
            if count > 0:
                print(f"- {cat}: {count}")
        sleep(2)
        return "cat_failed"

    betterprint("You have these cats with 2 or more copies:\n")

    for i,cat in enumerate(cats,1):
        count = cat_cards_in_hand.count(cat)
        print(f"{i}: {cat} (x{count})")
    
    while True:
        pass
    


    


def check(player):
    if KITTEN in player.hand:
        betterprint("OH NOOOO!!!! YOU PULLED AN EXPLODING KITTENN!! 💣💣💣")
        sleep(1)
        if DEFUSE in player.hand:
            reply = input("You have a defuse!! Do you wanna use it? (yes or no) ")
            if reply.lower() == "yes":
                player.hand.pop(DEFUSE)
                player.hand.pop(KITTEN)
                betterprint("DEFUSE is used! You survived!")
                return True
            else:
                player.hand.pop(KITTEN)
                player.alive = False
                betterprint(f"{player.name} has exploded 💥 , They're out of the game!!")
                sleep(1)
                return False
        else:
            player.hand.pop(KITTEN)
            player.alive = False
            betterprint(f"{player.name} has exploded 💥 , They're out of the game!!")
            sleep(1)
            return False
    return True


def intro():
    clear()
    betterprint("-Welcome to EXPLODDDINGGG KITTTEEENNNSSSS 💣💣💣-\n")
    betterprint("Do you know how to play?? (yes or no) ")
    play = input("")
    if play.lower() == "yes":
        pass
    else:
        print("In this game, the goal is to be the last player standing.\n")
        print("Each player starts with 8 cards including a defuse. \n")
        print("""On your turn you can:
- Draw a card (risky!)
- Play a card with special effects:
• ATTACK: Next player takes 2 turns
• SKIP: End your turn without drawing
• FAVOR: Steal a card from another player
• SHUFFLE: Randomize the deck
• SEE THE FUTURE: Look at top 3 cards
• CAT CARDS: Combine to steal from others
• NOPE: Cancel the previous action

If you draw the EXPLODING KITTEN, you need a defuse to survive!
Good luck and have fun!!!""")
        sleep(5)
        input("Done reading? Press Enter to move on...")
        clear()


def main():
    current = 0
    intro()
    numplayer = int(input("How many players are there? (2-4) "))
    while numplayer <2 or numplayer >4:
        numplayer = int(input("It needs to be between 2-4 players, sorry, re-enter your number of players"))
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
        

    


