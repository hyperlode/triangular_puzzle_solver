
import triangular_puzzle_solver

import triangular_grid
import triangular_pattern
import copy


# bounding box
ROWS = 2
COLS = 3
base_board = {(r,c):triangular_grid.CELL_OFF for r in range(ROWS) for c in range(COLS)}
# border

piece_0 = {
    (0,0):triangular_grid.CELL_ON,
    (0,1):triangular_grid.CELL_ON,
}

piece_1 = {
    (0,2):triangular_grid.CELL_ON,
    (1,0):triangular_grid.CELL_ON,
    (2,0):triangular_grid.CELL_ON,
    (3,0):triangular_grid.CELL_ON,
}


if __name__ == "__main__":


    solver = triangular_puzzle_solver.PuzzleSolver()
    base = solver.create_empty_base_board( ROWS, COLS, base_board)
        
    print(str(base))
