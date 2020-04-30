CELL_FAKE = 0  # for programatorical reasons
CELL_NOGO = 1  # not allowed --> i.e. board edge 
CELL_ON = 2
CELL_OFF = 3

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
        g = ""
        for row in range(self._rows):
            for col in range(self._cols):
                
                if self._cells[(row,col)] == CELL_FAKE:
                    if row % 2 == 0:
                        g += " /\\ "
                    else:
                        g += "\\EE/"
                        
                else:
                    if row % 2 == 0:
                        g += " /\\ "
                    else:
                        g += "\\  /"
                        
            g += "\n"
            for col in range(self._cols):
                if self._cells[(row,col)] == CELL_FAKE:
                    if row % 2 == 0:
                        g += "/EE\\"
                    else:
                        g += "_\\/_"
                else:
                    if row % 2 == 0:
                        g += "/__\\"
                    else:
                        g += "_\\/_"
            g += "\n"
        return g

    def set_cell(cell, on_else_off):
        value = CELL_OFF
        if on_else_off:
            value = CELL_ON
        self._cells[cell] = value


if __name__ == "__main__":
    g = TriangularGrid(10,14)
    print(str(g))
