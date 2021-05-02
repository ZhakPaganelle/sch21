import sys
import random
import pygame as pg
from pygame.locals import *
from numpy import array_split


FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
SPEED = 1

BACKGROUND = (100, 100, 100)
CELL_COLOR = (200, 200, 200)
SHOWED_CELL = (150, 200, 200)
PICKED_CELL = (200, 150, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pg.font.init()
FONT = pg.font.SysFont('arial', 36)


def main():
    global FPSCLOCK, DISPLAYSURF
    
    pg.init()
    FPSCLOCK = pg.time.Clock()
    DISPLAYSURF = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    new_game(DISPLAYSURF)


def new_game(surface):
    pg.display.set_caption('Сука')
    surface.fill(BACKGROUND)
    
    board, number_of_targets = get_random_board(7)

    board = make_class(board)

    targets = get_targets(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].draw(surface)
            pg.display.update()

    random.shuffle(board)
    blit_targets(surface, board)

    pg.event.clear(MOUSEBUTTONUP)
    run_game(surface, board, targets)


def run_game(surface, board, targets):
    while True:
        pg.display.update()
        
        if not targets:
            pg.display.set_caption('Заебись')
            show_victory(surface)
            FPSCLOCK.tick(1)
            FPSCLOCK.tick(1)
            new_game(surface)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == KEYUP and event.key == K_r:
                new_game(surface)
            elif event.type == pg.MOUSEBUTTONUP:
                if cell := check_click(surface, board, event.pos):
                    targets.remove(cell)
                    cell.is_active = 0


def check_for_quit():
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            terminate()


def terminate():
    pg.quit()
    sys.exit()


def get_random_board(cols, rows=None):
    if not rows:
        rows = cols

    board = [0 for i in range(cols*rows)]
    number_of_targets = random.randint(3, len(board)//7)
    for i in range(number_of_targets):
        board[i] = 1

    random.shuffle(board)
    board = array_split(board, cols)

    return board, number_of_targets


def make_class(board):
    cols = len(board[0])
    rows = len(board)

    cell_height = WINDOW_HEIGHT // rows
    cell_width = WINDOW_WIDTH // cols

    class_board = [[None for i in range(cols)] for j in range(rows)]

    for i in range(len(board)):
        for j in range(len(board[i])):
            class_board[i][j] = Cell(cell_width*i, cell_height*j, cell_width, cell_height, board[i][j], board[i][j])

    return class_board


def get_targets(board):
    targets = []
    for row in board:
        for cell in row:
            if cell.is_target:
                targets.append(cell)

    return targets


def blit_targets(surface, board):
    for row in board:
        for cell in row:
            if cell.is_target:
                cell.draw(surface, SHOWED_CELL)
                pg.display.update()
                check_for_quit()
                FPSCLOCK.tick(1)

                cell.draw(surface)
                pg.display.update()
                check_for_quit()
                FPSCLOCK.tick(2)


def check_click(surface, board, coords):
    for row in board:
        for cell in row:
            if cell.check_hit(coords):
                color = RED
                if cell.is_target:
                    color = GREEN

                cell.draw(surface, color)
                pg.display.update()

                return cell if cell.is_active else False


def show_victory(surface):
    surface.fill(WHITE)
    victory_text = FONT.render('Красава', True, BLACK)
    surface.blit(victory_text, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    pg.display.update()


class Cell:
    def __init__(self, coord_x, coord_y, width, height, is_target, is_active):
        self.x = coord_x
        self.y = coord_y
        self.height = height
        self.width = width
        self.is_target = is_target
        self.is_active = is_active

    def draw(self, surface, color=CELL_COLOR):
        figure = Rect((self.x+2, self.y+2, self.width-4, self.height-4))
        pg.draw.rect(surface, color, figure)

    def check_hit(self, coords):
        mouse_x, mouse_y = coords
        if self.x + 2 <= mouse_x <= self.x + self.width - 4 and self.y + 2 <= mouse_y <= self.y + self.height - 4:
            return True
        return False


if __name__ == '__main__':
    main()
