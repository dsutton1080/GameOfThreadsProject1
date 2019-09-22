import random


class Coordinates:
    # variables
    ship_coordinates = None

    def __init__(self):
        """

        """
        self.ship_coordinates = []

    def add_ship_coordinate(self, new_coordinate):
        """

        :param new_coordinate:
        """
        self.ship_coordinates.append(new_coordinate)
        self.print_all_coordinates()

    def return_all_coordinates(self):
        """

        :return:
        """
        return self.ship_coordinates

    def print_all_coordinates(self):
        """

        """
        print(self.ship_coordinates)


def startup():
    """

    """
    print("Welcome to Battleship!")
    plays_first()


def plays_first():
    """

    """
    coin_choice = input("Lets begin, heads or tails?: ")
    coin_list = ["heads", "tails"]
    correct = random.choice(coin_list)
    if (coin_choice.lower() != "heads") & (coin_choice.lower() != "tails"):
        print("Well, since you were unable to enter heads or tails I will choose for you.")
        print("Person to the left is Player1 and person to the right is Player2.")
    elif coin_choice.lower() == correct:
        print("If you chose " + correct + " you are Player1")
        print("The other person is Player2")
    elif coin_choice.lower() != correct:
        print("If you chose " + correct + " you are Player2")
        print("The other person is Player1")


def get_num_of_ships():
    """

    :return:
    """
    num_ships = input("How many ships should each player have: ")
    while not test_input(num_ships):
        num_ships = input("Please enter a valid input between 1 and 5: ")
    if test_input(num_ships):
        return int(num_ships)


def test_input(num_ships):
    """

    :param num_ships:
    :return:
    """
    try:
        if int(num_ships) in range(1, 6):
            return True
    except ValueError:
        return False


def add_ship(player, size):
    """

    :param player:
    :param size:
    """
    if size == 1:
        new_coordinate = input("Enter a single coordinate where you would like to place your ship: ")
        player.add_ship_coordinate(new_coordinate)
    if size in range(2, 6):
        temp = size
        while temp > 0:
            new_coordinate = input("Enter a coordinate where you would like to place your ship: ")
            player.add_ship_coordinate(new_coordinate)
            temp = temp - 1


def choose_ships(ship_num):
    """

    :param ship_num:
    """
    temp = 1
    player1 = Coordinates()
    while temp <= ship_num:
        print("This is a coordinate for ship " + str(temp))
        add_ship(player1, temp)
        temp = temp + 1


def main():
    """

    """
    startup()
    numOfShips = get_num_of_ships()
    choose_ships(numOfShips)


main()
