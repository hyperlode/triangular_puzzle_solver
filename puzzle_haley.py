import copy
import logging
import time
import datetime
from collections import defaultdict
import triangular_puzzle_solver

import triangular_grid
import triangular_pattern

import solver_database
import solver_database_level_build_up



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



GENERATE_PIECES = False
# only do if not hardcoded.
if GENERATE_PIECES:
    pieces_with_orientations, pieces_orientations_per_piece = prepare_puzzle_pieces(base_pieces_patterns)

else:
    # these are the hardcode prepared pieces ( use: prepare_puzzle_pieces() )
    # generated cropped pieces and their configurations
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

# we will work with all orientations as different pieces 
index_per_piece_with_orientation = [ (i,j) for i in range(len(pieces_with_orientations)) for j in range(len(pieces_with_orientations[i])) ]
assert len(index_per_piece_with_orientation) == 94, "There should be 94 pieces including different orientations."



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

starting_puzzle_boards = prepare_base_boards_with_hexagon( pieces_with_orientations[0][0], base_board)


def prepare_puzzle_pieces(base_pieces_patterns):
    solver = triangular_puzzle_solver.PuzzleSolver()
    # prepare puzzle pieces
    pieces_with_orientations = solver.prepare_pieces(base_pieces_patterns)
    # for patterns in prepared_patterns:
    #     print(patterns)

    pieces_orientations_per_piece = [len(p) for p in pieces_with_orientations]

    return pieces_with_orientations, pieces_orientations_per_piece

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

    # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s\t%(asctime)s\t:\t%(message)s\t(%(module)s/%(funcName)s/%(lineno)d)')
    # test_lode 
    logger = logging.getLogger("puzzle_haley")
    # logger.addHandler(test_lode)
    
    logger.setLevel(logging.INFO)
    return logger



def test_sequences_from_database_loop(boards, logger):


    solver = triangular_puzzle_solver.PuzzleSolver(logger)
    logger.info("start Haley puzzle solving.")
    

    conn = solver_database.create_connection(r"D:\Temp\puzzle_haley\attempts_no_boards.db")
    sequences_count = 5

    total_sequences_tested = 0
    total_pieces_tested = 0
    while True:
        
        id_first_row, sequences = solver_database.get_untested_sequences(conn, sequences_count)
        logger.info("*****get new sequences from database. (rows taken:{}) id first row:{}".format(sequences_count, id_first_row))
        
        # sequences.append([7,2,3,11,8,1,10,6,4,9,5])  # test to see if winners are detected.
        sequences = [[7,2,3,11,8,1,10,6,4,9,5]] + sequences 

        for s in sequences:
            print (s)
        st, pt = try_sequences_for_all_boards(boards, sequences)
        total_sequences_tested += st
        total_pieces_tested += pt
        logger.info('For now: Total tested sequences: {}, total pieces tested: {}'.format(total_sequences_tested, total_pieces_tested))
        solver_database.set_sequences_as_tested(conn, sequences)

def try_random_sequences_for_all_boards(boards):
    pieces_to_try_indeces =        [1,2,3,4,5,6,7,8,9,10,11]  # 0 is already placed on the board!\
    # winning_sequence_for_testing = [7,2,3,11,8,1,10,6,4,9,5]  # 0 is already placed on the board!\
    tested_sequences = 0
    pieces_tested_count = 0
    while True:
        tested_sequences += 1
        try:
            pieces_tested, longest_state, board_index = solver.analyse_randomize_sequence_of_pieces_on_multiple_boards(boards, pieces_with_orientations, pieces_to_try_indeces)
        
        except triangular_puzzle_solver.WinningSolutionFoundException as e:
           
            with open(r"D:\Temp\puzzle_haley\winners.txt","a") as f:
                f.write("{}\n".format(str(sequence_to_try)))

        logger.info('Tested sequences: {}, total pieces tested: {}'.format(tested_sequences, pieces_tested_count))

    return tested_sequences, pieces_tested_count

def try_sequences_for_all_boards(boards, sequences_to_try=None):
    # if no sequence to try provide (list of pieces to try in right sequence), a random one will be generated.
    solver  = triangular_puzzle_solver.PuzzleSolver()
    tested_sequences = 0
    pieces_tested_count = 0
    for sequence_to_try in sequences_to_try:
        tested_sequences += 1
        try:
            pieces_tested, longest_state, board_index = solver.analyse_sequence_of_pieces_on_multiple_boards(boards, pieces_with_orientations, sequence_to_try)

            pieces_tested_count += pieces_tested

        except triangular_puzzle_solver.WinningSolutionFoundException as e:
           
            with open(r"D:\Temp\puzzle_haley\tmptmp.txt","a") as f:
                f.write("{}\n".format(str(sequence_to_try)))

           
        # if len(longest_state) >= 11:
        #     logger.critical("winning sequence: {}".format(longest_state))
            

        logger.info('Tested sequences: {}, total pieces tested: {}'.format(tested_sequences, pieces_tested_count))
    return tested_sequences, pieces_tested_count

