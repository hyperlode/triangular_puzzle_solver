import triangular_grid
import triangular_pattern
import copy


class PuzzleSolver():
    # the puzzle contais twelve pieces that need to fit in certain pattern. 
    # all pieces can be flipped (ake. there is no front or backside) (2 sides)
    # the pieces are created on a triangular grid. (6 rotations)
    # this gives for every piece (2 x 6) 12 possibilities. Some pieces have many orientations, other don't. i.e. the hexagon has only one possible appearance on the grid (rotational symmetrie and no chiral forms). No matter how you rotate or flip it. 
    # I will try to solve this puzzle by putting in all pieces one by one. 
    #   Limiting the search space:
    #       -Sequence of the pieceds: As I know the hexagon has only one form, it will be first in the sequence. There is only one chance in 12 for a piece with  12 forms that his exact form will be used, so they go last ()
    #       - the board itself has also 6 rotational symmetrical shapes. Avoid Searching symmetrical solutions. The hexagon can only fit on five positions. 
    #               --> I'll start the board with the hexagon already placed in it. (--> 5 start boards)  This should greatly speed things up. (witht the hexagon in the dead center, there is still rotational symmetry. )
    #               --> Five starter boards with eleven pieces.
    #  
    # Save states for multiprocessing or interruptions. 
    # state = unique descriptive string with the sequence of all 11 (not 12) pieces on one of the five (prepopulated with the hexagon) boards
        
    def __init__(self):
        

        # craete five base boards.
        # hexagon postions: 
        self.transformer = triangular_pattern.TriangularPatternOperations()
        pass

    def solve(self):
        pass
    
    
    # def try_piece_on_board(self, board, piece):
    #     # 1 get 


    # preparation of puzzle pieces:
    def create_empty_base_board(self, rows, cols, grid_pattern):
        base = triangular_grid.TriangularGrid(rows, cols) # the size of the board.   (8,13)
        base.overlay_grid(grid_pattern)
        return base

    # step 1: make sure the pieces are sorted from least amount of orientation to most.
    # step 2: prepare all pieces. (double array, all forms of a piece per array)
    def prepare_pieces(self, base_pieces, show=False):
        # pieces = array with patterns. Return all orientations by rotating and mirroring, per piece, delete identical orientations)
        
        
        
        all_unique_pieces_orientations = []
        for pattern in base_pieces:
            transformed = self.transformer.get_all_orientations(pattern, True)

            if show:
                for piece in transformed:
                    show_pattern_on_grid(piece)
            all_unique_pieces_orientations.append(transformed)
        return all_unique_pieces_orientations

    # step 3: choose first piece as the master piece, we will put it on the board to avoid doing double work.
    def prepare_base_boards(self, board, piece, positions):
        # positions is an array containing translations arrays (containing  tuples like :(direction, steps))
        # will create a base board with the piece in it for every provided position.

        boards = []
    
        for translations in positions:
            board_copy = copy.deepcopy(board)

            # take the prepared hexagon 
            piece_positioned = piece
            for translation in translations:
                
                piece_positioned = self.transformer.translate(piece_positioned,translation[0],translation[1])
                # prepare dedicated puzzle board (add first piece)
            board_copy.overlay_grid(piece_positioned)

            boards.append(board_copy)

        return boards



def show_all_pieces_mirrored(patterns):
    for piece in patterns:
        show_mirrored(piece)

def show_mirrored(pattern):
        
    transformer = triangular_pattern.TriangularPatternOperations()
    
    vertical = transformer.mirror(pattern, False)
    horizontal = transformer.mirror(pattern, True)
    
    bounding_box = transformer.get_combined_bounding_box([pattern, horizontal, vertical])
    rows = bounding_box["max_r"] + 1
    cols = bounding_box["max_c"] + 1
    base = triangular_grid.TriangularGrid(rows, cols)    

    base.overlay_grid(pattern)
    base.overlay_grid(horizontal)
    base.overlay_grid(vertical)

    print(str(base))



