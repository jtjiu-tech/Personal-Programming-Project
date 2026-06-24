## Personal Programming Project - Yaretzi Pang
import os, time, random, cards_test
from colorama import Fore, Back, Style


colours = ["R", "Y", "G", "B", "R", "Y", "G", "B", "R", "Y", "G", "B", "R", "Y", "G", "B", "WC"]
status_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "S", "2+", "Re"]
numbers = 0
turn = 1
round = 1
win = False
selected_card = ""
selected_colour = ""
stored_card = ""
reverse_status = False

def intro():

    intro_list = [Style.BRIGHT + "The aim of the game is to lose all your cards", 
                  "Cards are represented with strings, the first character is the colour, and the second character is the number of status\n",
                  Fore.RED + "R - Red\n" + Fore.YELLOW + "Y - Yellow\n" + Fore.CYAN + "B - Blue\n" + Fore.GREEN+ "G - Green\n",
                  Fore.CYAN + "This is an example of a BLUE card, represented by the letter string 'B3'",
                  Style.BRIGHT + Fore.WHITE + "Some of the special cards include...",
                  "Reverse (YRe) - reverses the order of turns",
                  "Add 2 (R2+) - adds 2 cards to the next players deck",
                  "Skip (GS) - skips the next player's turn",
                  "Wild Card (WC) - allows the player to choose a random colour"]
    
    cards_dic = {'3': 'B3',
                '4': 'YRe',
                '5': 'R2+',
                '6': 'GS',
                '7': 'WC'}

    for i in range(9): 
        print(intro_list[i], "\n") #iterate through each item in intro_list, reduce need for multiple print statements
        time.sleep(1)

        if f'{i}' in cards_dic: #check if item position correlates with cards_dictionary
            output_card_design(cards_dic[f'{i}'])




    print("""\nRules:
1. You can only place a card on another card with the SAME NUMBER, COLOUR OR ACTION
2. If you have no cards to play or you choose to not play a card, you must draw a card
3. Only 1 card can be placed at a time
4. The game ends when a player has no cards\n""")
    
    input("The game will proceed when you press ENTER\n" + Style.RESET_ALL)
    clear_screen()

def clear_screen(): 

    print(Style.RESET_ALL + "(clearing screen)")
    for i in range(3):
        print(".")
        time.sleep(1)
    os.system("clear")


def create_players():

    players = {}
    num_of_cards_list = []
    player_names = []

    for i in range(num_of_players):
        
        player_name = input(Style.BRIGHT + f"What is player {i + 1}'s name?\n" + Style.RESET_ALL)

        while player_name.upper() in player_names:
            print(Style.BRIGHT + Fore.RED + "That's already someone's name!" + Style.RESET_ALL)
            player_name = input(Style.BRIGHT + f"What is player {i + 1}'s name?\n" + Style.RESET_ALL)

        players.update({f"{i}": [[], 7, player_name]}) #player dictionary: player number, cards, number of cards, name

        num_of_cards_list.append(players[f"{i}"][1])

        player_names.append(player_name.upper())


    return players, num_of_cards_list


def print_scoreboard(players):

    print(Style.BRIGHT + Fore.RED + "This is the scoreboard" + Style.RESET_ALL)

    length = 0

    for i in range(num_of_players):
        if len(players[f"{i}"][2]) > length: #changes length according to the longest name
            length = len(players[f"{i}"][2])

    spaces = length + 4

    print(Style.BRIGHT + f"""NUMBER    NAME{" " * (length)}NUMBER OF CARDS""" + Style.RESET_ALL)
    print(f"{(spaces + 25)* "="}")

    for i in range(num_of_players):

        while num_of_cards_list[i] != min(num_of_cards_list):
            i += 1

        print(f"{i + 1}         {players[f"{i}"][2]}{" " * (spaces - len(players[f"{i}"][2]))}{players[f"{i}"][1]}")
        print(f"{(spaces + 25 )* "-"}")
    
    print("\n")


