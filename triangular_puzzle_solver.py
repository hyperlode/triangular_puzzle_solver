import logging
import copy
import random

import triangular_grid
import triangular_pattern



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
        
    def __init__(self, logger=None):
        
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Puzzle solver init.")

        self.transformer = triangular_pattern.TriangularPatternOperations()

        # stats:
        self.state_saver = []
        self.tested_pieces = 0
      
    def solve(self):
        pass

    def build_up_state(self, board, pieces_with_orientations, state, show_every_step=False):
        for piece in state:
            piece, orientation = piece
            piece_pattern = pieces_with_orientations[piece][orientation]

            success = self.try_piece_on_board(board, piece_pattern)

            if not success:
               self.logger.error(board)
               raise
               
            if show_every_step:
                self.logger.info("\n {}".format(str(board)))
                
        return board

    def analyse_multiple_sequences_of_pieces(self, board, pieces_with_orientations, sequences_of_pieces_indeces, show_longest_state=False):

        combined_longest_state = []
        total_pieces_tested = 0
        for sequence_of_pieces_indeces_to_try in sequences_of_pieces_indeces:
            pieces_tested, longest_successful_state = self.analyse_sequence_of_pieces(board, pieces_with_orientations, sequence_of_pieces_indeces_to_try)

            total_pieces_tested += pieces_tested

            if len(longest_successful_state) > len(combined_longest_state):
                combined_longest_state = longest_successful_state

        if show_longest_state:
            self.build_up_state(board, pieces_with_orientations, combined_longest_state, True)

        return total_pieces_tested, combined_longest_state

    def analyse_randomize_sequence_of_pieces(self, board, pieces_with_orientations, pieces_indeces):
       random.shuffle(pieces_indeces)
       pieces_tested, longest_state = self.analyse_sequence_of_pieces(board, pieces_with_orientations, pieces_indeces, show_longest_state=False)
       return pieces_tested, longest_state

    def analyse_sequence_of_pieces(self, board, pieces_with_orientations, sequence_of_pieces_indeces_to_try, show_longest_state=False):

        self.logger.info("Start trying pieces sequence. (all orientations, top left to bottom right): {}".format(sequence_of_pieces_indeces_to_try))
        state = []
        try_board = copy.deepcopy(board)
        
        if len(state) > 0:
            try_board = self.build_up_state(try_board, pieces_with_orientations, state)
        success, state = self.try_sequence_recursive(try_board, sequence_of_pieces_indeces_to_try, pieces_with_orientations, state)

        pieces_tested = self.tested_pieces
        longest_state = self.state_saver[::]
        
        self.state_saver = []
        self.tested_pieces = 0 
        
        self.logger.info("Testing endend. Pieces tested:{}. Found? {}, state: {}. longest state length: {}/{} ({})".format(pieces_tested, success, state, len(longest_state), len(sequence_of_pieces_indeces_to_try), longest_state))

        if show_longest_state:
            self.build_up_state(board, pieces_with_orientations, longest_state, True)

        return pieces_tested, longest_state
        
    def try_sequence_recursive(self, board, try_sequence_of_pieces_index, pieces_with_orientations, state, last_tried=None):
        # pieces_with_orientations_contains the right sequence in which piece are tried. We will not swap pieces.
        # state  = sequence [(firstpieceindex,orientationindex),(secondpieceindex,orientationindex),...]
        if len(state) > len(self.state_saver):
            self.logger.debug("Longest state: {}".format(state))
            self.logger.debug(str(board))
            self.state_saver = state


        #print(state)
        # stop condition
        if len(state) == 11:
            self.logger.info("We have a winner!")
            self.logger.info(state)
            raise
        
        # assume board populated according to state.
        if last_tried is None:
            # take next piece with first iteration
            try_piece_index = try_sequence_of_pieces_index[len(state)]  
            orientation_index = 0
           
        else:
            # only use to restart for a certain state.
            try_piece_index, orientation_index_offset= last_tried          
            orientation_index += orientation_index_offset
           
        # relevant orientations for this piece.
        all_orientations_patterns = pieces_with_orientations[try_piece_index]
        total_orientations = len(all_orientations_patterns)

        # test stop condition
        all_tested = orientation_index >= total_orientations

        # go over all orientations
        while not all_tested:
            test_board = copy.deepcopy(board)
            
            # print("will search. at index: {}, index_offset = {}, orientations to try: {}  ({})".format( 
            #     try_piece_index, 
            #     orientation_index_offset, 
            #     len(try_pieces) ,
            #     try_pieces)
            #     ) 
            
            piece_fits, orientation_index, result_board = self.try_pieces_on_board(test_board, all_orientations_patterns, orientation_index)
            # print(result_board)
          
            # print("piece_fits? {} , {}".format(piece_fits, orientation_index_of_tried_pieces))

            if piece_fits:
                new_state = state[::]
                new_state.append((try_piece_index, orientation_index))
                success, return_state = self.try_sequence_recursive(result_board, try_sequence_of_pieces_index, pieces_with_orientations, new_state , last_tried=None)

                if success:   
                    # looking good     
                    return True, return_state
                else:
                    self.logger.debug("returned from recursion. current: ")
                
            # print("stats:")
            # print(state)
            # print(total_orientations)
            # print(orientation_index_offset)

            orientation_index += 1 # next piece

            if orientation_index >= total_orientations:
                all_tested = True
          
        return False, state

    # def next_step(self, board, pieces_with_orientations, state, last_tried=None):
    #     # pieces_with_orientations_contains the right sequence in which piece are tried. We will not swap pieces.
    #     # state  = sequence [(firstpieceindex,orientationindex),(secondpieceindex,orientationindex),...]


    #     used_pieces = [piece_index for piece_index, orientation in state]
    #     unused_pieces = [i for i in range(12) if i not in used_pieces] # retain order!

    #     # stop condition
    #     if len(unused_pieces) == 0:
    #         print("We have a winner!")
    #         print(state)
    #         raise


    #     # assume board populated according to state.
    #     if last_tried is None:

    #         # take next piece with first iteration
    #             # search next piece
    #         try_piece_index = unused_pieces.pop(0)
    #         print(unused_pieces)
            
    #         orientation_index_offset = 0
    #     else:
    #         # only use to restart for a certain state.
    #         try_piece_index, orientation_index_offset= last_tried          

    #     # try orientations.
    #     try_pieces = pieces_with_orientations[try_piece_index][orientation_index_offset:]

    #     success, orientation_index = self.try_pieces_on_board(board, try_pieces  )

    #     if success:
    #         orientation_index += orientation_index_offset
    #         state.append((try_piece_index, orientation_index))
    #         return True, state
    #     else:
    #         return False, state


    def try_pieces_on_board(self, board, pieces, start_piece_index=0):
        # check if any of the pieces fits on top left of board. if so, return new board and piece index.
        # else, return False
        index = start_piece_index

        while index < len(pieces):
            try_piece = pieces[index]
            test_board = copy.deepcopy(board)
            
            self.logger.debug("try piece index:{}".format(index))
            success = self.try_piece_on_board(test_board, try_piece)
            
            if success:
                
                # print(test_board)
                return True, index, test_board
            
            index+=1

        return False, index, None

    def try_piece_on_board(self, board, piece):
        
        # pieces are added to board from top left to bottom right.
        # check if piece fits in top left gap. (do not rotate or mirror piece. This is a simple operation.)
        
        # assume piece to be normalized. (i.e. top left coordinate as close to (0,0) as possible)

        # get next free cell on board.
        self.tested_pieces += 1
        free_cell = board.get_most_top_left_free_cell()
        
        # print("free_cell:{}".format(free_cell))
        if free_cell is None:
            self.logger.info("solution found!")
            self.logger.info(board.get_added_patterns())
            raise GridFullException
        
        # 2 check if \/(down) or /\ (up)  triangle
        free_cell_is_up_triangle = self.transformer.cell_up_else_down_facing_triangle(free_cell)

        # print("up facing triangle? :{}".format(free_cell_is_up_triangle))

        # check if piece works has good starting cell (get top left cell)
        piece_top_left_cell = self.transformer.get_most_top_left_cell_coordinate(piece)
        # print("piece top left cell:{}".format(piece_top_left_cell))

        piece_top_left_is_up_triangle = self.transformer.cell_up_else_down_facing_triangle(piece_top_left_cell)
        # print("up facing triangle? :{}".format(free_cell_is_up_triangle))

        # must be equal to have a chance to match.
        if free_cell_is_up_triangle != piece_top_left_is_up_triangle:
            self.logger.debug("non matching starting points. Will for sure not work.: free cell triange: {}  , piece top left triangle: {}".format(free_cell_is_up_triangle, piece_top_left_is_up_triangle))
            self.logger.debug(piece)
            return False

        # if ok, translate pattern to position
        # get top left cell diff

        # diff = tuple(map(operator.sub, , ))

        rb, cb = free_cell
        rp, cp = piece_top_left_cell

        diff = (rb - rp, cb - cp)  # can contain negative values (when testing non fitting pieces)! Warning: I already forsee situation where piece can get out of the board limits.
        
        # print("diff: {}".format(diff))
        translated_piece = self.transformer.translate_manual(piece, diff)

        # overlay pattern
        board.add_pattern(translated_piece)

        self.logger.debug(board)

        # check if legal. 
        legal = board.is_board_legal()

        if not legal:
            return False

        return True

    # def run_through_all(self, boards, pieces_with_orientations):

    #     # can be more than one starting board
      
    #     for board in boards:
    #         piece_index = len(board.get_added_patterns()) - 1  # skip the first piece if it's already implemented in the boards.
    #         orientation_per_piece = [0 for piece in range(pieces_with_orientations)]      
    #         board_per_piece.append(copy.deepcopy(board))

    #         for piece_index in range(pieces_with_orientations):
    #             piece_orientation_index = orientation_per_piece[piece_index]
    #             piece_to_be_added = pieces_with_orientations[piece_index][piece_orientation_index]

    #             board_for_piece_to_be_added = copy.deepcopy(board_per_piece[piece_index - 1])

    #             successs = self.try_piece_on_board(board_for_piece_to_be_added,piece_to_be_added)

    #             if success:
    #                 board_per_piece.append()
    #                 next 
        
    def check_winning_board(self, board):
        # if not board.is_board_legal()
        #     return False

        return board.all_cells_occupied()

    # preparation of puzzle pieces:
    def create_empty_base_board(self, rows, cols, grid_pattern):
        base = triangular_grid.TriangularGrid(rows, cols) # the size of the board.   (8,13)
        base.add_pattern(grid_pattern)
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
            board_copy.add_pattern(piece_positioned)

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

    base.add_pattern(pattern)
    base.add_pattern(horizontal)
    base.add_pattern(vertical)

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
    base.add_pattern(pattern_cells)
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
    # print(patterns)
    arranged_patterns = transformer.arrange_patterns_for_no_overlap(patterns, patterns_per_col, spacing)
    
    # print(arranged_patterns)
    # create fitting field.
    bounding_box = transformer.get_combined_bounding_box(arranged_patterns)

    # print(bounding_box)
    rows = bounding_box["max_r"] + 1  # rows one more than index.
    cols = bounding_box["max_c"] + 1
    
    # print(rows)
    # print(cols)
    base = triangular_grid.TriangularGrid(rows, cols)   
    
    for pattern in arranged_patterns:
        base.add_pattern(pattern)
    
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
    base.add_pattern(pattern_cells)
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

    
