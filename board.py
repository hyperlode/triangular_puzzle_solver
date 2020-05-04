import triangular_grid
import copy

CELL_EDGE = 666  # for programatorical reasons (to have no exception on the edge of the grid)
CELL_NOGO = 4  # not allowed --> i.e. board edge 
CELL_ON = 1
CELL_OFF = 0
CELL_DOUBLE_ON = 2  # if two "ON"-cells are overlayed on each other.


# pieces, made up of small triangles.
# x = cell
# o = 0,0 cell
# . = 0,0 coordinate, not part of piece

# ox
# xxxx
piece_0 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (1,0):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
} 

# oxxxxx
piece_1 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (0,2):CELL_ON,
    (0,3):CELL_ON,
    (0,4):CELL_ON,
    (0,5):CELL_ON,
} 

# oxxx
#  xx
piece_2 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (0,2):CELL_ON,
    (0,3):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
} 

# o
# xxxxx
piece_3 = {
    (0,0):CELL_ON,
    (1,0):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
    (1,4):CELL_ON,
} 

# oxx
#  xxx
piece_4 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (0,2):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
} 

#  .
#  xxx
#  xxx
piece_5 = {
    (1,0):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (2,0):CELL_ON,
    (2,1):CELL_ON,
    (2,2):CELL_ON,
} 


# . x
# xxxxx
piece_6 = {
    (0,2):CELL_ON,
    (1,0):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
    (1,4):CELL_ON,
} 

# . x
#  xxxxx
piece_7 = {
    (0,2):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
    (1,4):CELL_ON,
    (1,5):CELL_ON,
} 

#  0xxx
#    xx
piece_8 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (0,2):CELL_ON,
    (0,3):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
} 

#  0xx
#    xxx
piece_9 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (0,2):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
    (1,4):CELL_ON,
} 


#  .   xx
#   xxxx
piece_10 = {
    (0,4):CELL_ON,
    (0,5):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
    (1,3):CELL_ON,
    (1,4):CELL_ON,
} 

# oxx
# xxx
piece_11 = {
    (0,0):CELL_ON,
    (0,1):CELL_ON,
    (0,2):CELL_ON,
    (1,0):CELL_ON,
    (1,1):CELL_ON,
    (1,2):CELL_ON,
}

base_pieces = [
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
base_board = {(r,c):CELL_OFF for r in range(8) for c in range(13)}
# border
base_board[(0,0)] = CELL_NOGO
base_board[(0,1)] = CELL_NOGO
base_board[(0,2)] = CELL_NOGO
base_board[(0,3)] = CELL_NOGO
base_board[(0,4)] = CELL_NOGO
base_board[(0,5)] = CELL_NOGO
base_board[(0,9)] = CELL_NOGO
base_board[(0,10)] = CELL_NOGO
base_board[(0,11)] = CELL_NOGO
base_board[(0,12)] = CELL_NOGO
base_board[(1,0)] = CELL_NOGO
base_board[(1,10)] = CELL_NOGO
base_board[(1,11)] = CELL_NOGO
base_board[(1,12)] = CELL_NOGO
base_board[(2,0)] = CELL_NOGO
base_board[(3,0)] = CELL_NOGO
base_board[(4,12)] = CELL_NOGO
base_board[(5,12)] = CELL_NOGO
base_board[(6,0)] = CELL_NOGO
base_board[(6,1)] = CELL_NOGO
base_board[(6,2)] = CELL_NOGO
base_board[(6,12)] = CELL_NOGO
base_board[(7,0)] = CELL_NOGO
base_board[(7,1)] = CELL_NOGO
base_board[(7,2)] = CELL_NOGO
base_board[(7,3)] = CELL_NOGO
base_board[(7,7)] = CELL_NOGO
base_board[(7,8)] = CELL_NOGO
base_board[(7,9)] = CELL_NOGO
base_board[(7,10)] = CELL_NOGO
base_board[(7,11)] = CELL_NOGO
base_board[(7,12)] = CELL_NOGO


def create_puzzle_board():
    base = triangular_grid.TriangularGrid(8,13) # the size of the board. 
    base.overlay_grid(base_board,0,0)
    
def show_all_base_pieces():
    base = triangular_grid.TriangularGrid(3,6)    
    for piece in base_pieces:

        base_and_piece  = copy.deepcopy(base)
        x_offset = 0
        y_offset = 0
        base_and_piece.overlay_grid(piece,x_offset, y_offset)
        print(str(base_and_piece))

if __name__ == "__main__":
    puzzle_board = create_puzzle_board()
    print(str(puzzle_board))

    show_all_base_pieces()    
    

    