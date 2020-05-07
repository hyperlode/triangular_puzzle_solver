
import triangular_puzzle_solver

import triangular_grid
import triangular_pattern
import copy


# pieces, made up of small triangles.
# x = cell
# o = 0,0 cell
# . = 0,0 coordinate, not part of piece

# pieces numbered from least amount of orientations to most.

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

# sorted in ascending order of number of forms per piece
base_pieces_cells = [
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

if __name__ == "__main__":


    solver = triangular_puzzle_solver.PuzzleSolver()

    # prepare puzzle pieces
    prepared_patterns = solver.prepare_pieces(base_pieces_cells)
    # for patterns in prepared_patterns:
    #     print(patterns)

    hexagon_translations_for_all_possible_positions_on_board = [
            [("E",3),],
            [("E",3),("SE",1)],
            [("E",3),("SE",2)],
            [("E",2),("SE",2)],
            [("E",1),("SE",3)],
        ]
    hexagon = prepared_patterns[0][0]

    # prepare base board
    puzzle_board = solver.create_empty_base_board(8,13,base_board)

    # get all base boards.
    starting_puzzle_boards = solver.prepare_base_boards(puzzle_board, hexagon, hexagon_translations_for_all_possible_positions_on_board )
    
    for board in starting_puzzle_boards:

        print(str(board))