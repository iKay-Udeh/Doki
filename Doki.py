import pygame
import sys
import numpy as np
from pygame.locals import *



# colors        r    g     b
BGCOLOR   =   ( 0,   50,  135)
LINECOLOR =   ( 0,   0,     0)
HLTCOLOR  =   (25,   10,  125)
PONECOLOR =   (125,  10,   40)
PTWOCOLOR =   (100,  100,  30)
WHITE     =   (255,  255, 255)
RED       =   (255,    0,   0)

# dimensions
WINDOWWIDTH  = 500
WINDOWHEIGHT = 600
BOARDWIDTH   =  5
BOARDHEIGHT  =  6
BOXSIZE      = 100
LINEWIDTH    =  5
FPS          = 60

# initialize the gameboard

game_board = np.zeros((BOARDHEIGHT, BOARDWIDTH))
boxx, boxy = 0, 0

def main():
    global window

    # initialize pygame
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Doki!')

    game_pieces = 24   # number of both player one and player two board pieces
    player = 1
    game_over = False
    move_start = False
    col, row = 0, 0
    mouseX, mouseY = 0, 0
    FPSCLOCK = pygame.time.Clock()


    while True:   # game loop
        mouse_clicked = False
        window.fill(BGCOLOR)
        draw_lines()
        draw_game_pieces()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEMOTION and not game_over:
                mouseX, mouseY = event.pos

            if event.type == MOUSEBUTTONUP and not game_over:
                mouseX, mouseY = event.pos
                mouse_clicked = True

            col = int(mouseX // 100)
            row = int(mouseY // 100)

            draw_highlight(col, row)
            pygame.display.update()
            
            if mouse_clicked:
                if game_pieces != 0:
                    if check_available(col, row):
                        if player == 1:
                            if not check_three(col, row, player):
                                mark_board(col, row, player)
                                game_pieces -= 1
                                player = 2
                        elif player == 2:
                            if not check_three(col, row, player):
                                mark_board(col, row, player)
                                game_pieces -= 1
                                player = 1
                        draw_game_pieces()
                else:
                    move_start = True

                if move_start:
                    if game_board[row][col] == player:
                        highlight_selected(col, row)
                        pygame.display.update()
                        if player == 1:
                            move_piece(col, row, player)
                            if check_three(boxx, boxy, player):
                                highlight_opponent(player)
                                pygame.display.update()
                                remove_piece(player)
                            if check_win(player):
                                draw_win_animation(player)
                                game_over = True
                            player = 2

                        elif player == 2:
                            move_piece(col, row, player)
                            if check_three(boxx, boxy, player):
                                highlight_opponent(player)
                                pygame.display.update()
                                remove_piece(player)
                            if check_win(player):
                                draw_win_animation(player)
                                game_over = True
                            player = 1

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_lines():
    for col in range (BOARDWIDTH):
        pygame.draw.line(window, LINECOLOR, (0, col * 100 + 100), (WINDOWWIDTH, col * 100 + 100), LINEWIDTH)
    for row in range (BOARDHEIGHT):
        pygame.draw.line(window, LINECOLOR, (row * 100 + 100, 0), (row * 100 + 100, WINDOWHEIGHT), LINEWIDTH)

def draw_game_pieces():
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if game_board[row][col] == 1:
                color = PONECOLOR
                pygame.draw.circle(window, color, (col * BOXSIZE + (BOXSIZE / 2), row * BOXSIZE + (BOXSIZE / 2)),
                                   (BOXSIZE * 0.5) - 5)
                pygame.draw.circle(window, color, (col * BOXSIZE + (BOXSIZE / 2), row * BOXSIZE + (BOXSIZE / 2)),
                                   (BOXSIZE * 0.25) - 5)
            if game_board[row][col] == 2:
                color = PTWOCOLOR
                pygame.draw.circle(window, color, (col * BOXSIZE + (BOXSIZE / 2), row * BOXSIZE + (BOXSIZE / 2)),
                                   (BOXSIZE * 0.5) - 5)
                pygame.draw.circle(window, color, (col * BOXSIZE + (BOXSIZE / 2), row * BOXSIZE + (BOXSIZE / 2)),
                                   (BOXSIZE * 0.25) - 5)

def draw_highlight(col, row):
    pygame.draw.rect(window, HLTCOLOR, (col * 100, row * 100, BOXSIZE, BOXSIZE),5)

def check_available(col, row):
    if game_board[row][col] == 0:
        return True
    return False

def check_three(col, row, player):
    # check for three horizontal game pieces
    try:
        if game_board[row][col + 1] == player and game_board[row][col + 2] == player and game_board[row][col + 3] == player:
            return False # this returns false if it finds 4 game pieces as this is against the rule of the game
    except:
        pass

    if col != 0 and col != 4:
        if game_board[row][col + 1] == player and game_board[row][col - 1] == player:
            return True
        try:
            # this tries to see if the column plus 2 more equals to the current player
            # so as not to return an index out of range error
            if game_board[row][col + 1] == player and game_board[row][col + 2] == player:
                return True
        except:
            pass
        try:
            if game_board[row][col - 1] == player and game_board[row][col - 2] == player:
                return True
        except:
            pass

    if col == 0:
        if game_board[row][col + 1] == player and game_board[row][col + 2] == player:
            return True

    if col == 4:
        if game_board[row][col - 1] == player and game_board[row][col - 2] == player:
            return True

    # check for three vertical game pieces
    try:
        if game_board[row + 1][col] == player and game_board[row + 2][col] == player and game_board[row + 3][col] == player:
            return False
    except:
        pass

    if row != 0 and row != 5:
        if game_board[row + 1][col] == player and game_board[row - 1][col] == player:
            return True
        try:
            if game_board[row + 1][col] == player and game_board[row + 2][col] == player:
                return True
        except:
            pass
        try:
           if game_board[row - 1][col] == player and game_board[row - 2][col] == player:
               return True
        except:
            pass

    if row == 0:
        if game_board[row + 1][col] == player and game_board[row + 2][col] == player:
            return True

    if row == 5:
        if game_board[row - 1][col] == player and game_board[row - 2][col] == player:
            return True

    return False

def mark_board(col, row, player):
    game_board[row][col] = player

def highlight_selected(col, row):
    pygame.draw.rect(window, RED, (col * 100, row * 100, BOXSIZE, BOXSIZE), 5)

def move_piece(col, row, player):
    global boxx, boxy
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row = int(mouseY // 100)
                clicked_col = int(mouseX // 100)
                if row != 0 and row != 5:
                    if clicked_row == (row + 1):
                        if game_board[row + 1][col] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                    elif clicked_row == (row - 1):
                        if game_board[row - 1][col] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                if row == 0:
                    if clicked_row == (row + 1):
                        if game_board[row + 1][col] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                if row == 5:
                    if clicked_row == (row - 1):
                        if game_board[row - 1][col] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                if col != 0 and col != 4:
                    if clicked_col == (col + 1):
                        if game_board[row][col + 1] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                    if clicked_col == (col - 1):
                        if game_board[row][col - 1] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                if col == 0:
                    if clicked_col == (col + 1):
                        if game_board[row][col + 1] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                if col == 4:
                    if clicked_col == (col - 1):
                        if game_board[row][col - 1] == 0:
                            game_board[row][col] = 0
                            game_board[clicked_row][clicked_col] = player
                            selected = True
                boxx, boxy = clicked_col, clicked_row

    window.fill(BGCOLOR)
    draw_lines()
    draw_game_pieces()
    pygame.display.update()

def highlight_opponent(player):
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if game_board[row][col] != player and game_board[row][col] != 0:
                highlight_selected(col, row)

def remove_piece(player):
    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row = int(mouseY // 100)
                clicked_col = int(mouseX // 100)
                if game_board[clicked_row][clicked_col] != player and game_board[clicked_row][clicked_col] != 0:
                    game_board[clicked_row][clicked_col] = 0
                    selected = True

    window.fill(BGCOLOR)
    draw_lines()
    draw_game_pieces()
    pygame.display.update()

def check_win(player):
    count = 0
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if game_board[row][col] != player and game_board[row][col] != 0:
                count += 1
    if count < 3:
        return True
    return False

def draw_win_animation(player):
    font_init = pygame.font.SysFont('candara', 60, True)
    font_render = font_init.render(f'Player {player} Wins!', True, WHITE)
    font_rect = font_render.get_rect()
    font_rect.center = ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))

    window.blit(font_render, font_rect)
    pygame.display.update()

if __name__ == '__main__':
    main()