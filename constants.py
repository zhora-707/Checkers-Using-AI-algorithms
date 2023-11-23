import pygame

WIDTH, HEIGHT = 800, 800
INFO_WIDTH = 300
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# notation
FIELD_NUMBERS = [
    [None, 1,   None, 2,    None, 3,    None, 4],
    [5, None,   6, None,    7, None,    8, None],
    [None, 9,   None, 10,   None, 11,   None, 12],
    [13, None,  14, None,   15, None,   16, None],
    [None, 17,  None, 18,   None, 19,   None, 20],
    [21, None,  22, None,   23, None,   24, None],
    [None, 25,  None, 26,   None, 27,   None, 28],
    [29, None,  30, None,   31, None,   32, None]
]

# edge validation
EDGE_VALUES = [
    [None, 3,       None, 3,        None, 3,        None, 3],
    [1, None,       2, None,        2, None,        2, None],
    [None, 2,       None, 3,        None, 3,        None, 1],
    [1, None,       3, None,        3, None,        2, None],
    [None, 2,       None, 3,        None, 3,        None, 1],
    [1, None,       3, None,        3, None,        2, None],
    [None, 2,       None, 2,        None, 2,        None, 1],
    [1, None,       1, None,        1, None,        1, None],
]

# 3-way validation
OPENING_VALUES = EDGE_VALUES

MID_GAME_VALUES = [
    [None, 4,       None, 4,        None, 4,        None, 4],
    [1.5, None,     1.8, None,      1.8, None,      1.75, None],
    [None, 1.65,    None, 1.7,      None, 1.7,      None, 1.3],
    [1.1, None,     1.55, None,     1.55, None,     1.5, None],
    [None, 1.35,    None, 1.45,     None, 1.45,     None, 1],
    [0.7, None,     1.2, None,      1.2, None,      1.1, None],
    [None, 0.9,     None, 0.9,      None, 0.9,      None, 0.7],
    [0.5, None,     0.5, None,      0.5, None,      0.5, None],
]

ENDGAME_VALUES = [
    [None, 4,       None, 4,        None, 4,        None, 4],
    [2.6, None,     3, None,        3, None,        2.8, None],
    [None, 1.65,    None, 2,        None, 2,        None, 1.8],
    [1.3, None,     1.45, None,     1.45, None,     1.3, None],
    [None, 0.8,     None, 0.9,      None, 0.9,      None, 0.75],
    [0.35, None,    0.45, None,     0.45, None,     0.45, None],
    [None, 0.2,     None, 0.2,      None, 0.2,      None, 0.15],
    [0.1, None,     0.1, None,      0.1, None,      0.1, None]
]

# king validation
KING_VALUES = [
    [None, 3,   None, 3.5,  None, 3,     None, 3],
    [3, None,   3.5, None,  3.5, None,   3, None],
    [None, 3.5, None, 4,    None, 4,    None, 3],
    [3.5, None, 4, None,    4, None,    3.5, None],
    [None, 3.5, None, 4,    None, 4,    None, 3.5],
    [3, None,   4, None,    4, None,    3.5, None],
    [None, 3,   None, 3.5,  None, 3.5,  None, 3],
    [3, None,   3, None,    3.5, None,  3, None],
]

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# fonts
pygame.font.init()
NUMBER_FONT = pygame.font.SysFont('Times New Roman', 24)
NOTATION_FONT = pygame.font.SysFont('Times New Roman', 16)

DRAW = 'draw'
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
