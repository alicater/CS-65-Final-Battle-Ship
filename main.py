import pygame as pg
import random
import asyncio # necessary to use the module 'pygbag' to play game in browser
pg.init()

# All of the code that creates the window and sets up the
# variables needed to run the rest of the code
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

rows = 4
cols = 4

window = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pg.display.set_caption("Battleship")

# creates the variables for all the images needed for the game
bg_image =  pg.image.load("bg.jpg")
bg_image = pg.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
window.blit(bg_image, (0,0))
pg.display.update()

explosion = pg.image.load("explosion.png")
explosion = pg.transform.scale (explosion, (WINDOW_WIDTH//4, WINDOW_HEIGHT//4))
missed = pg.image.load("x.png")
missed = pg.transform.scale (missed, (WINDOW_WIDTH//4, WINDOW_HEIGHT//4))


def create_board(size = 4):
    """
    creates the board list

    Parameter: size = determines how many rows/columns will be in the list

    Returns: board list
    """
    board=[]
    for layout in range(size):
        board.append([""]*size)
    return board

def get_random_location(board):
    """
    Gets a random loaction which will be the 'battleship'

    Parameter: board = the list created in 'create_board' function

    Returns: the row and column the ship will be in
    """
    row = random.randint(0, len(board)-1)
    col = random.randint(0, len(board[0])-1)
    return row, col 

def convertCoordinate(x, y):
    """
    converts the mouse click's pixel coordinate into the corresponding 
    row and column on the grid

    Parameters: x = the x coordinate of the pixel, y = the y coordinate of the pizel

    Returns: the new row and column coordinate based on the grid
    """
    height_row = WINDOW_HEIGHT//rows
    new_y = y//height_row

    height_col = WINDOW_WIDTH//cols
    new_x = x//height_col
    return new_x, new_y

def draw_board(board, window):
    """
    divides the window into equally spaced rows and columns and draws lines
    creating a grid

    Parameter: board = the board list, window = the graphics/gui window

    Returns: updated window with the grid 
    """
    for row in range(rows):
        y = row*100
        pg.draw.line(window, (255,255,255), (0, y), (WINDOW_HEIGHT, y))
    for col in range(cols):
        x = col*100
        pg.draw.line(window, (255,255,255), (x, 0), (x, WINDOW_WIDTH))
    pg.display.update()

def play_game(correct_row, correct_col, player_row, player_col, window):
    """
    plays the game 

    Parameters: correct_row = the row index of the correct location
        correct_col = the column index of the correct location
        player_row = the row index of the player's guess
        player_col = the column index of the player's guess
        window = the graphics/gui window

    Returns: True or False based on if the user hit the 'battleship' or not
    """
    if player_col == correct_col and player_row == correct_row:
        cell_size = WINDOW_WIDTH // cols
        pixel_x = player_col * cell_size
        pixel_y = player_row * cell_size
        window.blit(explosion, (pixel_x, pixel_y)) 
        return True
    else:
        cell_size = WINDOW_WIDTH // cols
        pixel_x = player_col * cell_size
        pixel_y = player_row * cell_size
        window.blit(missed, (pixel_x, pixel_y))
        return False


 # All of the functions being run that are needed to set up the 'board'   
board = create_board()
draw_board(board, window)
correct_row, correct_col = get_random_location(board)

turns = 5
# number of turns user has to guess where battleship is

current_turn = 1 
# the current turn the user is at


# the while loop required to use and run the pygame  
async def main(): 

    current_turn = 1 
    # the current turn the user is at

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                col, row = convertCoordinate(x, y)
                result = play_game(correct_row, correct_col, row, col, window)
                pg.display.update()
                if result: 
                    running = False
                    break
                elif current_turn == turns:
                    running = False
                    break
                else:
                    current_turn += 1 
            if event.type == pg.QUIT:
                running = False
                break

        await asyncio.sleep(0)

asyncio.run(main())