def solve_by_random(board, ):

    pieces_to_try_indeces = [1,2,3,4,5,6,7,8,9,10,11]  # 0 is already placed on the board!\
    tested_sequences = 0
    
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


def test_manually(pieces_with_orientations):

    logger = logger_setup()
    solver = triangular_puzzle_solver.PuzzleSolver(logger)
    logger.info("start Haley puzzle solving.")
    
    # only do if not hardcoded.
    if GENERATE_PIECES:
        pieces_with_orientations, pieces_orientations_per_piece = prepare_puzzle_pieces(base_pieces_patterns)
    
    starting_puzzle_boards = prepare_base_boards_with_hexagon( pieces_with_orientations[0][0], base_board)
    
    
    board = starting_puzzle_boards[1]
    # seq = [(3,3)]

    success = solver.try_piece_on_board(board, pieces_with_orientations[3][3])
    success = solver.try_piece_on_board(board, pieces_with_orientations[8][11])

    if not success:
        print("Problemski!")

    print(board)

def solve_with_database(path_to_database):
    pass

class FindAllSolutions():
    def __init__(self, database_path, board, pieces_with_orientations, 
        index_per_piece_with_orientation, logger=None):
        # we will not do any flipping or rotating. So provide all wanted symmetries.
        # index_per_piece_with_orientation --> used pieces index with orientation .(list of tuples) 
        self.board = board
        self.pieces_with_orientations = pieces_with_orientations
        self.index_per_piece_with_orientation = index_per_piece_with_orientation
        self.logger = logger or logging.getLogger(__name__)
        
        self.solver = triangular_puzzle_solver.PuzzleSolver(self.logger)
        self.logger.info("Init environment for fitting pieces in board.")
        self.solver_db = solver_database_level_build_up.HaleyPuzzleBuildUpDatabase(database_path)

        
    def initiate_search(self, level=1):
        # assume level is zero for now.
        # determine level.

        # check for "started"

        NUMBER_OF_BASE_SEQUENCES_TO_RETRIEVE_PER_CALL = 100

        # when database is empty, we can't do anthing yet. so, build first level manually.
        self.check_and_build_first_level()
        

        self.level = 1  # at each program start, we start from the first level to check where to start adding.

        while True:
            # retrieve sequences to build upon. And check if we're looking on the right level.
            continue_level_search = True
            while continue_level_search:
                base_sequences = self.solver_db.get_sequences(solver_database_level_build_up.NOT_TESTED, 
                    level,
                    NUMBER_OF_BASE_SEQUENCES_TO_RETRIEVE_PER_CALL,
                    True,
                    )
            
                if len(base_sequences) == 0:
                    
                    level += 1
                    self.logger.info("level increased. Now adding to level {}".format(level))
                else:
                    continue_level_search = False

            # valid sequences found. time to add to it.
            next_level_results = []
            for base_sequence in base_sequences:
                next_level_results.extend( self.get_next_level_sequences(base_sequence))
            
            # write away new pieces.
            # print(next_level_results)
            self.solver_db.add_sequences(next_level_results,solver_database_level_build_up.NOT_TESTED)

            # mark base sequences as done.
            self.solver_db.change_statuses(base_sequences,solver_database_level_build_up.TESTED, True)
            self.logger.info("average additions per base: {}".format( len(next_level_results) / len(base_sequences)))
           
        # sequence = self.solver_db.get_sequences(solver_database_level_build_up.NOT_TESTED, level,1)
    
    def check_and_build_first_level(self):
        # if no one pieces sequences yet in table, we have to start from scratch.
        rows = self.solver_db.row_count(1)
        if rows == 0:
            print("not yet started.")
            sequences = self.get_next_level_sequences([])
            self.solver_db.add_sequences(sequences, solver_database_level_build_up.NOT_TESTED)
        

    def get_next_level_sequences(self, sequence):
        valid_pieces = self.extend_sequence_with_all_possibilities(sequence)
        next_sequences = [ sequence + [p] for p in valid_pieces]
        return next_sequences

    def extend_sequence_with_all_possibilities(self, sequence):
        # sequence is a list of tuples (pieceindex, orientationindex)
        
        useboard = copy.deepcopy(self.board)
        resultboard = self.solver.build_up_state(useboard, self.pieces_with_orientations, sequence)
        sequence_board = copy.deepcopy(resultboard)
        
        used_pieces = [p for p,o in sequence]
        pieces = [(p,o) for (p,o) in self.index_per_piece_with_orientation if p not in used_pieces]
        
        # logger.info("{} pieces to choose from. {}".format(len(pieces), pieces))
        list_of_successful_pieces = self.try_pieces_on_a_board(sequence_board, pieces)
        return list_of_successful_pieces

    def try_pieces_on_a_board(self, board, pieces):
        fitting_pieces = []
        for piece_index, piece_orientation in pieces:
            # logger.info(piece_index)
            fits =  self.try_extra_piece(board, piece_index, piece_orientation)
            if fits:
                fitting_pieces.append((piece_index, piece_orientation))

        return fitting_pieces

    def try_extra_piece(self, board, piece_index, piece_orientation ):

        pattern = self.pieces_with_orientations[piece_index][piece_orientation]
        testboard = copy.deepcopy(board)  # efwefaefawef  continue herer....
        
        fits = self.solver.try_piece_on_board(testboard, pattern)
        
        return fits

