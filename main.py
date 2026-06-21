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
        self.extra_turns = 0
        self.has_played_attack = False
        self.has_played_skip = False

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
    choice = input("Enter player number\n")
    
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
    for i in range(5,0,-1):
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
    for i in range(3):
        sleep(0.5)
        print(".", end="", flush=True)
    print()
    sleep(0.5)
    clear()



def player_turn(player):
    clear()
    while True:
        betterprint(f"{player.name}, what would you like to do?\n")
        print("1) Play a card")
        print("2) End your turn and draw a card")
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
    return check(player)


def use_card(player):
    clear()
    betterprint("Which card would you like to use? (enter a number)\n")
    player.show_hand()
    while True:
        try:
            playerinput = int(input())
            if 1 <= playerinput <= len(player.hand):
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
        return None
    elif card_selected in CATS:
        return cat_combos(player,players)
    elif card_selected == ATTACK:
        player.has_played_attack = True
        return attack(player,players)
    elif card_selected == NOPE:
        return nope()
    elif card_selected == SKIP:
        player.has_played_skip = True
        return skip(player)
    elif card_selected == SHUFFLE:
        return shuffle(deck)
    elif card_selected == FAVOR:
        return favor(player,players)
    elif card_selected == SEE:
        return seethefuture(deck)
    return None


def attack(player,players):
    betterprint(f"{player.name} played ATTACK! Next player takes 2 turns\n")
    sleep(1)
    current_index = players.index(player)
    #loops through every player starting with the next player
    for i in range(1,len(players)):
        #calculates index of next player (wraps around)
        next_player = players[(current_index + i) % len(players)]
        if next_player.alive:
            next_player.extra_turns += 2
            break

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
    clear()
    betterprint(f"{target.name}, here are your cards:")
    target.show_hand()
    card = input(f"{target.name}, which card would you give to {current_player.name}? (enter number): ")
    while True:
        try:
            card = int(card)
            if 1 <= card <= len(target.hand):
                break
            else:
                card = input(f"invalid choice!!! Choose a number between 1 and {len(target.hand)}")
        except ValueError:
            print(f"Invalid choice!!! Choose a number between 1 and {len(target.hand)}")

    cardindex = card -1
    stolencard = target.hand.pop(cardindex)
    current_player.hand.append(stolencard)
    clear()
    betterprint(f"{current_player.name} has recieved {stolencard} from {target.name}!")
    sleep(3)
    return "favor_done"
    #should work


def seethefuture(deck):
    betterprint("You see the future! Here are the next three cards in the deck:\n")
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
        try:
            choice = int(input("Choose a cat card to pair(enter number)"))
            if 1 <= choice <= len(cats):
                break
            print(f"Enter a number between 1 and {len(cats)}")
        except ValueError:
            print(f"Enter a number between 1 and {len(cats)}")
        
    chosen_cat = cats[choice - 1]

    player.hand.remove(chosen_cat)
    player.hand.remove(chosen_cat)

    target = select_target(player,players)
    if target is None:
        return "cat_failed"
    target.show_hand()
    

    while True:
        try:
            card = int(input(f"{target.name}, which card will you give to {player.name}? (enter number): "))
            if 1 <= card <= len(target.hand):
                break
            print(f"Enter a number between 1 and {len(target.hand)}")
        except ValueError:
            print(f"Enter a number between 1 and {len(target.hand)}")
    stolencard = target.hand.pop(card-1)
    player.hand.append(stolencard)
    betterprint(f"{player.name} stole {stolencard} from {target.name}!\n")
    return "cat_done"
    


    


def check(player):
    if KITTEN in player.hand:
        betterprint("OH NOOOO!!!! YOU PULLED AN EXPLODING KITTENN!! 💣💣💣")
        sleep(1)
        if DEFUSE in player.hand:
            reply = input("You have a defuse!! Do you wanna use it? (yes or no) ")
            if reply.lower() == "yes":
                player.hand.remove(DEFUSE)
                player.hand.remove(KITTEN)
                betterprint("DEFUSE is used! You survived!")
                return True
            else:
                player.hand.remove(KITTEN)
                player.alive = False
                betterprint(f"{player.name} has exploded 💥 , They're out of the game!!")
                sleep(1)
                return False
        else:
            player.hand.remove(KITTEN)
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
    while True:
        try:
            numplayer = int(input("How many players are there? (2-4)  "))
            if 2<= numplayer <= 4:
                break
        except ValueError:
            print("Invalid input! please enter a number")
    for i in range(numplayer):
        name = input(f"Player {i+1}, what should I call you?  ")
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
            current = (current + 1) % len(players)
            continue
            
        player.has_played_attack = False
        player.has_played_skip = False

        if player.extra_turns > 0:
            print(f"{player.name} has {player.extra_turns} extra turn(s)!\n")
            player.extra_turns -= 1
        
        else:
            pass
        turn_ended = False
        while not turn_ended:
            choice = player_turn(player)
            if choice == "1":
                card_selected = use_card(player)
                if card_selected:
                    result = card_played(card_selected,player,players,deck)
                    if result == "skipped":
                        betterprint(f"{player.name}'s turn is over!\n")
                        sleep(2)
                        turn_ended = True
                        break
                    elif result == "attack":
                        betterprint(f"{player.name}'s turn is over!\n")
                        sleep(2)
                        turn_ended = True
                        break
                    else:
                        betterprint("You can play another card or end your turn!\n")
                        sleep(1)
                        continue
                else:
                    continue
        
            elif choice == "2":
                betterprint(f"{player.name} ends their turn and draws a card!\n")
                if draw_card(player,deck) == False:
                    turn_ended = True
                    break
                else:
                    turn_ended = True
                    break

            elif choice == "3":
                player.show_hand()
                input("Done reading? Press Enter to move on...")
                clear()
                continue



    for player in players:
        if player.alive:
            betterprint(f"\n🏆 {player.name} is the winner!!! 🏆\n")
            break

main()
        

    


