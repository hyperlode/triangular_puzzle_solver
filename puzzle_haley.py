import copy
import logging
import time
import datetime
from collections import defaultdict
import triangular_puzzle_solver

import triangular_grid
import triangular_pattern



# pieces, made up of small triangles.
# x = cell
# o = 0,0 cell
# . = 0,0 coordinate, not part of piece

# pieces numbered from least amount of orientations to most.


# oxx
# xxx
piece_0 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (1,0):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
}

#  
#  .xxx
#   xxx

piece_1 = {
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (0,3):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
} 

# . x
# xxxxx
piece_2 = {
    (0,2):triangular_grid.CELL_ON,
    (1,0):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
    (1,4):triangular_grid.CELL_ON,
} 

#  0xx
#    xxx
piece_3 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
    (1,4):triangular_grid.CELL_ON,
} 


#  .   xx
#   xxxx
piece_4 = {
    (0,4):triangular_grid.CELL_ON,
    (0,5):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
    (1,4):triangular_grid.CELL_ON,
} 

# oxxxxx
piece_5 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (0,3):triangular_grid.CELL_ON,
    (0,4):triangular_grid.CELL_ON,
    (0,5):triangular_grid.CELL_ON,
} 

# oxxx
#  xx
piece_6 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (0,3):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
} 

# ox
# xxxx
piece_7 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (1,0):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
} 

# o
# xxxxx
piece_8 = {
    (0,0):triangular_grid.CELL_ON,
    (1,0):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
    (1,4):triangular_grid.CELL_ON,
} 

# oxx
#  xxx
piece_9 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
} 

# . x
#  xxxxx
piece_10 = {
    (0,2):triangular_grid.CELL_ON,
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
    (1,4):triangular_grid.CELL_ON,
    (1,5):triangular_grid.CELL_ON,
} 

#  0xxx
#    xx
piece_11 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
    (0,2):triangular_grid.CELL_ON,
    (0,3):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
    (1,3):triangular_grid.CELL_ON,
} 



# sorted in ascending order of number of forms per piece
base_pieces_patterns = [
    piece_0,
    piece_1,
    piece_2,
    piece_3,
    piece_4,
    piece_5,
    piece_6,
    piece_7,
    piece_8,
    piece_9,
    piece_10,
    piece_11,
]

# define board where pieces have to fit into.
# bounding box
base_board = {(r,c):triangular_grid.CELL_OFF for r in range(8) for c in range(13)}
# border
base_board[(0,0)] = triangular_grid.CELL_NOGO
base_board[(0,1)] = triangular_grid.CELL_NOGO
base_board[(0,2)] = triangular_grid.CELL_NOGO
base_board[(0,3)] = triangular_grid.CELL_NOGO
base_board[(0,4)] = triangular_grid.CELL_NOGO
base_board[(0,5)] = triangular_grid.CELL_NOGO
base_board[(0,9)] = triangular_grid.CELL_NOGO
base_board[(0,10)] = triangular_grid.CELL_NOGO
base_board[(0,11)] = triangular_grid.CELL_NOGO
base_board[(0,12)] = triangular_grid.CELL_NOGO
base_board[(1,0)] = triangular_grid.CELL_NOGO
base_board[(1,10)] = triangular_grid.CELL_NOGO
base_board[(1,11)] = triangular_grid.CELL_NOGO
base_board[(1,12)] = triangular_grid.CELL_NOGO
base_board[(2,0)] = triangular_grid.CELL_NOGO
base_board[(3,0)] = triangular_grid.CELL_NOGO
base_board[(4,12)] = triangular_grid.CELL_NOGO
base_board[(5,12)] = triangular_grid.CELL_NOGO
base_board[(6,0)] = triangular_grid.CELL_NOGO
base_board[(6,1)] = triangular_grid.CELL_NOGO
base_board[(6,2)] = triangular_grid.CELL_NOGO
base_board[(6,12)] = triangular_grid.CELL_NOGO
base_board[(7,0)] = triangular_grid.CELL_NOGO
base_board[(7,1)] = triangular_grid.CELL_NOGO
base_board[(7,2)] = triangular_grid.CELL_NOGO
base_board[(7,3)] = triangular_grid.CELL_NOGO
base_board[(7,7)] = triangular_grid.CELL_NOGO
base_board[(7,8)] = triangular_grid.CELL_NOGO
base_board[(7,9)] = triangular_grid.CELL_NOGO
base_board[(7,10)] = triangular_grid.CELL_NOGO
base_board[(7,11)] = triangular_grid.CELL_NOGO
base_board[(7,12)] = triangular_grid.CELL_NOGO


