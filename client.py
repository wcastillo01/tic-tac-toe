import pygame, os
from manager import *

pygame.init()

# ----- WINDOW INITIAL POSITION -----
os.environ['SDL_VIDEO_WINDOW_POS'] = '900,125'

# ----- VARIABLES -----

surface = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("tic-tac-toe-CLIENT")
active = True
gameover = False
current_player = "O"
surface.fill((76, 76, 225))
turn = False
playing = 'True'

# ---- FUNCTIONS ----

import threading 

def create_thread(target):
    thread = threading.Thread(target = target)
    thread.daemon = True 
    thread.start()

import socket

HOST = '127.0.0.1'
PORT = 6667
conn, addr = None, None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except:
    print("\n*** NO SERVER TO CONNECT TO ***\n\n")

def recieve_data():
    global turn
    while True:
        data = client.recv(1024).decode() # receive data from the server, it is a blocking method
        data = data.split('-') # the format of the data after splitting is: ['x', 'y', 'yourturn', 'playing']
        clicked_row, clicked_col = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            is_board_full()
        if board[clicked_row][clicked_col]==0 :
            play(clicked_row,clicked_col, 'X')


create_thread(recieve_data)

draw_grid(surface)

#  Main loop
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        # Waits for mouse to be clicked
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:

            clicked_col = int(event.pos[0] // GRID_SIZE)
            clicked_row = int(event.pos[1] // GRID_SIZE)            

            if turn:
                if(is_available(clicked_row, clicked_col)):
                    play(clicked_row, clicked_col, 'O')

                    # After a player's move cheks if there is a winner
                    if (check_win()):
                        print("\nPRESS R TO RESTART THE GAME\n\n")
                        gameover = True
                    send_data = '{}-{}-{}-{}'.format(clicked_row, clicked_col, 'yourturn', playing).encode()
                    client.send(send_data)
                    turn = False
                        # switch_player()


        # Waits for key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                gameover = False

    # updates the frames of the game 
    pygame.display.update() 
