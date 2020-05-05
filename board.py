import triangular_grid
import triangular_pattern
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
    base.overlay_grid(base_board)


def show_mirrored(pattern):
        
    transformer = triangular_pattern.TriangularPatternOperations()
    
    # pattern = transformer.translate(pattern,"SE",1)

    vertical = transformer.mirror(pattern, False)
    # vertical = transformer.translate(vertical,"S",1)
    horizontal = transformer.mirror(pattern, True)
    # horizontal = transformer.translate(horizontal,"E",1)

    bounding_box = transformer.get_combined_bounding_box([pattern, horizontal, vertical])
    rows = bounding_box["max_r"] + 1
    cols = bounding_box["max_c"] + 1
    base = triangular_grid.TriangularGrid(rows, cols)    

    base.overlay_grid(pattern)
    base.overlay_grid(horizontal)
    base.overlay_grid(vertical)

    print(str(base))


# -----------------------------------------------------
def show_all_base_pieces():
    base = triangular_grid.TriangularGrid(3,6)    
    for piece_cells in base_pieces_cells:
        piece = triangular_pattern.TriangularPattern(piece_cells)
        base_and_piece  = copy.deepcopy(base)
        base_and_piece.overlay_grid(piece.get_pattern())
        print(str(base_and_piece))

def show_all_pieces_mirrored():
    for piece in base_pieces_cells:
        show_mirrored(piece)
        
def show_pattern(pattern_cells):
    transformer = triangular_pattern.TriangularPatternOperations()
   
    bounding_box = transformer.get_bounding_box(pattern_cells)
    rows = bounding_box["max_r"] + 1
    cols = bounding_box["max_c"] + 1
    base = triangular_grid.TriangularGrid(rows, cols)  
    base.overlay_grid(pattern_cells)
    print(str(base)) 


def get_all_isomorphs(pattern_cells, delete_equal_patterns=False, show=False):
    # provide cells.

    transformer = triangular_pattern.TriangularPatternOperations()


    resulting_patterns = []
    
    # rotate all
    for degrees in range (0,360,60):
        resulting_patterns.append(transformer.rotate(pattern_cells, degrees, False))

    # rotate mirrored
    mirrored = transformer.mirror(pattern_cells, False, True)
    
    for degrees in range (0,360,60):
        resulting_patterns.append(transformer.rotate(mirrored, degrees, False))

    ### AFTERMATH

    # crop all to most compact form
    resulting_patterns  = [ transformer.crop_pattern_to_bounding_box(pattern) for pattern in resulting_patterns]

    # delete equals
    if delete_equal_patterns:
        resulting_patterns = transformer.delete_equal_patterns(resulting_patterns)
    

    if show:
        arrange_patterns_on_a_grid(resulting_patterns, 10)
    
    
    return resulting_patterns


def show_isomorphs_of_all_patterns(patterns,  delete_equal_patterns=False):
    # transformer = triangular_pattern.TriangularPatternOperations()
    resulting_patterns = []

    for pattern in patterns:
        resulting_patterns.extend(get_all_isomorphs(pattern, delete_equal_patterns))

    arrange_patterns_on_a_grid(resulting_patterns, 6)

    print("Number of patterns: {}".format(len(resulting_patterns)))


def arrange_patterns_on_a_grid(patterns, patterns_per_col):
    transformer = triangular_pattern.TriangularPatternOperations()

    arranged_patterns = transformer.arrange_patterns_for_no_overlap(patterns, patterns_per_col)
    
    # create fitting field.
    bounding_box = transformer.get_combined_bounding_box(arranged_patterns)
    rows = bounding_box["max_r"] + 1
    cols = bounding_box["max_c"] + 1
    base = triangular_grid.TriangularGrid(rows, cols)   
    
    for pattern in arranged_patterns:
        base.overlay_grid(pattern)
    
    print(str(base))


if __name__ == "__main__":
    puzzle_board = create_puzzle_board()
    print(str(puzzle_board))

    # show_all_base_pieces()    
    # show_all_pieces_mirrored()
    # show_mirrored(piece_0)
    # transformer = triangular_pattern.TriangularPatternOperations()
    # mirrored = transformer.mirror(piece_0, horizontal_else_vertical=False,crop=True)
    # show_pattern(mirrored)


    show_isomorphs_of_all_patterns(base_pieces_cells, True)



    