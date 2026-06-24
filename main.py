## Personal Programming Project John Tjiu
import time
from colorist import rgb, ColorRGB
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
def color_text(text, r, g, b):
    return f"{ColorRGB(r, g, b)}{text}{ColorRGB(255, 255, 255)}"

def gold(text):
    return color_text(text, 255, 204, 0)

def red(text):
    return color_text(text, 255, 0, 0)

def green(text):
    return color_text(text, 0, 255, 0)

def cyan(text):
    return color_text(text, 0, 255, 255)

def magenta(text):
    return color_text(text, 255, 0, 255)

def blue(text):
    return color_text(text, 0, 150, 255)

def orange(text):
    return color_text(text, 255, 165, 0)

def pink(text):
    return color_text(text, 255, 105, 180)

def bright(text):
    return color_text(text, 255, 255, 100)

def dim(text):
    return color_text(text, 150, 150, 150)


def announce_look_away():
    print("\n" + "="*50)
    print("🔒 OTHER PLAYERS: PLEASE LOOK AWAY NOW! 🔒")
    print("="*50)
    for i in range(3, 0, -1):
        print(f"👀 Looking away in {i}...")
        sleep(1)
    clear()

def announce_players_can_look():
    clear()
    print("\n" + "="*50)
    print("👁️ OTHER PLAYERS: YOU CAN LOOK BACK NOW! 👁️")
    print("="*50)
    sleep(3)
    clear()

def announce_private_action(current_player, action_name):
    clear()
    print("\n" + "🔒"*25)
    print(f"🔒 {current_player.name} is using {action_name} - PRIVATE ACTION 🔒")
    print("🔒"*25)
    announce_look_away()

def announce_public_action(player, action_name):
    """Announce a public action that everyone can see"""
    clear()
    print("\n" + "⭐"*30)
    print(f"⭐ {player.name} played {action_name}! ⭐")
    print("⭐"*30)
    sleep(1)




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


    while True:
        try:
            choice = int(input("Enter player number: ")) 
            if 1 <= choice <= len(available):
                return available[choice - 1]
            else:
                print(f"Enter a number between 1 and {len(available)}")
        except ValueError:
            print(f"Enter a number between 1 and {len(available)}")



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
        if player.extra_turns > 0:
            betterprint(f" {player.name} has {player.extra_turns} extra turn(s) remaining!\n")
            print("🔴" * player.extra_turns + " TURNS REMAINING\n")

    
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
    announce_private_action(player, "DRAWING A CARD")
    card = deck.pop(0)
    player.hand.append(card)
    getting_card()
    betterprint(f"You drew a {card}!!!\n")
    sleep(2)
    player.show_hand()
    input("Done reading? Press Enter to move on...")
    announce_players_can_look()
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

last_action = None
last_action_player = None
last_action_target = None
favor_cancelled = False


def card_played(card_selected, player, players, deck):
    global last_action, last_action_player, last_action_target
    
    if card_selected == DEFUSE:
        betterprint("You can't use a defuse, you didn't pull an exploding kitten...")
        sleep(1)
        clear()
        return None
    elif card_selected in CATS:
        return cat_combos(player, players)
    elif card_selected == ATTACK:
        last_action = "attack"
        last_action_player = player
        last_action_target = None
        announce_public_action(player, "ATTACK")
        player.has_played_attack = True
        return attack(player, players)
    elif card_selected == NOPE:
        announce_public_action(player, "NOPE")
        return nope()
    elif card_selected == SKIP:
        announce_public_action(player, "SKIP")
        player.has_played_skip = True
        return skip(player)
    elif card_selected == SHUFFLE:
        announce_public_action(player, "SHUFFLE")
        return shuffle(deck)
    elif card_selected == FAVOR:
        last_action = "favor"
        last_action_player = player
        last_action_target = None
        announce_private_action(player, "FAVOR")
        return favor(player, players) 
    elif card_selected == SEE:
        announce_private_action(player, "SEE THE FUTURE")
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
            betterprint(f" {next_player.name} now has {next_player.extra_turns} total turns to take! \n")
            break

    return "attack"
    #handle in main loop

