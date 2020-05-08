import traceback
import copy
# isometric grid, triangular grid.
# has one extra cell at all borders internally. 

'''
!!/\!!!!/\!!!!/\!!!!/
!/!!\!!/!!\!!/!!\!!/!
/____\/____\/____\/__
\!!!!/\ 0,1/\    /\!!
!\!!/00\  /02\  /  \!
__\/____\/____\/____\
!!/\ 1,0/\1,2 /\    /
!/!!\  /11\  /  \  /!
/____\/____\/____\/__
\!!!!/\ 2,1/\    /\!!
!\!!/20\  /  \  /  \!
__\/____\/____\/____\
!!/\    /\    /\    /
!/!!\  /  \  /  \  /!
/____\/____\/____\/__
\!!!!/\    /\    /\!!
!\!!/  \  /  \  /  \!
__\/____\/____\/____\
!!/\!!!!/\!!!!/\!!!!/
!/!!\!!/!!\!!/!!\!!/!
/____\/____\/____\/__
'''

CELL_EDGE = 8  # for programatorical reasons (to have no exception on the edge of the grid)
CELL_NOGO = 4  # not allowed --> i.e. board edge 
CELL_ON = 1
CELL_OFF = 0
# CELL_DOUBLE_ON = 2  # if two "ON"-cells are overlayed on each other.
CELL_ERROR = 667
CELL_PIECE_COLLISION_WITH_EDGE= 9
CELL_PIECE_COLLISION_WITH_NOGO = 5
CELL_PIECE_COLLISION_WITH_PIECE= 2

LEGAL_CELLS = [CELL_EDGE, CELL_NOGO, CELL_ON, CELL_OFF]


display_fill = {CELL_EDGE:"!", 
    CELL_NOGO:"-", 
    CELL_ON:"O", 
    CELL_OFF:" ", 
    CELL_PIECE_COLLISION_WITH_EDGE:"?", 
    CELL_PIECE_COLLISION_WITH_NOGO:"W", 
    CELL_PIECE_COLLISION_WITH_PIECE:"X",
    CELL_ERROR: "%",
    }