# show on triangular grid ------------------

def show_pattern_on_grid(pattern_cells, empty_spacing=0):
    transformer = triangular_pattern.TriangularPatternOperations()
   
    bounding_box = transformer.get_bounding_box(pattern_cells)
    rows = bounding_box["max_r"] + 1 + empty_spacing * 2
    cols = bounding_box["max_c"] + 1 + empty_spacing * 2

    if empty_spacing > 0:
        pattern_cells = transformer.translate(pattern_cells,"SE", empty_spacing)
        # pattern_cells = transformer.translate(pattern_cells,"E")

    base = triangular_grid.TriangularGrid(rows, cols)  
    base.overlay_grid(pattern_cells)
    print(str(base)) 


def show_orientations_of_pattern(pattern_cells, delete_equal_patterns=False):
    transformer = triangular_pattern.TriangularPatternOperations()

    resulting_patterns = transformer.get_all_orientations(pattern_cells, delete_equal_patterns)
    
    show_patterns_on_grid(resulting_patterns, 6, 1)
    print("Number of patterns: {}".format(len(resulting_patterns)))


def show_orientations_of_all_patterns(patterns,  delete_equal_patterns=False, show_one_pattern_at_a_time=False):
    transformer = triangular_pattern.TriangularPatternOperations()
    resulting_patterns = []

    if show_one_pattern_at_a_time:
        for pattern in patterns:
            show_orientations_of_pattern(pattern, delete_equal_patterns)
    else:

        for pattern in patterns:
            resulting_patterns.extend(transformer.get_all_orientations(pattern, delete_equal_patterns))

        if not show_one_pattern_at_a_time:
            show_patterns_on_grid(resulting_patterns, 10, 2)
            print("Number of patterns: {}".format(len(resulting_patterns)))
        

def show_patterns_on_grid(patterns, patterns_per_col, spacing=0):
    transformer = triangular_pattern.TriangularPatternOperations()
    print(patterns)
    arranged_patterns = transformer.arrange_patterns_for_no_overlap(patterns, patterns_per_col)
    
    print(arranged_patterns)
    # create fitting field.
    bounding_box = transformer.get_combined_bounding_box(arranged_patterns)

    print(bounding_box)
    rows = bounding_box["max_r"] + 1  # rows one more than index.
    cols = bounding_box["max_c"] + 1
    
    print(rows)
    print(cols)
    base = triangular_grid.TriangularGrid(rows, cols)   
    
    for pattern in arranged_patterns:
        base.overlay_grid(pattern)
    
    print(str(base))     
    
def rotate_and_show(pattern, degrees):
    transformer = triangular_pattern.TriangularPatternOperations()
    rotated = transformer.rotate(pattern,degrees,True)
    
    show_pattern_on_grid(rotated,0)
    show_pattern_on_grid(rotated,1)
    show_pattern_on_grid(rotated,2)

def test():
    pattern_cells = {(0,0):triangular_grid.CELL_ON}
    print(pattern_cells)
   
    rows = 1
    cols = 2

    base = triangular_grid.TriangularGrid(rows, cols)  
    base.overlay_grid(pattern_cells)
    print(str(base)) 

def general_tests_with_patterns():
    transformer = triangular_pattern.TriangularPatternOperations()
    
    # show_all_base_pieces()    
    # show_all_pieces_mirrored()
    # transformer = triangular_pattern.TriangularPatternOperations()
    #show_orientations_of_pattern(base_pieces_cells[5],True)
    #show_pattern_on_grid(base_pieces_cells[1])
    # show_patterns_on_grid(base_pieces_cells[:2],0)
    
    # show_orientations_of_all_patterns(base_pieces_cells, True, True) # show all patterns differntly
    # show_orientations_of_all_patterns(base_pieces_cells, True, False)  # show all patterns on one big field

if __name__ == "__main__":

    pass

    
