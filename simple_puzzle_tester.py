
import triangular_puzzle_solver

import triangular_grid
import triangular_pattern
import copy
import itertools


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
    (1,1):triangular_grid.CELL_ON,
    (1,2):triangular_grid.CELL_ON,
}

piece_2 = {
    (0,2):triangular_grid.CELL_ON,
    (1,0):triangular_grid.CELL_ON,
    (2,0):triangular_grid.CELL_ON,
    (3,0):triangular_grid.CELL_ON,
}

if __name__ == "__main__":


    # solver = triangular_puzzle_solver.PuzzleSolver()
    # puzzle_board = solver.create_empty_base_board( ROWS, COLS, base_board)
    # print(solver.try_piece_on_board(puzzle_board, piece_0))

    # print(str(puzzle_board))
    # pieces = [piece_0, piece_1, piece_2]

    # print(solver.try_piece_on_board(puzzle_board, piece_1))
    # print(str(puzzle_board))


    pass

    # l = [1,2,3,4]

    # permiter = itertools.permutations(l)
    # # >> new_iterator.__setstate__(state)>> new_iterator.__setstate__(state)
    # print(permiter.__getstate__())
    # permiter.__setstate__ ((0,0,0,2))

    # print(l)
    # for i in l:
    #     print(i)




    # print(str(base))
    # tups = {(0,5):2, (0,4):4,(1,3):455,(3,3):8}
    # print(sorted(list(tups)))

    # print(tups)
    # print("efihjef")