class TriangularGrid():

    def __init__(self, rows, cols):
        self._rows = rows + 2
        self._cols = cols + 2

        self._cells = {}
        for row in range(self._rows):
            for col in range(self._cols):
                if row == 0 or col == 0:
                    self._cells[(row, col)] = CELL_EDGE
                elif row == self._rows - 1 \
                     or col == self._cols - 1:
                    self._cells[(row, col)] = CELL_EDGE
                else:
                    self._cells[(row, col)] = CELL_OFF
        
        self._added_patterns = []

    def is_board_legal(self):
        # check for collisions
        for v in self._cells.values():
            if v not in LEGAL_CELLS:
                return False
        return True

    def all_cells_occupied(self):
        # assume legal board
        # will return False if empty cells...

        for v in self._cells.values():
            if v == CELL_OFF:
                return False
        return True
        
    def get_most_top_left_free_cell(self):
        # get most top row.
        # of most top row, get most left col.

        # I'm lucky, this is standard behaviour. tuples will be sorted first by first el, then second el.
        # cells = sorted(list(self._cells))
        for r in range(self._rows):
            for c in range(self._cols):
                if self._cells[(r,c)] == CELL_OFF:
                    return self.internal_cell_to_cell((r,c))
        
        return None  # no free cells: means basically a full grid. in puzzle solving, that means: winner!



    def cell_to_internal_cell(self, cell):
 
        r,c = cell
        return (r+1, c+1) # transform to internal board

    def internal_cell_to_cell(self, internal_cell):
        r,c = internal_cell 
        return (r-1, c-1)

    def get_neighbours(self, cell):
        # get all valid adjecent triangles.
        cell = self.cell_to_internal_cell(cell)

        r,c = cell
        neighbours = [(r,c-1),(r,c+1)]  # horizonal
        if (r + c) % 2 == 0:
            # even sum cells = upwards pointing triangles
            neighbours.append((r+1,c))
        else:
            neighbours.append((r-1,c))
        valid_neighbours = [cell for cell in neighbours if self._cells[cell] != CELL_EDGE] 

        return  [self.internal_cell_to_cell(cell) for cell in valid_neighbours]
        
    def set_cell(self, cell, on_else_off=True):
        cell = self.cell_to_internal_cell(cell)
        value = CELL_OFF
        if on_else_off:
            value = CELL_ON

        if self._cells[cell] == CELL_EDGE:
            raise IllegalCellException

        if self._cells[cell] == CELL_NOGO:
            raise NoGoCellException
        
        self._cells[cell] = value
        
    def get_added_patterns(self):
        # get in sequence of addition. 
        return self._added_patterns

    def add_pattern(self, pattern, add=True, neglect_outside_board_errors=True):
        # no offsets! Do a translation of the pattern before you provide it here.
        # pattern is just a matrix for a triangular pattern with cells that are ON or OFF. 
        
        if add:
            for cell, value in pattern.items():
                cell = self.cell_to_internal_cell(cell)
                r,c = cell

                try:
                    self._cells[(r, c)] += value 
                except KeyError as e:
                    # outside boundaries, but we don't care. We just don't add it. As this is already further reachign than the border around the board, there are most probably already some illegal squares there. 
                    if not neglect_outside_board_errors:
                        print(e)
                        raise                    
                    pass 
            self._added_patterns.append(pattern)
            return self._cells
        else:    

            return_cells = copy.deepcopy(self._cells)
            for cell, value in pattern.items():
                r,c = cell
                
                try:
                    return_cells[(r, c)] += value  
                except KeyError as e:
                    # outside boundaries, but we don't care. We just don't add it. As this is already further reachign than the border around the board, there are most probably already some illegal squares there. 
                    if not neglect_outside_board_errors:
                        print(e)
                        raise                    
                    pass 

            return return_cells
          
    def __str__(self):

        grid_disp = []     
        # print(self._cells)

        for row in range(self._rows):
            even_row = row % 2 == 0
            
            row_disp = []

            for col in range(self._cols):
                cell_disp = []
                even_col = col % 2 == 0

                # edge cases
                try:

                    if self._cells[(row,col)] > CELL_EDGE:

                        disp_fill_neighbour_left = display_fill[CELL_PIECE_COLLISION_WITH_EDGE]
                        disp_fill_neighbour_right = display_fill[CELL_PIECE_COLLISION_WITH_EDGE]
                        disp_fill_current = display_fill[CELL_PIECE_COLLISION_WITH_EDGE]

                    elif self._cells[(row,col)] == CELL_EDGE:
                        
                        if row == 0 or row == self._rows-1:

                            disp_fill_neighbour_left = display_fill[CELL_EDGE]
                            disp_fill_neighbour_right = display_fill[CELL_EDGE]
                            disp_fill_current = display_fill[CELL_EDGE]

                        elif col == 0:
                            disp_fill_neighbour_left = display_fill[CELL_EDGE]
                            disp_fill_current = display_fill[self._cells[(row,col)]]

                        elif col == self._cols-1:
                            if col % 2 == 0:
                                disp_fill_current = display_fill[CELL_EDGE]
                                disp_fill_neighbour_left = display_fill[self._cells[(row,col-1)]]
        
                            else:
                                disp_fill_neighbour_right = display_fill[CELL_EDGE]
                                disp_fill_neighbour_left = display_fill[self._cells[(row,col-1)]]
                                disp_fill_current = display_fill[self._cells[(row,col)]]

                    else:
                        disp_fill_current = display_fill[self._cells[(row,col)]]
                        disp_fill_neighbour_right = display_fill[self._cells[(row,col+1)]]
                        disp_fill_neighbour_left = display_fill[self._cells[(row,col-1)]]
                except Exception as e:
                    print("Error: {} . Info: (row,col):({},{}) cell value = {}".format(traceback.format_exc(), row, col, self._cells[(row,col)]))
                    # raise
                    disp_fill_current = display_fill[CELL_ERROR]
                    disp_fill_neighbour_right = display_fill[CELL_ERROR]
                    disp_fill_neighbour_left = display_fill[CELL_ERROR]


                if even_row:
                    if even_col:
                        # left: col -1 
                        # right: current
                        cell_disp.append("{}{}/".format(disp_fill_neighbour_left,disp_fill_neighbour_left))
                        cell_disp.append("{}/{}".format(disp_fill_neighbour_left, disp_fill_current))
                        cell_disp.append("/__")
                    else:
                        # left : col-1
                        # right: current 
                        cell_disp.append("\\{}{}".format(
                            disp_fill_current,disp_fill_current))
                        cell_disp.append("{}\\{}".format(
                            disp_fill_neighbour_left, disp_fill_current))
                        cell_disp.append("__\\")
                else:
                    #odd row

                    if even_col:
                        # left  : col -1 
                        # right: current
                        
                        cell_disp.append("\\{}{}".format(
                            disp_fill_current,disp_fill_current))
                        cell_disp.append("{}\\{}".format(
                            disp_fill_neighbour_left, disp_fill_current))
                        cell_disp.append("__\\")
                    else:
                        # right: current cell
                        # left: col - 1 
                        
                        cell_disp.append("{}{}/".format(
                            disp_fill_neighbour_left,disp_fill_neighbour_left))
                        cell_disp.append("{}/{}".format(
                            disp_fill_neighbour_left, disp_fill_current))
                        cell_disp.append("/__")

                row_disp.append(cell_disp)
            
            grid_disp.append(row_disp)


        grid_str = ""
        for row in range(self._rows):
            for line in range(3):
                for col in range(self._cols):
                    grid_str += grid_disp[row][col][line]
                
                grid_str += "\n"

        return grid_str

    
if __name__ == "__main__":

    g = TriangularGrid(5,5)
    print(str(g))
    # g = TriangularGrid(10,15)
    # try:
    #     # g.set_cell((0,0),CELL_ON)
    #     # g.set_cell((1,1),CELL_ON)
    #     pass
    # except Exception as e:
    #     print("Failed to iopass cells test. {}{}".format(e, traceback.format_exc()))

    # g.set_cell((0,0),CELL_ON)
    # g.set_cell((3,3),CELL_ON)
    # g.set_cell((3,4),CELL_ON)
    # g.set_cell((9,13),CELL_ON)

    # print(g.get_neighbours((0,1)))

    # # g.set_cell((4,5),CELL_ON)
    # print(str(g))
