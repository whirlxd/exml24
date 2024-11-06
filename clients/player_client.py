import socketio
import requests
import time
import os

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


@sio.on('reset')
def reset():
    print("Resetting")
    os._exit(0)

@sio.on('board')
def handle_server_message(data):
    if not connected:
        print("Not connected yet,ignoring message")
        return
    board,points = data
    process(board,points)
def process(board, points):
    from collections import deque

    def find_pacman(board):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == 'p':
                    return (i, j)
        return None

    def find_ghosts(board):
        ghosts = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell in ['a', 'b', 'c', 'd']:
                    ghosts.append((i, j))
        return ghosts

    def is_safe(x, y, ghosts, safe_distance=3):
        for gx, gy in ghosts:
            if abs(x - gx) + abs(y - gy) <= safe_distance:
                return False
        return True

    def find_nearest_safe_food(board, start, ghosts):
        rows, cols = len(board), len(board[0])
        visited = set()
        queue = deque([(start, [])])

        while queue:
            (x, y), path = queue.popleft()
            if (board[x][y] == '.') and is_safe(x, y, ghosts):
                return path
            for dx, dy, move in [(-1, 0, 0), (1, 0, 1), (0, -1, 2), (0, 1, 3)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and
                        board[nx][ny] != '#' and (nx, ny) not in visited):
                    if is_safe(nx, ny, ghosts):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [move]))
        return []

    pacman_pos = find_pacman(board)
    ghosts = find_ghosts(board)

    path = find_nearest_safe_food(board, pacman_pos, ghosts)

    move = [0, 0, 0, 0]
    if path:
        next_move = path[0]
        move[next_move] = 1
    else:
        # No safe path to food; try to move away from nearest ghost
        from random import choice
        possible_moves = []
        for dx, dy, move_dir in [(-1, 0, 0), (1, 0, 1), (0, -1, 2), (0, 1, 3)]:
            nx, ny = pacman_pos[0] + dx, pacman_pos[1] + dy
            if (0 <= nx < len(board) and 0 <= ny < len(board[0]) and
                    board[nx][ny] != '#' and is_safe(nx, ny, ghosts)):
                possible_moves.append(move_dir)
        if possible_moves:
            selected_move = choice(possible_moves)
            move[selected_move] = 1
        else:
            # Stay in place if no safe moves
            move[0] = 1  # Default to up

    send_move(move)
    import numpy as np
    from collections import deque

    def find_pacman(board):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == 'p':
                    return (i, j)
        return None

    def find_nearest_food(board, start):
        rows, cols = len(board), len(board[0])
        visited = set()
        queue = deque([(start, [])])

        while queue:
            (x, y), path = queue.popleft()
            if board[x][y] == '.':
                return path

            for dx, dy, move in [(-1, 0, 0), (1, 0, 1), (0, -1, 2), (0, 1, 3)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and
                        board[nx][ny] != '#' and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [move]))
        return []

    pacman_position = find_pacman(board)
    path_to_food = find_nearest_food(board, pacman_position)

    move = [0, 0, 0, 0]
    if path_to_food:
        next_move = path_to_food[0]
        move[next_move] = 1
    else:
        # Default action if no path found
        move[0] = 1  # Move up

    send_move(move)

def send_move(move):
   url = f"{link}/move/player"
   payload = move
   headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
   response = requests.post(url, json=payload, headers=headers)
   print(response.text)


sio.connect(link,headers={'Authorization': f'Bearer {token}','Name':name})

sio.wait()