def nope():
    global last_action, last_action_player, last_action_target, players, favor_cancelled
    
    if last_action is None:
        betterprint("There's no action to NOPE!\n")
        sleep(1)
        return "nope_failed"
    
    betterprint(f"NOPE! The {last_action} by {last_action_player.name} is cancelled!\n")
    sleep(1)
    
    if last_action == "attack":
        current_index = players.index(last_action_player)
        for i in range(1, len(players)):
            next_player = players[(current_index + i) % len(players)]
            if next_player.alive:
                if next_player.extra_turns >= 2:
                    next_player.extra_turns -= 2
                else:
                    next_player.extra_turns = 0
                betterprint(f"Removed 2 extra turns from {next_player.name}\n")
                break
    
    elif last_action == "favor":

        favor_cancelled = True
        betterprint("The favor has been cancelled! No cards will be stolen.\n")

    

    if last_action != "favor":
        last_action = None
        last_action_player = None
        last_action_target = None
    
    return "nope_success"

def skip(player):
    betterprint(f"{player.name} used SKIP! Their turn is skipped\n")
    sleep(1)
    return "skipped"
    #handle in main loop

def shuffle(deck):
    betterprint("Shuffling the deck...\n")
    random.shuffle(deck)
    sleep(1)
    betterprint("Deck shuffled\n")
    return "shuffled"
    #should work


def favor(current_player, players):
    global last_action, last_action_target, favor_cancelled
    
    # Check if this favor was cancelled BEFORE doing anything
    if favor_cancelled:
        favor_cancelled = False
        last_action = None
        last_action_player = None
        last_action_target = None
        betterprint("The favor was cancelled! No cards were stolen.\n")
        return "favor_cancelled"

    target = select_target(current_player, players)
    if target is None:
        return "favor_failed"

    last_action_target = target
    betterprint(f"{current_player.name} is asking for a card from {target.name}!")

    sleep(1)
    clear()
    print(f"{target.name}'s hand (only {target.name} should see this):")
    sleep(5)
    target.show_hand()

    while True:
        try:
            card_input = input(f"{target.name}, which card would you give to {current_player.name}? (enter number): ")
            card_index = int(card_input)
            if 1 <= card_index <= len(target.hand):
                break
            else:
                print(f"Invalid choice!!! Choose a number between 1 and {len(target.hand)}")
        except ValueError:
            print(f"Invalid choice!!! Choose a number between 1 and {len(target.hand)}")

    stolen_card = target.hand.pop(card_index - 1)
    current_player.hand.append(stolen_card)
    clear()
    betterprint(f"{current_player.name} has received {stolen_card} from {target.name}! \n")
    sleep(3)
    announce_players_can_look()
    
    last_action = None
    last_action_player = None
    last_action_target = None
    
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
    announce_players_can_look()
    return "Seen_the_future"
    #should work

def cat_combos(player,players):
    #basically adds all cards in players hand that are in the list CATS into a new list
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

    removed_count = 0
    for i in range(len(player.hand) -1, -1, -1):
        if player.hand[i] == chosen_cat:
            player.hand.pop(i)
            removed_count += 1
            if removed_count == 2:
                break

    target = select_target(player, players)
    if target is None:
        for i in range(2):
            player.hand.append(chosen_cat)
        return "cat_failed"
    
    announce_private_action(player, "CAT COMBO")
    print(f"📋 {target.name}'s hand (only {player.name} should see this):")
    sleep(3)
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
    sleep(2)
    announce_players_can_look()
    return "cat_done"
    


    


def check(player):
    if KITTEN in player.hand:
        betterprint("YOU PULLED AN EXPLODING KITTEN!!! 💣💣💣 \n")
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
            betterprint(f"🔴🔴🔴 {player.name} has {player.extra_turns} turn(s) remaining! 🔴🔴🔴\n")
            sleep(1)


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
                        attack_played = True
                        break
                    elif result == "nope_success":
                        betterprint("The action was cancelled by NOPE!\n")
                        sleep(1)
                        break

                    elif result =="nope_failed":
                        continue

                    elif result == "favor_cancelled":
                        betterprint("The favor was cancelled!\n")
                        sleep(1)
                        continue

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

        if player.extra_turns > 0:
            player.extra_turns -= 1
            if player.extra_turns > 0:

                betterprint(f"🔄 {player.name} has {player.extra_turns} turn(s) remaining!\n")
                sleep(1)
                continue
            else:

                current = (current + 1) % len(players)
                while not players[current].alive:
                    current = (current + 1) % len(players)
        else:
            current = (current + 1) % len(players)
            while not players[current].alive:
                current = (current + 1) % len(players)
        last_action = None
        last_action_player = None
        last_action_target = None

    for player in players:
        if player.alive:
            betterprint(f"\n🏆 {player.name} is the winner!!! 🏆\n")
            break
main()
        

    


