# import tkinter as tk


def startup():
    print("Welcome to Battleship!")

def set_number():



def get_num_of_ships(phase):
    if phase == "first":
        num_ships = input("How many ships should each player have: ")
    if phase != "first":
        num_ships = phase
    print(num_ships)
    if test_input(num_ships):
        return int(num_ships)


def test_input(num_ships):
    try:
        if int(num_ships) in range(1, 6):
            print("valid input found")
            return num_ships
    except ValueError:
        new_num_ships = input("Please enter a valid input between 1 and 5: ")
        get_num_of_ships(new_num_ships)


def choose_ships(ship_num):
    if ship_num == 1:
        print("1x1")
    if ship_num == 2:
        print("1x1, 2x1")
    if ship_num == 3:
        print("1x1, 2x1, 3x1")
    if ship_num == 4:
        print("1x1, 2x1, 3x1, 4x1")
    if ship_num == 5:
        print("1x1, 2x1, 3x1, 4x1, 5x1")


startup()
numOfShips = get_num_of_ships("first")
choose_ships(numOfShips)
