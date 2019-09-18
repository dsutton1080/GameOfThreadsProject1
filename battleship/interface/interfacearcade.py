# New to arcade, based off of a template: http://arcade.academy/examples/starting_template.html#starting-template
import arcade, random
# pip install arcade

# Grid info
numofrows = 8
numofcols = 8
# grid tile info
width = 40
height = 40
# how thicc the lines should be
thicc = 2
# window size
window_width = (width + thicc) * numofcols + thicc
window_height = (height + thicc) * numofrows + thicc
windowtitle = "Array Backed Grid Example"

# Setting color values
black = (0, 0, 0)  # background
white = (255, 255, 255)  # normal color for no activity
red = (255, 0, 0)  # declares hit
grey = (193, 205, 205)  # declares miss
aqua = (0, 255, 255)  # ship color
green =(0, 255, 0)  # selector color
# Setting values for the colors
ship = 1
hit = 2
miss = 3
selector = 4
gamewidth = 800
gameheight = 600
menuwidth = 800
menuheight = 600

ships_1 = [ [1] ]
ships_2 = [ [1], [2,2]]
ships_3 = [ [1], [2,2], [3,3,3] ]
ships_4 = [ [1], [2,2], [3,3,3], [4,4,4,4]]
ships_5 = [ [1], [2,2], [3,3,3], [4,4,4,4], [5,5,5,5,5] ]



def new_board():
    board = [[0 for x in range(numofcols)] for y in range(numofrows)]
    return board


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.YALE_BLUE)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Battleship!",menuwidth/2, menuheight/2, arcade.color.BLACK, font_size=40, anchor_x='center')
        arcade.draw_text("Click when ready", menuwidth / 2, menuheight / 2-75, arcade.color.YELLOW_ROSE, font_size=20,anchor_x='center')
    def on_mouse_press(self, x,y,button, modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)

class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Ship selection", menuwidth / 2, menuheight / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("How many ships would you like to play with", menuwidth / 2, menuheight / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.board = None
        self.game_over = False
    def on_show(self):
        arcade.set_background_color(arcade.color.ALABAMA_CRIMSON)
    def on_draw(self):
        arcade.start_render()

    def draw_grid(self, grid, offset_x, offset_y):
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column]:
                    color = arcade.color.YELLOW
                    x = (thicc + width) * (column + offset_x) + thicc + width // 2
                    y = window_height - (thicc + height) * (row + offset_y) + thicc + height // 2

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, width, height, color)

def main():
    game = arcade.Window(gamewidth, gameheight, "BattleShip!")
    game.total_score =0
    menuview = MenuView()
    game.show_view(menuview)
    arcade.run()

if __name__ == "__main__":
    main()
