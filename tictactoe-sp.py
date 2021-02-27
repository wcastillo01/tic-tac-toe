import pygame, os
from manager import *

pygame.init()

# ----- WINDOW INITIAL POSITION -----
os.environ['SDL_VIDEO_WINDOW_POS'] = '900,125'

# ----- VARIABLES -----

surface = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("tic-tac-toe")
active = True
gameover = False
current_player = "X"
surface.fill((76, 76, 225))
turn = True

import threading 

def create_thread(target):
    thread = threading.thread(target = target)
    thread.daemon = True 
    thread.start()

import socket

HOST = '127.0.0.1'
PORT = 5050
Connection_established = False
conn, addr = None, None


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

draw_grid(surface)

#  Main loop
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        # Waits for mouse to be clicked
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            mouse_positionX = event.pos[0]
            mouse_positionY = event.pos[1]

            clicked_row = int(mouse_positionY // GRID_SIZE)
            clicked_col = int(mouse_positionX // GRID_SIZE)
            
            # Checks with is_available function if the spot can be choosed
            if(is_available(clicked_row, clicked_col)):
                play(clicked_row, clicked_col, 'X')

                # After a player's move cheks if there is a winner
                if (check_win()):
                    print("\nPRESS R TO RESTART THE GAME\n\n")
                    gameover = True
                draw_play()
                if not gameover:
                    random_number()
            
            else:
                print("This spot is taken, try in another one\n")

        # Waits for key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                gameover = False

    # updates the frames of the game 
    pygame.display.update() 