def player_turn(turn, round, selected_card, selected_colour, stored_card, win, reverse_status):

    print_scoreboard(players)
    input("Please press ENTER to continue")

    if round == 1:
        generating = True
        time.sleep(1)
        print("The game is now starting...Please give the computer to Player 1")
        clear_screen()
    else:
        generating = False


    card_list = get_card_list(generating, turn)
    output_player_cards(card_list, turn)
    if selected_card != "DRAW":
        stored_card = selected_card
    
    selected_card, card_list = get_selected_card(card_list, stored_card, turn, selected_colour, round) #ask player to choose card
    time.sleep(1)
    print("Place the computer where everyone can see")
    clear_screen()
    print(f"Player {turn} has placed down {selected_card}")

    if selected_card != "DRAW":
        output_card_design(selected_card)
        players[f"{turn - 1}"][1] -= 1

    turn, selected_colour, reverse_status = card_effect(selected_card, turn, reverse_status)

    win = check_win(card_list)

    if reverse_status == False:
        if turn < num_of_players:
            turn += 1
        elif turn == num_of_players:
            turn = 1
            round += 1
    else:
        if turn == 1:
            turn = num_of_players
            round += 1
        elif turn < num_of_players:
            turn -= 1
        

    time.sleep(3)
    if win == False:
        print(Style.BRIGHT + f"Hand the computer to player {turn}" + Style.RESET_ALL)
        clear_screen()
        player_turn(turn, round, selected_card, selected_colour, stored_card, win, reverse_status)
    else:
        for i in range(3):
            print(".")
        print(Style.BRIGHT + Fore.RED + f"Player {turn-1} has no cards left!")
        print(Style.BRIGHT + Fore.YELLOW + r""" .----------------.  .----------------.  .----------------.   .----------------.  .----------------.  .-----------------.
| .--------------. || .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. |
| |  ____  ____  | || |     ____     | || | _____  _____ | | | | _____  _____ | || |     _____    | || | ____  _____  | |
| | |_  _||_  _| | || |   .'    `.   | || ||_   _||_   _|| | | ||_   _||_   _|| || |    |_   _|   | || ||_   \|_   _| | |
| |   \ \  / /   | || |  /  .--.  \  | || |  | |    | |  | | | |  | | /\ | |  | || |      | |     | || |  |   \ | |   | |
| |    \ \/ /    | || |  | |    | |  | || |  | '    ' |  | | | |  | |/  \| |  | || |      | |     | || |  | |\ \| |   | |
| |    _|  |_    | || |  \  `--'  /  | || |   \ `--' /   | | | |  |   /\   |  | || |     _| |_    | || | _| |_\   |_  | |
| |   |______|   | || |   `.____.'   | || |    `.__.'    | | | |  |__/  \__|  | || |    |_____|   | || ||_____|\____| | |
| |              | || |              | || |              | | | |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'   '----------------'  '----------------'  '----------------' """)


def card_effect(card, turn, reverse_status):

    selected_colour = ""

    if card[1:] == "2+":
        print(f"Player {turn + 1} now has 2 extra cards")
        players[f"{turn}"][1] += 2
        for i in range(2):
            card = draw_card()
            players[f"{turn}"][0].append(card)
    elif card[1:] == "S":
        print(f"Player {turn + 1}'s turn has been skipped")
        turn += 1
    elif card[1:] == "Re":
        print("The order of turns has now been switched")
        reverse_status = not reverse_status
    elif card[1:] == "C":
        selected_colour = ""

        while not selected_colour in colours:
            selected_colour = input(f"Player {turn}, choose a colour (R, Y, G, B)\n").upper()

        print(f"The colour is now {selected_colour}")


    return turn, selected_colour, reverse_status
    

def check_win(card_list):


    if len(card_list) != 0:
        win = False
    else:
        win = True


    return win
 

def get_selected_card(card_list, stored_card, turn, selected_colour, round):

    if stored_card != "":
        print(Style.BRIGHT + f"The previous card was {stored_card}" + Style.RESET_ALL)
    
    player_card = input(f"Please select what card you want to place down {card_list} or 'DRAW' to draw a card\n")
    valid_card = check_selected_card(stored_card, player_card, turn, selected_colour, round)


    while (player_card not in card_list or valid_card == False) and player_card != "DRAW":
        print(Fore.RED + Style.BRIGHT + "Sorry, you can't play that card" + Style.RESET_ALL)
        player_card = input(f"Please select what card you want to place down {card_list} or 'DRAW' to draw a card\n")
        valid_card = check_selected_card(stored_card, player_card, turn, selected_colour, round)


    if player_card == "DRAW":
        new_card = draw_card()
        players[f"{turn - 1}"][1] += 1
        card_list.append(new_card)
        print(f"Your cards are now {card_list}")
    else:
        card_list.remove(player_card)

    return player_card, card_list