solutions_board_0 = [ (2, 3), (1, 2), (4, 5), (8, 11), (7, 9), (9, 2), (6, 2), (11, 6), (3, 4), (5, 2), (10, 6),  #  part of the database big search. 
            [(2, 3), (3, 5), (11, 3), (6, 0), (1, 1), (4, 4), (7, 0), (5, 0), (10, 2), (9, 5), (8, 10)],  # 2020-05-09 after 67000 random sequences tries
            [(8,6), (3,5 ), (6,0 ), (10,11 ), (4,5 ), (2,4 ), (7,9 ), (11,3 ), (1,0 ), (9,3 ), (5,0 )],  # 2020-05-25 245000 attempts  
            [(2,3), (10,0 ), (11,3 ), (6,0 ), (8,5 ), (9,1 ), (5,0 ), (1,2 ), (7,2 ), (4,2 ), (3,3 )],  # 2020-05-25  322000 attempts 
            [(7, 6), (2, 0), (3, 5), (11, 1), (8, 4), (1, 0), (10, 7), (6, 3), (4, 0), (9, 3), (5, 0)],  # 2020-05-26 535000 attempts
            ]

def print_sequence_on_board(board, sequence):

    solver = triangular_puzzle_solver.PuzzleSolver(logger)
    if type(sequence) is str:
        elements = sequence.split(",")
        seq = []
        for p,o in zip(elements[0::2], elements[1::2]):
            seq.append((int(p),int(o)))
        sequence = seq

    solver.build_up_state(board, pieces_with_orientations,sequence,True)
    
    # start with zero level
    # try to pick up from database.
    # if nothing, advance a level

    # when sequence found
    # search alll next levels
    # post them to the database
    # repeat.


if __name__ == "__main__":

    logger = logger_setup()
    database_path = r"C:\temp\haley_puzzle\Haley_puzzle_board_{}.db".format(0)
    # database_path = r"D:\Temp\puzzle_haley\Haley_puzzle_board_{}.db".format(0)

    # print_sequence_on_board(starting_puzzle_boards[0], [(2,3)])
    # print_sequence_on_board(starting_puzzle_boards[0], "2,5,4,2,11,2,5,5,7,10,10,11")
    # exit()

    findall = FindAllSolutions(
        database_path,
        starting_puzzle_boards[0],
        pieces_with_orientations,
        index_per_piece_with_orientation[1:],
        logger
        )
    findall.initiate_search()

    exit()
    # solve_board_0_by_level_build_up( db_path, starting_puzzle_boards[0], pieces_with_orientations, index_per_piece_with_orientation[1:], logger)
    
    # next_level_pieces = findall.extend_sequence_with_all_possibilities([(2,3),(1,1),(3,2)])
    seqs = [[]]
    while True:
        new_seqs = []
        for seq in seqs:
            # logger.info("check {}".format(seq))
            new_seqs.extend(findall.get_next_level_sequences(seq))
        logger.info(len(new_seqs))
        seqs = new_seqs
        logger.info("next level")

        # for s in seqs:
            
        #     logger.info(s)
    exit()


    # show_a_solution()
    # exit()

    
    


    # try_sequences_for_all_boards(starting_puzzle_boards, sequences_to_try= [[7,2,3,11,8,1,10,6,4,9,5]])
    try_sequences_for_all_boards(starting_puzzle_boards, sequences_to_try= [[2,1,4,8,7,9,6,11,3,5,10]])

    # test_sequences_from_database_loop(starting_puzzle_boards, logger)
    
   

    # board = starting_puzzle_boards[0]
    # solve_by_random(board)

    # solve_sequence_for_all_boards(starting_puzzle_boards, None)