# these are the hardcode prepared pieces ( use: prepare_puzzle_pieces() )
# generated cropped pieces and their configurations
GENERATE_PIECES = False
pieces_with_orientations = [
    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 0): 1, (1, 1): 1, (1, 2): 1}],

    [{(0, 1): 1, (0, 2): 1, (0, 3): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1},
    {(1, 1): 1, (1, 2): 1, (0, 2): 1, (2, 3): 1, (1, 3): 1, (1, 4): 1},
    {(2, 1): 1, (1, 1): 1, (1, 0): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1}],

    [{(0, 2): 1, (1, 0): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1},
    {(1, 0): 1, (2, 0): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1},
    {(1, 1): 1, (2, 3): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(1, 2): 1, (0, 4): 1, (0, 3): 1, (0, 2): 1, (0, 1): 1, (0, 0): 1},
    {(1, 3): 1, (0, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1},
    {(1, 2): 1, (0, 0): 1, (1, 0): 1, (1, 1): 1, (2, 1): 1, (2, 2): 1}],

    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1},
    {(2, 1): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1, (0, 4): 1},
    {(2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(1, 0): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (0, 3): 1, (0, 4): 1},
    {(2, 0): 1, (2, 1): 1, (1, 1): 1, (1, 0): 1, (0, 0): 1, (0, 1): 1},
    {(2, 3): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1, (1, 0): 1, (0, 0): 1}],

    [{(0, 4): 1, (0, 5): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1},
    {(1, 0): 1, (0, 0): 1, (3, 0): 1, (2, 0): 1, (2, 1): 1, (1, 1): 1},
    {(0, 2): 1, (0, 1): 1, (1, 5): 1, (1, 4): 1, (0, 4): 1, (0, 3): 1},
    {(1, 2): 1, (1, 1): 1, (0, 5): 1, (0, 4): 1, (0, 3): 1, (0, 2): 1},
    {(2, 2): 1, (3, 2): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1},
    {(1, 4): 1, (1, 5): 1, (0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1}],

    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1, (0, 4): 1, (0, 5): 1},
    {(3, 0): 1, (2, 0): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1},
    {(2, 4): 1, (2, 3): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(0, 1): 1, (0, 2): 1, (0, 3): 1, (0, 4): 1, (0, 5): 1, (0, 6): 1},
    {(2, 0): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (0, 3): 1},
    {(3, 2): 1, (2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 0): 1, (0, 0): 1}],

    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1, (1, 1): 1, (1, 2): 1},
    {(2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (2, 3): 1, (1, 3): 1},
    {(1, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1, (0, 4): 1, (0, 3): 1},
    {(1, 4): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1, (0, 3): 1, (0, 2): 1},
    {(0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1, (0, 0): 1, (1, 0): 1},
    {(0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1, (1, 0): 1, (1, 1): 1}],

    [{(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1},
    {(1, 0): 1, (0, 0): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (0, 3): 1},
    {(2, 2): 1, (2, 1): 1, (2, 3): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1},
    {(1, 4): 1, (1, 3): 1, (0, 4): 1, (0, 3): 1, (0, 2): 1, (0, 1): 1},
    {(0, 4): 1, (1, 4): 1, (0, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1},
    {(0, 1): 1, (0, 2): 1, (0, 0): 1, (1, 0): 1, (1, 1): 1, (2, 1): 1},
    {(1, 0): 1, (1, 1): 1, (0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1},
    {(2, 2): 1, (2, 3): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1},
    {(1, 4): 1, (0, 4): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(0, 4): 1, (0, 3): 1, (1, 4): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1},
    {(0, 1): 1, (0, 0): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1},
    {(0, 0): 1, (1, 0): 1, (0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1}],

    [{(0, 0): 1, (1, 0): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1},
    {(2, 1): 1, (2, 2): 1, (2, 3): 1, (1, 3): 1, (1, 4): 1, (0, 4): 1},
    {(2, 2): 1, (2, 3): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(1, 4): 1, (0, 4): 1, (0, 3): 1, (0, 2): 1, (0, 1): 1, (0, 0): 1},
    {(0, 4): 1, (0, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1},
    {(0, 1): 1, (0, 0): 1, (1, 0): 1, (1, 1): 1, (2, 1): 1, (2, 2): 1},
    {(1, 0): 1, (0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1, (0, 4): 1},
    {(2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (0, 3): 1},
    {(2, 3): 1, (2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 0): 1, (0, 0): 1},
    {(0, 4): 1, (1, 4): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1, (1, 0): 1},
    {(0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1, (2, 0): 1},
    {(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1, (2, 3): 1}],

    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1},
    {(1, 0): 1, (0, 0): 1, (0, 1): 1, (1, 2): 1, (0, 2): 1, (0, 3): 1},
    {(2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1},
    {(1, 4): 1, (1, 3): 1, (1, 2): 1, (0, 3): 1, (0, 2): 1, (0, 1): 1},
    {(0, 4): 1, (1, 4): 1, (1, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1},
    {(0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 0): 1, (1, 1): 1, (2, 1): 1},
    {(1, 0): 1, (1, 1): 1, (1, 2): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1},
    {(2, 2): 1, (2, 3): 1, (1, 3): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1},
    {(1, 4): 1, (0, 4): 1, (0, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(0, 4): 1, (0, 3): 1, (0, 2): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1},
    {(0, 1): 1, (0, 0): 1, (1, 0): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1},
    {(0, 0): 1, (1, 0): 1, (1, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1}],

    [{(0, 2): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1, (1, 5): 1},
    {(1, 0): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (0, 3): 1},
    {(2, 0): 1, (2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 0): 1, (0, 0): 1},
    {(1, 4): 1, (0, 5): 1, (0, 4): 1, (0, 3): 1, (0, 2): 1, (0, 1): 1},
    {(1, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1, (2, 0): 1},
    {(0, 3): 1, (0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1, (2, 3): 1},
    {(1, 2): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1, (0, 4): 1, (0, 5): 1},
    {(2, 2): 1, (2, 0): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1},
    {(1, 4): 1, (2, 3): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1, (0, 1): 1},
    {(0, 4): 1, (1, 5): 1, (1, 4): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1},
    {(0, 1): 1, (0, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (2, 1): 1},
    {(1, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1, (2, 3): 1, (2, 4): 1}],

    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 1, (1, 2): 1, (1, 3): 1},
    {(2, 1): 1, (1, 1): 1, (1, 2): 1, (0, 2): 1, (1, 3): 1, (1, 4): 1},
    {(2, 2): 1, (2, 1): 1, (1, 1): 1, (1, 0): 1, (1, 2): 1, (0, 2): 1},
    {(1, 4): 1, (1, 3): 1, (1, 2): 1, (1, 1): 1, (0, 2): 1, (0, 1): 1},
    {(0, 4): 1, (1, 4): 1, (1, 3): 1, (2, 3): 1, (1, 2): 1, (1, 1): 1},
    {(0, 1): 1, (0, 2): 1, (1, 2): 1, (1, 3): 1, (1, 1): 1, (2, 1): 1},
    {(1, 0): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1, (0, 2): 1, (0, 3): 1},
    {(2, 0): 1, (2, 1): 1, (1, 1): 1, (1, 2): 1, (1, 0): 1, (0, 0): 1},
    {(2, 3): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1, (1, 1): 1, (1, 0): 1},
    {(0, 4): 1, (0, 3): 1, (0, 2): 1, (0, 1): 1, (1, 2): 1, (1, 1): 1},
    {(0, 3): 1, (0, 2): 1, (1, 2): 1, (1, 1): 1, (1, 3): 1, (2, 3): 1},
    {(0, 0): 1, (1, 0): 1, (1, 1): 1, (2, 1): 1, (1, 2): 1, (1, 3): 1}],
    ]

pieces_orientations_per_piece = [1, 3, 6, 6, 6, 6, 6, 12, 12, 12, 12, 12]

def prepare_puzzle_pieces(base_pieces_patterns):
    solver = triangular_puzzle_solver.PuzzleSolver()
    # prepare puzzle pieces
    pieces_with_orientations = solver.prepare_pieces(base_pieces_patterns)
    # for patterns in prepared_patterns:
    #     print(patterns)

    pieces_orientations_per_piece = [len(p) for p in pieces_with_orientations]

    return pieces_with_orientations, pieces_orientations_per_piece

def prepare_base_boards_with_hexagon(hexagon, base_board):  
    solver = triangular_puzzle_solver.PuzzleSolver()
    hexagon_translations_for_all_possible_positions_on_board = [
            [("E",3),],
            [("E",3),("SE",1)],
            [("E",3),("SE",2)],
            [("E",2),("SE",2)],
            [("E",1),("SE",3)],
        ]

    # prepare base board
    puzzle_board = solver.create_empty_base_board(8,13,base_board)

    # get all base boards.
    starting_puzzle_boards = solver.prepare_base_boards(puzzle_board, hexagon, hexagon_translations_for_all_possible_positions_on_board )

    # for board in starting_puzzle_boards:
    #     print(str(board))

    return starting_puzzle_boards

def logger_setup():
    # logger setup 
    #logging.basicConfig(format='%(asctime)s - %(module)s (ln:%(lineno)d): %(message)s', level=logging.INFO)
    # logging.basicConfig(format='%(asctime)s : %(message)s \t\t (%(module)s:%(lineno)d)', level=logging.INFO)
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - %(module)s/%(funcName)s/%(lineno)d: \n \t %(message)s', level=logging.INFO)

    message_format = logging.Formatter('%(levelname)s\t%(asctime)s\t:\t%(message)s\t(%(module)s/%(funcName)s/%(lineno)d)')

    # logging.basicConfig(format= message_format, level=logging.INFO)

    # logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')

    # works, but logs everything....
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')
    # logger = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')
    # test_lode 
    logger = logging.getLogger("puzzle_haley")
    # logger.addHandler(test_lode)
    
    logger.setLevel(logging.INFO)
    return logger

def solve_by_random(board, ):

    state = [(0,0)]
    last_tried = None

    pieces_to_try_indeces = [1,2,3,4,5,6,7,8,9,10,11]  # 0 is already placed on the board!\
    tested_sequences = 0
    # stats = {}
    while True:
        tested_sequences += 1
        pieces_tested, longest_state = solver.analyse_randomize_sequence_of_pieces(board, pieces_with_orientations, pieces_to_try_indeces)

        if len(longest_state) >= 11:
            logger.critical("winning sequence: {}".format(longest_state))
            raise

        # show_board = copy.deepcopy(board)
        # solver.build_up_state(show_board, pieces_with_orientations, longest_state,True)
        logger.info('Tested sequences: {}'.format(tested_sequences))


def show_a_solution():
    # winner found 2020-05-09
    '''
    2020-05-09 19:00:00,296 MainThread Start trying pieces sequence. (all orientations, top left to bottom right): [2, 5, 9, 3, 11, 10, 6, 1, 4, 7, 8]
    2020-05-09 19:00:00,369 MainThread Testing endend. Pieces tested:42. Found? False, state: []. longest state length: 2/11 ([(2, 3), (5, 1)])
    2020-05-09 19:00:00,369 MainThread Tested sequences: 58391
    2020-05-09 19:00:00,371 MainThread Start trying pieces sequence. (all orientations, top left to bottom right): [2, 3, 11, 6, 1, 4, 7, 5, 10, 9, 8]
    2020-05-09 19:00:00,561 MainThread We have a winner!
    2020-05-09 19:00:00,561 MainThread [(2, 3), (3, 5), (11, 3), (6, 0), (1, 1), (4, 4), (7, 0), (5, 0), (10, 2), (9, 5), (8, 10)]
    Traceback (most recent call last):
    File "puzzle_haley.py", line 542, in <module>
        pieces_tested, longest_state = solver.analyse_randomize_sequence_of_pieces(board, pieces_with_orientations, pieces_to_try_indeces)
    File "C:\Data\GIT\triangular_puzzle_haley\triangular_puzzle_solver.py", line 74, in analyse_randomize_sequence_of_pieces
        pieces_tested, longest_state = self.analyse_sequence_of_pieces(board, pieces_with_orientations, pieces_indeces, show_longest_state=False)
    File "C:\Data\GIT\triangular_puzzle_haley\triangular_puzzle_solver.py", line 85, in analyse_sequence_of_pieces
        success, state = self.try_sequence_recursive(try_board, sequence_of_pieces_indeces_to_try, pieces_with_orientations, state)
    File "C:\Data\GIT\triangular_puzzle_haley\triangular_puzzle_solver.py", line 154, in try_sequence_recursive
        success, return_state = self.try_sequence_recursive(result_board, try_sequence_of_pieces_index, pieces_with_orientations, new_state , last_tried=None)
    File "C:\Data\GIT\triangular_puzzle_haley\triangular_puzzle_solver.py", line 154, in try_sequence_recursive
        success, return_state = self.try_sequence_recursive(result_board, try_sequence_of_pieces_index, pieces_with_orientations, new_state , last_tried=None)
    File "C:\Data\GIT\triangular_puzzle_haley\triangular_puzzle_solver.py", line 154, in try_sequence_recursive
        success, return_state = self.try_sequence_recursive(result_board, try_sequence_of_pieces_index, pieces_with_orientations, new_state , last_tried=None)
    [Previous line repeated 8 more times]
    File "C:\Data\GIT\triangular_puzzle_haley\triangular_puzzle_solver.py", line 115, in try_sequence_recursive
        raise
    RuntimeError: No active exception to reraise

    C:\Data\GIT\triangular_puzzle_haley>
    '''
    logger = logger_setup()
    solver = triangular_puzzle_solver.PuzzleSolver(logger)
   
    starting_puzzle_boards = prepare_base_boards_with_hexagon( pieces_with_orientations[0][0], base_board)
    board = starting_puzzle_boards[0]
    
    show_board = copy.deepcopy(board)
    winning_states = [
            [(2, 3), (3, 5), (11, 3), (6, 0), (1, 1), (4, 4), (7, 0), (5, 0), (10, 2), (9, 5), (8, 10)],  # 2020-05-09 after 67000 random sequences tries
            [(8,6), (3,5 ), (6,0 ), (10,11 ), (4,5 ), (2,4 ), (7,9 ), (11,3 ), (1,0 ), (9,3 ), (5,0 )],  # 2020-05-25 245000 attempts  
            [(2,3), (10,0 ), (11,3 ), (6,0 ), (8,5 ), (9,1 ), (5,0 ), (1,2 ), (7,2 ), (4,2 ), (3,3 )],  # 2020-05-25  322000 attempts 
            [(7, 6), (2, 0), (3, 5), (11, 1), (8, 4), (1, 0), (10, 7), (6, 3), (4, 0), (9, 3), (5, 0)],  # 2020-05-26 535000 attempts
            # [(,), (, ), (, ), (, ), (, ), (, ), (, ), (, ), (, ), (, ), (, )],
        ]


    solver.build_up_state(show_board, pieces_with_orientations, winning_states[2],True)

if __name__ == "__main__":
    show_a_solution()
    exit()

    logger = logger_setup()
    solver = triangular_puzzle_solver.PuzzleSolver(logger)
    logger.info("start Haley puzzle solving.")
    
    # only do if not hardcoded.
    if GENERATE_PIECES:
        pieces_with_orientations, pieces_orientations_per_piece = prepare_puzzle_pieces(base_pieces_patterns)
    
    starting_puzzle_boards = prepare_base_boards_with_hexagon( pieces_with_orientations[0][0], base_board)
    board = starting_puzzle_boards[0]

    solve_by_random(board)