def draw_card():

    card = ""
    status = random.choice(colours)
    card = card + status

    if status == "R" or status == "Y" or status == "G" or status == "B":
        status = random.choice(status_list)
    
        card = card + status


    return card


def check_selected_card(stored_card, selected_card, turn, selected_colour, round):

    valid_card = False

    if stored_card != "WC":

        if round == 1 and turn == 1:
            valid_card = True
        else:
            if stored_card[0] == selected_card[0] or (stored_card[1:] == selected_card[1:]) or selected_card == "WC" or stored_card == "":
                valid_card = True
            else:
                valid_card = False

    elif stored_card == "":
        valid_card = True

    else:
        print(f"The colour chosen was '{selected_colour}'")
        if selected_card[0] == selected_colour or selected_card == "WC":
            valid_card = True
        else:
            valid_card = False

    if round == 1:
        if selected_card[1:] == "S" or selected_card[1:] == "Re" or selected_card[1:] == "2+" or selected_card[1:] == "C":
                    print(Fore.RED + "Special card cannot be played during round 1")
                    valid_card = False

    return valid_card


def output_player_cards(card_list, turn):

    print(f"Player {turn}, your cards are:")

    for card in card_list:
        output_card_design(card)
        time.sleep(1)



def get_card_list(generating, turn):

    if generating == True:
        card_list = generate_cards(turn)

        players[f"{turn - 1}"][0] = card_list

    card_list = players[f"{turn - 1}"][0]
    
    return card_list


def output_card_design(card):
    
    if card[1:] == "0":
        card_design = cards_test.status_num_0
    elif card[1:] == "1":
        card_design = cards_test.status_num_1
    elif card[1:] == "2":
        card_design = cards_test.status_num_2
    elif card[1:] == "3":
        card_design = cards_test.status_num_3
    elif card[1:] == "4":
        card_design = cards_test.status_num_4
    elif card[1:] == "5":
        card_design = cards_test.status_num_5
    elif card[1:] == "6":
        card_design = cards_test.status_num_6
    elif card[1:] == "7":
        card_design = cards_test.status_num_7
    elif card[1:] == "8":
        card_design = cards_test.status_num_8
    elif card[1:] == "9":
        card_design = cards_test.status_num_9
    elif card[1:] == "Re":
        card_design = cards_test.status_reverse
    elif card[1:] == "C":
        card_design = cards_test.status_wild
    elif card[1:] == "2+":
        card_design = cards_test.status_add_2
    elif card[1:] == "S":
        card_design = cards_test.status_skip
    
    for line in card_design:
            l = ""
            for char in line:

                if char == ":":
                    l += Back.WHITE

                elif card[0] == "R" or char == "/":
                    l += Back.RED
                elif card[0] == "Y" or char == "]":
                    l += Back.YELLOW
                elif card[0] == "B" or char == ";":
                    l += Back.CYAN
                elif card[0] == "G" or char == "[":
                    l += Back.GREEN

                
                l += char + Style.RESET_ALL

            print(l)
    
    print("")


def generate_cards(turn):

    card_list = []

    for i in range(players[f"{turn - 1}"][1]):
        card = draw_card()
        card_list.append(card)

    
    return card_list





print(Style.BRIGHT + r""" .----------------.  .-----------------. .----------------. 
| .--------------. || .--------------. || .--------------. |
| | _____  _____ | || | ____  _____  | || |     ____     | |
| ||_   _||_   _|| || ||_   \|_   _| | || |   .'    `.   | |
| |  | |    | |  | || |  |   \ | |   | || |  /  .--.  \  | |
| |  | '    ' |  | || |  | |\ \| |   | || |  | |    | |  | |
| |   \ `--' /   | || | _| |_\   |_  | || |  \  `--'  /  | |
| |    `.__.'    | || ||_____|\____| | || |   `.____.'   | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' """)

intro_status = ""
while intro_status != "Y" and intro_status != "N":
    intro_status = input(Fore.CYAN + "Would you like an intro to the game? (Y/N)\n").upper()

if intro_status == "Y":
    intro()


num_of_players = 0
valid_players = False
while not valid_players:
    try:
        num_of_players = int(input(Style.RESET_ALL + "How many players are playing (pick a number from 2-4)\n"))
 
    except(TypeError, ValueError):
        continue

    if num_of_players >= 2 and num_of_players <= 4:
            valid_players = True


clear_screen()
generating = True
players, num_of_cards_list = create_players()
player_turn(turn, round, selected_card, selected_colour, stored_card, win, reverse_status)