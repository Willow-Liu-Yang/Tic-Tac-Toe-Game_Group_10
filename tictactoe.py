

import pygame
import sys


pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


size = 300
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption('Tic Tac Toe')


board = [[None]*3, [None]*3, [None]*3]
current_player = 'X'


def draw_grid():
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (100, 0), (100, 300), 2)
    pygame.draw.line(screen, BLACK, (200, 0), (200, 300), 2)
    pygame.draw.line(screen, BLACK, (0, 100), (300, 100), 2)
    pygame.draw.line(screen, BLACK, (0, 200), (300, 200), 2)


def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * 100 + 20, row * 100 + 20), (col * 100 + 80, row * 100 + 80), 2)
                pygame.draw.line(screen, RED, (col * 100 + 80, row * 100 + 20), (col * 100 + 20, row * 100 + 80), 2)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * 100 + 50, row * 100 + 50), 40, 2)


def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] is not None:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] is not None:
        return board[0][2]
    return None


running = True
while running:
    draw_grid()
    draw_marks()
    winner = check_winner()

    if winner:
        print(f'{winner} wins!')
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not winner:
            x, y = event.pos
            row, col = y // 100, x // 100
            if board[row][col] is None:
                board[row][col] = current_player
                current_player = 'O' if current_player == 'X' else 'X'

    pygame.display.flip()

pygame.quit()
sys.exit()
