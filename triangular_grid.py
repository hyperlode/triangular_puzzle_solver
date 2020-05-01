import traceback

CELL_FAKE = 0  # for programatorical reasons
CELL_NOGO = 1  # not allowed --> i.e. board edge 
CELL_ON = 2
CELL_OFF = 3

display_fill = {CELL_FAKE:"!", CELL_NOGO:"-", CELL_ON:"O", CELL_OFF:" "}

class TriangularGrid():

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols

        self._cells = {}
        for row in range(self._rows):
            for col in range(self._cols):
                if row == 0 or col == 0:
                    self._cells[(row, col)] = CELL_FAKE
                elif row == self._rows - 1 \
                     or col == self._cols - 1:
                    self._cells[(row, col)] = CELL_FAKE
                else:
                    self._cells[(row, col)] = CELL_OFF
                
    
    def __str__(self):

        grid_disp = []     


        for row in range(self._rows):
            even_row = row % 2 == 0
            
            row_disp = []

            for col in range(self._cols):
                cell_disp = []
                even_col = col % 2 == 0

                if self._cells[(row,col)] == CELL_FAKE:

                    disp_fill_current = display_fill[CELL_FAKE]
                    disp_fill_neighbour_left = display_fill[CELL_FAKE]
                    disp_fill_neightbour_right = display_fill[CELL_FAKE]
                else:
                     disp_fill_current = display_fill[self._cells[(row,col)]]
                     disp_fill_neighbour_left = display_fill[self._cells[(row,col-1)]]
                     disp_fill_neightbour_right = display_fill[self._cells[(row,col+1)]]


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

    def set_cell(self, cell, on_else_off):
        value = CELL_OFF
        if on_else_off:
            value = CELL_ON

        if self._cells[cell] == CELL_FAKE:
            raise IllegalCellException

        if self._cells[cell] == CELL_NOGO:
            raise NoGoCellException
        
        self._cells[cell] = value


if __name__ == "__main__":
    g = TriangularGrid(10,14)
    try:
        # g.set_cell((0,0),CELL_ON)
        # g.set_cell((1,1),CELL_ON)
        pass
    except Exception as e:
        print("Failed to iopass cells test. {}{}".format(e, traceback.format_exc()))

    g.set_cell((2,3),CELL_ON)
    g.set_cell((3,3),CELL_ON)
    g.set_cell((3,4),CELL_ON)

    # g.set_cell((4,5),CELL_ON)
    print(str(g))
