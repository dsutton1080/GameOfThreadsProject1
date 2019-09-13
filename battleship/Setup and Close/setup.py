# import tkinter as tk


def startup():
    print("Welcome to Battleship!")


def get_num_of_ships():
    num_ships = input("How many ships should each player have: ")
    while not test_input(num_ships):
        num_ships = input("Please enter a valid input between 1 and 5: ")
    if test_input(num_ships):
        return int(num_ships)


def test_input(num_ships):
    try:
        if int(num_ships) in range(1, 6):
            return True
    except ValueError:
        return False


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
numOfShips = get_num_of_ships()
choose_ships(numOfShips)
