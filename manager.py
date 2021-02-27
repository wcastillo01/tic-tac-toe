import pygame 
# from tictactoe import current_player

# COLORS UTILIZED
WHITE = (255,255,255)

# ----- CONSTANTS -----
BOARD_ROWS = 3
BOARD_COLS = 3
WIDTH = 600
HEIGHT = WIDTH
GRID_SIZE = WIDTH // BOARD_ROWS


CIRCLE_WIDTH = 15
X_WIDTH = 25 
CIRCLE_RADIUS = GRID_SIZE//3
SPACE = GRID_SIZE//4

PADDING = int(GRID_SIZE * 0.025)

# VARIABLES

surface = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("tic-tac-toe")
active = True
gameover = False
current_player = "X"
winner = None
surface.fill((76, 76, 225))



# GAMEBOARD CREATED
board = [[0 for i in range(BOARD_ROWS)] for j in range(BOARD_COLS)] 

# FUNCTIONS 

# Draws lines that make up the grid
def draw_grid(surface):         
    pygame.draw.line(surface, ((217,216,216)) , (0, GRID_SIZE), (600, GRID_SIZE), PADDING) # Horizontal lines 
    pygame.draw.line(surface, ((217,216,216)) , (0, GRID_SIZE*2 ), (600, GRID_SIZE*2 ), PADDING) # Horizontal lines 
    pygame.draw.line(surface, ((217,216,216)) , (GRID_SIZE, 0), (GRID_SIZE, 600), PADDING) # Vertical lines  
    pygame.draw.line(surface, ((217,216,216)) , (GRID_SIZE*2 , 0), (GRID_SIZE*2 , 600), PADDING) # Vertical lines 


# Prints board at a given state
def print_board(player):

    if player == "X":
        player = 'O'
    elif player == "O":
        player = "X"
    print(f"{player}'s turn:\n")
    for rows in board:
        print(rows)
    print("\n")

# Checks if spot is available
def is_available(row, col):
    return board[row][col] == 0
           
 
# Checks if board is full
def is_board_full():
    for row in range(BOARD_ROWS):
        for cols in range(BOARD_COLS):
            if board[row][cols] == 0:
                return False

# Makes a visual representation of the player's move
def draw_play():
    for row in range(BOARD_ROWS):
        for cols in range(BOARD_COLS):
            if board[row][cols] == "X":
                pygame.draw.line(surface, WHITE, (cols*GRID_SIZE + SPACE, row * GRID_SIZE + GRID_SIZE - SPACE), (cols* GRID_SIZE + GRID_SIZE - SPACE, row * GRID_SIZE + SPACE), X_WIDTH)
                pygame.draw.line(surface, WHITE, (cols*GRID_SIZE + SPACE, row*GRID_SIZE + SPACE), (cols*GRID_SIZE+GRID_SIZE - SPACE, row*GRID_SIZE+GRID_SIZE - SPACE), X_WIDTH)
                
            elif board[row][cols] == "O":
                pygame.draw.circle(surface, WHITE, (int(cols*GRID_SIZE+GRID_SIZE/2), int(row*GRID_SIZE+GRID_SIZE/2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


# After a player's move checks if there is a winner
def check_win():
    if check_rows():
        return True
    if check_cols():
        return True
    if check_diagonal():
        return True
    
# checks if there is a winner in all rows
def check_rows():
    for rows in range(BOARD_ROWS):
        if board[rows][0] == board[rows][1] == board[rows][2] != 0:
            horizontal_win(rows)
            return True

# checks if there is a winner in all columns
def check_cols():
    for cols in range(BOARD_COLS):
        if board[0][cols] == board[1][cols] == board[2][cols] != 0:
            vertical_win(cols)
            return True

# checks if there is a winner in all diagonals
def check_diagonal():
    if board[1][1] == board[0][2] == board[2][0] != 0:    
        diagonal_win()
        return True
    elif board[1][1] == board[0][0] == board[2][2] != 0:
        diagonal_win_left()
        return True

# Draws a vertical line when a player wins
def vertical_win(cols):
    line = (cols * GRID_SIZE) + GRID_SIZE / 2
    pygame.draw.line(surface, WHITE, (line, 15), (line, HEIGHT - 15), 15)

# Draws a horizontal line when a player wins
def horizontal_win(rows):
    line = (rows * GRID_SIZE) + GRID_SIZE / 2
    pygame.draw.line(surface, WHITE, (15, line), (600-15, line), 15)


# Draws a ascending diagonal line when a player wins
def diagonal_win():
    pygame.draw.line(surface, WHITE, (15, HEIGHT-15), (HEIGHT-15, 15), 15)

# Draws a descending diagonal line when a player wins
def diagonal_win_left():
    pygame.draw.line(surface, WHITE, (15, 15), (HEIGHT-15, HEIGHT-15), 15)

# Starts a new game
def restart():
    surface.fill((76, 76, 225))
    draw_grid(surface)
    for row in range(BOARD_ROWS):
        for cols in range(BOARD_COLS):
            board[row][cols] = 0

# Lets player mark a spot in the array
def play(row, col, player):
    global gameover
    board[row][col] = player
    print_board(player)
    if check_win():
        gameover = True
    check_win()
    draw_play()

def random_number():
    from random import seed
    from random import randint

    seed(1)

    while True:
        clicked_row = randint(0,2)
        clicked_col = randint(0,2)

        if is_available(clicked_row, clicked_col):

            global gameover
            board[clicked_row][clicked_col] = 'O'
            print_board('O')
            if check_win():
                gameover = True
            check_win()
            draw_play()
            break
        

