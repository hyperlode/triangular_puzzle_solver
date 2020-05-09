import copy
import logging
import time
import datetime

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



FAKE_TEST_PIECES_WITH_ORIENTATIONS = [
    [{(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 0): 1, (1, 1): 1, (1, 2): 1}],

    # [{(0, 1): 1, (0, 2): 1, (0, 3): 1, (1, 1): 1, (1, 2): 1, (1, 3): 1},
    # {(1, 1): 1, (1, 2): 1, (0, 2): 1, (2, 3): 1, (1, 3): 1, (1, 4): 1},
    # {(2, 1): 1, (1, 1): 1, (1, 0): 1, (1, 3): 1, (1, 2): 1, (0, 2): 1}],

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
    

    # message_format = logging.Formatter('%(levelname)s\t%(asctime)s\t:\t%(message)s\t(%(module)s/%(funcName)s/%(lineno)d)')
    # logging.basicConfig(format= message_format, level=logging.INFO)
    

    # logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')
    
    logger = logging.getLogger(__name__)

    return logger


if __name__ == "__main__":

    logger = logger_setup()
    solver = triangular_puzzle_solver.PuzzleSolver(logger)
    logger.info("start Haley puzzle solving.")
    
    # only do if not hardcoded.
    if GENERATE_PIECES:
        pieces_with_orientations, pieces_orientations_per_piece = prepare_puzzle_pieces(base_pieces_patterns)
    
    starting_puzzle_boards = prepare_base_boards_with_hexagon( pieces_with_orientations[0][0], base_board)

    board = starting_puzzle_boards[0]
    state = [(0,0)]
    last_tried = None

    # triangular_puzzle_solver.show_pattern_on_grid()
    #pieces_with_orientations = FAKE_TEST_PIECES_WITH_ORIENTATIONS
    
    # success, state = solver.next_step(board, pieces_with_orientations, state, (1,0))

    # NOT WORKING. sequence_of_pieces_indeces_to_try = [1,2,3,4,5,6,7,8,9,10,11]  # 0 is already placed on the board


    # 0 is already placed on the board!
    permutations = [
        [1,2,3,4,5,6,7,8,9,10,11],
        [2,1,3,4,5,6,7,8,9,10,11],
    ]

    for sequence_of_pieces_indeces_to_try in permutations:
        
        logger.info("Start trying pieces sequence. (all orientations, top left to bottom right): {}".format(sequence_of_pieces_indeces_to_try))
        state = []
        try_board = copy.deepcopy(board)
        
        if len(state) > 0:
            try_board = solver.build_up_state(try_board, pieces_with_orientations, state)
        success, state = solver.try_sequence_recursive(try_board, sequence_of_pieces_indeces_to_try, pieces_with_orientations, state)

        logger.info("Testing endend. Found? {}, state: {}".format(success, state))
        
        # print(success)
        # print(state)




