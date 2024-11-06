import socketio
import requests
import os
import time 

link = "http://127.0.0.1:5000"

token = input('Enter your token: ')
name = input('Enter your name: ')


sio = socketio.Client()
connected = False
@sio.event
def connect():
    global connected
    connected = True
    print("Connected to server")
    sio.emit('request')

@sio.event
def disconnect():
    global connected
    connected = False
    print("Disconnected from server")
    os._exit(0)

@sio.event
def reconnect():
    global connected
    connected = True
    print("Reconnected to server")

@sio.on('board')
def handle_server_message(data):
   
    if not connected:
        print("Not connected yet,ignoring message")
        return
    board,points = data
    process(board,points)

@sio.on('reset')
def reset():

    print("Resetting")
    os._exit(0)   

def process(board, points):
    import numpy as np
    from collections import deque

    def find_ghost_positions(board):
        ghosts = {}
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell in 'abcd':
                    ghosts[cell] = (i, j)
        return ghosts

    def find_pacman(board):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == 'p':
                    return (i, j)
        return None

    def get_move_direction(start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if abs(dx) > abs(dy):
            return 0 if dx < 0 else 1  # Up or Down
        else:
            return 2 if dy < 0 else 3  # Left or Right

    pacman_position = find_pacman(board)
    ghost_positions = find_ghost_positions(board)

    ghost_moves = []
    for ghost_id in ['a', 'b', 'c', 'd']:
        move = [0, 0, 0, 0]
        ghost_pos = ghost_positions.get(ghost_id)
        if ghost_pos:
            direction = get_move_direction(ghost_pos, pacman_position)
            move[direction] = 1
        else:
            # Default action if ghost position not found
            move[0] = 1  # Move up
        ghost_moves.append(move)

    send_move(ghost_moves)

def send_move(move):
   url = f"{link}/move/ghost"
   payload = move
   headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
   response = requests.post(url, json=payload, headers=headers)
   print(response.text)


sio.connect(link,headers={'Authorization': f'Bearer {token}','Name':name})

sio.wait()

