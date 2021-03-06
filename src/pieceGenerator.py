import random
from config import *
from piece import *

class PieceGenerator:
    def __init__(self):
        S_SHAPE_TEMPLATE = [['.....',
                             '.....',
                             '..OO.',
                             '.OO..',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..OO.',
                             '...O.',
                             '.....']]

        Z_SHAPE_TEMPLATE = [['.....',
                             '.....',
                             '.OO..',
                             '..OO.',
                             '.....'],
                            ['.....',
                             '..O..',
                             '.OO..',
                             '.O...',
                             '.....']]

        I_SHAPE_TEMPLATE = [['..O..',
                             '..O..',
                             '..O..',
                             '..O..',
                             '.....'],
                            ['.....',
                             '.....',
                             'OOOO.',
                             '.....',
                             '.....']]

        O_SHAPE_TEMPLATE = [['.....',
                             '.....',
                             '.OO..',
                             '.OO..',
                             '.....']]

        J_SHAPE_TEMPLATE = [['.....',
                             '.O...',
                             '.OOO.',
                             '.....',
                             '.....'],
                            ['.....',
                             '..OO.',
                             '..O..',
                             '..O..',
                             '.....'],
                            ['.....',
                             '.....',
                             '.OOO.',
                             '...O.',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..O..',
                             '.OO..',
                             '.....']]

        L_SHAPE_TEMPLATE = [['.....',
                             '...O.',
                             '.OOO.',
                             '.....',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..O..',
                             '..OO.',
                             '.....'],
                            ['.....',
                             '.....',
                             '.OOO.',
                             '.O...',
                             '.....'],
                            ['.....',
                             '.OO..',
                             '..O..',
                             '..O..',
                             '.....']]

        T_SHAPE_TEMPLATE = [['.....',
                             '..O..',
                             '.OOO.',
                             '.....',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..OO.',
                             '..O..',
                             '.....'],
                            ['.....',
                             '.....',
                             '.OOO.',
                             '..O..',
                             '.....'],
                            ['.....',
                             '..O..',
                             '.OO..',
                             '..O..',
                             '.....']]

        self.pieces = {
                'S': S_SHAPE_TEMPLATE,
                'Z': Z_SHAPE_TEMPLATE,
                'J': J_SHAPE_TEMPLATE,
                'L': L_SHAPE_TEMPLATE,
                'I': I_SHAPE_TEMPLATE,
                'O': O_SHAPE_TEMPLATE,
                'T': T_SHAPE_TEMPLATE
            }

        # offsets given as (x_left, x_right, y_top)
        self.offsets = {
                'S': [(1, 1, 2), (2, 1, 1)],
                'Z': [(1, 1, 2), (1, 2, 1)],
                'I': [(2, 2 ,0), (0, 1, 2)],
                'O': [(1, 2, 2)],
                'J': [(1, 1, 1), (2, 1, 1), (1, 1, 2), (1, 2, 1)],
                'L': [(1, 1, 1), (2, 1, 1), (1, 1, 2), (1, 2, 1)],
                'T': [(1, 1, 1), (2, 1, 1), (1, 1, 2), (1, 2, 1)]
            }

    # generate a specific piece
    def genPiece(self, shape, rotation):
        color = random.randint(0, len(COLORS) - 1)
        templates = self.pieces[shape]
        offsets = self.offsets[shape]
        return Piece(shape, rotation, color, templates, offsets)

    # generate random piece given a shape
    def genRandPieceFromShape(self, shape):
        rotation = random.choice(range(len(self.pieces[shape])))
        return self.genPiece(shape, rotation)

    # generate random piece
    def genRandPiece(self):
        shape = random.choice(list(self.pieces.keys()))
        rotation = random.choice(range(len(self.pieces[shape])))
        return self.genPiece(shape, rotation)
