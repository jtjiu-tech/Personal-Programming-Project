import random
from random import randint
import colorama
from colorama import init, Fore, Back, Style
colorama.init()
import os
import time

BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
CYAN = Fore.CYAN
WHITE = Fore.WHITE
RED = Fore.RED
MAGENTA = Fore.MAGENTA
BLACK = Fore.BLACK
PLAYER_DOT = "●"

VALID_colours = ["BLUE", "YELLOW", "GREEN", "CYAN", "WHITE", "RED", "MAGENTA", "BLACK"]



def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def show_loading_message(message, seconds):
    clear_terminal()
    print(message)
    time.sleep(seconds)

def get_valid_int(question):
    valid = False
    number = 0

    while valid == False:
        try:
            number = int(input(question))
            valid = True
        except ValueError:
            print("Please enter a whole number.")

    return number

def display_help():
    print("SNAKES AND LADDERS RULES")
    print("Each player starts on square 1.")
    print("Players take turns rolling the dice.")
    print("Move forward by the number rolled.")
    print("Ladders move you up the board.")
    print("Snakes move you down the board.")
    print("If you land on another player, they go back to square 1.")
    print("You must roll the exact number to reach the final square.")
    print("The first player to reach the final square wins.")
    print()
    print("Board labels:")
    print("L1 Start = the start of ladder 1")
    print("L1 End = the end of ladder 1")
    print("S1 Start = the start of snake 1")
    print("S1 End = the end of snake 1")
    print()



def reset_other_players(current_player_index, player_positions):
    current_position = player_positions[current_player_index]
    for i in range(len(player_positions)):
        if i != current_player_index:
            if player_positions[i] == current_position:
                print(f"Player {current_player_index + 1} landed on Player {i + 1}!")
                print(f"Player {i + 1} has been sent back to square 1.")
                player_positions[i] = 1


def roll_dice():

    return randint(1, 6)

def check_if_past_100():
    ###
    pass

def check_for_special_tile(player_position, ladders, snakes):
    if player_position in ladders:
        new_position = ladders[player_position]
        print(f"You landed on a ladder! Climb up from {player_position} to {new_position}")
        return new_position

    elif player_position in snakes:
        new_position = snakes[player_position]
        print(f"Oh no! You landed on a snake! Slide down from {player_position} to {new_position}")
        return new_position

    else:
        return player_position
    


def take_turn(current_player_index, player_positions, ladders, snakes, final_square, board, width):

    show_loading_message("Displaying board now...", 4)

    clear_terminal()
    display_board_with_players(board, player_positions, player_colours, width)
    print()
    display_player_positions(player_positions)
    print()
    print(f"Player {current_player_index + 1}'s turn")



    dice_role = input("Press Enter to roll the dice, or H for help: ")

    if dice_role.upper() == "H":
        display_help()
        input("Press Enter to roll the dice...")




    dice_roll = roll_dice()
    print(f"Player {current_player_index + 1} rolled a {dice_roll}")

    time.sleep(2)

    starting_position = player_positions[current_player_index]
    new_position = starting_position + dice_roll

    if new_position > final_square:
        print(f"Player {current_player_index + 1} needs an exact roll to finish.")
        time.sleep(2)
        return False

    player_positions[current_player_index] = new_position

    checked_position = check_for_special_tile(new_position, ladders, snakes)
    player_positions[current_player_index] = checked_position

    reset_other_players(current_player_index, player_positions)

    print(f"Player {current_player_index + 1} is now on square {player_positions[current_player_index]}")

    time.sleep(3)
    
    if player_positions[current_player_index] == final_square:
        print(f"Player {current_player_index + 1} wins!")
        print("GAME OVER")
        return True
    
    if dice_roll == 6:
        print(f"Player {current_player_index + 1} rolled a 6 and gets another turn!")
        time.sleep(2)
        return take_turn(current_player_index, player_positions, ladders, snakes, final_square, board, width)

    return False

def num_of_players():
    player_num_not_valid = True
    player_num=0
    while player_num_not_valid == True:
        player_num = get_valid_int("How many players will be playing? ")
        if player_num < 9 and player_num>1:
            player_num_not_valid = False
        else:
            print("Invalid Player number. There is a maximum of 8 players and a minimum of 2")
    return player_num

player_colours = []

