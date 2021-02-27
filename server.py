import pygame, os
from manager import *

pygame.init()

# ----- WINDOW INITIAL POSITION -----
os.environ['SDL_VIDEO_WINDOW_POS'] = '225,125'

# ----- VARIABLES -----

surface = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("tic-tac-toe-SERVER")
active = True
gameover = False
current_player = "X"
surface.fill((76, 76, 225))
turn = True
playing = 'True'

import threading 

def create_thread(target):
    thread = threading.Thread(target = target)
    thread.daemon = True 
    thread.start()

import socket

HOST = '127.0.0.1'
PORT = 6667
Connection_established = False
conn, addr = None, None


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

def recieve_data():
    global turn 
    connected = True
    while connected:
        data = conn.recv(1024).decode() # receive data from the client, it is a blocking method
        data = data.split('-') # the format of the data after splitting is: ['x', 'y', 'yourturn', 'playing']
        clicked_row, clicked_col = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            is_board_full()
        if  board[clicked_row][clicked_col] == 0:
            play(clicked_row,clicked_col, 'O')
        

# ----- Waits for a client to connect -----
def waiting_connection():
    global connection_established, conn, addr
    conn, addr = server.accept()
    connection_established = True
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        recieve_data()
    except:
        print("\n***HOST OR CLIENT DISCONNECTED***\n\n")
    finally: 
        connection_established = False
        conn.close()

create_thread(waiting_connection)
draw_grid(surface)

#  Main loop
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            connection_established = False
        # Waits for mouse to be clicked
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:

            clicked_row = int(event.pos[1] // GRID_SIZE)
            clicked_col = int(event.pos[0] // GRID_SIZE)

            if turn:
                if(is_available(clicked_row, clicked_col)):
                    play(clicked_row, clicked_col, 'X')

                    # After a player's move cheks if there is a winner
                 
                    if not gameover:
                        send_data = '{}-{}-{}-{}'.format(clicked_row, clicked_col, 'yourturn', playing).encode()
                        conn.send(send_data)
                        turn = False
                    if (check_win()):
                        print("\nPRESS R TO RESTART THE GAME\n\n")
                        gameover = True
        # Waits for key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                gameover = False

    # updates the frames of the game 
    pygame.display.update() 
