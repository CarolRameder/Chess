import pygame as pg
import random
from Move import Move
from State import GameState

"""
Initialisation of global variables for the games
"""
wid = height = 512
dim = 8
field_sz = height // dim
img = {}
MAX_FPS = 30


def load_graphics():
    """
    Method for loading the graphical representation of the pieces
    """
    pieces = ['bp', 'br', 'bn', 'bb', 'bk', 'bq', 'wp', 'wr', 'wn', 'wb', 'wk', 'wq']
    for p in pieces:
        img[p] = pg.transform.scale(pg.image.load("images/" + p + ".png"), (field_sz, field_sz))


def draw_game_state(screen, gs):
    """
    Method for representing graphically a game state
    :parameter screen: display size
    :parameter gs: current game state
    """
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    """
    Method for drawing the board
    :parameter screen: display size
    """
    colors = [pg.Color("Cornsilk"), pg.Color("SaddleBrown")]
    for r in range(dim):
        for c in range(dim):
            color = colors[((r + c) % 2)]#you cand determine a square color by its location
            pg.draw.rect(screen, color, pg.Rect(c * field_sz, r * field_sz, field_sz, field_sz))


def draw_pieces(screen, board):
    """
    Method for drawing the pieces
    :parameter screen: display size
    :parameter board: board state
    """
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != '--':
                screen.blit(img[piece], pg.Rect(c * field_sz, r * field_sz, field_sz, field_sz))


def main():
    # Initialise PyGame context
    pg.init()
    screen = pg.display.set_mode((wid, height))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    load_graphics()

    # Initialise variables for the game engine
    click2 = []
    current = GameState()
    evn = ()
    valid_mov = current.get_valid_moves()
    flag = False

    # Select player type
    player_type = "a"
    while player_type not in ('c', 'p'):
        player_type = input("Type p-person or c-computer for choosing the opponent:")

    comp_turn = False  # computer plays black pieces
    run=True
    while run:  # playing sequence
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                #handling coordinates and clicks
                loc = pg.mouse.get_pos()
                col = loc[0] // field_sz
                lin = loc[1] // field_sz
                evn = (lin, col)
                click2.append(evn)

                if len(click2) == 2:  # selection was made
                    move = Move(click2[0], click2[1], current.board)  # compute move
                    for i in range(len(valid_mov)):
                        if move == valid_mov[i]:
                            current.make_move(valid_mov[i], check_valid=False)
                            flag = True
                            evn = ()
                            click2 = []
                            comp_turn = not comp_turn
                            if player_type == 'p':
                                comp_turn = not comp_turn
                    if not flag:
                        click2 = [evn]

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    current.undo_move()
                    flag = True
        if flag:
            valid_mov = current.get_valid_moves()
            flag = False

        #pygame front end actualisation
        draw_game_state(screen, current)
        clock.tick(MAX_FPS)
        pg.display.flip()

        if comp_turn:
            if len(valid_mov) == 0:
                break
            #make a random move
            j = random.randint(0, len(valid_mov)-1)
            cmove = valid_mov[j]
            current.make_move(cmove, check_valid=False)

            valid_mov = current.get_valid_moves()
            comp_turn = not comp_turn

            # pygame front end actualisation
            draw_game_state(screen, current)
            clock.tick(MAX_FPS)
            pg.display.flip()


if __name__ == "__main__":
    main()