def select_player_colours(player_num):
    for i in range(player_num):
        notvalid = True
        while notvalid == True:
            colour = input(f"Player {i+1}, Which colour would you like to choose? ").upper()
            if colour in VALID_colours:
                if eval(colour) in player_colours:
                    print(f"{colour} has already been chosen. Please choose another colour.")
                else:
                    player_colours.append(eval(colour))
                    print(eval(colour), f"Success! You chose {colour}", Style.RESET_ALL)
                    notvalid = False
            else:
                print(f"{colour} is not a valid colour, the options are {VALID_colours}.")

def create_board():
    width = 0
    height = 0
    while 2 >= width or width > 11:
        width = get_valid_int("What would you like the width of the board to be? ")
    while 2 >= height or height > 11:
        height = get_valid_int("What would you like the height of the board to be? ")
    board = []
    current_square_num = 1
    for i in range(height):
        row = []
        for j in range(width):
            row.append(current_square_num)
            current_square_num += 1
        board.append(row)
    
    return board, width, height

def display_board(board):
    for row in board:
        formatted_row = [str(cell).center(10) for cell in row]
        print("| " + " | ".join(formatted_row) + " |")

def display_player_positions(player_positions):
    for i in range(len(player_positions)):
        print(f"Player {i + 1}: square {player_positions[i]}")

def game_setup():
    print()
    print()
    print("WELCOME TO SNAKES AND LADDERS!")
    print("Press H before rolling the dice if you need help.")
    print()
    board, width, height = create_board()
    final_square = width * height
    player_num = num_of_players()
    select_player_colours(player_num)

    player_positions = [1] * player_num

    ladders = set_ladder_map(width, height, board)
    snakes = set_snake_map(width, height, board)


    current_player_index = 0
    game_over = False

    while game_over == False:
        game_over = take_turn(current_player_index, player_positions, ladders, snakes, final_square, board, width)

        if game_over == False:
            current_player_index = (current_player_index + 1) % player_num


def display_board_with_players(board, player_positions, player_colours, width):
    display_board_copy = []

    for row in board:
        display_board_copy.append(row.copy())

    for i in range(len(player_positions)):
        position = player_positions[i]

        row = (position - 1) // width
        col = (position - 1) % width

        player_display = player_colours[i] + PLAYER_DOT.center(10) + Style.RESET_ALL
        display_board_copy[row][col] = player_display

    display_board(display_board_copy)

def set_ladder_map(width, height, board):
    board_area = width * height
    ladder_num = 0
    if 0 < board_area <= 20:
        ladder_num += 1
    elif 20 < board_area <=50:
        ladder_num += 2
    elif 50 < board_area <=100:
        ladder_num += 4
    else:
        ladder_num += 7
    ladders = {}
    
    for i in range (ladder_num):
        placed = False
        while placed == False:

            ladder_start = randint(1, board_area - 2) 
            ladder_end = randint(ladder_start + 1, board_area - 1)
            
            if ladder_start not in ladders and ladder_end not in ladders.values():
                ladders[ladder_start] = ladder_end
                row_s = (ladder_start - 1) // width
                col_s = (ladder_start - 1) % width
                row_e = (ladder_end - 1) // width
                col_e = (ladder_end - 1) % width
                board[row_s][col_s] = f"L{i+1} Start" 
                board[row_e][col_e] = f"L{i+1} End"
                placed = True
    return ladders

def set_snake_map(width, height, board):
    board_area = width * height
    snake_num = 0
    if 0 < board_area <= 20:
        snake_num += 1
    elif 20 < board_area <=50:
        snake_num += 2
    elif 50 < board_area <=100:
        snake_num += 4
    else:
        snake_num += 7
    snakes = {}

    for i in range (snake_num):
        placed = False
        while placed == False:
            snake_end = randint(1, board_area - 2) 
            snake_start = randint(snake_end + 1, board_area - 1)

            row_s = (snake_start - 1) // width
            col_s = (snake_start - 1) % width
            row_e = (snake_end - 1) // width
            col_e = (snake_end - 1) % width

            if snake_start not in snakes and snake_end not in snakes.values() and board[row_s][col_s] == snake_start and board[row_e][col_e] == snake_end:
                snakes[snake_start] = snake_end
                board[row_s][col_s] = f"S{i+1} Start" 
                board[row_e][col_e] = f"S{i+1} End"
                placed = True
    return snakes
    


game_setup()