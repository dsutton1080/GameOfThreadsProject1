# New to Pygame, based off of a template: http://programarcadegames.com/python_examples/f.php?file=pygame_base_template.py
import pygame, os, sys

# ---- SETUP ----
pygame.init()
# how fast the screen updates
clock = pygame.time.Clock()

# Setting color values
black = (0,0,0) #background
white = (255,255,255) # normal color for no activity
red = (255,0,0) # declares hit
grey = (193,205,205) #declares miss
aqua = (0,255,255) #ship color
green =(0,255,0) #selector color
ani =4
# Setting values for the colors
ship = 1
hit = 2
miss = 3

# 2d array
grid = []
numofrows = 8
numofcols = 8

for row in range(numofrows+1):
    grid.append([])
    for col in range(numofcols+1):
        grid[row].append(0)
print(grid)

# Width and Height for each grid square
width = 40
height = 40
thicc = 2 # grid lines thickness
x = ((thicc + width) * col + thicc)
y = (thicc + height) * row + thicc

# window
window_width = (width * numofcols) + (thicc * (numofcols+1))
window_height = (height * numofrows) + (thicc * (numofrows + 1))

windowsize = [window_width, window_height]
screen = pygame.display.set_mode(windowsize)
pygame.display.set_caption('Battleship!') # title of screen





done = False

# -------------
# draws the grid
def grid1():
    for row in range(numofrows):
        for col in range(numofcols):
            color = white
            if grid[row][col] == 1:
                color = green
            pygame.draw.rect(screen, color, [(thicc + width) * col + thicc, (thicc + height) * row + thicc, width, height])


def grid2():
    for row in range(numofrows):
        for col in range(numofcols):
            color = white
            if grid[row][col] == 1:
                color = green
            pygame.draw.rect(screen, color, [(thicc + width) * col + thicc, (thicc + height) * row + thicc, width, height])


# ----------- Main loop
while not done:
    for event in pygame.event.get():  # user did something
        if event.type == pygame.QUIT:  # if user clicked close
            done = True  # exits
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left') # player.control()
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right') # player.control()
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('up')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down') # player.control()
            if event.key == pygame.K_RETURN:
                print('enter')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left stop') # player.control()
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right stop') # player.control()
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('up stop') # player.control()
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down stop') # player.control()
            if event.key == pygame.K_RETURN:
                print('enter stop')
        elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                #change xy to grid
                col = (position[0] // (width + thicc))+1
                row = (position[1] // (height + thicc)) +1
                grid[row][col] = 1
                print("click ", position, "grid ", row, col)
                print(grid)

    screen.fill(black)  # set background color

    grid1()

    # 60 fps
    clock.tick(60)

    pygame.display.flip()
pygame.quit()

