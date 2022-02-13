import random
import csv
import pygame
import sys
from time import sleep

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


class StateError(Exception):
    pass

class SetupKeyError(Exception):
    pass

def open_csv_return_array(location):
    with open(location, 'r') as f:
        csv_reader = csv.reader(f)        
        return [[int(i) for i in j] for j in list(csv_reader)]

class Cell():
    def __init__(self, index, state = None):
        self.index = index
        if state == None:
            self.state = random.randint(0,1)
        elif state == 1 or state == 0:
            self.state = state
        else:
            raise StateError(f'Invalid state. State must be 0 or 1, {state} submitted')

    def check_next_state(self, board=None):
        if board != None:
            self.board = board
        self.next_state = None
        self.counter = 0

        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                iindex = self.index[0] - (i - 1)
                jindex = self.index[1] - (j - 1)
                if iindex < 0 or iindex > len(self.board.board) - 1 or jindex < 0 or jindex > len(self.board.board[i]) - 1:
                    continue
                self.counter += self.board.board[iindex][jindex].state

        if self.state and (self.counter < 2 or self.counter > 3):
            #was live, over or under population
            self.next_state = 0
        elif self.state:
            # was live, perfect
            self.next_state = 1
        elif self.state == 0 and self.counter == 3:
            #was dead, perfect, alive
            self.next_state = 1
        else:
            self.next_state = 0
    
    def next_generation(self):
        self.state = self.next_state

    def __repr__(self):
        return f'{self.state}'

    def __str__(self):
        return f'{self.state}'

class Board():
    def __init__(self, **kwargs):
        self.sent_board = False
        if 'location' in kwargs:
            #opens file and returns list of list of cells
            list_of_cells = open_csv_return_array(kwargs['location'])
            self.board = []
            for iindex, i in enumerate(list_of_cells):
                self.board.append([])
                for jindex, j in enumerate(i):
                    try:
                        self.board[iindex].append(Cell((iindex,jindex), j))
                    except StateError:
                        print(f'Cell index ({iindex},{jindex} state was attempted to be set to {j}. Now set to 0')
                        self.board[iindex].append(Cell((iindex,jindex), 0))
        elif 'width' in kwargs and 'height' in kwargs:
            self.board = [[Cell((i,j)) for j in range(kwargs['width'])] for i in range(kwargs['height'])]
        else:
            raise SetupKeyError('No valid **kwargs entered')

    def __repr__(self):
        return f'Board Sized {len(self.board)}hx{len(self.board[0])}w'

    def check_for_next_generation(self):
        for row in self.board:
            for cell in row:
                if self.sent_board:
                    cell.check_next_state()
                else:
                    cell.check_next_state(self)
        self.sent_board = True

    def next_generation(self):
        for row in self.board:
            for cell in row:
                cell.next_generation()

def draw_grid(surface, board, gw, gh):
    for rowindex, row in enumerate(board.board):
        for colindex, cell in enumerate(row):
            r = pygame.Rect((gw * colindex, gh * rowindex), (gw, gh))
            if cell.state == 1:
                pygame.draw.rect(surface, (255, 255, 255), r)
            else:
                pygame.draw.rect(surface, (0, 0, 0), r)


def main(rows, columns, board):
    GRID_WIDTH = SCREEN_WIDTH / columns
    GRID_HEIGHT = SCREEN_HEIGHT / rows

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    myfont = pygame.font.SysFont('Monospace', 16)

    counter = 0

    input()

    while True:
        clock.tick(100)
        draw_grid(surface, board, GRID_WIDTH, GRID_HEIGHT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(surface, (0,0))
        text = myfont.render(f'Generation {counter}', 1, (255, 0, 0))
        screen.blit(text, (5,10))
        pygame.display.update()
        board.check_for_next_generation()
        #sleep(0.2)
        board.next_generation()
        counter += 1


if '__main__' == __name__:
    selection = input('Enter L for csv and S for size')
    if selection.upper() == 'L':
        x = Board(location = input('Enter Location: '))
    elif selection.upper() == 'S':
        x = Board(width = int(input('Enter width: ')), height = int(input('Enter height: ')))
    main(len(x.board), len(x.board[0]), x)
